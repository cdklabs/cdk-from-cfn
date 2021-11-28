use crate::ir::reference::{Origin, Reference};
use crate::parser::condition::{ConditionParseTree, ConditionValue, ConditionsParseTree};
use crate::CloudformationParseTree;
use topological_sort::TopologicalSort;

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
    let mut topo: TopologicalSort<String> = TopologicalSort::new();
    // Identify condition dependencies
    for (condition_name, condition_parts) in conditions_parse_tree.conditions.iter() {
        topo.insert(condition_name.to_string());
        find_dependencies(condition_name, &condition_parts.val, &mut topo);
    }
    let mut sorted = Vec::new();
    while !topo.is_empty() {
        match topo.pop() {
            None => {
                panic!("There are cyclic deps in the conditions clauses")
            }
            Some(item) => {
                let condition = conditions_parse_tree.conditions.get(&item).unwrap();
                sorted.push(condition.clone())
            }
        }
    }

    sorted
}

/**
 * Recursively identify the dependency conditions of a CloudFormation condition.
 */
fn find_dependencies(
    root_condition_name: &str,
    condition_val: &ConditionValue,
    topological_sort: &mut TopologicalSort<String>,
) {
    match condition_val {
        ConditionValue::And(x) | ConditionValue::Or(x) => x
            .iter()
            .for_each(|cond| find_dependencies(root_condition_name, cond, topological_sort)),
        ConditionValue::Equals(a, b) => {
            find_dependencies(root_condition_name, a, topological_sort);
            find_dependencies(root_condition_name, b, topological_sort);
        }
        ConditionValue::Not(a) => {
            find_dependencies(root_condition_name, a, topological_sort);
        }
        ConditionValue::Ref(_x) | ConditionValue::Str(_x) => {}
        ConditionValue::Condition(x) => {
            topological_sort.insert(root_condition_name);
            topological_sort.add_dependency(x.to_string(), root_condition_name.to_string())
        }
        ConditionValue::FindInMap(name, l1, l2) => {
            find_dependencies(root_condition_name, name, topological_sort);
            find_dependencies(root_condition_name, l1, topological_sort);
            find_dependencies(root_condition_name, l2, topological_sort);
        }
    };
}

#[cfg(test)]
mod tests {
    use crate::ir::conditions::{determine_order, translate_ir, ConditionIr};
    use crate::ir::reference::{Origin, PseudoParameter, Reference};
    use crate::parser::condition::{ConditionParseTree, ConditionValue};
    use crate::ConditionsParseTree;
    use std::collections::HashMap;

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
    fn test_sorting() {
        let a = ConditionParseTree {
            name: "A".to_string(),
            val: ConditionValue::Ref("Hello".to_string()),
        };

        let b = ConditionParseTree {
            name: "B".to_string(),
            val: ConditionValue::Condition("A".to_string()),
        };

        let mut hash = HashMap::new();
        hash.insert("A".to_string(), a.clone());
        hash.insert("B".to_string(), b.clone());
        let conditions = ConditionsParseTree { conditions: hash };

        let ordered = determine_order(&conditions);

        assert_eq!(ordered, vec![a, b]);
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
