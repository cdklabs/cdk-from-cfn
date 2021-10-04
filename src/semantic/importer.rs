use crate::CloudformationParseTree;
use std::collections::HashSet;

pub struct Importer {
    type_names: HashSet<TypeName>,
}

impl Importer {
    pub fn new(parse_tree: &CloudformationParseTree) -> Importer {
        let mut type_names = HashSet::new();
        for resource in parse_tree.resources.resources.iter() {
            let type_name = TypeName::new(&resource.resource_type);
            type_names.insert(type_name);
        }

        Importer { type_names }
    }

    pub fn synthesize(&self) -> Vec<String> {
        self.type_names.iter().map(|x| x.synthesize()).collect()
    }
}

#[derive(PartialEq, PartialOrd, Clone, Debug, Eq, Hash)]
struct TypeName {
    organization: String,
    service: String,
}

impl TypeName {
    // In CloudFormation, typenames are always of the form `<Organization>::<Service>::<Resource>
    fn new(name: &str) -> TypeName {
        let mut split_ref = name.split("::");

        // These must always exist.
        let organization = split_ref.next().unwrap().to_ascii_lowercase();
        let service = split_ref.next().unwrap().to_ascii_lowercase();

        TypeName {
            organization,
            service,
        }
    }
    fn synthesize(&self) -> String {
        return format!(
            "import * as {} from '@aws-cdk/{}-{}';",
            self.service, self.organization, self.service
        );
    }
}
