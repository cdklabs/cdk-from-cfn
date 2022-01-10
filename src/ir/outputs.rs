use crate::CloudformationParseTree;
use crate::ir::resources::{ResourceIr, ResourceTranslationInputs, translate_resource};
use crate::specification::{Complexity, SimpleType};

pub struct OutputInstruction {
    pub name: String,
    pub export: Option<ResourceIr>,
    pub value: ResourceIr,
}

pub fn translate(parse_tree: &CloudformationParseTree) -> Vec<OutputInstruction> {
    let outputs = &parse_tree.outputs;
    let mut instructions = Vec::new();
    for (name, output) in outputs.outputs.iter() {
        let resource_translator = ResourceTranslationInputs{
            parse_tree,
            complexity: Complexity::Simple(SimpleType::Json),
            resource_metadata: None
        };

        let value = translate_resource(&output.value, &resource_translator).unwrap();
        let mut export = Option::None;
        if let Some(x) = &output.export {
            export = Option::Some(translate_resource(x, &resource_translator).unwrap());
        }

        instructions.push(OutputInstruction {
            name: name.to_string(),
            export,
            value
        })
    }
    instructions
}
