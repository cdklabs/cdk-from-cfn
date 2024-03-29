use std::borrow::Cow;

use indexmap::IndexMap;

use crate::{
    cdk::{Primitive, Schema, TypeReference, TypeUnion},
    code::CodeBuffer,
    ir::{conditions::ConditionIr, importer::ImportInstruction, resources::ResourceIr},
    primitives::WrapperF64,
};

use super::CsharpEmitter;

#[test]
fn test_fn_split() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Split(
        "-".into(),
        Box::new(ResourceIr::String("My-EC2-Instance".into())),
    );
    let result = resource_ir.emit_csharp(&output, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_fn_split_other() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Split(
        "-".into(),
        Box::new(ResourceIr::Join(
            ",".to_string(),
            vec![
                ResourceIr::String("a".into()),
                ResourceIr::String("b".into()),
                ResourceIr::String("c".into()),
            ],
        )),
    );
    let result = resource_ir.emit_csharp(&output, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_condition_ir_map() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let condition_ir = ConditionIr::Map(
        "ConditionIrMap".into(),
        Box::new(ConditionIr::Str("FirstLevelKey".into())),
        Box::new(ConditionIr::Str("SecondLevelKey".into())),
    );
    let result = condition_ir.emit_csharp(&output, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_condition_ir_split() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let condition_ir = ConditionIr::Split(
        "-".into(),
        Box::new(ConditionIr::Str("string-to-split".into())),
    );
    let result = condition_ir.emit_csharp(&output, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_alexa_org() {
    let import_instruction = ImportInstruction {
        organization: "Alexa".into(),
        service: Some("Ask".into()),
    };
    let result = import_instruction.to_csharp();
    assert_eq!("using Amazon.CDK.Alexa.Ask;", result.unwrap());
}

#[test]
fn test_resource_ir_double() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Double(WrapperF64::new(2.0));
    let result = resource_ir.emit_csharp(&output, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_select() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir =
        ResourceIr::Select(1, Box::new(ResourceIr::String("Not an array".into())));
    let result = resource_ir.emit_csharp(&output, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_cidr() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Cidr(
        Box::new(ResourceIr::String("0.0.0.0".into())),
        Box::new(ResourceIr::String("16".into())),
        Box::new(ResourceIr::String("255.255.255.0".into())),
    );
    let result = resource_ir.emit_csharp(&output, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_invalid_resource_object_structure() {
  let output = CodeBuffer::default();
  let schema = Cow::Borrowed(Schema::builtin());
  let resource_ir = ResourceIr::Object(
    TypeReference::Union(TypeUnion::Static(&[])),
    IndexMap::default(),
  );
  let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
  let expected = "Type reference Union(\n    Static(\n        [],\n    ),\n) not implemented for ResourceIr::Object";
  assert_eq!(expected, result.to_string());
}

#[test]
fn test_invalid_resource_object_primitive() {
  let output = CodeBuffer::default();
  let schema = Cow::Borrowed(Schema::builtin());
  let resource_ir = ResourceIr::Object(
    TypeReference::Primitive(Primitive::String),
    IndexMap::default(),
  );
  let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
  let expected = "Cannot emit ResourceIr::Object with non-json simple structure (String)";
  assert_eq!(expected, result.to_string());
}

#[test]
fn test_invalid_organization() {
  let bad_org = "NotAws";
  let import_instruction = ImportInstruction {
    organization: bad_org.to_string(),
    service: Option::None,
  };
  let result = import_instruction.to_csharp().unwrap_err();
  let expected = format!("Expected organization to be AWS or Alexa. Found {bad_org}");
  assert_eq!(expected, result.to_string());
}
