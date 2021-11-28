use crate::CloudformationParseTree;
use std::collections::HashSet;

pub struct Importer {
    type_names: HashSet<TypeName>,
}

impl Importer {
    pub fn translate(parse_tree: &CloudformationParseTree) -> Vec<ImportInstruction> {
        let mut type_names = HashSet::new();
        for resource in parse_tree.resources.resources.iter() {
            let name = &resource.resource_type;
            let mut split_ref = name.split("::");

            // These must always exist.
            // In CloudFormation, typenames are always of the form `<Organization>::<Service>::<Resource>
            let organization = split_ref.next().unwrap().to_ascii_lowercase();
            let service = split_ref.next().unwrap().to_ascii_lowercase();
            let type_name = TypeName {
                organization,
                service,
            };
            type_names.insert(type_name);
        }

        let mut import_instructions: Vec<ImportInstruction> = vec![
            // We will always include the cdk, as it's used to build the stack.
            ImportInstruction {
                name: "cdk".to_string(),
                path: vec!["aws-cdk-lib".to_string()],
            },
        ];

        for type_name in type_names.iter() {
            import_instructions.push(ImportInstruction {
                name: type_name.service.to_string(),
                path: vec![
                    "aws-cdk-lib".to_string(),
                    format!("{}-{}", type_name.organization, type_name.service).to_string(),
                ],
            })
        }

        import_instructions
    }
}

// ImportInstruction look something like:
// import * as $name from '$path[0]/$path[1]...';
// which should account for many import styles.
#[derive(PartialEq, PartialOrd, Clone, Debug)]
pub struct ImportInstruction {
    pub name: String,
    pub path: Vec<String>,
}

#[derive(PartialEq, PartialOrd, Clone, Debug, Eq, Hash)]
struct TypeName {
    organization: String,
    service: String,
}
