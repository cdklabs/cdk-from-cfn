use crate::parser::parameters::Parameter;
use indexmap::IndexMap;
use voca_rs::case::camel_case;

pub struct Constructor {
    pub inputs: Vec<ConstructorParameter>,
}

impl Constructor {
    pub(super) fn from<S>(parse_tree: IndexMap<String, Parameter, S>) -> Self {
        Self {
            inputs: parse_tree
                .into_iter()
                .map(|(name, param)| ConstructorParameter {
                    name: camel_case(&name),
                    description: param.description,
                    constructor_type: param.parameter_type.to_string(),
                    default_value: param.default,
                })
                .collect(),
        }
    }
}

pub struct ConstructorParameter {
    pub name: String,
    pub description: Option<String>,
    pub constructor_type: String,
    pub default_value: Option<String>,
}

#[cfg(test)]
mod tests;
