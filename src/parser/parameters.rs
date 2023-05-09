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
    
    #[test]
    fn test_parameter_type_display() {
        assert_eq!(ParameterType::String.to_string(), "String");
        assert_eq!(ParameterType::Number.to_string(), "Number");
        assert_eq!(ParameterType::ListOfNumbers.to_string(), "List<Number>");
        assert_eq!(ParameterType::CommaDelimitedList.to_string(), "CommaDelimitedList");
        assert_eq!(ParameterType::Other("CustomType".to_string()).to_string(), "CustomType");
    }
}
