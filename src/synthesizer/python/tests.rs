use crate::ir::{conditions::ConditionIr, importer::ImportInstruction};

use super::synthesize_condition_recursive;

#[test]
fn test_invalid_organization() {
    let bad_org = "NotAws";
    let import_instruction = ImportInstruction {
        organization: bad_org.to_string(),
        service: Option::None,
    };
    let result = import_instruction.to_python().unwrap_err();
    let expected = format!("Expected organization to be AWS or Alexa. Found {bad_org}");
    assert_eq!(expected, result.to_string());
}

#[test]
fn test_alexa_org() {
    let import_instruction = ImportInstruction {
        organization: "Alexa".into(),
        service: Some("Ask".into()),
    };
    let result = import_instruction.to_python();
    assert_eq!("import alexa_ask as ask from ask", result.unwrap());
}

#[test]
fn test_condition_ir_not_simple() {
    let condition_ir = ConditionIr::Not(
        Box::new(ConditionIr::Condition("condition".into())),
    );
    let result = synthesize_condition_recursive(&condition_ir);
    assert_eq!("not (condition)", result);
}
