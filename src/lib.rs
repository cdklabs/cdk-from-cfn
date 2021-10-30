#![allow(dead_code)]

use crate::parser::condition::{build_conditions, ConditionsParseTree};
use crate::parser::lookup_table::{build_mappings, MappingsParseTree};
use crate::parser::parameters::{build_parameters, Parameters};
use crate::parser::resource::{build_resources, ResourceValue, ResourcesParseTree};
use serde_json::Value;

pub mod integrations;
pub mod parser;
pub mod semantic;
pub mod specification;

pub trait CustomIntegration {
    fn is_type(resource_type: &str) -> bool;
    fn synthesize(rv: &ResourceValue) -> String;
}

#[derive(Debug)]
pub struct TransmuteError {
    details: String,
}

impl TransmuteError {
    fn new(msg: &str) -> TransmuteError {
        TransmuteError {
            details: msg.to_string(),
        }
    }
}

pub struct Import {
    package: String,
}

pub struct CdkBuilder {
    // Each cfn resource we use, is in a different package. Each resource will add imports to this
    // list.
    imports: Vec<Import>,
}

pub struct CloudformationParseTree {
    pub parameters: Parameters,
    pub mappings: MappingsParseTree,
    pub conditions: ConditionsParseTree,
    pub resources: ResourcesParseTree,
}

impl CloudformationParseTree {
    pub fn build(json_obj: &Value) -> Result<CloudformationParseTree, TransmuteError> {
        let parameters = match json_obj["Parameters"].as_object() {
            None => Parameters::new(),
            Some(params) => build_parameters(params)?,
        };
        let conditions = build_conditions(json_obj["Conditions"].as_object().unwrap())?;
        let resources = build_resources(json_obj["Resources"].as_object().unwrap())?;
        let mappings: MappingsParseTree =
            build_mappings(json_obj["Mappings"].as_object().unwrap())?;

        Ok(CloudformationParseTree {
            parameters,
            conditions,
            resources,
            mappings,
        })
    }
}
