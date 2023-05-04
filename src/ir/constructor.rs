use crate::CloudformationParseTree;
use voca_rs::case::camel_case;

pub struct Constructor {
    pub inputs: Vec<ConstructorParameter>,
}

impl Constructor {
    pub fn new() -> Constructor {
        Constructor { inputs: Vec::new() }
    }

    pub fn translate(parse_tree: &CloudformationParseTree) -> Constructor {
        let mut inputs = Vec::with_capacity(parse_tree.parameters.len());
        for (name, param) in &parse_tree.parameters {
            let default: Option<&String> = param.default.as_ref();
            inputs.push(ConstructorParameter {
                name: camel_case(name),
                description: param.description.clone(),
                constructor_type: param.parameter_type.to_string(),
                default_value: default.map(|v| v.to_string()),
            })
        }
        Constructor { inputs }
    }
}
impl Default for Constructor {
    fn default() -> Self {
        Self::new()
    }
}

pub struct ConstructorParameter {
    pub name: String,
    pub description: Option<String>,
    pub constructor_type: String,
    pub default_value: Option<String>,
}
