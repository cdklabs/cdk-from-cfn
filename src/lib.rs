#![allow(dead_code)]

use indexmap::IndexMap;
use parser::condition::ConditionFunction;
use parser::lookup_table::MappingTable;
use parser::output::Output;
use parser::parameters::Parameter;
use parser::resource::{ResourceAttributes, ResourceValue};

pub mod errors;
pub mod integrations;
pub mod ir;
pub mod parser;
pub mod primitives;
pub mod specification;
pub mod synthesizer;

#[doc(inline)]
pub use errors::*;

pub trait CustomIntegration {
    fn is_type(resource_type: &str) -> bool;
    fn synthesize(rv: &ResourceValue) -> String;
}

pub struct Import {
    package: String,
}

pub struct CdkBuilder {
    // Each cfn resource we use, is in a different package. Each resource will add imports to this
    // list.
    imports: Vec<Import>,
}

#[derive(Debug, serde::Deserialize)]
#[serde(rename_all = "PascalCase")]
pub struct CloudformationParseTree {
    pub description: Option<String>,

    #[serde(default, rename = "Transform")]
    pub transforms: Vec<String>,

    #[serde(default)]
    pub conditions: IndexMap<String, ConditionFunction>,
    #[serde(default)]
    pub mappings: IndexMap<String, MappingTable>,
    #[serde(default)]
    pub outputs: IndexMap<String, Output>,
    #[serde(default)]
    pub parameters: IndexMap<String, Parameter>,

    pub resources: IndexMap<String, ResourceAttributes>,
}
