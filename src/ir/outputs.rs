use indexmap::IndexMap;

use crate::ir::resources::{ResourceIr, ResourceTranslator};
use crate::parser::output::Output;
use crate::specification::{CfnType, Structure};
use crate::TransmuteError;

use super::ReferenceOrigins;

pub struct OutputInstruction {
    pub name: String,
    pub export: Option<ResourceIr>,
    pub value: ResourceIr,
    pub condition: Option<String>,
    pub description: Option<String>,
}

impl OutputInstruction {
    pub(super) fn from(
        parse_tree: IndexMap<String, Output>,
        origins: &ReferenceOrigins,
    ) -> Result<Vec<Self>, TransmuteError> {
        let mut list = Vec::with_capacity(parse_tree.len());

        for (name, output) in parse_tree {
            let resource_translator = ResourceTranslator {
                complexity: Structure::Simple(CfnType::Json),
                origins,
                resource_metadata: None,
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
