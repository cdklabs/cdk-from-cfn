use crate::ir::reference::{Origin, Reference};
use crate::ir::sub::{sub_parse_tree, SubValue};
use crate::parser::resource::{DeletionPolicy, IntrinsicFunction, ResourceValue};
use crate::primitives::WrapperF64;
use crate::specification::{CfnType, Specification, Structure};
use crate::{CloudformationParseTree, TransmuteError};
use indexmap::IndexMap;
use std::collections::{HashMap, HashSet};
use std::ops::Deref;
use topological_sort::TopologicalSort;

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
    Array(Structure, Vec<ResourceIr>),
    Object(Structure, IndexMap<String, ResourceIr>),

    /// Rest is meta functions
    /// https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-conditions.html#w2ab1c33c28c21c29
    If(String, Box<ResourceIr>, Box<ResourceIr>),
    Join(String, Vec<ResourceIr>),
    Split(String, Box<ResourceIr>),
    Ref(Reference),
    Sub(Vec<ResourceIr>),
    Map(Box<ResourceIr>, Box<ResourceIr>, Box<ResourceIr>),
    Base64(Box<ResourceIr>),
    ImportValue(Box<ResourceIr>),
    GetAZs(Box<ResourceIr>),
    Select(i64, Box<ResourceIr>),
    Cidr(Box<ResourceIr>, Box<ResourceIr>, Box<ResourceIr>),
}

/// ResourceTranslationInputs is a place to store all the intermediate recursion
/// for resource types.
#[derive(Clone, Debug)]
pub struct ResourceTranslationInputs<'t> {
    pub parse_tree: &'t CloudformationParseTree,
    pub complexity: Structure,
    pub resource_metadata: Option<ResourceMetadata<'t>>,
}

#[derive(Clone, Debug)]
pub struct ResourceMetadata<'t> {
    specification: &'t Specification,
    property_type: Option<&'t str>,
    resource_type: &'t str,
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
    // Referrers are a meta concept of "anything other resource that ResourceInstruction references".
    // This could be in a property or dependency path.
    pub referrers: HashSet<String>,
    pub resource_type: String,
    pub properties: IndexMap<String, ResourceIr>,
}

pub fn translates_resources(parse_tree: &CloudformationParseTree) -> Vec<ResourceInstruction> {
    let spec = Specification::default();
    let mut resource_instructions = Vec::new();
    for (name, resource) in &parse_tree.resources {
        let mut props = IndexMap::with_capacity(resource.properties.len());
        let resource_spec = spec.get_resource(&resource.resource_type).unwrap();
        for (name, prop) in resource.properties.iter() {
            let complexity = resource_spec.structure(name).unwrap();

            let property_type =
                Specification::full_property_name(&complexity, &resource.resource_type);
            let property_type = property_type.as_deref();
            let rt = ResourceTranslationInputs {
                parse_tree,
                complexity,
                resource_metadata: Option::Some(ResourceMetadata {
                    specification: &spec,
                    property_type,
                    resource_type: &resource.resource_type,
                }),
            };

            let ir = translate_resource(prop, &rt).unwrap();

            props.insert(name.to_string(), ir);
        }
        let metadata = optional_ir_json(parse_tree, &resource.metadata).unwrap();
        let update_policy = optional_ir_json(parse_tree, &resource.update_policy).unwrap();

        let mut resource_instruction = ResourceInstruction {
            name: name.clone(),
            resource_type: resource.resource_type.to_string(),
            dependencies: resource.depends_on.clone(),
            deletion_policy: resource.deletion_policy,
            condition: resource.condition.clone(),
            properties: props,
            metadata,
            update_policy,

            // Everything below this line will be blown away by "later updates".
            referrers: HashSet::default(),
        };
        let references = generate_references(&resource_instruction);
        resource_instruction.referrers = references;
        resource_instructions.push(resource_instruction);
    }
    order(resource_instructions)
}

fn order(resource_instructions: Vec<ResourceInstruction>) -> Vec<ResourceInstruction> {
    let mut topo = TopologicalSort::new();
    let mut hash = HashMap::with_capacity(resource_instructions.len());
    for resource_instruction in resource_instructions {
        topo.insert(resource_instruction.name.to_string());

        for dep in resource_instruction.dependencies.iter() {
            topo.add_dependency(dep, resource_instruction.name.to_string());
        }
        for (_, property) in resource_instruction.properties.iter() {
            find_dependencies(&resource_instruction.name, property, &mut topo)
        }
        hash.insert(resource_instruction.name.to_string(), resource_instruction);
    }

    let mut sorted_instructions = Vec::with_capacity(hash.len());
    while !topo.is_empty() {
        match topo.pop() {
            None => {
                panic!("Cyclic dependency in your resources ")
            }
            Some(x) => {
                let rs = match hash.remove(&x) {
                    None => {
                        panic!("Attempted to reference or depend on a resource not defined in the CloudFormation template. Resource: {}", x);
                    }
                    Some(x) => x,
                };
                sorted_instructions.push(rs);
            }
        }
    }
    sorted_instructions
}

fn optional_ir_json(
    parse_tree: &CloudformationParseTree,
    input: &Option<ResourceValue>,
) -> Result<Option<ResourceIr>, TransmuteError> {
    let mut policy: Option<ResourceIr> = Option::None;
    if let Some(x) = input {
        let complexity = Structure::Simple(CfnType::Json);
        let rt = ResourceTranslationInputs {
            parse_tree,
            complexity,
            resource_metadata: Option::None,
        };

        let ir = translate_resource(x, &rt).unwrap();
        policy = Option::Some(ir);
    }

    Ok(policy)
}

fn generate_references(resource_instruction: &ResourceInstruction) -> HashSet<String> {
    let mut references = HashSet::with_capacity(resource_instruction.dependencies.len());
    for dep in resource_instruction.dependencies.iter() {
        references.insert(dep.clone());
    }

    for (_, property) in resource_instruction.properties.iter() {
        let opt_refs = find_references(property);
        if let Some(x) = opt_refs {
            references.extend(x)
        }
    }

    references
}

fn find_references(resource: &ResourceIr) -> Option<Vec<String>> {
    match resource {
        ResourceIr::Null
        | ResourceIr::Bool(_)
        | ResourceIr::Number(_)
        | ResourceIr::Double(_)
        | ResourceIr::String(_) => Option::None,

        ResourceIr::Array(_, arr) => {
            let mut v = Vec::with_capacity(arr.len());
            for resource in arr {
                if let Some(vec) = find_references(resource) {
                    v.extend(vec);
                }
            }

            Option::Some(v)
        }
        ResourceIr::Object(_, hash) => {
            let mut v = Vec::with_capacity(hash.len());
            for resource in hash.values() {
                if let Some(vec) = find_references(resource) {
                    v.extend(vec);
                }
            }

            Option::Some(v)
        }
        ResourceIr::If(_, x, y) => {
            let mut v = Vec::with_capacity(2);
            if let Some(vec) = find_references(x.deref()) {
                v.extend(vec);
            }
            if let Some(vec) = find_references(y.deref()) {
                v.extend(vec);
            }

            Option::Some(v)
        }
        ResourceIr::Join(_, arr) => {
            let mut v = Vec::new();
            for resource in arr {
                if let Some(vec) = find_references(resource) {
                    v.extend(vec);
                }
            }

            Option::Some(v)
        }
        ResourceIr::Split(_, ir) => find_references(ir),
        ResourceIr::Ref(x) => match x.origin {
            Origin::Parameter | Origin::Condition | Origin::PseudoParameter(_) => Option::None,
            Origin::LogicalId => Option::Some(vec![x.name.to_string()]),
            Origin::GetAttribute(_) => Option::Some(vec![x.name.to_string()]),
        },
        ResourceIr::Sub(arr) => {
            let mut v = Vec::new();
            for resource in arr {
                if let Some(vec) = find_references(resource) {
                    v.extend(vec);
                }
            }

            Option::Some(v)
        }
        ResourceIr::Map(x, y, z) => {
            let mut v = Vec::new();
            if let Some(vec) = find_references(x.deref()) {
                v.extend(vec);
            }
            if let Some(vec) = find_references(y.deref()) {
                v.extend(vec);
            }
            if let Some(vec) = find_references(z.deref()) {
                v.extend(vec);
            }
            Option::Some(v)
        }
        ResourceIr::Base64(x) => find_references(x.deref()),
        ResourceIr::ImportValue(x) => find_references(x.deref()),
        ResourceIr::Select(_, x) => find_references(x.deref()),
        ResourceIr::GetAZs(x) => find_references(x.deref()),
        ResourceIr::Cidr(x, y, z) => {
            let mut v = Vec::new();
            if let Some(vec) = find_references(x.deref()) {
                v.extend(vec);
            }
            if let Some(vec) = find_references(y.deref()) {
                v.extend(vec);
            }
            if let Some(vec) = find_references(z.deref()) {
                v.extend(vec);
            }
            Option::Some(v)
        }
    }
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
        | ResourceIr::String(_) => {}

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
            Origin::Parameter | Origin::Condition | Origin::PseudoParameter(_) => {}
            Origin::LogicalId => {
                topo.add_dependency(x.name.to_string(), resource_name.to_string());
            }
            Origin::GetAttribute(_) => {
                topo.add_dependency(x.name.to_string(), resource_name.to_string());
            }
        },
        ResourceIr::Sub(arr) => {
            for x in arr {
                find_dependencies(resource_name, x, topo);
            }
        }
        ResourceIr::Map(x, y, z) => {
            find_dependencies(resource_name, x.deref(), topo);
            find_dependencies(resource_name, y.deref(), topo);
            find_dependencies(resource_name, z.deref(), topo);
        }
        ResourceIr::Base64(x) => {
            find_dependencies(resource_name, x.deref(), topo);
        }
        ResourceIr::ImportValue(x) => {
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

pub fn translate_resource(
    resource_value: &ResourceValue,
    resource_translator: &ResourceTranslationInputs,
) -> Result<ResourceIr, TransmuteError> {
    match resource_value {
        ResourceValue::Null => Ok(ResourceIr::Null),
        ResourceValue::Bool(b) => Ok(ResourceIr::Bool(*b)),
        ResourceValue::Number(n) => Ok(ResourceIr::Number(*n)),
        ResourceValue::Double(d) => Ok(ResourceIr::Double(*d)),
        ResourceValue::String(s) => {
            if let Structure::Simple(simple_type) = &resource_translator.complexity {
                return match simple_type {
                    CfnType::Boolean => Ok(ResourceIr::Bool(s.parse().unwrap())),
                    CfnType::Integer => Ok(ResourceIr::Number(s.parse().unwrap())),
                    CfnType::Double => Ok(ResourceIr::Number(s.parse().unwrap())),
                    &_ => Ok(ResourceIr::String(s.to_string())),
                };
            }
            Ok(ResourceIr::String(s.to_string()))
        }
        ResourceValue::Array(parse_resource_vec) => {
            let mut array_ir = Vec::new();
            for parse_resource in parse_resource_vec {
                let x = translate_resource(parse_resource, resource_translator)?;
                array_ir.push(x);
            }

            Ok(ResourceIr::Array(
                resource_translator.complexity.clone(),
                array_ir,
            ))
        }
        ResourceValue::Object(o) => {
            let mut new_hash = IndexMap::with_capacity(o.len());
            for (s, rv) in o {
                let property_ir = match resource_translator.complexity {
                    Structure::Simple(_) => translate_resource(rv, resource_translator)?,
                    Structure::Composite(_) => {
                        // Update the rule with it's underlying property rule.
                        let mut new_rt = resource_translator.clone();
                        let resource_metadata =
                            resource_translator.resource_metadata.as_ref().unwrap();
                        let rule = resource_metadata
                            .specification
                            .property_type(
                                resource_translator
                                    .resource_metadata
                                    .as_ref()
                                    .unwrap()
                                    .property_type
                                    .unwrap(),
                            )
                            .unwrap();
                        let properties = rule.as_properties().unwrap();
                        let property_rule = properties.get(s).unwrap();
                        new_rt.complexity = property_rule.get_structure();
                        let opt = Specification::full_property_name(
                            &property_rule.get_structure(),
                            resource_metadata.resource_type,
                        );
                        let mut new_metadata = resource_metadata.clone();
                        new_metadata.property_type = opt.as_deref();
                        new_rt.resource_metadata.replace(new_metadata);
                        translate_resource(rv, &new_rt)?
                    }
                };

                new_hash.insert(s.to_string(), property_ir);
            }

            Ok(ResourceIr::Object(
                resource_translator.complexity.clone(),
                new_hash,
            ))
        }
        ResourceValue::IntrinsicFunction(intrinsic) => {
            match intrinsic.as_ref() {
                IntrinsicFunction::Sub { string, replaces } => {
                    let mut excess_map = IndexMap::new();
                    if let Some(replaces) = replaces {
                        match replaces {
                            ResourceValue::Object(obj) => {
                                excess_map.reserve(obj.len());
                                for (key, val) in obj.iter() {
                                    let val_str = translate_resource(val, resource_translator)?;
                                    excess_map.insert(key.to_string(), val_str);
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

                    let vars = sub_parse_tree(string)?;
                    let r = vars
                        .iter()
                        .map(|x| match &x {
                            SubValue::String(x) => ResourceIr::String(x.to_string()),
                            SubValue::Variable(x) => match excess_map.get(x) {
                                None => {
                                    ResourceIr::Ref(find_ref(x, resource_translator.parse_tree))
                                }
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
                    let mut rt = resource_translator.clone();
                    rt.complexity = Structure::Simple(CfnType::String);
                    let map_name_str = translate_resource(map_name, &rt)?;
                    let top_level_key_str = translate_resource(top_level_key, &rt)?;
                    let second_level_key_str = translate_resource(second_level_key, &rt)?;
                    Ok(ResourceIr::Map(
                        Box::new(map_name_str),
                        Box::new(top_level_key_str),
                        Box::new(second_level_key_str),
                    ))
                }
                IntrinsicFunction::GetAtt {
                    logical_name,
                    attribute_name,
                } => Ok(ResourceIr::Ref(Reference::new(
                    logical_name,
                    Origin::GetAttribute(attribute_name.clone()),
                ))),
                IntrinsicFunction::If {
                    condition_name,
                    value_if_true,
                    value_if_false,
                } => {
                    let value_if_true = translate_resource(value_if_true, resource_translator)?;
                    let value_if_false = translate_resource(value_if_false, resource_translator)?;

                    Ok(ResourceIr::If(
                        condition_name.clone(),
                        Box::new(value_if_true),
                        Box::new(value_if_false),
                    ))
                }
                IntrinsicFunction::Join { sep, list } => {
                    let mut irs = Vec::new();
                    match list {
                        ResourceValue::Array(list) => {
                            irs.reserve(list.len());
                            for rv in list.iter() {
                                let resource_ir = translate_resource(rv, resource_translator)?;
                                irs.push(resource_ir)
                            }
                        }
                        list => irs.push(translate_resource(list, resource_translator)?),
                    }

                    Ok(ResourceIr::Join(sep.to_string(), irs))
                }
                IntrinsicFunction::Split { sep, string } => {
                    let ir = translate_resource(string, resource_translator)?;

                    Ok(ResourceIr::Split(sep.clone(), Box::new(ir)))
                }
                IntrinsicFunction::Ref(x) => {
                    Ok(ResourceIr::Ref(find_ref(x, resource_translator.parse_tree)))
                }
                IntrinsicFunction::Base64(x) => {
                    let ir = translate_resource(x, resource_translator)?;
                    Ok(ResourceIr::Base64(Box::new(ir)))
                }
                IntrinsicFunction::ImportValue(x) => {
                    let ir = translate_resource(x, resource_translator)?;
                    Ok(ResourceIr::ImportValue(Box::new(ir)))
                }
                IntrinsicFunction::Select { index, list } => {
                    let index = match index.deref() {
                        ResourceValue::String(x) => match x.parse::<i64>() {
                            Ok(x) => x,
                            Err(_) => {
                                return Err(TransmuteError::new("index must be int for Select"))
                            }
                        },
                        ResourceValue::Number(x) => *x,
                        _ => {
                            return Err(TransmuteError::new("Separator for join must be a string"))
                        }
                    };

                    let obj = translate_resource(list, resource_translator)?;
                    Ok(ResourceIr::Select(index, Box::new(obj)))
                }
                IntrinsicFunction::GetAZs(x) => {
                    let ir = translate_resource(x, resource_translator)?;
                    Ok(ResourceIr::GetAZs(Box::new(ir)))
                }
                IntrinsicFunction::Cidr {
                    ip_block,
                    count,
                    cidr_bits,
                } => {
                    let mut rt = resource_translator.clone();
                    rt.complexity = Structure::Simple(CfnType::String);
                    let ip_block_str = translate_resource(ip_block, &rt)?;
                    let count_str = translate_resource(count, &rt)?;
                    let cidr_bits_str = translate_resource(cidr_bits, &rt)?;
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

fn find_ref(x: &str, parse_tree: &CloudformationParseTree) -> Reference {
    let opt_pseudo = Reference::match_pseudo_parameter(x);

    if let Some(pseudo) = opt_pseudo {
        return Reference::new(x, Origin::PseudoParameter(pseudo));
    }

    for (name, _) in &parse_tree.parameters {
        if name == x {
            return Reference::new(x, Origin::Parameter);
        }
    }

    // if x has a period, it is actually a get-attr
    if x.contains('.') {
        let splits = x.split('.');
        let sp: Vec<&str> = splits.collect();
        let name = sp[0];
        let attr = sp[1];

        return Reference::new(name, Origin::GetAttribute(attr.to_string()));
    }
    Reference::new(x, Origin::LogicalId)
}

#[cfg(test)]
mod tests {
    use std::collections::HashSet;

    use indexmap::IndexMap;

    use crate::ir::reference::{Origin, Reference};
    use crate::ir::resources::{generate_references, order, ResourceInstruction, ResourceIr};

    #[test]
    fn test_ir_ordering() {
        let ir_instruction = ResourceInstruction {
            name: "A".to_string(),
            condition: None,
            metadata: Option::None,
            deletion_policy: Option::None,
            update_policy: Option::None,
            dependencies: Vec::new(),
            resource_type: "".to_string(),
            referrers: HashSet::default(),
            properties: IndexMap::default(),
        };

        let later = ResourceInstruction {
            name: "B".to_string(),
            condition: None,
            dependencies: Vec::new(),
            metadata: Option::None,
            deletion_policy: Option::None,
            update_policy: Option::None,
            resource_type: "".to_string(),
            referrers: HashSet::default(),
            properties: create_property(
                "something",
                ResourceIr::Ref(Reference::new("A", Origin::LogicalId)),
            ),
        };

        let misordered = vec![later.clone(), ir_instruction.clone()];

        let actual = order(misordered);
        assert_eq!(actual, vec![ir_instruction, later]);
    }

    #[test]
    fn test_ref_links() {
        let ir_instruction = ResourceInstruction {
            name: "A".to_string(),
            condition: None,
            metadata: Option::None,
            deletion_policy: Option::None,
            update_policy: Option::None,
            dependencies: vec!["foo".to_string()],
            resource_type: "".to_string(),
            referrers: HashSet::default(),
            properties: create_property(
                "something",
                ResourceIr::Ref(Reference::new("bar", Origin::LogicalId)),
            ),
        };

        let refs = generate_references(&ir_instruction);
        assert_eq!(refs, HashSet::from(["foo".into(), "bar".into()]));
    }

    fn create_property(name: &str, resource: ResourceIr) -> IndexMap<String, ResourceIr> {
        IndexMap::from([(name.into(), resource)])
    }
}
