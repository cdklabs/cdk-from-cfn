use serde::de::Error;

#[test]
fn test_import_instruction_error() {
    let error = crate::Error::ImportInstructionError {
        message: "Import instruction error".to_string(),
    };
    assert_eq!(error.to_string(), "Import instruction error");
}

#[test]
fn test_resource_translation_error() {
    let error = crate::Error::ResourceTranslationError {
        message: "Resource instruction error".to_string(),
    };
    assert_eq!(error.to_string(), "Resource instruction error");
}

#[test]
fn test_sub_parse_error() {
    let error = crate::Error::SubParseError {
        message: "Sub parse error".to_string(),
    };
    assert_eq!(error.to_string(), "Sub parse error");
}

#[test]
fn test_resource_instruction_error() {
    let error = crate::Error::ResourceInstructionError {
        message: "Resource instruction error".to_string(),
    };
    assert_eq!(error.to_string(), "Resource instruction error");
}

#[test]
fn test_resource_type_error() {
    let error = crate::Error::ResourceTypeError {
        message: "Resource type error".to_string(),
    };
    assert_eq!(error.to_string(), "Resource type error");
}

#[test]
fn test_yaml_parse_error() {
    let yaml_error = serde_yaml::Error::custom("YAML parsing error");
    let transmute_error: crate::Error = yaml_error.into();

    assert_eq!(transmute_error.to_string(), "YAML parsing error");
}
