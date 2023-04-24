#![allow(dead_code)]

use crate::parser::condition::{build_conditions, ConditionsParseTree};
use crate::parser::lookup_table::{build_mappings, MappingsParseTree};
use crate::parser::output::{build_outputs, OutputsParseTree};
use crate::parser::parameters::{build_parameters, Parameters};
use crate::parser::resource::{build_resources, ResourceValue, ResourcesParseTree};
use serde_yaml::Value;
use std::collections::HashSet;

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

    pub logical_lookup: HashSet<String>,
}

impl CloudformationParseTree {
    pub fn build(json_obj: &Value) -> Result<CloudformationParseTree, TransmuteError> {
        let parameters = match json_obj["Parameters"].as_mapping() {
            None => Parameters::new(),
            Some(params) => build_parameters(params)?,
        };

        let conditions = match json_obj["Conditions"].as_mapping() {
            None => ConditionsParseTree::new(),
            Some(x) => build_conditions(x)?,
        };

        // All stacks must have resources, so no checking.
        let resources = build_resources(json_obj["Resources"].as_mapping().unwrap())?;

        let logical_lookup = CloudformationParseTree::build_logical_lookup(&resources);

        let mappings = match json_obj["Mappings"].as_mapping() {
            None => MappingsParseTree::new(),
            Some(x) => build_mappings(x)?,
        };
        let outputs = match json_obj["Outputs"].as_mapping() {
            None => OutputsParseTree::new(),
            Some(x) => build_outputs(x)?,
        };

        Ok(CloudformationParseTree {
            parameters,
            conditions,
            resources,
            mappings,
            outputs,
            logical_lookup,
        })
    }

    pub fn build_logical_lookup(resources: &ResourcesParseTree) -> HashSet<String> {
        let mut logical_lookup = HashSet::new();
        for resource in resources.resources.iter() {
            logical_lookup.insert(resource.name.clone());
        }
        logical_lookup
    }

    pub fn contains_logical_id(&self, logical_id: &str) -> bool {
        self.logical_lookup.contains(logical_id)
    }
}