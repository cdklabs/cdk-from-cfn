use crate::{parser::parameters::Parameter, Hasher};
use indexmap::IndexMap;
use voca_rs::case::camel_case;

#[derive(Debug, Default)]
pub struct Constructor {
    pub inputs: Vec<ConstructorParameter>,
}

impl Constructor {
    pub(super) fn from(parse_tree: IndexMap<String, Parameter, Hasher>) -> Self {
        Self {
            inputs: parse_tree
                .into_iter()
                .map(|(name, param)| ConstructorParameter {
                    name: camel_case(&name),
                    description: param.description,
                    constructor_type: match param.parameter_type {
                        crate::parser::parameters::ParameterType::String => {
                            if param.allowed_values.is_some() {
                                let values = param.allowed_values.clone().unwrap();
                                if values.len() == 2 {
                                    if (values[0].to_lowercase() == "true"
                                        && values[1].to_lowercase() == "false")
                                        || (values[0].to_lowercase() == "false"
                                            && values[1].to_lowercase() == "true")
                                    {
                                        crate::parser::parameters::ParameterType::Bool.to_string()
                                    } else {
                                        param.parameter_type.to_string()
                                    }
                                } else {
                                    param.parameter_type.to_string()
                                }
                            } else {
                                param.parameter_type.to_string()
                            }
                        }
                        _ => param.parameter_type.to_string(),
                    },
                    default_value: param.default,
                    allowed_values: param.allowed_values,
                    no_echo: param.no_echo,
                })
                .collect(),
        }
    }
}

#[derive(Debug, Default)]
pub struct ConstructorParameter {
    pub name: String,
    pub description: Option<String>,
    pub constructor_type: String,
    pub default_value: Option<String>,
    pub allowed_values: Option<Vec<String>>,
    pub no_echo: Option<String>,
}

#[cfg(test)]
mod tests;
