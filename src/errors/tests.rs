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
    let error: crate::Error = yaml_error.into();
    assert_eq!(error.to_string(), "YAML parsing error");
}

#[test]
fn test_unsupported_language_error() {
    let error = crate::Error::UnsupportedLanguageError {
        language: "php".to_string(),
    };
    assert_eq!(error.to_string(), "php is not a supported language");
}

#[test]
fn test_type_reference_error() {
    let error = crate::Error::TypeReferenceError {
        message: "Type reference error".to_string(),
    };
    assert_eq!(error.to_string(), "Type reference error");
}

#[test]
fn test_primitive_error() {
    let error = crate::Error::PrimitiveError {
        message: "Primitive error".to_string(),
    };
    assert_eq!(error.to_string(), "Primitive error");
}
