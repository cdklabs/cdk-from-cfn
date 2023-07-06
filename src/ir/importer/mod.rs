use indexmap::IndexMap;

use crate::parser::resource::ResourceAttributes;
use crate::TransmuteError;
use std::collections::HashSet;

// ImportInstruction look something like:
// import * as $name from '$path[0]/$path[1]...';
// which should account for many import styles.
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ImportInstruction {
    pub name: String,
    pub path: Vec<String>,
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
            // In CloudFormation, custom typenames are always of the form `Custom::<Resource>`
            } else if let Some(double) =
                type_name.split_once("::")
                    .map(|(custom, resource)| (custom, resource, ""))
            {
                double
            } else {
                return Err(TransmuteError::new(format!(
                    "invalid resource type name: {type_name}"
                )));
            };

            // These must always exist.
            // In CloudFormation, typenames are always of the form `<Organization>::<Service>::<Resource>`
            let organization = organization.to_ascii_lowercase();
            let service = service.to_ascii_lowercase();
            type_names.insert(TypeName {
                organization,
                service,
            });
        }

        let mut import_instructions: Vec<ImportInstruction> = vec![
            // We will always include the cdk, as it's used to build the stack.
            ImportInstruction {
                name: "cdk".to_string(),
                path: vec!["aws-cdk-lib".to_string()],
            },
        ];

        import_instructions.reserve(type_names.len());
        for type_name in &type_names {
            import_instructions.push(ImportInstruction {
                name: type_name.service.to_string(),
                path: vec![
                    "aws-cdk-lib".to_string(),
                    format!("{}-{}", type_name.organization, type_name.service).to_string(),
                ],
            })
        }

        import_instructions.sort_by(|left, right| left.name.cmp(&right.name));

        Ok(import_instructions)
    }
}

#[derive(Clone, Debug, Hash, PartialEq, Eq, PartialOrd)]
struct TypeName {
    organization: String,
    service: String,
}
