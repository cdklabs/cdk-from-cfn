use crate::ir::conditions::ConditionInstruction;
use crate::ir::constructor::Constructor;
use crate::ir::importer::ImportInstruction;
use crate::ir::mappings::MappingInstruction;
use crate::ir::outputs::OutputInstruction;
use crate::ir::resources::ResourceInstruction;
use crate::{CloudformationParseTree, TransmuteError};

pub mod conditions;
pub mod constructor;
pub mod importer;
pub mod mappings;
pub mod outputs;
pub mod reference;
pub mod resources;
pub mod sub;

pub struct CloudformationProgramIr {
    pub imports: Vec<ImportInstruction>,
    pub constructor: Constructor,
    pub conditions: Vec<ConditionInstruction>,
    pub mappings: Vec<MappingInstruction>,
    pub resources: Vec<ResourceInstruction>,
    pub outputs: Vec<OutputInstruction>,
}

impl CloudformationProgramIr {
    fn new() -> CloudformationProgramIr {
        CloudformationProgramIr {
            imports: Vec::new(),
            constructor: Constructor::new(),
            conditions: Vec::new(),
            mappings: Vec::new(),
            resources: Vec::new(),
            outputs: Vec::new(),
        }
    }

    // new_from_parse_tree takes a parse tree and translates it fully into Intermediate representation.
    // because there could be incorrect semantics, Result::Error can only happen on semantic error,
    // not parsing errors.
    pub fn new_from_parse_tree(
        parse_tree: &CloudformationParseTree,
    ) -> Result<CloudformationProgramIr, TransmuteError> {
        let conditions = conditions::translate_conditions(parse_tree);
        let imports = importer::Importer::translate(parse_tree);
        let constructor = constructor::Constructor::translate(parse_tree);
        let mappings = mappings::translate(parse_tree);
        let resources = resources::translates_resources(parse_tree);
        let outputs = outputs::translate(parse_tree);
        Ok(CloudformationProgramIr {
            imports,
            constructor,
            conditions,
            mappings,
            resources,
            outputs,
        })
    }
}
