use crate::parser::resource::build_resources_recursively;
use crate::{ResourceValue, TransmuteError};
use serde_json::{Map, Value};
use std::collections::HashMap;

#[derive(Debug)]
pub struct OutputsParseTree {
    pub outputs: HashMap<String, Output>,
}

impl OutputsParseTree {
    pub fn new() -> OutputsParseTree {
        OutputsParseTree {
            outputs: HashMap::new(),
        }
    }

    pub fn add(&mut self, output: Output) {
        self.outputs.insert(output.logical_name.clone(), output);
    }
}

#[derive(Debug)]
pub struct Output {
    // This is the top level name, also stored in the hash
    pub logical_name: String,
    pub value: ResourceValue, // TODO - I think this is limited, may want to make it an enum.
    pub export: Option<ResourceValue>,
    pub condition: Option<String>,
    pub description: Option<String>,
}

impl Output {
    fn new(
        logical_name: String,
        value: ResourceValue,
        export: Option<ResourceValue>,
        condition: Option<String>,
        description: Option<String>,
    ) -> Output {
        Output {
            logical_name,
            value,
            export,
            condition,
            description,
        }
    }
}

impl Default for OutputsParseTree {
    fn default() -> Self {
        Self::new()
    }
}

pub fn build_outputs(vals: &Map<String, Value>) -> Result<OutputsParseTree, TransmuteError> {
    let mut outputs = OutputsParseTree::new();
    for (logical_id, value) in vals.iter() {
        let val = match value.get("Value") {
            None => {
                // All outputs *MUST* have a value. Fail
                return Err(TransmuteError::new(
                    "All outputs must have a value, but this does not",
                ));
            }
            Some(x) => build_resources_recursively(logical_id, x)?,
        };

        // For all Exports that exist, it must have a Name object, if either don't exist, don't record.
        let export = match value.get("Export").and_then(|x| x.get("Name")) {
            None => Option::None,
            Some(x) => Option::Some(build_resources_recursively(logical_id, x)?),
        };

        let condition = value
            .get("Condition")
            .and_then(|t| t.as_str())
            .map(|t| t.to_string());

        let description = value
            .get("Description")
            .and_then(|t| t.as_str())
            .map(|t| t.to_string());

        outputs.add(Output {
            logical_name: logical_id.to_string(),
            value: val,
            export,
            condition,
            description,
        });
    }

    Ok(outputs)
}
