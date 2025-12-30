// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

// All kinds of Clippy warnings we're not interested int
#![allow(
    // Many tests assert against unit value, I'm not rewriting them now
    clippy::unit_cmp,
    // We should be allowed to do `Ok(value)` when value is `()`
    clippy::unit_arg,
)]

use indexmap::IndexMap;
use parser::condition::ConditionFunction;
use parser::lookup_table::MappingTable;
use parser::output::Output;
use parser::parameters::Parameter;
use parser::resource::ResourceAttributes;
use serde::{Deserialize, Deserializer};

pub mod cdk;
pub mod code;
pub mod errors;
pub mod ir;
pub mod parser;
pub mod primitives;
pub mod synthesizer;

mod util;

#[doc(inline)]
pub use errors::*;

#[doc(inline)]
pub use util::Hasher;

#[derive(Debug, serde::Deserialize)]
#[serde(rename_all = "PascalCase")]
pub struct CloudformationParseTree {
    pub description: Option<String>,

    #[serde(
        default,
        rename = "Transform",
        deserialize_with = "string_or_seq_string"
    )]
    pub transforms: Vec<String>,

    #[serde(default)]
    pub conditions: IndexMap<String, ConditionFunction, Hasher>,
    #[serde(default)]
    pub mappings: IndexMap<String, MappingTable, Hasher>,
    #[serde(default)]
    pub outputs: IndexMap<String, Output, Hasher>,
    #[serde(default)]
    pub parameters: IndexMap<String, Parameter, Hasher>,

    pub resources: IndexMap<String, ResourceAttributes, Hasher>,
}

fn string_or_seq_string<'de, D>(deserializer: D) -> Result<Vec<String>, D::Error>
where
    D: Deserializer<'de>,
{
    #[derive(Deserialize)]
    #[serde(untagged)]
    pub enum Transform {
        String(String),
        Vec(Vec<String>),
    }

    Ok(match Transform::deserialize(deserializer)? {
        Transform::String(transform) => vec![transform],
        Transform::Vec(transform) => transform,
    })
}

#[cfg(target_family = "wasm")]
pub mod wasm {
    use cdk::Schema;
    use wasm_bindgen::prelude::*;

    use super::*;

    /// Returns an array containing all supported language names.
    #[wasm_bindgen]
    pub fn supported_languages() -> Box<[JsValue]> {
        vec![
            #[cfg(feature = "typescript")]
            wasm_bindgen::intern("typescript").into(),
            #[cfg(feature = "golang")]
            wasm_bindgen::intern("go").into(),
            #[cfg(feature = "java")]
            wasm_bindgen::intern("java").into(),
            #[cfg(feature = "python")]
            wasm_bindgen::intern("python").into(),
            #[cfg(feature = "csharp")]
            wasm_bindgen::intern("csharp").into(),
        ]
        .into_boxed_slice()
    }

    /// Transforms the provided template into a CDK application in the specified
    /// language.
    #[wasm_bindgen]
    pub fn transmute(
        template: &str,
        language: &str,
        stack_name: &str,
        stack_type: Option<String>,
    ) -> Result<String, JsError> {
        let cfn_tree: CloudformationParseTree = serde_yaml::from_str(template)?;
        let ir = crate::ir::CloudformationProgramIr::from(cfn_tree, Schema::builtin())?;
        let mut output = Vec::new();

        let lang = match language {
            "go" => "golang",
            other => other,
        };

        let stack_type_enum: crate::synthesizer::StackType = stack_type
            .as_deref()
            .unwrap_or("stack")
            .parse()
            .unwrap_or_default();

        ir.synthesize(lang, &mut output, stack_name, stack_type_enum)?;

        String::from_utf8(output).map_err(Into::into)
    }

    #[cfg(feature = "console_error_panic_hook")]
    #[wasm_bindgen(start)]
    fn wasm_init() {
        console_error_panic_hook::set_once();
    }
}
