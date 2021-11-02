use crate::parser::condition::{determine_order, ConditionValue};
use crate::CloudformationParseTree;

// ConditionInstructions are simple assignment + boolean
// clauses, as conditions are based on those composite values.
// It may have made more sense to copy completely to the parse tree
// but for now we will keep ConditionInstruction + ConditionIr
// as a single entity.
#[derive(Debug, Clone)]
pub struct ConditionInstruction {
    name: String,
    value: ConditionIr,
}

#[derive(Debug, Clone)]
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
    Condition(String),
}

fn translate(parse_tree: &CloudformationParseTree) -> Vec<ConditionInstruction> {
    let mut list = Vec::new();
    for cond in determine_order(&parse_tree.conditions) {
        let ir = translate_ir(&cond.val, parse_tree);
        list.push(ConditionInstruction {
            name: cond.name,
            value: ir,
        });
    }

    list
}

fn translate_ir(value: &ConditionValue, parse_tree: &CloudformationParseTree) -> ConditionIr {
    match value {
        ConditionValue::And(x) => {
            let and_list = x
                .iter()
                .cloned()
                .map(|y| translate_ir(&y, parse_tree))
                .collect();
            ConditionIr::And(and_list)
        }
        ConditionValue::Equals(x, y) => {
            let x = translate_ir(x, parse_tree);
            let y = translate_ir(y, parse_tree);

            ConditionIr::Equals(Box::new(x), Box::new(y))
        }
        ConditionValue::Not(x) => {
            let x = translate_ir(x, parse_tree);
            ConditionIr::Not(Box::new(x))
        }
        ConditionValue::Or(x) => {
            let or_list = x
                .iter()
                .cloned()
                .map(|y| translate_ir(&y, parse_tree))
                .collect();
            ConditionIr::And(or_list)
        }
        ConditionValue::FindInMap(name, x, y) => {
            let name = translate_ir(name, parse_tree);
            let x = translate_ir(x, parse_tree);
            let y = translate_ir(y, parse_tree);

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

#[derive(Debug, Clone)]
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
            Origin::Condition => self.name.to_string(),
            Origin::PseudoParameter(x) => match x {
                PseudoParameter::Partition => String::from("this.partition"),
                PseudoParameter::Region => String::from("this.region"),
                PseudoParameter::StackId => String::from("this.stackId"),
                PseudoParameter::StackName => String::from("this.stackName"),
                PseudoParameter::URLSuffix => String::from("this.urlSuffix"),
            },
        }
    }

    fn match_pseudo_parameter(val: &str) -> Option<PseudoParameter> {
        let pseudo = match val {
            "AWS::Region" => PseudoParameter::Region,
            "AWS::Partition" => PseudoParameter::Partition,
            "AWS::StackName" => PseudoParameter::StackName,
            "AWS::UrlSuffix" => PseudoParameter::URLSuffix,
            "AWS::StackId" => PseudoParameter::StackId,
            &_ => return Option::None,
        };

        Option::Some(pseudo)
    }
}

// Origin for the ReferenceTable
#[derive(Debug, Clone)]
pub enum Origin {
    Parameter,
    LogicalId,
    Condition,
    PseudoParameter(PseudoParameter),
}

#[derive(Debug, Clone)]
pub enum PseudoParameter {
    Partition,
    Region,
    StackId,
    StackName,
    URLSuffix,
}
