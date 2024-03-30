use super::*;

use std::borrow::Cow;

use crate::cdk::Schema;
use crate::code::CodeBuffer;
use crate::ir::importer::ImportInstruction;
use crate::ir::resources::ResourceIr;
use crate::primitives::WrapperF64;

#[test]
fn test_invalid_organization() {
    let bad_org = "NotAws";
    let import_instruction = ImportInstruction {
        organization: bad_org.to_string(),
        service: Option::None,
    };
    let result = import_instruction.to_java_import().unwrap_err();
    let expected = format!("Expected organization to be AWS or Alexa. Found {bad_org}");
    assert_eq!(expected, result.to_string());
}

#[test]
fn test_alexa_organization() {
    let import_instruction = ImportInstruction {
        organization: "Alexa".to_string(),
        service: Some("service".to_string()),
    };
    let result = import_instruction.to_java_import();
    assert_eq!(
        "import software.amazon.awscdk.alexa.service.*;",
        result.unwrap()
    );
}

#[test]
fn test_resource_ir_bool() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Bool(true);
    let result = emit_java(resource_ir, &output, Option::None, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_number() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Number(10);
    let result = emit_java(resource_ir, &output, Option::None, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_double() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Double(WrapperF64::new(2.0));
    let result = emit_java(resource_ir, &output, Option::None, &schema);
    assert_eq!((), result.unwrap());
}
