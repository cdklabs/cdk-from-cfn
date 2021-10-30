use crate::parser::condition::{ConditionValue, ConditionsParseTree};
use crate::parser::resource::ResourceValue;
use crate::CloudformationParseTree;
use std::collections::HashMap;
use std::ops::Deref;

/// ReferenceTable is for producing variable names and resolving references in other bits of code.
/// As an example, say you have:
/// ```json
/// {  "Ref" : "John" }
/// ```
/// Is `John` a parameter or a Logical Id? We need to keep track of this information after the parse
/// tree is built. This way we can build up references across stacks, if need be.
pub struct ReferenceTable {
    table: HashMap<String, Reference>,
    callers: HashMap<String, Vec<String>>,
}

impl ReferenceTable {
    pub fn new(parse_tree: &CloudformationParseTree) -> ReferenceTable {
        let mut table = ReferenceTable {
            table: HashMap::new(),
            callers: HashMap::new(),
        };

        populate_condition_references(&mut table, &parse_tree.conditions);
        table
    }

    pub fn insert(&mut self, name: &str, obj: Reference) {
        self.table.insert(String::from(name), obj);
    }

    pub fn add_link(&mut self, reference_name: &str, caller: &str) {
        let mut called = match self.callers.get(reference_name) {
            None => Vec::new(),
            Some(s) => s.to_vec(),
        };

        let contained = called.iter().find(|x| x.as_str() == caller);

        match contained {
            None => {
                called.push(String::from(caller));
            }
            // We already have the caller, dont call again
            Some(_) => {}
        }

        self.callers.insert(String::from(reference_name), called);
    }

    pub fn iter_links(&self) -> impl Iterator<Item = &String> {
        println!("{:?}", self.callers.keys());
        self.callers.keys()
    }

    pub fn get_links(&self, name: &str) -> Option<Vec<String>> {
        self.callers.get(name).cloned()
    }

    pub fn get(&self, name: &str) -> Option<&Reference> {
        self.table.get(name)
    }
}

#[derive(Debug)]
pub struct Reference {
    pub origin: Origin,
    pub name: String,
}

impl Reference {
    fn synthesize(&self) -> String {
        match &self.origin {
            Origin::Parameter => {
                format!("props.{}", self.name)
            }
            Origin::LogicalId => self.name.to_string(),
            Origin::PseudoParameter(x) => match x {
                PseudoParameter::Partition => String::from("this.partition"),
                PseudoParameter::Region => String::from("this.region"),
                PseudoParameter::StackId => String::from("this.stackId"),
                PseudoParameter::StackName => String::from("this.stackName"),
                PseudoParameter::URLSuffix => String::from("this.urlSuffix"),
            },
        }
    }
}

// Origin for the ReferenceTable
#[derive(Debug)]
pub enum Origin {
    Parameter,
    LogicalId,
    PseudoParameter(PseudoParameter),
}

#[derive(Debug)]
pub enum PseudoParameter {
    Partition,
    Region,
    StackId,
    StackName,
    URLSuffix,
}

fn populate_condition_references(rt: &mut ReferenceTable, conditions: &ConditionsParseTree) {
    for (name, condition) in conditions.conditions.iter() {
        rt.insert(
            name,
            Reference {
                name: String::from(name),
                origin: Origin::LogicalId,
            },
        );
        populate_traversal(rt, name, &condition.val);
    }
}

fn populate_traversal(rt: &mut ReferenceTable, name: &str, condition: &ConditionValue) {
    match condition {
        ConditionValue::And(v) => {
            for cv in v.iter() {
                populate_traversal(rt, name, cv);
            }
        }
        ConditionValue::Equals(b1, b2) => {
            populate_traversal(rt, name, b1.deref());
            populate_traversal(rt, name, b2.deref());
        }
        ConditionValue::Not(b) => populate_traversal(rt, name, b.deref()),
        ConditionValue::Or(v) => {
            for cv in v.iter() {
                populate_traversal(rt, name, cv);
            }
        }
        /*ConditionValue::Sub(v) => {
            for cv in v.iter() {
                populate_traversal(rt, name, cv);
            }
        }*/
        ConditionValue::FindInMap(map_name, l1, l2) => {
            populate_traversal(rt, name, map_name.as_ref());
            populate_traversal(rt, name, l1.as_ref());
            populate_traversal(rt, name, l2.as_ref());
        }
        ConditionValue::Str(_) => {}
        ConditionValue::Ref(r) => {
            rt.insert(
                r,
                Reference {
                    name: String::from(r),
                    origin: Origin::Parameter,
                },
            );
            rt.add_link(r, name)
        }
        ConditionValue::Condition(r) => rt.add_link(r, name),
    }
}

#[allow(dead_code)]
fn resolve_resource_recursively(resource_value: &ResourceValue) -> i64 {
    match resource_value {
        ResourceValue::Null => 0,
        ResourceValue::Bool(_) => 0,
        ResourceValue::Number(_) => 0,
        ResourceValue::String(_) => 0,
        ResourceValue::Array(arr) => {
            let mut amount = 0;
            for rv in arr.iter() {
                amount += resolve_resource_recursively(rv);
            }

            amount
        }
        ResourceValue::Object(obj) => {
            let mut amount = 0;
            for rv in obj.values() {
                amount += resolve_resource_recursively(rv);
            }

            amount
        }
        ResourceValue::Sub(arr) => {
            let mut amount = 0;
            for rv in arr.iter() {
                amount += resolve_resource_recursively(rv);
            }

            amount
        }
        ResourceValue::FindInMap(a, b, c) => {
            let mut amount = 0;
            amount += resolve_resource_recursively(a.deref());
            amount += resolve_resource_recursively(b.deref());
            amount += resolve_resource_recursively(c.deref());
            amount + 1
        }
        ResourceValue::GetAtt(a, b) => {
            let mut amount = 0;
            amount += resolve_resource_recursively(a.deref());
            amount += resolve_resource_recursively(b.deref());
            amount + 1
        }
        ResourceValue::If(a, b, c) => {
            let mut amount = 0;
            amount += resolve_resource_recursively(a.deref());
            amount += resolve_resource_recursively(b.deref());
            amount += resolve_resource_recursively(c.deref());
            amount + 1
        }
        ResourceValue::Join(arr) => {
            let mut amount = 0;
            for rv in arr.iter() {
                amount += resolve_resource_recursively(rv);
            }

            amount
        }
        ResourceValue::Ref(_) => 1,
    }
}
