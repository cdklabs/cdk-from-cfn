#![allow(dead_code)]

use crate::parser::condition::{build_conditions, ConditionsParseTree};
use crate::parser::lookup_table::{build_mappings, MappingsParseTree};
use crate::parser::output::{build_outputs, OutputsParseTree};
use crate::parser::parameters::{build_parameters, Parameters};
use crate::parser::resource::{build_resources, ResourceValue, ResourcesParseTree};
use serde_json::Value;

pub mod integrations;
pub mod ir;
pub mod parser;
pub mod primitives;
pub mod specification;
pub mod synthesizer;

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

#[derive(Debug)]
pub struct CloudformationParseTree {
    pub parameters: Parameters,
    pub mappings: MappingsParseTree,
    pub conditions: ConditionsParseTree,
    pub resources: ResourcesParseTree,
    pub outputs: OutputsParseTree,
}

impl CloudformationParseTree {
    pub fn build(json_obj: &Value) -> Result<CloudformationParseTree, TransmuteError> {
        let parameters = match json_obj["Parameters"].as_object() {
            None => Parameters::new(),
            Some(params) => build_parameters(params)?,
        };

        let conditions = match json_obj["Conditions"].as_object() {
            None => ConditionsParseTree::new(),
            Some(x) => build_conditions(x)?,
        };

        // All stacks must have resources, so no checking.
        let resources = build_resources(json_obj["Resources"].as_object().unwrap())?;

        let mappings = match json_obj["Mappings"].as_object() {
            None => MappingsParseTree::new(),
            Some(x) => build_mappings(x)?,
        };
        let outputs = match json_obj["Outputs"].as_object() {
            None => OutputsParseTree::new(),
            Some(x) => build_outputs(x)?,
        };

        Ok(CloudformationParseTree {
            parameters,
            conditions,
            resources,
            mappings,
            outputs,
        })
    }
}
