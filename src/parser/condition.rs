use crate::TransmuteError;
use serde_json::{Map, Value};
use std::collections::HashMap;

#[derive(Debug)]
pub enum ConditionValue {
    And(Vec<ConditionValue>),
    Equals(Box<ConditionValue>, Box<ConditionValue>),
    Not(Box<ConditionValue>),
    Or(Vec<ConditionValue>),
    // First item in sub
    Sub(Vec<ConditionValue>),
    FindInMap(Vec<ConditionValue>),
    // Recursion ending
    Str(String),
    Ref(String),
    Condition(String),
}

impl ConditionValue {
    // Complexity is defined as "continuous recursion or end state".
    // if something is just a string, ref or condition, it is considered
    // "simple", as there is no recursion needed to resolve it's value.
    pub fn is_simple(&self) -> bool {
        matches!(
            self,
            ConditionValue::Condition(_) | ConditionValue::Ref(_) | ConditionValue::Str(_)
        )
    }
}

#[derive(Debug)]
pub struct ConditionParseTree {
    pub name: String,
    pub val: ConditionValue,
}

impl ConditionParseTree {
    pub fn synthesize(&self) -> String {
        let synthed = synthesize_condition_recursive(&self.val);
        format!("const {} = {};", self.name, synthed)
    }
}

fn synthesize_condition_recursive(val: &ConditionValue) -> String {
    match val {
        ConditionValue::And(x) => {
            let a: Vec<String> = x
                .iter()
                .map(|x| synthesize_condition_recursive(x))
                .collect();

            let inner = a.join(" && ");
            format!("({})", inner)
        }
        ConditionValue::Equals(a, b) => {
            format!(
                "{} == {}",
                synthesize_condition_recursive(a.as_ref()),
                synthesize_condition_recursive(b.as_ref())
            )
        }
        ConditionValue::Not(x) => {
            if x.is_simple() {
                format!("!{}", synthesize_condition_recursive(x.as_ref()))
            } else {
                format!("!({})", synthesize_condition_recursive(x.as_ref()))
            }
        }
        ConditionValue::Or(x) => {
            let a: Vec<String> = x
                .iter()
                .map(|x| synthesize_condition_recursive(x))
                .collect();

            let inner = a.join(" || ");
            format!("({})", inner)
        }
        ConditionValue::Str(x) => {
            format!("\"{}\"", x)
        }
        ConditionValue::Ref(x) => match x.as_str() {
            "AWS::Region" => String::from("this.region"),
            "AWS::Partition" => String::from("this.partition"),
            x => {
                format!("props.{}", x)
            }
        },
        ConditionValue::Condition(x) => x.clone(),
        _ => {
            panic!("boom");
        }
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
            v => ConditionValue::Str(v.to_string()),
        };

        return Ok(cond);
    }

    Err(TransmuteError {
        details: String::from("Nothing found?"),
    })
}
