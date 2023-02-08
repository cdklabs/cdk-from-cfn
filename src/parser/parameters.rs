use crate::TransmuteError;
use serde_json::{Map, Value};
use std::collections::HashMap;

// template anatomy can be found here: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html
#[derive(Debug)]
pub struct Parameters {
    pub params: HashMap<String, Parameter>,
}

impl Parameters {
    pub fn new() -> Parameters {
        Parameters {
            params: HashMap::new(),
        }
    }

    pub fn add(&mut self, param: Parameter) {
        self.params.insert(param.logical_name.clone(), param);
    }
}

#[derive(Debug)]
pub struct Parameter {
    // This is the top level name, also stored in the hash
    pub logical_name: String,
    pub parameter_type: String, // TODO - I think this is limited, may want to make it an enum.
    pub default: Option<String>,
}

impl Parameter {
    fn new(logical_name: String, parameter_type: String, default: Option<String>) -> Parameter {
        Parameter {
            logical_name,
            parameter_type,
            default,
        }
    }
}

impl Default for Parameters {
    fn default() -> Self {
        Self::new()
    }
}

pub fn build_parameters(vals: &Map<String, Value>) -> Result<Parameters, TransmuteError> {
    let mut params = Parameters::new();
    for (name, obj) in vals {
        let t = match obj.get("Type") {
            Some(v) => v.to_string(),
            None => {
                return Err(TransmuteError {
                    details: format!("Type was not specified correctly {name}"),
                })
            }
        };

        let def: Option<String> = obj.get("Default").map(|d| d.to_string());

        params.add(Parameter::new(name.clone(), t, def));
    }

    Ok(params)
}
