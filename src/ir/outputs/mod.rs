// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use indexmap::IndexMap;

use crate::cdk::{Primitive, Schema, TypeReference};
use crate::ir::resources::{ResourceIr, ResourceTranslator};
use crate::parser::output::Output;
use crate::parser::resource::ResourceValue;
use crate::util::Hasher;
use crate::Error;

use super::ReferenceOrigins;

#[derive(Debug, PartialEq)]
pub struct OutputInstruction {
    pub name: String,
    pub export: Option<ResourceIr>,
    pub value: ResourceIr,
    pub condition: Option<String>,
    pub description: Option<String>,
}

impl OutputInstruction {
    pub(super) fn from(
        parse_tree: IndexMap<String, Output, Hasher>,
        schema: &Schema,
        origins: &ReferenceOrigins,
    ) -> Result<Vec<Self>, Error> {
        let mut list = Vec::with_capacity(parse_tree.len());

        for (name, output) in parse_tree {
            let resource_translator = ResourceTranslator {
                schema,
                origins,
                value_type: Some(TypeReference::Primitive(Primitive::Json)),
            };

            let value = resource_translator.translate(output.value)?;
            let condition = output.condition;
            let description = output.description;
            let mut export: Option<ResourceIr> = None;
            if let Some(ResourceValue::Object(x)) = output.export {
                if let Some(x) = x.get_key_value("Name") {
                    export = Some(resource_translator.translate(x.1.clone())?);
                }
            }

            list.push(Self {
                name,
                export,
                value,
                condition,
                description,
            })
        }

        Ok(list)
    }
}

#[cfg(test)]
mod tests;
