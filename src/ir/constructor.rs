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
        let mut inputs = Vec::new();
        for (name, param) in parse_tree.parameters.params.iter() {
            inputs.push(ConstructorParameter {
                name: camel_case(name),
                constructor_type: param.parameter_type.to_string(),
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
    pub constructor_type: String,
}
