use std::collections::HashMap;

use crate::ir::conditions::ConditionInstruction;
use crate::ir::constructor::Constructor;
use crate::ir::importer::ImportInstruction;
use crate::ir::mappings::MappingInstruction;
use crate::ir::outputs::OutputInstruction;
use crate::ir::resources::ResourceInstruction;
use crate::{CloudformationParseTree, TransmuteError};

use self::reference::{Origin, PseudoParameter};

pub mod conditions;
pub mod constructor;
pub mod importer;
pub mod mappings;
pub mod outputs;
pub mod reference;
pub mod resources;
pub mod sub;

pub struct CloudformationProgramIr {
    pub description: Option<String>,
    pub transforms: Vec<String>,

    pub imports: Vec<ImportInstruction>,
    pub constructor: Constructor,
    pub conditions: Vec<ConditionInstruction>,
    pub mappings: Vec<MappingInstruction>,
    pub resources: Vec<ResourceInstruction>,
    pub outputs: Vec<OutputInstruction>,
}

impl CloudformationProgramIr {
    // new_from_parse_tree takes a parse tree and translates it fully into Intermediate representation.
    // because there could be incorrect semantics, Result::Error can only happen on semantic error,
    // not parsing errors.
    pub fn from(
        parse_tree: CloudformationParseTree,
    ) -> Result<CloudformationProgramIr, TransmuteError> {
        let origins = ReferenceOrigins::new(&parse_tree);

        Ok(CloudformationProgramIr {
            description: parse_tree.description,
            transforms: parse_tree.transforms,
            conditions: ConditionInstruction::from(parse_tree.conditions),
            imports: ImportInstruction::from(&parse_tree.resources)?,
            constructor: Constructor::from(parse_tree.parameters),
            mappings: MappingInstruction::from(parse_tree.mappings),
            resources: ResourceInstruction::from(parse_tree.resources, &origins)?,
            outputs: OutputInstruction::from(parse_tree.outputs, &origins)?,
        })
    }
}

#[derive(Debug)]
struct ReferenceOrigins {
    origins: HashMap<String, Origin>,
}

impl ReferenceOrigins {
    fn new(parse_tree: &CloudformationParseTree) -> Self {
        let mut origins = HashMap::default();

        origins.extend(
            parse_tree
                .parameters
                .iter()
                .map(|(name, _)| (name.clone(), Origin::Parameter)),
        );

        origins.extend(
            parse_tree
                .resources
                .iter()
                .map(|(name, _)| (name.clone(), Origin::LogicalId)),
        );

        Self { origins }
    }

    fn for_ref(&self, ref_name: &str) -> Option<Origin> {
        if let Some(pseudo) = PseudoParameter::try_from(ref_name) {
            Some(Origin::PseudoParameter(pseudo))
        } else {
            self.origins.get(ref_name).cloned()
        }
    }
}
