use crate::ir::resources::{translate_resource, ResourceIr, ResourceTranslationInputs};
use crate::specification::{CfnType, Structure};
use crate::CloudformationParseTree;

pub struct OutputInstruction {
    pub name: String,
    pub export: Option<ResourceIr>,
    pub value: ResourceIr,
    pub condition: Option<String>,
    pub description: Option<String>,
}

pub fn translate(parse_tree: &CloudformationParseTree) -> Vec<OutputInstruction> {
    let mut instructions = Vec::with_capacity(parse_tree.outputs.len());
    for (name, output) in &parse_tree.outputs {
        let resource_translator = ResourceTranslationInputs {
            parse_tree,
            complexity: Structure::Simple(CfnType::Json),
            resource_metadata: None,
        };

        let value = translate_resource(&output.value, &resource_translator).unwrap();
        let condition = output.condition.clone();
        let description = output.description.clone();
        let mut export = Option::None;
        if let Some(x) = &output.export {
            export = Option::Some(translate_resource(x, &resource_translator).unwrap());
        }

        instructions.push(OutputInstruction {
            name: name.to_string(),
            export,
            value,
            condition,
            description,
        })
    }
    instructions
}
