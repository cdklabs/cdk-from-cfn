use indexmap::IndexMap;

use crate::parser::resource::ResourceAttributes;
use crate::TransmuteError;
use std::collections::HashSet;

// ImportInstruction look something like:
// import * as $name from '$path[0]/$path[1]...';
// which should account for many import styles.
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ImportInstruction {
    pub organization: String,
    pub service: Option<String>,
}

impl ImportInstruction {
    pub(super) fn from(
        parse_tree: &IndexMap<String, ResourceAttributes>,
    ) -> Result<Vec<Self>, TransmuteError> {
        let mut type_names = HashSet::new();
        for (_, resource) in parse_tree {
            let type_name = &resource.resource_type;

            let (organization, service, _) = if let Some(triple) =
                type_name.split_once("::").and_then(|(organization, rest)| {
                    rest.split_once("::")
                        .map(|(service, resource)| (organization, service, resource))
                }) {
                triple
            } else {
                return Err(TransmuteError::new(format!(
                    "invalid resource type name: {type_name}"
                )));
            };

            type_names.insert(TypeName {
                organization: organization.to_string(),
                service: Some(service.to_string()),
            });
        }

        let mut import_instructions = vec![ImportInstruction {
            organization: "AWS".to_string(),
            service: None,
        }];

        import_instructions.reserve(type_names.len());
        for type_name in &type_names {
            import_instructions.push(ImportInstruction {
                organization: type_name.organization.clone(),
                service: type_name.service.clone(),
            })
        }

        import_instructions.sort_by(|left, right| left.service.cmp(&right.service));

        Ok(import_instructions)
    }
}

#[derive(Clone, Debug, Hash, PartialEq, Eq, PartialOrd)]
struct TypeName {
    organization: String,
    service: Option<String>,
}
