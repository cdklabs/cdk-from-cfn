use crate::ir::reference::{Origin, Reference};
use crate::parser::resource::{ResourceValue, WrapperF64};
use crate::parser::sub::{sub_parse_tree, SubValue};
use crate::specification::{spec, Complexity, SimpleType, Specification};
use crate::{CloudformationParseTree, TransmuteError};
use std::collections::HashMap;
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
    Array(Complexity, Vec<ResourceIr>),
    Object(Complexity, HashMap<String, ResourceIr>),

    /// Rest is meta functions
    /// https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-conditions.html#w2ab1c33c28c21c29
    If(String, Box<ResourceIr>, Box<ResourceIr>),
    Join(String, Vec<ResourceIr>),
    Ref(Reference),
    Sub(Vec<ResourceIr>),
    Map(Box<ResourceIr>, Box<ResourceIr>, Box<ResourceIr>),
    Base64(Box<ResourceIr>),
    ImportValue(Box<ResourceIr>),
    GetAZs(Box<ResourceIr>),
    Select(i64, Box<ResourceIr>),
}

/// ResourceTranslationInputs is a place to store all the intermediate recursion
/// for resource types.
#[derive(Clone, Debug)]
pub struct ResourceTranslationInputs<'t> {
    pub parse_tree: &'t CloudformationParseTree,
    pub complexity: Complexity,
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
    pub deletion_policy: Option<String>,
    pub dependencies: Vec<String>,
    pub resource_type: String,
    pub properties: HashMap<String, ResourceIr>,
}

pub fn translates_resources(parse_tree: &CloudformationParseTree) -> Vec<ResourceInstruction> {
    let spec = spec();
    let mut resource_instructions = Vec::new();
    for resource in parse_tree.resources.resources.iter() {
        let mut props = HashMap::new();
        let resource_spec = spec.get_resource(&resource.resource_type).unwrap();
        for (name, prop) in resource.properties.iter() {
            let complexity = resource_spec.property_complexity(name).unwrap();

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
        resource_instructions.push(ResourceInstruction {
            name: resource.name.to_string(),
            resource_type: resource.resource_type.to_string(),
            dependencies: resource.dependencies.clone(),
            deletion_policy: resource.deletion_policy.clone(),
            condition: resource.condition.clone(),
            properties: props,
            metadata,
            update_policy,
        });
    }
    order(resource_instructions)
}

fn order(resource_instructions: Vec<ResourceInstruction>) -> Vec<ResourceInstruction> {
    let mut topo = TopologicalSort::new();
    let mut hash = HashMap::new();
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

    let mut sorted_instructions = Vec::new();
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
        let complexity = Complexity::Simple(SimpleType::Json);
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
            if let Complexity::Simple(simple_type) = &resource_translator.complexity {
                return match simple_type {
                    SimpleType::Boolean => Ok(ResourceIr::Bool(s.parse().unwrap())),
                    SimpleType::Integer => Ok(ResourceIr::Number(s.parse().unwrap())),
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
            let mut new_hash = HashMap::new();
            for (s, rv) in o {
                let property_ir = match resource_translator.complexity {
                    Complexity::Simple(_) => translate_resource(rv, resource_translator)?,
                    Complexity::Complex(_) => {
                        // Update the rule with it's underlying property rule.
                        let mut new_rt = resource_translator.clone();
                        let resource_metadata =
                            resource_translator.resource_metadata.as_ref().unwrap();
                        let rule = resource_metadata
                            .specification
                            .property_types
                            .get(
                                &resource_translator
                                    .resource_metadata
                                    .as_ref()
                                    .unwrap()
                                    .property_type
                                    .unwrap()
                                    .to_string(),
                            )
                            .unwrap();
                        let properties = rule.properties.as_ref().unwrap();
                        let property_rule = properties.get(s).unwrap();
                        new_rt.complexity = property_rule.get_complexity();
                        let opt = Specification::full_property_name(
                            &property_rule.get_complexity(),
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
        ResourceValue::Sub(arr) => {
            // Sub has two ways of being built: Either resolution via a bunch of objects
            // or everything is in the first sub element, and that's it.
            // just resolve the objects.
            let val = &arr[0];
            let val = match val {
                ResourceValue::String(x) => x,
                _ => return Err(TransmuteError::new("First value in sub must be a string")),
            };

            let mut excess_map = HashMap::new();
            if arr.len() > 1 {
                let mut iter = arr.iter();
                iter.next();

                for obj in iter {
                    match obj {
                        ResourceValue::Object(obj) => {
                            for (key, val) in obj.iter() {
                                let val_str = translate_resource(val, resource_translator)?;
                                excess_map.insert(key.to_string(), val_str);
                            }
                        }
                        _ => {
                            // these aren't possible, so panic
                            return Err(TransmuteError::new("Sub excess map must be an object"));
                        }
                    }
                }
            }
            let vars = sub_parse_tree(val.as_str())?;
            let r = vars
                .iter()
                .map(|x| match &x {
                    SubValue::String(x) => ResourceIr::String(x.to_string()),
                    SubValue::Variable(x) => match excess_map.get(x) {
                        None => {
                            // if x has a period, it is actually a get-attr
                            ResourceIr::Ref(find_ref(x, resource_translator.parse_tree))
                        }
                        Some(x) => x.clone(),
                    },
                })
                .collect();
            Ok(ResourceIr::Sub(r))
        }
        ResourceValue::FindInMap(mapper, first, second) => {
            let mapper_str = translate_resource(mapper, resource_translator)?;
            let first_str = translate_resource(first, resource_translator)?;
            let second_str = translate_resource(second, resource_translator)?;
            Ok(ResourceIr::Map(
                Box::new(mapper_str),
                Box::new(first_str),
                Box::new(second_str),
            ))
        }
        ResourceValue::GetAtt(name, attribute) => {
            let name: &ResourceValue = name.as_ref();
            let attribute: &ResourceValue = attribute.as_ref();
            let resource_name = match name {
                ResourceValue::String(x) => x,
                _ => {
                    return Err(TransmuteError::new(
                        "Get attribute first element must be a string",
                    ))
                }
            };
            let attr_name = match attribute {
                ResourceValue::String(x) => x,
                _ => {
                    return Err(TransmuteError::new(
                        "Get attribute first element must be a string",
                    ))
                }
            };
            Ok(ResourceIr::Ref(Reference::new(
                resource_name,
                Origin::GetAttribute(attr_name.to_string()),
            )))
        }
        ResourceValue::If(bool_expr, true_expr, false_expr) => {
            let bool_expr = match bool_expr.as_ref() {
                ResourceValue::String(x) => x,
                &_ => {
                    return Err(TransmuteError::new(
                        "Resource value if statement truth must be a string",
                    ));
                }
            };
            let true_expr = translate_resource(true_expr, resource_translator)?;
            let false_expr = translate_resource(false_expr, resource_translator)?;

            Ok(ResourceIr::If(
                bool_expr.to_string(),
                Box::new(true_expr),
                Box::new(false_expr),
            ))
        }
        ResourceValue::Join(x) => {
            let sep = x.get(0).unwrap();

            let sep = match sep {
                ResourceValue::String(x) => x,
                _ => return Err(TransmuteError::new("Separator for join must be a string")),
            };

            let iterator = x.iter().skip(1);

            let mut irs = Vec::new();
            for rv in iterator {
                let resource_ir = translate_resource(rv, resource_translator)?;
                irs.push(resource_ir)
            }

            Ok(ResourceIr::Join(sep.to_string(), irs))
        }
        ResourceValue::Ref(x) => Ok(ResourceIr::Ref(find_ref(x, resource_translator.parse_tree))),
        ResourceValue::Base64(x) => {
            let ir = translate_resource(x, resource_translator)?;
            Ok(ResourceIr::Base64(Box::new(ir)))
        }
        ResourceValue::ImportValue(x) => {
            let ir = translate_resource(x, resource_translator)?;
            Ok(ResourceIr::ImportValue(Box::new(ir)))
        }
        ResourceValue::Select(index, x) => {
            let index = match index.deref() {
                ResourceValue::String(x) => match x.parse::<i64>() {
                    Ok(x) => x,
                    Err(_) => return Err(TransmuteError::new("index must be int for Select")),
                },
                ResourceValue::Number(x) => *x,
                _ => return Err(TransmuteError::new("Separator for join must be a string")),
            };

            let obj = translate_resource(x.deref(), resource_translator)?;
            Ok(ResourceIr::Select(index, Box::new(obj)))
        }
        ResourceValue::GetAZs(x) => {
            let ir = translate_resource(x, resource_translator)?;
            Ok(ResourceIr::GetAZs(Box::new(ir)))
        }
    }
}

fn find_ref(x: &str, parse_tree: &CloudformationParseTree) -> Reference {
    let opt_pseudo = Reference::match_pseudo_parameter(x);

    if let Some(pseudo) = opt_pseudo {
        return Reference::new(x, Origin::PseudoParameter(pseudo));
    }

    for (name, _) in parse_tree.parameters.params.iter() {
        if name == x {
            return Reference::new(x, Origin::Parameter);
        }
    }

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
    use crate::ir::reference::{Origin, Reference};
    use crate::ir::resources::{order, ResourceInstruction, ResourceIr};
    use std::collections::HashMap;

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
            properties: HashMap::new(),
        };

        let later = ResourceInstruction {
            name: "B".to_string(),
            condition: None,
            dependencies: Vec::new(),
            metadata: Option::None,
            deletion_policy: Option::None,
            update_policy: Option::None,
            resource_type: "".to_string(),
            properties: create_property(
                "something",
                ResourceIr::Ref(Reference::new("A", Origin::LogicalId)),
            ),
        };

        let misordered = vec![later.clone(), ir_instruction.clone()];

        let actual = order(misordered);
        assert_eq!(actual, vec![ir_instruction, later]);
    }

    fn create_property(name: &str, resource: ResourceIr) -> HashMap<String, ResourceIr> {
        let mut hash = HashMap::new();
        hash.insert(name.to_string(), resource);
        hash
    }
}
