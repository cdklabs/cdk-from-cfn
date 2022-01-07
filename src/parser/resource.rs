use crate::TransmuteError;
use serde_json::{Map, Value};
use std::collections::HashMap;

#[derive(Debug, Eq, PartialEq)]
pub enum ResourceValue {
    // Literally just json bits here
    Null,
    Bool(bool),
    Number(i64),
    String(String),
    Array(Vec<ResourceValue>),
    Object(HashMap<String, ResourceValue>),

    /// Rest is meta functions
    /// https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-conditions.html#w2ab1c33c28c21c29
    Sub(Vec<ResourceValue>),
    FindInMap(Box<ResourceValue>, Box<ResourceValue>, Box<ResourceValue>),
    GetAtt(Box<ResourceValue>, Box<ResourceValue>),
    If(Box<ResourceValue>, Box<ResourceValue>, Box<ResourceValue>),
    Join(Vec<ResourceValue>),
    Ref(String),
    Base64(Box<ResourceValue>),
    ImportValue(Box<ResourceValue>),
    Select(Box<ResourceValue>, Box<ResourceValue>), // GetAZs
                                                    // Cidr
}

impl ResourceValue {}

#[derive(Debug, Eq, PartialEq)]
pub struct ResourceParseTree {
    pub name: String,
    pub resource_type: String,
    pub condition: Option<String>,
    pub properties: HashMap<String, ResourceValue>,
}

#[derive(Debug)]
pub struct ResourcesParseTree {
    pub resources: Vec<ResourceParseTree>,
}

pub fn build_resources(
    resource_map: &Map<String, Value>,
) -> Result<ResourcesParseTree, TransmuteError> {
    let mut resources = Vec::new();

    for (name, json_value) in resource_map.iter() {
        let resource_object = json_value.as_object().unwrap();
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
        for (prop_name, prop_value) in resource_object
            .get("Properties")
            .and_then(|x| x.as_object())
            .unwrap()
        {
            let result = build_resources_recursively(name, prop_value)?;
            properties.insert(prop_name.to_owned(), result);
        }
        resources.push(ResourceParseTree {
            name: name.to_owned(),
            resource_type,
            condition,
            properties,
        })
    }

    Ok(ResourcesParseTree { resources })
}

fn build_resources_recursively(name: &str, obj: &Value) -> Result<ResourceValue, TransmuteError> {
    let val = match obj {
        Value::String(x) => return Ok(ResourceValue::String(x.to_string())),
        Value::Object(x) => x,
        Value::Null => return Ok(ResourceValue::Null),
        Value::Bool(b) => return Ok(ResourceValue::Bool(b.to_owned())),
        Value::Number(n) => return Ok(ResourceValue::Number(n.as_i64().unwrap())),
        Value::Array(arr) => {
            let mut v = Vec::new();
            for item in arr.iter() {
                let obj = build_resources_recursively(name, item)?;
                v.push(obj);
            }

            return Ok(ResourceValue::Array(v));
        }
    };

    if val.len() > 1 {
        let mut hm = HashMap::new();
        for (name, obj) in val {
            hm.insert(name.to_owned(), build_resources_recursively(name, obj)?);
        }

        return Ok(ResourceValue::Object(hm));
    } else {
        #[allow(clippy::never_loop)]
        for (resource_name, resource_object) in val {
            let cond: ResourceValue = match resource_name.as_str() {
                "Fn::Sub" => {
                    let mut v = Vec::new();
                    match resource_object {
                        Value::String(str) => {
                            v.push(ResourceValue::String(str.to_owned()));
                        }
                        Value::Array(arr) => {
                            for obj in arr.iter() {
                                let resource = build_resources_recursively(name, obj)?;
                                v.push(resource);
                            }
                        }
                        _ => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Sub can only be eitehr an array or a string {}",
                                    name
                                ),
                            });
                        }
                    }
                    ResourceValue::Sub(v)
                }
                "Fn::FindInMap" => {
                    let v = match resource_object.as_array() {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Map is supposed to be an array entry {}",
                                    name
                                ),
                            })
                        }
                        Some(x) => x,
                    };

                    let first_obj = match v.get(0) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Map is supposed to have 3 values in array, has 0 {}",
                                    name
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;
                    let second_obj = match v.get(1) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Map is supposed to have 3 values in array, has 1 {}",
                                    name
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;
                    let third_obj = match v.get(2) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Map is supposed to have 3 values in array, has 2 {}",
                                    name
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
                "Fn::GetAtt" => {
                    let v = match resource_object.as_array() {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Map is supposed to be an array entry {}",
                                    name
                                ),
                            })
                        }
                        Some(x) => x,
                    };

                    let first_obj = match v.get(0) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Map is supposed to have 3 values in array, has 0 {}",
                                    name
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;
                    let second_obj = match v.get(1) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Map is supposed to have 3 values in array, has 1 {}",
                                    name
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;

                    ResourceValue::GetAtt(Box::new(first_obj), Box::new(second_obj))
                }
                "Fn::Base64" => {
                    let resolved_obj = build_resources_recursively(name, resource_object)?;
                    ResourceValue::Base64(Box::new(resolved_obj))
                }
                "Fn::ImportValue" => {
                    let resolved_obj = build_resources_recursively(name, resource_object)?;
                    ResourceValue::ImportValue(Box::new(resolved_obj))
                }
                "Fn::Select" => {
                    let arr = resource_object.as_array().unwrap();

                    let index = match arr.get(0) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Select is supposed to have 2 values in array, has 0 {}",
                                    name
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;
                    let obj = match arr.get(1) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Select is supposed to have 2 values in array, has 1 {}",
                                    name
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;

                    ResourceValue::Select(Box::new(index), Box::new(obj))
                }
                "Fn::If" => {
                    let v = match resource_object.as_array() {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::If is supposed to be an array entry {}",
                                    name
                                ),
                            })
                        }
                        Some(x) => x,
                    };

                    let first_obj = match v.get(0) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::If is supposed to have 3 values in array, has 0 {}",
                                    name
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;
                    let second_obj = match v.get(1) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::If is supposed to have 3 values in array, has 1 {}",
                                    name
                                ),
                            })
                        }
                        Some(x) => build_resources_recursively(name, x),
                    }?;
                    let third_obj = match v.get(2) {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::If is supposed to have 3 values in array, has 2 {}",
                                    name
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
                "Fn::Join" => {
                    let arr = match resource_object.as_array() {
                        None => {
                            return Err(TransmuteError {
                                details: format!(
                                    "Fn::Map is supposed to be an array entry {}",
                                    name
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
                "Ref" => {
                    let ref_name = match resource_object.as_str() {
                        None => {
                            return Err(TransmuteError {
                                details: format!("Condition must a string {}", name),
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
                v => {
                    let mut hm = HashMap::new();
                    hm.insert(
                        v.to_owned(),
                        build_resources_recursively(name, resource_object)?,
                    );
                    ResourceValue::Object(hm)
                }
            };

            return Ok(cond);
        }
    }

    Err(TransmuteError {
        details: String::from("Nothing found?"),
    })
}
