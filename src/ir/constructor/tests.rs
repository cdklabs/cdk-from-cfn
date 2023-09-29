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
    assert_eq!(constructor.inputs[0].allowed_values, None);

    assert_eq!(constructor.inputs[1].name, "param2");
    assert_eq!(
        constructor.inputs[1].description,
        Some("description2".to_string())
    );
    assert_eq!(constructor.inputs[1].constructor_type, "Number");
    assert_eq!(constructor.inputs[1].default_value, None);
    assert_eq!(constructor.inputs[1].allowed_values, None);
}

#[test]
fn test_constructor_parameter() {
    let param = ConstructorParameter {
        name: "Param1".to_string(),
        description: Some("description1".to_string()),
        constructor_type: "String".to_string(),
        default_value: Some("default1".to_string()),
        allowed_values: Some(vec!["true".to_string(), "false".to_string()]),
    };

    assert_eq!(param.name, "Param1");
    assert_eq!(param.description, Some("description1".to_string()));
    assert_eq!(param.constructor_type, "String");
    assert_eq!(param.default_value, Some("default1".to_string()));
    assert_eq!(
        param.allowed_values,
        Some(vec!["true".to_string(), "false".to_string()])
    );
}
