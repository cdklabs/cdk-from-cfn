use crate::TransmuteError;
use serde_json::{Map, Value};
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

pub fn build_conditions(vals: &Map<String, Value>) -> Result<ConditionsParseTree, TransmuteError> {
    let mut conditions = ConditionsParseTree {
        conditions: HashMap::new(),
    };
    for (name, obj) in vals {
        let cond = build_condition_recursively(name, obj)?;
        let condition = ConditionParseTree {
            name: name.clone(),
            val: cond,
        };
        conditions.conditions.insert(name.clone(), condition);
    }
    Ok(conditions)
}

fn build_condition_recursively(name: &str, obj: &Value) -> Result<ConditionValue, TransmuteError> {
    let val = match obj {
        Value::String(x) => return Ok(ConditionValue::Str(x.to_string())),
        Value::Number(x) => return Ok(ConditionValue::Str(x.to_string())),
        Value::Object(x) => x,
        _ => {
            return Err(TransmuteError {
                details: format!("Condition must be an object or string {}, {:?}", name, obj),
            })
        }
    };

    // there should only be one key, but for now iterate over all keys
    #[allow(clippy::never_loop)]
    for (condition_name, condition_object) in val {
        let cond: ConditionValue = match condition_name.as_str() {
            "Fn::And" => {
                let mut v: Vec<ConditionValue> = Vec::new();
                let arr = match condition_object.as_array() {
                    None => {
                        return Err(TransmuteError::new(
                            format!("Condition must be an array {}", name).as_str(),
                        ))
                    }
                    Some(x) => x,
                };

                for a in arr {
                    v.push(build_condition_recursively(name, a)?);
                }

                ConditionValue::And(v)
            }
            "Fn::Equals" => {
                let arr = match condition_object.as_array() {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Condition must be an array {}", name),
                        })
                    }
                    Some(x) => x,
                };

                let obj1 = match arr.get(0) {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Equal condition must have 2 array values {}", name),
                        })
                    }
                    Some(x) => build_condition_recursively(name, x),
                }?;
                let obj2 = match arr.get(1) {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Equal condition must have 2 array values {}", name),
                        })
                    }
                    Some(x) => build_condition_recursively(name, x),
                }?;
                ConditionValue::Equals(Box::new(obj1), Box::new(obj2))
            }
            "Fn::Not" => {
                let arr = match condition_object.as_array() {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Condition must be an array {}", name),
                        })
                    }
                    Some(x) => x,
                };

                let obj1 = match arr.get(0) {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Equal condition must have 2 array values {}", name),
                        })
                    }
                    Some(x) => build_condition_recursively(name, x),
                }?;
                ConditionValue::Not(Box::new(obj1))
            }
            "Fn::Or" => {
                let arr = match condition_object.as_array() {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Condition must be an array {}", name),
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
            "Condition" => {
                let condition_name = match condition_object.as_str() {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Condition must a string {}", name),
                        })
                    }
                    Some(x) => x,
                };
                ConditionValue::Condition(condition_name.to_string())
            }
            "Ref" => {
                let ref_name = match condition_object.as_str() {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Condition must a string {}", name),
                        })
                    }
                    Some(x) => x,
                };
                ConditionValue::Ref(ref_name.to_string())
            }
            "Fn::FindInMap" => {
                let arr = match condition_object.as_array() {
                    None => {
                        return Err(TransmuteError {
                            details: format!("Condition must be an array {}", name),
                        })
                    }
                    Some(x) => x,
                };

                let m1 = build_condition_recursively(name, arr.get(0).unwrap())?;
                let m2 = build_condition_recursively(name, arr.get(1).unwrap())?;
                let m3 = build_condition_recursively(name, arr.get(2).unwrap())?;
                ConditionValue::FindInMap(Box::new(m1), Box::new(m2), Box::new(m3))
            }
            v => ConditionValue::Str(v.to_string()),
        };

        return Ok(cond);
    }

    Err(TransmuteError {
        details: String::from("Nothing found?"),
    })
}
