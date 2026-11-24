// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use std::collections::HashMap;

use crate::cdk::Schema;
use crate::ir::conditions::ConditionInstruction;
use crate::ir::constructor::Constructor;
use crate::ir::importer::ImportInstruction;
use crate::ir::mappings::MappingInstruction;
use crate::ir::outputs::OutputInstruction;
use crate::ir::resources::ResourceInstruction;
use crate::parser::resource::ResourceValue;
use crate::{CloudformationParseTree, Error};

use self::reference::{Origin, PseudoParameter};

const CDK_METADATA_RESOURCE_TYPE: &str = "AWS::CDK::Metadata";
const CDK_METADATA_AVAILABLE_CONDITION: &str = "CDKMetadataAvailable";
const CDK_PATH_METADATA_KEY: &str = "aws:cdk:path";
const BOOTSTRAP_VERSION_PARAMETER: &str = "BootstrapVersion";
const CDK_SKIP_MARKER: &str = "[cdk:skip]";
const CHECK_BOOTSTRAP_VERSION_RULE: &str = "CheckBootstrapVersion";

pub mod conditions;
pub mod constructor;
pub mod importer;
pub mod mappings;
pub mod outputs;
pub mod reference;
pub mod resources;
pub mod sub;

#[derive(Debug, Default)]
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
        mut parse_tree: CloudformationParseTree,
        schema: &Schema,
    ) -> Result<CloudformationProgramIr, Error> {
        strip_cdk_generated_elements(&mut parse_tree);
        let origins = ReferenceOrigins::new(&parse_tree);

        Ok(CloudformationProgramIr {
            description: parse_tree.description,
            transforms: parse_tree.transforms,
            conditions: ConditionInstruction::from(parse_tree.conditions)?,
            imports: ImportInstruction::from(&parse_tree.resources)?,
            constructor: Constructor::from(parse_tree.parameters),
            mappings: MappingInstruction::from(parse_tree.mappings),
            resources: ResourceInstruction::from(parse_tree.resources, schema, &origins)?,
            outputs: OutputInstruction::from(parse_tree.outputs, schema, &origins)?,
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

        origins.extend(parse_tree.parameters.iter().map(|(name, param)| {
            if param
                .no_echo
                .as_ref()
                .is_some_and(|x| x.to_lowercase() == "true")
            {
                (name.clone(), Origin::CfnParameter)
            } else {
                (name.clone(), Origin::Parameter)
            }
        }));

        origins.extend(parse_tree.resources.iter().map(|(name, res)| {
            let is_custom_resource = res.resource_type.starts_with("Custom::")
                || res.resource_type == "AWS::CloudFormation::CustomResource";
            (
                name.clone(),
                Origin::LogicalId {
                    conditional: res.condition.is_some(),
                    is_custom_resource,
                },
            )
        }));

        Self { origins }
    }

    fn for_ref(&self, ref_name: &str) -> Option<Origin> {
        if let Some(pseudo) = PseudoParameter::try_from(ref_name) {
            Some(Origin::PseudoParameter(pseudo))
        } else {
            self.origins.get(ref_name).cloned()
        }
    }

    fn is_conditional(&self, logical_id: &str) -> bool {
        self.for_ref(logical_id)
            .map(|orig| match orig {
                Origin::LogicalId { conditional, .. } => conditional,
                _ => false,
            })
            .unwrap_or(false)
    }

    fn is_custom_resource(&self, logical_id: &str) -> bool {
        self.for_ref(logical_id)
            .map(|orig| match orig {
                Origin::LogicalId {
                    is_custom_resource, ..
                } => is_custom_resource,
                _ => false,
            })
            .unwrap_or(false)
    }
}

/// Removes CDK-synthesizer-generated elements from a CloudFormation parse tree
/// before translating it into IR, logging a skip message to stderr for each
/// removed element so the target CDK app's own synthesizer can manage them.
fn strip_cdk_generated_elements(parse_tree: &mut CloudformationParseTree) {
    let skip_bootstrap_param = parse_tree
        .parameters
        .get(BOOTSTRAP_VERSION_PARAMETER)
        .and_then(|param| param.description.as_deref())
        .is_some_and(|desc| desc.trim_end().ends_with(CDK_SKIP_MARKER));
    if skip_bootstrap_param {
        parse_tree
            .parameters
            .shift_remove(BOOTSTRAP_VERSION_PARAMETER);
        eprintln!("Skipping CDK-generated parameter '{BOOTSTRAP_VERSION_PARAMETER}'.");
    }

    if parse_tree
        .rules
        .shift_remove(CHECK_BOOTSTRAP_VERSION_RULE)
        .is_some()
    {
        eprintln!("Skipping CDK-generated rule '{CHECK_BOOTSTRAP_VERSION_RULE}'.");
    }

    if parse_tree
        .conditions
        .shift_remove(CDK_METADATA_AVAILABLE_CONDITION)
        .is_some()
    {
        eprintln!("Skipping CDK-generated condition '{CDK_METADATA_AVAILABLE_CONDITION}'.");
    }

    parse_tree.resources.retain(|name, attrs| {
        if attrs.resource_type == CDK_METADATA_RESOURCE_TYPE {
            eprintln!(
                "Skipping CDK-generated resource '{name}' of type '{CDK_METADATA_RESOURCE_TYPE}'."
            );
            return false;
        }

        if let Some(ResourceValue::Object(metadata)) = &mut attrs.metadata {
            if metadata.shift_remove(CDK_PATH_METADATA_KEY).is_some() {
                eprintln!(
                    "Skipping CDK-generated metadata '{CDK_PATH_METADATA_KEY}' on resource '{name}'."
                );
            }
            if metadata.is_empty() {
                attrs.metadata = None;
            }
        }

        true
    });
}

#[cfg(test)]
mod tests;
