use crate::TransmuteError;
use serde_json::{Map, Value};
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub enum ConditionValue {
    And(Vec<ConditionValue>),
    Equals(Box<ConditionValue>, Box<ConditionValue>),
    Not(Box<ConditionValue>),
    Or(Vec<ConditionValue>),
    FindInMap(
        Box<ConditionValue>,
        Box<ConditionValue>,
        Box<ConditionValue>,
    ),
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

#[derive(Debug, Clone)]
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

impl PartialEq for ConditionParseTree {
    fn eq(&self, other: &ConditionParseTree) -> bool {
        self.name == other.name
    }
}

fn synthesize_condition_recursive(val: &ConditionValue) -> String {
    match val {
        ConditionValue::And(x) => {
            let a: Vec<String> = x.iter().map(synthesize_condition_recursive).collect();

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
            let a: Vec<String> = x.iter().map(synthesize_condition_recursive).collect();

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
        ConditionValue::FindInMap(named_resource, l1, l2) => {
            format!(
                "{}[{}][{}]",
                synthesize_condition_recursive(named_resource.as_ref()),
                synthesize_condition_recursive(l1.as_ref()),
                synthesize_condition_recursive(l2.as_ref())
            )
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

/**
 * Provides an ordering of conditions contained in the tree based on relative dependencies.
 */
pub fn determine_order(conditions_parse_tree: ConditionsParseTree) -> Vec<ConditionParseTree> {
    let mut condition_dependency_tracker: HashMap<String, ConditionNode> = HashMap::new();
    // Create a ConditionNode for each ConditionParseTree
    for (condition_name, condition_parts) in conditions_parse_tree.conditions.iter() {
        let node = ConditionNode::new(condition_name.clone(), condition_parts.clone());
        condition_dependency_tracker.insert(condition_name.clone(), node);
    }

    // Identify condition dependencies
    for (condition_name, condition_parts) in conditions_parse_tree.conditions.iter() {
        find_dependencies(
            condition_name,
            &condition_parts.val,
            &mut condition_dependency_tracker,
        );
    }

    // Identify leaf conditions, i.e. conditions with no dependencies
    let mut root_nodes = Vec::new();
    for (_, condition_node) in condition_dependency_tracker.iter() {
        if condition_node.uses.is_empty() {
            root_nodes.push(condition_node.clone());
        }
    }

    // Determine an ordering of conditions that ensures all dependent conditions are defined
    // before a condition that uses it
    let mut node_order: Vec<ConditionParseTree> = Vec::new();
    root_nodes.sort_by(|a, b| a.name.cmp(&b.name.to_string()));
    root_nodes.iter().for_each(|node| {
        resolve_order(node, &mut node_order, &condition_dependency_tracker);
    });

    node_order
}

/**
 * Derive an ordering of conditions that ensure all dependency conditions are declared before
 * conditions that use them.
 */
fn resolve_order(
    condition_node: &ConditionNode,
    node_order: &mut Vec<ConditionParseTree>,
    condition_tracker: &HashMap<String, ConditionNode>,
) {
    if !node_order.contains(&condition_node.condition) {
        condition_node.uses.iter().for_each(|node_id| {
            let node = condition_tracker.get(node_id).unwrap();
            resolve_order(node, node_order, condition_tracker);
        });
        if !node_order.contains(&condition_node.condition) {
            node_order.push(condition_node.condition.clone());
        }
        condition_node.used_by.iter().for_each(|node_id| {
            let node = condition_tracker.get(node_id).unwrap();
            resolve_order(node, node_order, condition_tracker);
        });
    }
}

/**
 * Recursively identify the dependency conditions of a CloudFormation condition.
 */
fn find_dependencies(
    root_condition_name: &str,
    condition_val: &ConditionValue,
    condition_dependency_tracker: &mut HashMap<String, ConditionNode>,
) {
    match condition_val {
        ConditionValue::And(x) | ConditionValue::Or(x) => x.iter().for_each(|cond| {
            find_dependencies(root_condition_name, cond, condition_dependency_tracker)
        }),
        ConditionValue::Equals(a, b) => {
            find_dependencies(root_condition_name, a, condition_dependency_tracker);
            find_dependencies(root_condition_name, b, condition_dependency_tracker);
        }
        ConditionValue::Not(a) => {
            find_dependencies(root_condition_name, a, condition_dependency_tracker);
        }
        ConditionValue::Ref(_x) | ConditionValue::Str(_x) => {}
        ConditionValue::Condition(x) => {
            let mut root_condition_node = condition_dependency_tracker
                .remove(root_condition_name)
                .unwrap();
            let mut used_by_condition_node = condition_dependency_tracker.remove(x).unwrap();
            // Associate root condition with its dependency and vice-versa
            root_condition_node.uses.push(x.clone());
            used_by_condition_node
                .used_by
                .push(root_condition_node.name.clone());

            condition_dependency_tracker
                .insert(root_condition_name.to_string(), root_condition_node);
            condition_dependency_tracker.insert(x.clone(), used_by_condition_node);
        }
        ConditionValue::FindInMap(name, l1, l2) => {
            find_dependencies(root_condition_name, name, condition_dependency_tracker);
            find_dependencies(root_condition_name, l1, condition_dependency_tracker);
            find_dependencies(root_condition_name, l2, condition_dependency_tracker);
        }
    };
}

#[derive(Clone)]
struct ConditionNode {
    name: String,
    condition: ConditionParseTree,
    used_by: Vec<String>,
    uses: Vec<String>,
}

impl ConditionNode {
    fn new(name: String, condition: ConditionParseTree) -> ConditionNode {
        ConditionNode {
            name,
            condition,
            used_by: Vec::new(),
            uses: Vec::new(),
        }
    }
}
