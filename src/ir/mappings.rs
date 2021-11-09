use crate::parser::lookup_table::MappingInnerValue;
use crate::CloudformationParseTree;
use std::collections::HashMap;

pub struct MappingInstruction {
    pub name: String,
    pub map: HashMap<String, HashMap<String, MappingInnerValue>>,
}

impl MappingInstruction {
    pub fn find_first_type(&self) -> &MappingInnerValue {
        let value = self.map.values().next().unwrap();
        let inner_value = value.values().next().unwrap();
        inner_value
    }
}
pub fn translate(parse_tree: &CloudformationParseTree) -> Vec<MappingInstruction> {
    let mapping_parse_tree = &parse_tree.mappings;
    let mut instructions = Vec::new();
    for (name, map) in mapping_parse_tree.mappings.iter() {
        instructions.push(MappingInstruction {
            name: name.to_string(),
            map: map.mappings.clone(),
        })
    }
    instructions
}
