// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use std::fmt;

#[derive(Debug, PartialEq, serde::Deserialize)]
#[serde(rename_all = "PascalCase")]
pub struct Parameter {
    pub allowed_values: Option<Vec<String>>,
    pub default: Option<String>,
    pub description: Option<String>,
    #[serde(rename = "Type")]
    pub parameter_type: ParameterType,
    pub no_echo: Option<String>,
}

#[derive(Clone, Debug, PartialEq, serde_enum_str::Deserialize_enum_str)]
pub enum ParameterType {
    String,
    Number,
    #[serde(rename = "List<Number>")]
    ListOfNumbers,
    CommaDelimitedList,
    Bool,
    #[serde(other)]
    Other(String),
}

impl fmt::Display for ParameterType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            ParameterType::String => write!(f, "String"),
            ParameterType::Number => write!(f, "Number"),
            ParameterType::ListOfNumbers => write!(f, "List<Number>"),
            ParameterType::CommaDelimitedList => write!(f, "CommaDelimitedList"),
            ParameterType::Other(s) => write!(f, "{s}"),
            ParameterType::Bool => write!(f, "Boolean"),
        }
    }
}

#[cfg(test)]
mod tests;
