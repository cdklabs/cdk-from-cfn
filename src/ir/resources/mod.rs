use std::collections::{BTreeSet, HashMap, HashSet};
use std::convert::TryInto;
use std::fmt;
use std::ops::Deref;

use base64::Engine;
use indexmap::IndexMap;
use topological_sort::TopologicalSort;

use crate::cdk::*;
use crate::ir::reference::{Origin, Reference};
use crate::ir::sub::{sub_parse_tree, SubValue};
use crate::parser::resource::{
    DeletionPolicy, IntrinsicFunction, ResourceAttributes, ResourceValue,
};
use crate::primitives::WrapperF64;
use crate::Hasher;
use crate::TransmuteError;

use super::ReferenceOrigins;

// ResourceIr is the intermediate representation of a nested stack resource.
// It is slightly more refined than the ResourceValue, in some cases always resolving
// known types. It also decorates objects with the necessary information for a separate
// system to output all the necessary internal structures appropriately.
#[derive(Clone, Debug, PartialEq)]
pub enum ResourceIr {
    Null,
    Bool(bool),
    Number(i64),
    Double(WrapperF64),
    String(String),

    // Higher level resolutions
    Array(TypeReference, Vec<ResourceIr>),
    Object(TypeReference, IndexMap<String, ResourceIr, Hasher>),

    // Rest is meta functions
    // https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-conditions.html#w2ab1c33c28c21c29
    If(String, Box<ResourceIr>, Box<ResourceIr>),
    Join(String, Vec<ResourceIr>),
    Split(String, Box<ResourceIr>),
    Ref(Reference),
    Sub(Vec<ResourceIr>),
    Map(String, Box<ResourceIr>, Box<ResourceIr>),
    Base64(Box<ResourceIr>),
    ImportValue(Box<ResourceIr>),
    GetAZs(Box<ResourceIr>),
    Select(usize, Box<ResourceIr>),
    Cidr(Box<ResourceIr>, Box<ResourceIr>, Box<ResourceIr>),
}

// ResourceTranslationInputs is a place to store all the intermediate recursion
// for resource types.
#[derive(Clone)]
pub(super) struct ResourceTranslator<'a, 'b> {
    pub schema: &'a Schema,
    pub origins: &'b ReferenceOrigins,
    pub value_type: Option<TypeReference>,
}

impl<'a, 'b> ResourceTranslator<'a, 'b> {
    const fn json(schema: &'a Schema, origins: &'b ReferenceOrigins) -> Self {
        Self {
            schema,
            origins,
            value_type: Some(TypeReference::Primitive(Primitive::Json)),
        }
    }

    pub(super) fn translate(
        &self,
        resource_value: ResourceValue,
    ) -> Result<ResourceIr, TransmuteError> {
        match resource_value {
            ResourceValue::Null => Ok(ResourceIr::Null),
            ResourceValue::Bool(b) => Ok(ResourceIr::Bool(b)),
            ResourceValue::Number(n) => Ok(ResourceIr::Number(n)),
            ResourceValue::Double(d) => Ok(ResourceIr::Double(d)),
            ResourceValue::String(s) => {
                if let Some(TypeReference::Primitive(simple_type)) = self.value_type {
                    return match simple_type {
                        Primitive::Boolean => {
                            Ok(ResourceIr::Bool(s.parse().map_err(|cause| {
                                TransmuteError::new(format!("{cause}"))
                            })?))
                        }
                        Primitive::Number => {
                            Ok(ResourceIr::Number(s.parse().map_err(|cause| {
                                TransmuteError::new(format!("{cause}"))
                            })?))
                        }
                        _ => Ok(ResourceIr::String(s)),
                    };
                }
                Ok(ResourceIr::String(s))
            }
            ResourceValue::Array(parse_resource_vec) => {
                let item_type = match &self.value_type {
                    Some(TypeReference::List(item_type)) => Some(item_type.deref().clone()),
                    value_type => value_type.clone(),
                };
                let array_ir = {
                    let item_translator = Self {
                        schema: self.schema,
                        origins: self.origins,
                        value_type: item_type.clone(),
                    };

                    let mut array_ir = Vec::with_capacity(parse_resource_vec.len());
                    for parse_resource in parse_resource_vec {
                        array_ir.push(item_translator.translate(parse_resource)?);
                    }
                    array_ir
                };

                Ok(ResourceIr::Array(item_type.unwrap_or_default(), array_ir))
            }
            ResourceValue::Object(o) => {
                let mut is_resource_ir_array = false;
                let property_bag: Box<dyn PropertyBag> = match &self.value_type {
                    Some(TypeReference::Named(name)) => {
                        Box::new(self.schema.type_named(name).cloned().unwrap())
                    }
                    Some(TypeReference::Map(item_type)) => Box::new(MapOf(item_type)),
                    Some(TypeReference::List(item_type)) => {
                        is_resource_ir_array = true;
                        Box::new(MapOf(item_type))
                    }
                    Some(TypeReference::Primitive(Primitive::Json)) |
                    Some(TypeReference::Union(TypeUnion::Static([TypeReference::Named(_), ..]))) => {
                        Box::new(MapOf(&TypeReference::Primitive(Primitive::Json)))
                    }
                    other => unimplemented!("{other:?}"),
                };

                let mut new_hash = IndexMap::with_capacity_and_hasher(o.len(), Hasher::default());
                for (s, rv) in o {
                    let property_type = property_bag.property(&s);
                    let property_ir = Self {
                        schema: self.schema,
                        origins: self.origins,
                        value_type: property_type.map(|pt| pt.value_type),
                    }
                    .translate(rv)?;

                    new_hash.insert(s, property_ir);
                }

                let resource_ir =
                    ResourceIr::Object(self.value_type.clone().unwrap_or_default(), new_hash);

                if is_resource_ir_array {
                    return Ok(ResourceIr::Array(
                        self.value_type.clone().unwrap_or_default(),
                        Vec::from([resource_ir]),
                    ));
                }

                Ok(resource_ir)
            }
            ResourceValue::IntrinsicFunction(intrinsic) => {
                match *intrinsic {
                    IntrinsicFunction::Sub { string, replaces } => {
                        let mut excess_map = IndexMap::<_, _, Hasher>::default();
                        if let Some(replaces) = replaces {
                            match replaces {
                                ResourceValue::Object(obj) => {
                                    excess_map.reserve(obj.len());
                                    for (key, val) in obj.into_iter() {
                                        excess_map.insert(key.to_string(), self.translate(val)?);
                                    }
                                }
                                _ => {
                                    // these aren't possible, so panic
                                    return Err(TransmuteError::new(
                                        "Sub excess map must be an object",
                                    ));
                                }
                            }
                        }

                        let vars = sub_parse_tree(&string)?;
                        let r = vars
                            .into_iter()
                            .map(|x| match x {
                                SubValue::String(x) => ResourceIr::String(x),
                                SubValue::Variable(x) => match excess_map.get(&x) {
                                    None => ResourceIr::Ref(self.translate_ref(&x)),
                                    Some(x) => x.clone(),
                                },
                            })
                            .collect();
                        Ok(ResourceIr::Sub(r))
                    }
                    IntrinsicFunction::FindInMap {
                        map_name,
                        top_level_key,
                        second_level_key,
                    } => {
                        let rt = self.with_value_type(TypeReference::Primitive(Primitive::String));
                        let top_level_key_str = rt.translate(top_level_key)?;
                        let second_level_key_str = rt.translate(second_level_key)?;
                        Ok(ResourceIr::Map(
                            map_name,
                            Box::new(top_level_key_str),
                            Box::new(second_level_key_str),
                        ))
                    }
                    IntrinsicFunction::GetAtt {
                        logical_name,
                        attribute_name,
                    } => Ok(ResourceIr::Ref(Reference::new(
                        &logical_name,
                        Origin::GetAttribute {
                            attribute: attribute_name.replace('.', ""),
                            conditional: self.origins.is_conditional(&logical_name),
                        },
                    ))),
                    IntrinsicFunction::If {
                        condition_name,
                        value_if_true,
                        value_if_false,
                    } => {
                        let value_if_true = self.translate(value_if_true)?;
                        let value_if_false = self.translate(value_if_false)?;

                        Ok(ResourceIr::If(
                            condition_name,
                            Box::new(value_if_true),
                            Box::new(value_if_false),
                        ))
                    }
                    IntrinsicFunction::Join { sep, list } => {
                        let irs = match list {
                            ResourceValue::Array(list) => {
                                let mut irs = Vec::with_capacity(list.len());
                                for item in list {
                                    irs.push(self.translate(item)?);
                                }
                                irs
                            }
                            list => vec![self.translate(list)?],
                        };

                        Ok(ResourceIr::Join(sep, irs))
                    }
                    IntrinsicFunction::Split { sep, string } => {
                        let ir = self.translate(string)?;

                        Ok(ResourceIr::Split(sep, Box::new(ir)))
                    }
                    IntrinsicFunction::Ref(x) => Ok(ResourceIr::Ref(self.translate_ref(&x))),
                    IntrinsicFunction::Base64(x) => match x {
                        ResourceValue::String(b64) => {
                            match base64::engine::general_purpose::STANDARD.decode(&b64) {
                                Ok(decoded) => match String::from_utf8(decoded) {
                                    Ok(text) => Ok(ResourceIr::String(text)),
                                    Err(_) => {
                                        Ok(ResourceIr::Base64(Box::new(ResourceIr::String(b64))))
                                    }
                                },
                                Err(cause) => Err(TransmuteError::new(format!(
                                    "invalid base64: {b64:?} -- {cause}"
                                ))),
                            }
                        }
                        x => {
                            let ir = self.translate(x)?;
                            Ok(ResourceIr::Base64(Box::new(ir)))
                        }
                    },
                    IntrinsicFunction::ImportValue(x) => {
                        let ir = self.translate(x)?;
                        Ok(ResourceIr::ImportValue(Box::new(ir)))
                    }
                    IntrinsicFunction::Select { index, list } => {
                        let index = match index {
                            ResourceValue::String(x) => match x.parse::<usize>() {
                                Ok(x) => x,
                                Err(_) => {
                                    return Err(TransmuteError::new("index must be int for Select"))
                                }
                            },
                            ResourceValue::Number(x) => match x.try_into() {
                                Ok(x) => x,
                                Err(cause) => {
                                    return Err(TransmuteError::new(format!(
                                        "index is too large for Select: {cause}"
                                    )))
                                }
                            },
                            _ => return Err(TransmuteError::new("index must be int for Select")),
                        };

                        let obj = self.translate(list)?;
                        Ok(ResourceIr::Select(index, Box::new(obj)))
                    }
                    IntrinsicFunction::GetAZs(x) => {
                        let ir = self.translate(x)?;
                        Ok(ResourceIr::GetAZs(Box::new(ir)))
                    }
                    IntrinsicFunction::Cidr {
                        ip_block,
                        count,
                        cidr_bits,
                    } => {
                        let rt = self.with_value_type(TypeReference::Primitive(Primitive::String));
                        let ip_block_str = rt.translate(ip_block)?;
                        let count_str = rt.translate(count)?;
                        let cidr_bits_str = rt.translate(cidr_bits)?;
                        Ok(ResourceIr::Cidr(
                            Box::new(ip_block_str),
                            Box::new(count_str),
                            Box::new(cidr_bits_str),
                        ))
                    }

                    unimplemented => unimplemented!("{unimplemented:?}"),
                }
            }
        }
    }

    fn translate_ref(&self, x: &str) -> Reference {
        if let Some(origin) = self.origins.for_ref(x) {
            Reference::new(x, origin)
        } else if let Some((name, attribute)) = x.split_once('.') {
            Reference::new(
                name,
                Origin::GetAttribute {
                    attribute: attribute.into(),
                    conditional: self.origins.is_conditional(name),
                },
            )
        } else {
            Reference::new(x, Origin::LogicalId { conditional: false })
        }
    }

    #[inline]
    fn with_value_type(&self, value_type: TypeReference) -> Self {
        Self {
            schema: self.schema,
            origins: self.origins,
            value_type: Some(value_type),
        }
    }
}

#[derive(Clone)]
struct MapOf<'a>(&'a TypeReference);
impl PropertyBag for MapOf<'_> {
    fn property(&self, key: &str) -> Option<Property> {
        Some(Property {
            name: voca_rs::case::camel_case(key).into(),
            required: false,
            value_type: self.0.clone(),
        })
    }
}

// ResourceInstruction is all the information needed to output a resource assignment.
#[derive(Clone, Debug, PartialEq)]
pub struct ResourceInstruction {
    pub name: String,
    pub condition: Option<String>,
    pub metadata: Option<ResourceIr>,
    pub update_policy: Option<ResourceIr>,
    pub deletion_policy: Option<DeletionPolicy>,
    pub dependencies: Vec<String>,
    pub resource_type: ResourceType,
    pub properties: IndexMap<String, ResourceIr, Hasher>,

    // `references` identify the logical ID of all other template entities that this resource
    // contains a reference to (i.e: it uses them).
    pub references: BTreeSet<String>,
}

impl ResourceInstruction {
    pub(super) fn from(
        parse_tree: IndexMap<String, ResourceAttributes, Hasher>,
        schema: &Schema,
        origins: &ReferenceOrigins,
    ) -> Result<Vec<Self>, TransmuteError> {
        let mut instructions = Vec::with_capacity(parse_tree.len());

        for (resource_name, attributes) in parse_tree {
            let resource_type = ResourceType::parse(&attributes.resource_type)?;
            let resource_spec = schema.resource_type(&attributes.resource_type);

            let metadata = if let Some(metadata) = attributes.metadata {
                Some(ResourceTranslator::json(schema, origins).translate(metadata)?)
            } else {
                None
            };

            let update_policy = if let Some(up) = attributes.update_policy {
                Some(ResourceTranslator::json(schema, origins).translate(up)?)
            } else {
                None
            };

            let mut properties =
                IndexMap::with_capacity_and_hasher(attributes.properties.len(), Hasher::default());
            for (prop_name, prop) in attributes.properties {
                let property_type = resource_spec.and_then(|spec| spec.property(&prop_name));
                let property_type = property_type.map(|prop| prop.value_type);
                if property_type.is_none() {
                    let resource_type = format!(
                        "{:#?}::{:#?}::{:#?}",
                        resource_type.scope().to_uppercase(),
                        resource_type.service(),
                        resource_type.type_name(),
                    )
                    .replace('\"', "");
                    return Err(TransmuteError::new(format!(
                        "{prop_name} is not a valid property for resource {resource_name} of type {resource_type}"
                    )));
                }
                let translator = ResourceTranslator {
                    schema,
                    origins,
                    value_type: property_type,
                };
                properties.insert(prop_name, translator.translate(prop)?);
            }

            let mut instruction = Self {
                name: resource_name,
                condition: attributes.condition,
                metadata,
                update_policy,
                deletion_policy: attributes.deletion_policy,
                dependencies: attributes.depends_on,
                resource_type,
                properties,
                references: BTreeSet::default(),
            };
            instruction.generate_references();
            instructions.push(instruction);
        }

        Ok(order(instructions))
    }

    fn generate_references(&mut self) {
        self.references.extend(self.dependencies.iter().cloned());
        for (_, property) in &self.properties {
            self.references.extend(find_references(property));
        }
    }
}

#[derive(Clone, Debug, PartialEq)]
pub enum ResourceType {
    Alexa { service: String, type_name: String },
    // A standard resource type (AWS::<service>::<type_name>)
    AWS { service: String, type_name: String },
    // A custom resource type (Custom::<something>)
    Custom(String),
}

impl ResourceType {
    fn parse(from: &str) -> Result<Self, TransmuteError> {
        let mut parts = from.split("::");
        let first = parts.next().unwrap();

        match first {
            "Custom" => {
                let name = match parts.next() {
                    Some("") | None => {
                        return Err(TransmuteError::new(format!(
                            "invalid resource type: {from:?}"
                        )))
                    }
                    Some(name) => name,
                };
                if parts.next().is_some() {
                    return Err(TransmuteError::new(format!(
                        "invalid resource type: {from:?} (only two segments expected)"
                    )));
                }
                Ok(Self::Custom(name.into()))
            }
            "Alexa" => {
                let service = match parts.next() {
                    Some("") | None => {
                        return Err(TransmuteError::new(format!(
                            "invalid resource type: {from:?} (missing service name)"
                        )))
                    }
                    Some(service) => service.into(),
                };
                let type_name = match parts.next() {
                    Some("") | None => {
                        return Err(TransmuteError::new(format!(
                            "invalid resource type: {from:?} (missing resource type name)"
                        )))
                    }
                    Some(type_name) => type_name.into(),
                };
                if parts.next().is_some() {
                    return Err(TransmuteError::new(format!(
                        "invalid resource type: {from:?} (only three segments expected)"
                    )));
                }
                Ok(Self::Alexa { service, type_name })
            }
            "AWS" => {
                let service = match parts.next() {
                    Some("") | None => {
                        return Err(TransmuteError::new(format!(
                            "invalid resource type: {from:?} (missing service name)"
                        )))
                    }
                    Some(service) => {
                        if service.to_lowercase().eq("serverless") {
                            "SAM".into()
                        } else {
                            service.into()
                        }
                    }
                };
                let type_name = match parts.next() {
                    Some("") | None => {
                        return Err(TransmuteError::new(format!(
                            "invalid resource type: {from:?} (missing resource type name)"
                        )))
                    }
                    Some(type_name) => type_name.into(),
                };
                if parts.next().is_some() {
                    return Err(TransmuteError::new(format!(
                        "invalid resource type: {from:?} (only three segments expected)"
                    )));
                }
                Ok(Self::AWS { service, type_name })
            }
            other => Err(TransmuteError::new(format!(
                "unknown resource type namespace: {other} (in {from:?})"
            ))),
        }
    }

    pub fn scope(&self) -> &str {
        match self {
            Self::Alexa { .. } => "alexa",
            Self::AWS { .. } => "aws",
            Self::Custom(..) => "custom",
        }
    }
    pub fn service(&self) -> &str {
        match self {
            Self::Alexa { service, .. } | Self::AWS { service, .. } => service,
            Self::Custom(_) => "CloudFormation",
        }
    }

    pub fn type_name(&self) -> &str {
        match self {
            Self::Alexa { type_name, .. } | Self::AWS { type_name, .. } => type_name,
            Self::Custom(_) => "CustomResource",
        }
    }
}

impl fmt::Display for ResourceType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Alexa { service, type_name } => write!(f, "Alexa::{}::{}", service, type_name),
            Self::AWS { service, type_name } => write!(f, "AWS::{}::{}", service, type_name),
            Self::Custom(name) => write!(f, "Custom::{}", name),
        }
    }
}

fn order(resource_instructions: Vec<ResourceInstruction>) -> Vec<ResourceInstruction> {
    let mut topo = TopologicalSort::new();
    let mut hash = HashMap::with_capacity(resource_instructions.len());
    for resource_instruction in resource_instructions {
        topo.insert(resource_instruction.name.to_string());

        for dep in &resource_instruction.dependencies {
            topo.add_dependency(dep, resource_instruction.name.to_string());
        }
        for (_, property) in &resource_instruction.properties {
            find_dependencies(&resource_instruction.name, property, &mut topo)
        }
        hash.insert(resource_instruction.name.to_string(), resource_instruction);
    }

    let mut sorted_instructions = Vec::with_capacity(hash.len());
    while !topo.is_empty() {
        let mut list = topo.pop_all();
        if list.is_empty() {
            panic!("Cyclic dependency in your resources ")
        }
        // Ensures consistent ordering of generated code...
        list.sort();
        sorted_instructions.extend(list.into_iter().map(|name| match hash.remove(&name) {
            None => panic!("Attempted to reference or depend on a resource not defined in the CloudFormation template. Resource: {}", name),
            Some(instruction) => instruction,
        }));
    }
    sorted_instructions
}

pub(crate) fn find_references(resource: &ResourceIr) -> HashSet<String> {
    let mut set = HashSet::default();

    match resource {
        ResourceIr::Null
        | ResourceIr::Bool(_)
        | ResourceIr::Number(_)
        | ResourceIr::Double(_)
        | ResourceIr::String(_)
        | ResourceIr::ImportValue(_) => { /* No references */ }

        ResourceIr::Array(_, arr) => {
            for resource in arr {
                set.extend(find_references(resource));
            }
        }
        ResourceIr::Object(_, hash) => {
            for resource in hash.values() {
                set.extend(find_references(resource));
            }
        }
        ResourceIr::If(_, x, y) => {
            set.extend(find_references(x.deref()));
            set.extend(find_references(y.deref()));
        }
        ResourceIr::Join(_, arr) => {
            for resource in arr {
                set.extend(find_references(resource));
            }
        }
        ResourceIr::Split(_, ir) => set = find_references(ir),
        ResourceIr::Ref(x) => match x.origin {
            Origin::CfnParameter
            | Origin::Parameter
            | Origin::Condition
            | Origin::PseudoParameter(_) => { /* No references */ }
            Origin::GetAttribute { .. } | Origin::LogicalId { .. } => {
                set.insert(x.name.clone());
            }
        },
        ResourceIr::Sub(arr) => {
            for resource in arr {
                set.extend(find_references(resource));
            }
        }
        ResourceIr::Map(_, y, z) => {
            set.extend(find_references(y.deref()));
            set.extend(find_references(z.deref()));
        }
        ResourceIr::Base64(x) => set = find_references(x.deref()),
        ResourceIr::Select(_, x) => set = find_references(x.deref()),
        ResourceIr::GetAZs(x) => set = find_references(x.deref()),
        ResourceIr::Cidr(x, y, z) => {
            set.extend(find_references(x.deref()));
            set.extend(find_references(y.deref()));
            set.extend(find_references(z.deref()));
        }
    }

    set
}

fn find_dependencies(
    resource_name: &str,
    resource: &ResourceIr,
    topo: &mut TopologicalSort<String>,
) {
    match resource {
        ResourceIr::Null
        | ResourceIr::Bool(_)
        | ResourceIr::Number(_)
        | ResourceIr::Double(_)
        | ResourceIr::String(_)
        | ResourceIr::ImportValue(_) => {}

        ResourceIr::Array(_, arr) => {
            for x in arr {
                find_dependencies(resource_name, x, topo);
            }
        }
        ResourceIr::Object(_, hash) => {
            for x in hash.values() {
                find_dependencies(resource_name, x, topo);
            }
        }
        ResourceIr::If(_, x, y) => {
            find_dependencies(resource_name, x.deref(), topo);
            find_dependencies(resource_name, y.deref(), topo);
        }
        ResourceIr::Join(_, arr) => {
            for x in arr {
                find_dependencies(resource_name, x, topo);
            }
        }
        ResourceIr::Split(_, ir) => find_dependencies(resource_name, ir, topo),
        ResourceIr::Ref(x) => match x.origin {
            Origin::CfnParameter
            | Origin::Parameter
            | Origin::Condition
            | Origin::PseudoParameter(_) => {}
            Origin::LogicalId { .. } => {
                topo.add_dependency(x.name.to_string(), resource_name.to_string());
            }
            Origin::GetAttribute { .. } => {
                topo.add_dependency(x.name.to_string(), resource_name.to_string());
            }
        },
        ResourceIr::Sub(arr) => {
            for x in arr {
                find_dependencies(resource_name, x, topo);
            }
        }
        ResourceIr::Map(_, y, z) => {
            find_dependencies(resource_name, y.deref(), topo);
            find_dependencies(resource_name, z.deref(), topo);
        }
        ResourceIr::Base64(x) => {
            find_dependencies(resource_name, x.deref(), topo);
        }
        ResourceIr::Select(_, x) => {
            find_dependencies(resource_name, x.deref(), topo);
        }
        ResourceIr::GetAZs(x) => {
            find_dependencies(resource_name, x.deref(), topo);
        }
        ResourceIr::Cidr(x, y, z) => {
            find_dependencies(resource_name, x.deref(), topo);
            find_dependencies(resource_name, y.deref(), topo);
            find_dependencies(resource_name, z.deref(), topo);
        }
    }
}

#[cfg(test)]
mod tests;
