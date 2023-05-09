use std::fmt;

#[derive(Debug, PartialEq, serde::Deserialize)]
#[serde(rename_all = "PascalCase")]
pub struct Parameter {
    pub allowed_values: Option<Vec<String>>,
    pub default: Option<String>,
    pub description: Option<String>,
    #[serde(rename = "Type")]
    pub parameter_type: ParameterType,
}

#[derive(Clone, Debug, PartialEq, serde_enum_str::Deserialize_enum_str)]
pub enum ParameterType {
    String,
    Number,
    #[serde(rename = "List<Number>")]
    ListOfNumbers,
    CommaDelimitedList,
    #[serde(other)]
    Other(String),
}

impl fmt::Display for ParameterType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            ParameterType::String => write!(f, "String"),
            ParameterType::Number => write!(f, "Number"),
            ParameterType::ListOfNumbers => write!(f, "List<Number>"),
            ParameterType::CommaDelimitedList => write!(f, "CommaDelimitedList"),
            ParameterType::Other(s) => write!(f, "{}", s),
        }
    }
}
        
#[cfg(test)]
mod tests {
    use super::*;
    use serde_yaml::Mapping;

    #[test]
    fn test_add_parameter() {
        let mut params = Parameters::new();
        params.add(Parameter::new(
            "p1".to_string(),
            "Number".to_string(),
            Option::from("0".to_string()),
        ));
        let result: &Parameter = params.params.get("p1").unwrap();
        assert_eq!(result.logical_name, "p1".to_string());
        assert_eq!(result.default, Option::from("0".to_string()));
        assert_eq!(result.parameter_type, "Number".to_string());
    }

    #[test]
    fn test_build_parameters() {
        let yaml_text = r#"
        Param1:
            Type: String
        Param2:
            Type: Number
            Default: "0"
          "#;

        let map: Mapping = serde_yaml::from_str(&yaml_text).unwrap();
        let params = build_parameters(&map).unwrap();

        assert_eq!(
            params,
            Parameters {
                params: {
                    let mut map = HashMap::new();
                    map.insert(
                        "Param1".into(),
                        Parameter::new("Param1".into(), "String".into(), None),
                    );
                    map.insert(
                        "Param2".into(),
                        Parameter::new("Param2".into(), "Number".into(), Some("0".into())),
                    );
                    map
                }
            }
        );
    }
}
