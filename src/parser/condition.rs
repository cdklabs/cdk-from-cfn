use crate::TransmuteError;
use serde_yaml::{Mapping, Value};
use std::borrow::Cow;
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub enum ConditionValue {
    // Higher level boolean operators
    And(Vec<ConditionValue>),
    Equals(Box<ConditionValue>, Box<ConditionValue>),
    Not(Box<ConditionValue>),
    Or(Vec<ConditionValue>),

    // Cloudformation meta-functions
    FindInMap(
        Box<ConditionValue>,
        Box<ConditionValue>,
        Box<ConditionValue>,
    ),

    // End of recursion, the base primitives to work with
    Str(String),
    Ref(String),
    Condition(String),
}

#[derive(Debug, Clone)]
pub struct ConditionParseTree {
    pub name: String,
    pub val: ConditionValue,
}

impl PartialEq for ConditionParseTree {
    fn eq(&self, other: &ConditionParseTree) -> bool {
        self.name == other.name
    }
}

pub fn is_intrinsic(x: &str) -> bool {
    x.starts_with("AWS::")
}

#[derive(Debug)]
pub struct ConditionsParseTree {
    pub conditions: HashMap<String, ConditionParseTree>,
}

impl ConditionsParseTree {
    pub fn new() -> ConditionsParseTree {
        ConditionsParseTree {
            conditions: HashMap::new(),
        }
    }
}

impl Default for ConditionsParseTree {
    fn default() -> Self {
        Self::new()
    }
}

pub fn build_conditions(vals: &Mapping) -> Result<ConditionsParseTree, TransmuteError> {
    let mut conditions = ConditionsParseTree::new();

    for (name, obj) in vals {
        let name = name.as_str().unwrap();
        let cond = build_condition_recursively(name, obj)?;
        let condition = ConditionParseTree {
            name: name.to_string(),
            val: cond,
        };
        conditions.conditions.insert(name.to_string(), condition);
    }
    Ok(conditions)
}

fn build_condition_recursively(name: &str, obj: &Value) -> Result<ConditionValue, TransmuteError> {
    let val: Cow<Mapping> = match obj {
        Value::String(x) => return Ok(ConditionValue::Str(x.to_string())),
        Value::Number(x) => return Ok(ConditionValue::Str(x.to_string())),
        Value::Bool(x) => return Ok(ConditionValue::Str(x.to_string())),
        Value::Mapping(x) => Cow::Borrowed(x),
        Value::Tagged(x) => {
            let mut mapping = Mapping::new();
            mapping.insert(
                serde_yaml::Value::String(format!("!{}", x.tag)),
                x.value.clone(),
            );
            Cow::Owned(mapping)
        }
        _ => {
            return Err(TransmuteError {
                details: format!("Condition must be an object or string {name}, {obj:?}"),
            })
        }
    };

    // At this point, we have an object-json, and need to iterate over all
    // the keys
    #[allow(clippy::never_loop)]
    for (condition_name, condition_object) in val.as_ref() {
        let cond: ConditionValue = match condition_name.as_str() {
            Some("!And" | "Fn::And") => {
                let mut v: Vec<ConditionValue> = Vec::new();
                let arr = match condition_object.as_sequence() {
                    None => {
                        return Err(TransmuteError::new(
                            format!("Condition must be an array {name}").as_str(),
                        ))
                    }
                    Some(x) => x,
                };

                for a in arr {
                    v.push(build_condition_recursively(name, a)?);
                }

                ConditionValue::And(v)
            }
            Some("!Equals" | "Fn::Equals") => {
                let arr = match condition_object.as_sequence() {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Condition must be an array {name}"),
                        })
                    }
                    Some(x) => x,
                };

                let obj1 = match arr.get(0) {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Equal condition must have 2 array values {name}"),
                        })
                    }
                    Some(x) => build_condition_recursively(name, x),
                }?;
                let obj2 = match arr.get(1) {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Equal condition must have 2 array values {name}"),
                        })
                    }
                    Some(x) => build_condition_recursively(name, x),
                }?;
                ConditionValue::Equals(Box::new(obj1), Box::new(obj2))
            }
            Some("!Not" | "Fn::Not") => {
                let arr = match condition_object.as_sequence() {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Condition must be an array {name}"),
                        })
                    }
                    Some(x) => x,
                };

                let obj1 = match arr.get(0) {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Equal condition must have 2 array values {name}"),
                        })
                    }
                    Some(x) => build_condition_recursively(name, x),
                }?;
                ConditionValue::Not(Box::new(obj1))
            }
            Some("!Or" | "Fn::Or") => {
                let arr = match condition_object.as_sequence() {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Condition must be an array {name}"),
                        })
                    }
                    Some(x) => x,
                };

                let mut v: Vec<ConditionValue> = Vec::new();

                for a in arr {
                    v.push(build_condition_recursively(name, a)?);
                }

                ConditionValue::Or(v)
            }
            Some("!Condition" | "Condition") => {
                let condition_name = match condition_object.as_str() {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Condition must a string {name}"),
                        })
                    }
                    Some(x) => x,
                };
                ConditionValue::Condition(condition_name.to_string())
            }
            Some("!Ref" | "Ref") => {
                let ref_name = match condition_object.as_str() {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Condition must a string {name}"),
                        })
                    }
                    Some(x) => x,
                };
                ConditionValue::Ref(ref_name.to_string())
            }
            Some("!FindInMap" | "Fn::FindInMap") => {
                let arr = match condition_object.as_sequence() {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Fn::FindInMap must form an array {name}"),
                        })
                    }
                    Some(x) => x,
                };

                let m1 = build_condition_recursively(name, arr.get(0).unwrap())?;
                let m2 = build_condition_recursively(name, arr.get(1).unwrap())?;
                let m3 = build_condition_recursively(name, arr.get(2).unwrap())?;
                ConditionValue::FindInMap(Box::new(m1), Box::new(m2), Box::new(m3))
            }
            Some(v) => ConditionValue::Str(v.to_string()),
            None => unimplemented!("Condition name is not a string"),
        };

        return Ok(cond);
    }

    Err(TransmuteError {
        details: format!("Could not match the pattern for {name}, {obj:?}"),
    })
}
