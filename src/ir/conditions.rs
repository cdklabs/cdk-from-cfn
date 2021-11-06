use crate::ir::reference::{Origin, Reference};
use crate::parser::condition::{ConditionParseTree, ConditionValue, ConditionsParseTree};
use crate::CloudformationParseTree;
use std::collections::HashMap;

// ConditionInstructions are simple assignment + boolean
// clauses, as conditions are based on those composite values.
// It may have made more sense to copy completely to the parse tree
// but for now we will keep ConditionInstruction + ConditionIr
// as a single entity.
#[derive(Debug, Clone, PartialEq)]
pub struct ConditionInstruction {
    pub name: String,
    pub value: ConditionIr,
}

#[derive(Debug, Clone, PartialEq)]
pub enum ConditionIr {
    // Higher level boolean operators
    And(Vec<ConditionIr>),
    Equals(Box<ConditionIr>, Box<ConditionIr>),
    Not(Box<ConditionIr>),
    Or(Vec<ConditionIr>),

    // Cloudformation meta-functions
    Map(Box<ConditionIr>, Box<ConditionIr>, Box<ConditionIr>),

    // End of recursion, the base primitives to work with
    Str(String),
    Ref(Reference),
}

impl ConditionIr {
    // Complexity is defined as "continuous recursion or end state".
    // if something is just a string, ref or condition, it is considered
    // "simple", as there is no recursion needed to resolve it's value.
    pub fn is_simple(&self) -> bool {
        matches!(self, ConditionIr::Ref(_) | ConditionIr::Str(_))
    }
}

pub fn translate_conditions(parse_tree: &CloudformationParseTree) -> Vec<ConditionInstruction> {
    let mut list = Vec::new();
    for cond in determine_order(&parse_tree.conditions) {
        let ir = translate_ir(&cond.val);
        list.push(ConditionInstruction {
            name: cond.name,
            value: ir,
        });
    }

    list
}

fn translate_ir(value: &ConditionValue) -> ConditionIr {
    match value {
        ConditionValue::And(x) => {
            let and_list = x.iter().cloned().map(|y| translate_ir(&y)).collect();
            ConditionIr::And(and_list)
        }
        ConditionValue::Equals(x, y) => {
            let x = translate_ir(x);
            let y = translate_ir(y);

            ConditionIr::Equals(Box::new(x), Box::new(y))
        }
        ConditionValue::Not(x) => {
            let x = translate_ir(x);
            ConditionIr::Not(Box::new(x))
        }
        ConditionValue::Or(x) => {
            let or_list = x.iter().cloned().map(|y| translate_ir(&y)).collect();
            ConditionIr::Or(or_list)
        }
        ConditionValue::FindInMap(name, x, y) => {
            let name = translate_ir(name);
            let x = translate_ir(x);
            let y = translate_ir(y);

            ConditionIr::Map(Box::new(name), Box::new(x), Box::new(y))
        }
        ConditionValue::Str(x) => ConditionIr::Str(x.clone()),
        ConditionValue::Ref(x) => {
            // The only 2 references allowed in conditions is parameters or pseudo parameters.
            // so assume it's a parameter and check for pseudo fill-ins
            let mut origin = Origin::Parameter;
            if let Option::Some(s) = Reference::match_pseudo_parameter(x) {
                origin = Origin::PseudoParameter(s);
            }
            ConditionIr::Ref(Reference {
                origin,
                name: x.clone(),
            })
        }
        ConditionValue::Condition(x) => ConditionIr::Ref(Reference {
            origin: Origin::Condition,
            name: x.clone(),
        }),
    }
}

/**
 * Provides an ordering of conditions contained in the tree based on relative dependencies.
 */
pub fn determine_order(conditions_parse_tree: &ConditionsParseTree) -> Vec<ConditionParseTree> {
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

#[cfg(test)]
mod tests {
    use crate::ir::conditions::{translate_ir, ConditionIr};
    use crate::ir::reference::{Origin, PseudoParameter, Reference};
    use crate::parser::condition::ConditionValue;

    #[test]
    fn test_eq_translation() {
        let condition_structure: ConditionValue = ConditionValue::Equals(
            Box::new(ConditionValue::Str("us-west-2".into())),
            Box::new(ConditionValue::Ref("AWS::Region".into())),
        );

        let condition_ir = translate_ir(&condition_structure);
        assert_eq!(
            ConditionIr::Equals(
                Box::new(ConditionIr::Str("us-west-2".into())),
                Box::new(ConditionIr::Ref(Reference::new(
                    "AWS::Region",
                    Origin::PseudoParameter(PseudoParameter::Region)
                )))
            ),
            condition_ir
        );
    }

    #[test]
    fn test_condition_translation() {
        let condition_structure: ConditionValue = ConditionValue::Condition("other".into());
        let condition_ir = translate_ir(&condition_structure);
        assert_eq!(
            (ConditionIr::Ref(Reference::new("other", Origin::Condition))),
            condition_ir
        );
    }

    fn test_simple() {
        assert_eq!(
            ConditionIr::Str("hi".into()),
            translate_ir(&ConditionValue::Str("hi".into()))
        );
    }
}
