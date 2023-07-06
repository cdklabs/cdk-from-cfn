use indexmap::IndexMap;

use crate::cdk::{Primitive, Schema, TypeReference};
use crate::ir::resources::{ResourceIr, ResourceTranslator};
use crate::parser::output::Output;
use crate::util::Hasher;
use crate::TransmuteError;

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
    ) -> Result<Vec<Self>, TransmuteError> {
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
            let export = match output.export {
                Some(x) => Some(resource_translator.translate(x)?),
                None => None,
            };

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
