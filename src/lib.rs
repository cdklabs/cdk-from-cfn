use indexmap::IndexMap;
use parser::condition::ConditionFunction;
use parser::lookup_table::MappingTable;
use parser::output::Output;
use parser::parameters::Parameter;
use parser::resource::ResourceAttributes;

pub mod errors;
pub mod ir;
pub mod parser;
pub mod primitives;
pub mod specification;
pub mod synthesizer;

#[doc(inline)]
pub use errors::*;

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
