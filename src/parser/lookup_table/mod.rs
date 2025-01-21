// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use crate::{primitives::WrapperF64, Hasher};
use indexmap::IndexMap;
use std::fmt::{Display, Formatter};

#[derive(Clone, Debug, PartialEq, serde::Deserialize)]
#[serde(transparent)]
pub struct MappingTable {
    pub mappings: IndexMap<String, IndexMap<String, MappingInnerValue, Hasher>, Hasher>,
}

/**
 * MappingInnerValue tracks the allowed value types in a Mapping as defined by CloudFormation in the
 * link below. The values are allowed to only be a String or List:
 *
 * https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html#mappings-section-structure-syntax
 *
 * In reality, all values are allowed from the json specification. If we detect any other conflicting
 * numbers, then the type becomes "Any" to allow for the strangeness.
 */
#[derive(Debug, Clone, PartialEq, serde::Deserialize)]
#[serde(untagged)]
pub enum MappingInnerValue {
    Number(i64),
    Float(WrapperF64),
    Bool(bool),
    String(String),
    List(Vec<String>),
}

impl Display for MappingInnerValue {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            MappingInnerValue::String(string_val) => write!(f, "'{string_val}'"),
            MappingInnerValue::List(list_val) => {
                let quoted_list_values: Vec<String> =
                    list_val.iter().map(|val| format!("'{val}'")).collect();
                write!(f, "[{}]", quoted_list_values.join(","))
            }
            MappingInnerValue::Number(val) => write!(f, "{val}"),
            MappingInnerValue::Float(val) => write!(f, "{val}"),
            MappingInnerValue::Bool(val) => write!(f, "{val}"),
        }
    }
}
