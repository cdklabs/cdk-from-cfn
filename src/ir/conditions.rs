use crate::ir::reference::{Origin, Reference};
use crate::parser::condition::{ConditionFunction, ConditionValue};
use crate::CloudformationParseTree;
use indexmap::IndexMap;
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
    let mut list = Vec::with_capacity(parse_tree.conditions.len());
    for name in determine_order(&parse_tree.conditions) {
        let value = parse_tree.conditions[name].as_ir();
        list.push(ConditionInstruction {
            name: name.into(),
            value,
        });
    }

    list
}

impl ConditionFunction {
    fn as_ir(&self) -> ConditionIr {
        match self {
            Self::And(x) => {
                let and_list = x.iter().map(ConditionValue::as_ir).collect();
                ConditionIr::And(and_list)
            }
            Self::Equals(x, y) => {
                let x = x.as_ir();
                let y = y.as_ir();

                ConditionIr::Equals(Box::new(x), Box::new(y))
            }
            Self::Not(x) => {
                let x = x.as_ir();
                ConditionIr::Not(Box::new(x))
            }
            Self::Or(x) => {
                let or_list = x.iter().map(ConditionValue::as_ir).collect();
                ConditionIr::Or(or_list)
            }
            Self::If { .. } => unimplemented!(),
        }
    }
}

impl ConditionValue {
    fn as_ir(&self) -> ConditionIr {
        match self {
            Self::Function(function) => function.as_ir(),
            Self::FindInMap(name, x, y) => {
                let name = name.as_ir();
                let x = x.as_ir();
                let y = y.as_ir();

                ConditionIr::Map(Box::new(name), Box::new(x), Box::new(y))
            }
            Self::String(x) => ConditionIr::Str(x.clone()),
            Self::Ref(x) => {
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
            Self::Condition(x) => ConditionIr::Ref(Reference {
                origin: Origin::Condition,
                name: x.clone(),
            }),
        }
    }
}

/**
 * Provides an ordering of conditions contained in the tree based on relative dependencies.
 */
pub fn determine_order(conditions: &IndexMap<String, ConditionFunction>) -> Vec<&str> {
    let mut topo: TopologicalSort<&str> = TopologicalSort::new();
    // Identify condition dependencies
    for (name, value) in conditions {
        topo.insert(name.as_str());
        value.find_dependencies(name, &mut topo);
    }

    let mut sorted = Vec::with_capacity(conditions.len());
    while !topo.is_empty() {
        match topo.pop() {
            None => {
                panic!("There are cyclic deps in the conditions clauses")
            }
            Some(item) => sorted.push(item),
        }
    }

    sorted
}

impl ConditionFunction {
    fn find_dependencies<'a>(
        &'a self,
        logical_id: &'a str,
        topo_sort: &'_ mut TopologicalSort<&'a str>,
    ) {
        match self {
            Self::And(list) | Self::Or(list) => list
                .iter()
                .for_each(|val| val.find_dependencies(logical_id, topo_sort)),
            Self::Equals(a, b) => {
                a.find_dependencies(logical_id, topo_sort);
                b.find_dependencies(logical_id, topo_sort);
            }
            Self::Not(cond) => cond.find_dependencies(logical_id, topo_sort),
            Self::If {
                condition_name,
                if_true,
                if_false,
                ..
            } => {
                topo_sort.add_dependency(condition_name.as_str(), logical_id);
                if_true.find_dependencies(logical_id, topo_sort);
                if_false.find_dependencies(logical_id, topo_sort);
            }
        }
    }
}

impl ConditionValue {
    fn find_dependencies<'a>(
        &'a self,
        logical_id: &'a str,
        topo_sort: &'_ mut TopologicalSort<&'a str>,
    ) {
        match self {
            Self::Condition(cond) => {
                topo_sort.add_dependency(cond.as_str(), logical_id);
            }
            Self::FindInMap(name, key1, key2) => {
                name.find_dependencies(logical_id, topo_sort);
                key1.find_dependencies(logical_id, topo_sort);
                key2.find_dependencies(logical_id, topo_sort);
            }
            Self::Function(func) => func.find_dependencies(logical_id, topo_sort),
            Self::Ref(_) | Self::String(_) => {}
        }
    }
}

#[cfg(test)]
mod tests {
    use indexmap::IndexMap;

    use crate::ir::conditions::{determine_order, ConditionIr};
    use crate::ir::reference::{Origin, PseudoParameter, Reference};
    use crate::parser::condition::{ConditionFunction, ConditionValue};

    #[test]
    fn test_eq_translation() {
        let condition_structure = ConditionFunction::Equals(
            ConditionValue::String("us-west-2".into()),
            ConditionValue::Ref("AWS::Region".into()),
        );

        let condition_ir = condition_structure.as_ir();
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
        let a = ConditionFunction::Equals(
            ConditionValue::Ref("Foo".into()),
            ConditionValue::Ref("Bar".into()),
        );

        let b = ConditionFunction::Not(ConditionValue::Condition("A".into()));

        let hash = IndexMap::from([("A".into(), a), ("B".into(), b)]);
        let ordered = determine_order(&hash);

        assert_eq!(ordered, vec!["A", "B"]);
    }

    #[test]
    fn test_condition_translation() {
        let condition_structure: ConditionValue = ConditionValue::Condition("other".into());
        let condition_ir = condition_structure.as_ir();
        assert_eq!(
            (ConditionIr::Ref(Reference::new("other", Origin::Condition))),
            condition_ir
        );
    }

    fn test_simple() {
        assert_eq!(
            ConditionIr::Str("hi".into()),
            ConditionValue::String("hi".into()).as_ir()
        );
    }
}
