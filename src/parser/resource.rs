use crate::primitives::WrapperF64;
use crate::TransmuteError;
use numberkit::is_digit;
use serde_yaml::{Mapping, Value};
use std::borrow::Cow;
use std::collections::HashMap;

#[derive(Debug, Eq, PartialEq)]
pub enum ResourceValue {
    // Literally just json bits here
    Null,
    Bool(bool),
    Number(i64),
    Double(WrapperF64),
    String(String),
    Array(Vec<ResourceValue>),
    Object(HashMap<String, ResourceValue>),

    /// Rest is meta functions
    /// https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-conditions.html#w2ab1c33c28c21c29
    Sub(Vec<ResourceValue>),
    FindInMap(Box<ResourceValue>, Box<ResourceValue>, Box<ResourceValue>),
    GetAtt(Box<ResourceValue>, Box<ResourceValue>),
    GetAZs(Box<ResourceValue>),
    If(Box<ResourceValue>, Box<ResourceValue>, Box<ResourceValue>),
    Join(Vec<ResourceValue>),
    Ref(String),
    Base64(Box<ResourceValue>),
    ImportValue(Box<ResourceValue>),
    Select(Box<ResourceValue>, Box<ResourceValue>),
    Cidr(Box<ResourceValue>, Box<ResourceValue>, Box<ResourceValue>),
}

impl ResourceValue {}

#[derive(Debug, Eq, PartialEq)]
pub struct ResourceParseTree {
    pub name: String,
    pub resource_type: String,
    pub condition: Option<String>,
    pub metadata: Option<ResourceValue>,
    pub dependencies: Vec<String>,
    pub update_policy: Option<ResourceValue>,
    pub deletion_policy: Option<String>,
    pub properties: HashMap<String, ResourceValue>,
}

#[derive(Debug)]
pub struct ResourcesParseTree {
    pub resources: Vec<ResourceParseTree>,
}

pub fn build_resources(resource_map: &Mapping) -> Result<ResourcesParseTree, TransmuteError> {
    let mut resources = Vec::new();

    for (name, json_value) in resource_map.iter() {
        let name = name.as_str().expect("mapping key was not a string");
        let resource_object = json_value.as_mapping().unwrap();
        let resource_type = resource_object
            .get("Type")
            .unwrap()
            .as_str()
            .unwrap()
            .to_owned();
        let condition = resource_object
            .get("Condition")
            .and_then(|t| t.as_str())
            .map(|t| t.to_string());

        let mut properties = HashMap::new();
        if let Some(x) = resource_object
            .get("Properties")
            .and_then(|x| x.as_mapping())
        {
            for (prop_name, prop_value) in x {
                let prop_name = prop_name.as_str().unwrap();
                let result = build_resources_recursively(name, prop_value)?;
                properties.insert(prop_name.to_owned(), result);
            }
        }

        let metadata_obj = resource_object.get("Metadata");
        let mut metadata = Option::None;
        if let Some(x) = metadata_obj {
            metadata = Option::Some(build_resources_recursively(name, x)?);
        }

        let update_policy_obj = resource_object.get("UpdatePolicy");
        let mut update_policy = Option::None;
        if let Some(x) = update_policy_obj {
            update_policy = Option::Some(build_resources_recursively(name, x)?);
        }

        let deletion_policy = resource_object
            .get("DeletionPolicy")
            .and_then(|x| x.as_str())
            .map(|x| x.to_string());

        let depends_on = resource_object.get("DependsOn");
        let mut dependencies = Vec::new();

        if let Some(x) = depends_on {
            match x {
                Value::String(x) => {
                    dependencies.push(x.to_string());
                }
                Value::Sequence(x) => {
                    for dep in x.iter() {
                        match dep.as_str() {
                            None => {
                                return Err(TransmuteError {
                                    details: format!(
                                        "DependsOn attribute has an array of non-strings, which isn't allowed {name}"
                                    ),
                                })
                            }
                            Some(x) => {
                                dependencies.push(x.to_string());
                            }
                        }
                    }
                }
                _ => {
                    return Err(TransmuteError {
                        details: format!(
                            "DependsOn attribute can only be a string or an array {name}"
                        ),
                    })
                }
            }
        }

        resources.push(ResourceParseTree {
            name: name.to_owned(),
            metadata,
            dependencies,
            update_policy,
            deletion_policy,
            resource_type,
            condition,
            properties,
        })
    }

    Ok(ResourcesParseTree { resources })
}

pub fn build_resources_recursively(
    name: &str,
    obj: &Value,
) -> Result<ResourceValue, TransmuteError> {
    let val: Cow<Mapping> = match obj {
        Value::String(x) => return Ok(ResourceValue::String(x.to_string())),
        Value::Null => return Ok(ResourceValue::Null),
        Value::Bool(b) => return Ok(ResourceValue::Bool(b.to_owned())),
        Value::Number(n) => {
            if is_digit(n.to_string(), false) {
                return Ok(ResourceValue::Number(n.as_i64().unwrap()));
            }
            let v = WrapperF64::new(n.as_f64().unwrap());
            return Ok(ResourceValue::Double(v));
        }
        Value::Sequence(arr) => {
            let mut v = Vec::new();
            for item in arr.iter() {
                let obj = build_resources_recursively(name, item)?;
                v.push(obj);
            }

            return Ok(ResourceValue::Array(v));
        }
        // Only real follow-up object
        Value::Mapping(x) => Cow::Borrowed(x),
        Value::Tagged(x) => {
            let mut mapping = Mapping::new();
            mapping.insert(Value::String(format!("!{}", x.tag)), x.value.clone());
            Cow::Owned(mapping)
        }
    };

    if val.len() > 1 || val.is_empty() {
        let mut hm = HashMap::new();
        for (name, obj) in val.as_ref() {
            let name = name.as_str().unwrap();
            hm.insert(name.to_owned(), build_resources_recursively(name, obj)?);
        }

        return Ok(ResourceValue::Object(hm));
    } else {
        #[allow(clippy::never_loop)]
        for (resource_name, resource_object) in val.as_ref() {
            let cond: ResourceValue = match resource_name.as_str() {
                Some("!Sub" | "Fn::Sub") => {
                    let mut v = Vec::new();
                    match resource_object {
                        Value::String(str) => {
                            v.push(ResourceValue::String(str.to_owned()));
                        }
                        Value::Sequence(arr) => {
                            for obj in arr.iter() {
                                let resource = build_resources_recursively(name, obj)?;
                                v.push(resource);
                            }
                        }
                        _ => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Sub can only be either an array or a string {name}"
                                ),
                            });
                        }
                    }
                    ResourceValue::Sub(v)
                }
                Some("!FindInMap" | "Fn::FindInMap") => {
                    let v = match resource_object.as_sequence() {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::FindInMap is supposed to be an array entry {name}"
                                ),
                            })
                        }
                        Some(x) => x,
                    };

                    let first_obj = match v.get(0) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                "Fn::FindInMap is supposed to have 3 values in array, has 0 {name}"
                            ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;
                    let second_obj = match v.get(1) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                "Fn::FindInMap is supposed to have 3 values in array, has 1 {name}"
                            ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;
                    let third_obj = match v.get(2) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                "Fn::FindInMap is supposed to have 3 values in array, has 2 {name}"
                            ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;
                    ResourceValue::FindInMap(
                        Box::new(first_obj),
                        Box::new(second_obj),
                        Box::new(third_obj),
                    )
                }
                Some("!GetAtt" | "Fn::GetAtt") => {
                    match resource_object {
                        // Short form: "Fn::GetAttr": "blah.blah"
                        Value::String(x) => {
                            let split_str: Vec<&str> = x.splitn(2, '.').collect();
                            let resource_ref = split_str.first().unwrap();
                            let attribute_ref = split_str.get(1).unwrap();

                            ResourceValue::GetAtt(
                                Box::new(ResourceValue::String(resource_ref.to_string())),
                                Box::new(ResourceValue::String(attribute_ref.to_string())),
                            )
                        }
                        Value::Sequence(v) => {
                            let first_obj = match v.get(0) {
                                None => {
                                    return Err(TransmuteError {
                                        details: format!(
                                            "Fn::GetAtt is supposed to have 3 values in array, has 0 {name}"
                                        ),
                                    })
                                }
                                Some(x) => build_resources_recursively(name, x),
                            }?;
                            let second_obj = match v.get(1) {
                                None => {
                                    return Err(TransmuteError {
                                        details: format!(
                                            "Fn::GetAtt is supposed to have 3 values in array, has 1 {name}"
                                        ),
                                    })
                                }
                                Some(x) => build_resources_recursively(name, x),
                            }?;

                            ResourceValue::GetAtt(Box::new(first_obj), Box::new(second_obj))
                        }
                        &_ => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::GetAtt is supposed to be an array entry {name}"
                                ),
                            })
                        }
                    }
                }
                Some("!GetAZs" | "Fn::GetAZs") => {
                    let v = match resource_object {
                        Value::String(_) => {
                            build_resources_recursively(name, resource_object)
                        }
                        Value::Mapping(_) => {
                            build_resources_recursively(name, resource_object)
                        }
                        x => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::GetAZs only takes a string as input for resource {name} value: {x:?}"
                                ),
                            })

                        }
                    }?;

                    ResourceValue::GetAZs(Box::new(v))
                }

                Some("!Base64" | "Fn::Base64") => {
                    let resolved_obj = build_resources_recursively(name, resource_object)?;
                    ResourceValue::Base64(Box::new(resolved_obj))
                }
                Some("!ImportValue" | "Fn::ImportValue") => {
                    let resolved_obj = build_resources_recursively(name, resource_object)?;
                    ResourceValue::ImportValue(Box::new(resolved_obj))
                }
                Some("!Select" | "Fn::Select") => {
                    let arr = resource_object.as_sequence().unwrap();

                    let index = match arr.get(0) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Select is supposed to have 2 values in array, has 0 {name}"
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;
                    let obj = match arr.get(1) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Select is supposed to have 2 values in array, has 1 {name}"
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;

                    ResourceValue::Select(Box::new(index), Box::new(obj))
                }
                Some("!If" | "Fn::If") => {
                    let v = match resource_object.as_sequence() {
                        None => {
                            return Err(TransmuteError {
                                details: format!("Fn::If is supposed to be an array entry {name}"),
                            })
                        }
                        Some(x) => x,
                    };

                    let first_obj = match v.get(0) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::If is supposed to have 3 values in array, has 0 {name}"
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;
                    let second_obj = match v.get(1) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::If is supposed to have 3 values in array, has 1 {name}"
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;
                    let third_obj = match v.get(2) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::If is supposed to have 3 values in array, has 2 {name}"
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;
                    ResourceValue::If(
                        Box::new(first_obj),
                        Box::new(second_obj),
                        Box::new(third_obj),
                    )
                }
                Some("!Join" | "Fn::Join") => {
                    let arr = match resource_object.as_sequence() {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Join is supposed to be an array entry {name}"
                                ),
                            })
                        }
                        Some(x) => x,
                    };

                    let mut v = Vec::new();

                    for obj in arr.iter() {
                        let resource = build_resources_recursively(name, obj)?;
                        v.push(resource);
                    }

                    ResourceValue::Join(v)
                }
                Some("!Cidr" | "Fn::Cidr") => {
                    let v = match resource_object.as_sequence() {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Cidr is supposed to be an array entry {name}"
                                ),
                            })
                        }
                        Some(x) => x,
                    };

                    let first_obj = match v.get(0) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Cidr is supposed to have 3 values in array, has 0 {name}"
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;
                    let second_obj = match v.get(1) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Cidr is supposed to have 3 values in array, has 1 {name}"
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;
                    let third_obj = match v.get(2) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Cidr is supposed to have 3 values in array, has 2 {name}"
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;

                    ResourceValue::Cidr(
                        Box::new(first_obj),
                        Box::new(second_obj),
                        Box::new(third_obj),
                    )
                }
                Some("!Ref" | "Ref") => {
                    let ref_name = match resource_object.as_str() {
                        None => {
                            return Err(TransmuteError {
                                details: format!("Condition must a string {name}"),
                            })
                        }
                        Some(x) => x,
                    };

                    match ref_name {
                        "AWS::NoValue" => ResourceValue::Null,
                        &_ => ResourceValue::Ref(ref_name.to_string()),
                    }
                }

                // If it is none of the above, it must be part of the resource properties, continue
                // parsing as if this was an object with a single property.
                Some(v) => {
                    let mut hm = HashMap::new();
                    hm.insert(
                        v.to_owned(),
                        build_resources_recursively(name, resource_object)?,
                    );
                    ResourceValue::Object(hm)
                }

                None => unimplemented!("resource key is not a string"),
            };

            return Ok(cond);
        }
    }

    Err(TransmuteError {
        details: format!("Could not find a parsable path for resource {name}, {obj:?}"),
    })
}
