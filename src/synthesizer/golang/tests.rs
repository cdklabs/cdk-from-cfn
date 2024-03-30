use indexmap::IndexMap;

use super::*;

use std::borrow::Cow;

use crate::cdk::Schema;
use crate::code::CodeBuffer;
use crate::ir::conditions::ConditionIr;
use crate::ir::importer::ImportInstruction;
use crate::primitives::WrapperF64;

use super::GolangEmitter;

#[test]
fn test_invalid_organization() {
    let bad_org = "NotAws";
    let import_instruction = ImportInstruction {
        organization: bad_org.to_string(),
        service: Option::None,
    };
    let result = import_instruction.to_golang().unwrap_err();
    let expected = format!("Expected organization to be AWS or Alexa. Found {bad_org}");
    assert_eq!(expected, result.to_string());
}

#[test]
fn test_alexa_organization() {
    let import_instruction = ImportInstruction {
        organization: "Alexa".to_string(),
        service: Some("service".to_string()),
    };
    let result = import_instruction.to_golang();
    assert_eq!(
        "service \"github.com/aws/aws-cdk-go/awscdk/v2/alexaservice\"",
        result.unwrap()
    );
}

#[test]
fn test_condition_ir_map() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let condition_ir = ConditionIr::Map(
        "ConditionIrMap".to_string(),
        Box::new(ConditionIr::Str("key".to_string())),
        Box::new(ConditionIr::Str("value".to_string())),
    );
    let context = &mut GoContext::new(
        &schema,
        output.section(false),
        output.section(false),
        output.section(false),
        output.section(false),
    );
    let result = condition_ir.emit_golang(context, &output, Some(","));
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_double() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Double(WrapperF64::new(2.0));
    let context = &mut GoContext::new(
        &schema,
        output.section(false),
        output.section(false),
        output.section(false),
        output.section(false),
    );
    let result = resource_ir.emit_golang(context, &output, Some(","));
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_object_primitive_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Object(
        TypeReference::Primitive(Primitive::Boolean),
        IndexMap::new(),
    );
    let context = &mut GoContext::new(
        &schema,
        output.section(false),
        output.section(false),
        output.section(false),
        output.section(false),
    );
    let result = resource_ir
        .emit_golang(context, &output, Option::None)
        .unwrap_err();
    assert_eq!(
        "Cannot emit ResourceIr::Object with non-json simple structure (Boolean)",
        result.to_string(),
    );
}

#[test]
fn test_resource_ir_object_list_structure() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Object(
        TypeReference::List(ItemType::Static(&TypeReference::Primitive(
            Primitive::Number,
        ))),
        IndexMap::new(),
    );
    let context = &mut GoContext::new(
        &schema,
        output.section(false),
        output.section(false),
        output.section(false),
        output.section(false),
    );
    let result = resource_ir.emit_golang(context, &output, Option::None);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_cidr_null_mask() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Cidr(
        Box::new(ResourceIr::String("0.0.0.0".into())),
        Box::new(ResourceIr::String("16".into())),
        Box::new(ResourceIr::Null),
    );
    let context = &mut GoContext::new(
        &schema,
        output.section(false),
        output.section(false),
        output.section(false),
        output.section(false),
    );
    let result = resource_ir.emit_golang(context, &output, Option::None);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_cidr_string_mask() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Cidr(
        Box::new(ResourceIr::String("0.0.0.0".into())),
        Box::new(ResourceIr::String("16".into())),
        Box::new(ResourceIr::String("255.255.255.0".into())),
    );
    let context = &mut GoContext::new(
        &schema,
        output.section(false),
        output.section(false),
        output.section(false),
        output.section(false),
    );
    let result = resource_ir.emit_golang(context, &output, Option::None);
    assert_eq!((), result.unwrap());
}

fn test_reference_with_trailer() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let context = &mut GoContext::new(
        &schema,
        output.section(false),
        output.section(false),
        output.section(false),
        output.section(false),
    );
    let reference = Reference {
        origin: Origin::Condition {},
        name: "origin".into(),
    };
    let result = reference.emit_golang(context, &output, Some(","));
    assert_eq!((), result.unwrap());
}
