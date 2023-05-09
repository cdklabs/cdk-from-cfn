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
mod tests {
    use super::*;

    use crate::parser;
    use parser::parameters::ParameterType;

    #[test]
    fn test_constructor_from() {
        let mut parse_tree = IndexMap::new();
        parse_tree.insert(
            "param1".to_string(),
            Parameter {
                allowed_values: None,
                default: Some("default1".to_string()),
                description: Some("description1".to_string()),
                parameter_type: ParameterType::String,
            },
        );
        parse_tree.insert(
            "param2".to_string(),
            Parameter {
                allowed_values: None,
                default: None,
                description: Some("description2".to_string()),
                parameter_type: ParameterType::Number,
            },
        );

        let constructor = Constructor::from(parse_tree);

        assert_eq!(constructor.inputs.len(), 2);

        assert_eq!(constructor.inputs[0].name, "param1");
        assert_eq!(
            constructor.inputs[0].description,
            Some("description1".to_string())
        );
        assert_eq!(constructor.inputs[0].constructor_type, "String");
        assert_eq!(
            constructor.inputs[0].default_value,
            Some("default1".to_string())
        );

        assert_eq!(constructor.inputs[1].name, "param2");
        assert_eq!(
            constructor.inputs[1].description,
            Some("description2".to_string())
        );
        assert_eq!(constructor.inputs[1].constructor_type, "Number");
        assert_eq!(constructor.inputs[1].default_value, None);
    }

    #[test]
    fn test_constructor_parameter() {
        let param = ConstructorParameter {
            name: "Param1".to_string(),
            description: Some("description1".to_string()),
            constructor_type: "String".to_string(),
            default_value: Some("default1".to_string()),
        };

        assert_eq!(param.name, "Param1");
        assert_eq!(param.description, Some("description1".to_string()));
        assert_eq!(param.constructor_type, "String");
        assert_eq!(param.default_value, Some("default1".to_string()));
    }
}
