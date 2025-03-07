// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use indexmap::IndexMap;
use topological_sort::TopologicalSort;

use super::reference::PseudoParameter;

use crate::ir::reference::{Origin, Reference};
use crate::parser::condition::{ConditionFunction, ConditionValue};
use crate::util::Hasher;

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

impl ConditionInstruction {
    pub(super) fn from(mut parse_tree: IndexMap<String, ConditionFunction, Hasher>) -> Vec<Self> {
        let order: Vec<String> = determine_order(&parse_tree)
            .into_iter()
            .map(ToString::to_string)
            .collect();

        order
            .into_iter()
            .map(|name| {
                let value = parse_tree.shift_remove(&name).unwrap().into_ir();
                ConditionInstruction { name, value }
            })
            .collect()
    }
}

#[derive(Debug, Clone, PartialEq)]
pub enum ConditionIr {
    // Higher level boolean operators
    And(Vec<ConditionIr>),
    Equals(Box<ConditionIr>, Box<ConditionIr>),
    Not(Box<ConditionIr>),
    Or(Vec<ConditionIr>),
    Condition(String),

    // Cloudformation meta-functions
    Map(String, Box<ConditionIr>, Box<ConditionIr>),
    Split(String, Box<ConditionIr>),
    Select(usize, Box<ConditionIr>),

    // End of recursion, the base primitives to work with
    Str(String),
    Ref(Reference),
}

impl ConditionIr {
    #[inline]
    pub fn is_simple(&self) -> bool {
        matches!(self, Self::Str(_) | Self::Ref(_))
    }
}

impl ConditionFunction {
    fn into_ir(self) -> ConditionIr {
        match self {
            Self::And(x) => {
                let and_list = x.into_iter().map(ConditionValue::into_ir).collect();
                ConditionIr::And(and_list)
            }
            Self::Equals(x, y) => {
                let x = x.into_ir();
                let y = y.into_ir();

                ConditionIr::Equals(Box::new(x), Box::new(y))
            }
            Self::Not(x) => {
                let x = x.into_ir();
                ConditionIr::Not(Box::new(x))
            }
            Self::Or(x) => {
                let or_list = x.into_iter().map(ConditionValue::into_ir).collect();
                ConditionIr::Or(or_list)
            }
            Self::Condition(x) => ConditionIr::Condition(x),
            Self::If { .. } => unimplemented!(),
        }
    }
}

impl ConditionValue {
    fn into_ir(self) -> ConditionIr {
        match self {
            Self::Function(function) => function.into_ir(),
            Self::FindInMap(name, x, y) => {
                let x = x.into_ir();
                let y = y.into_ir();

                ConditionIr::Map(name, Box::new(x), Box::new(y))
            }
            Self::Split(delimiter, x) => {
                let x = x.into_ir();
                ConditionIr::Split(delimiter, Box::new(x))
            }
            Self::Select(index, x) => {
                let x = x.into_ir();
                ConditionIr::Select(index, Box::new(x))
            }
            Self::String(x) => ConditionIr::Str(x),
            Self::Ref(name) => {
                // The only 2 references allowed in conditions is parameters or pseudo parameters.
                // so assume it's a parameter and check for pseudo fill-ins
                let mut origin = Origin::Parameter;
                if let Option::Some(s) = PseudoParameter::try_from(&name) {
                    origin = Origin::PseudoParameter(s);
                }
                ConditionIr::Ref(Reference { origin, name })
            }
            Self::Condition(name) => ConditionIr::Ref(Reference {
                origin: Origin::Condition,
                name,
            }),
        }
    }
}

/**
 * Provides an ordering of conditions contained in the tree based on relative dependencies.
 */
pub fn determine_order<S>(
    conditions: &indexmap::IndexMap<String, ConditionFunction, S>,
) -> Vec<&str> {
    let mut topo: TopologicalSort<&str> = TopologicalSort::new();
    // Identify condition dependencies
    for (name, value) in conditions {
        topo.insert(name.as_str());
        value.find_dependencies(name, &mut topo);
    }

    let mut sorted = Vec::with_capacity(conditions.len());
    while !topo.is_empty() {
        let mut list = topo.pop_all();
        if list.is_empty() {
            panic!("There are cyclic deps in the conditions clauses")
        }
        // Ensure consistent ordering in generated code...
        list.sort();
        sorted.extend(list);
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
            Self::Condition(x) => {
                topo_sort.add_dependency(x.as_str(), logical_id);
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
            Self::FindInMap(_, key1, key2) => {
                key1.find_dependencies(logical_id, topo_sort);
                key2.find_dependencies(logical_id, topo_sort);
            }
            Self::Split(_, key1) => {
                key1.find_dependencies(logical_id, topo_sort);
            }
            Self::Select(_, key1) => {
                key1.find_dependencies(logical_id, topo_sort);
            }
            Self::Function(func) => func.find_dependencies(logical_id, topo_sort),
            Self::Ref(_) | Self::String(_) => {}
        }
    }
}

#[cfg(test)]
mod tests;
