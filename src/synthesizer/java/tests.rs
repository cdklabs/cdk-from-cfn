use indexmap::IndexMap;

use super::*;

use std::borrow::Cow;

use crate::cdk::{Schema, TypeUnion};
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

#[test]
fn test_tag_value_resource_ir_bool() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Bool(true);
    let result = emit_tag_value(resource_ir, &output, Option::None, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_tag_value_resource_ir_double() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Double(WrapperF64::new(2.0));
    let result = emit_tag_value(resource_ir, &output, Option::None, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_tag_value_resource_ir_number() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Number(10);
    let result = emit_tag_value(resource_ir, &output, Option::None, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_object_type_reference_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Object(
        TypeReference::Union(TypeUnion::Static(&[])),
        IndexMap::new(),
    );
    let result = emit_tag_value(resource_ir, &output, Option::None, &schema).unwrap_err();
    assert_eq!(
        "Type reference Union(\n    Static(\n        [],\n    ),\n) not implemented for ResourceIr::Object",
        result.to_string(),
    );
}

#[test]
fn test_resource_ir_select_idx_greater_than_list_len() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let named_type = TypeReference::Named("AWS::Service::Resource".into());
    let resource_ir = ResourceIr::Select(
        1,
        Box::new(ResourceIr::Array(
            TypeReference::List(ItemType::Boxed(Box::new(named_type))),
            vec![],
        )),
    );
    let result = emit_java(resource_ir, &output, Option::None, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_split_non_string() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Split(
        "-".to_string(),
        Box::new(ResourceIr::Null),
    );
    let result = emit_java(resource_ir, &output, Option::None, &schema);
    assert_eq!((), result.unwrap());
}
