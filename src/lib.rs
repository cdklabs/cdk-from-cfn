#![cfg_attr(coverage_nightly, feature(no_coverage))]

use indexmap::IndexMap;
use parser::condition::ConditionFunction;
use parser::lookup_table::MappingTable;
use parser::output::Output;
use parser::parameters::Parameter;
use parser::resource::ResourceAttributes;
use wasm_bindgen::prelude::*;

pub mod errors;
pub mod ir;
pub mod parser;
pub mod primitives;
pub mod specification;
pub mod synthesizer;

mod code;

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

#[wasm_bindgen]
pub fn transmute(template: &str, language: &str) -> Result<String, JsError> {
    let cfn_tree: CloudformationParseTree = serde_yaml::from_str(template)?;
    let ir = crate::ir::CloudformationProgramIr::from(cfn_tree)?;
    let mut output = Vec::new();

    let synthesizer: Box<dyn crate::synthesizer::Synthesizer> = match language {
        #[cfg(feature = "typescript")]
        "typescript" => Box::new(crate::synthesizer::Typescript {}),
        #[cfg(feature = "golang")]
        "go" => Box::<crate::synthesizer::Golang>::default(),
        unsupported => panic!("unsupported language: {}", unsupported),
    };

    ir.synthesize(synthesizer.as_ref(), &mut output)?;

    String::from_utf8(output).map_err(Into::into)
}

#[cfg(target_family = "wasm")]
#[cfg(feature = "console_error_panic_hook")]
#[wasm_bindgen(start)]
fn wasm_init() {
    console_error_panic_hook::set_once();
}
