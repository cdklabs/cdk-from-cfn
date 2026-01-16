// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use indexmap::IndexMap;

use super::*;

use std::borrow::Cow;
use std::str::FromStr;

use crate::cdk::Schema;
use crate::code::CodeBuffer;
use crate::ir::conditions::ConditionIr;
use crate::ir::importer::ImportInstruction;
use crate::primitives::WrapperF64;
use crate::synthesizer::ClassType;

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
        ClassType::Stack,
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
        ClassType::Stack,
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
        ClassType::Stack,
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
        ClassType::Stack,
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
        ClassType::Stack,
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
        ClassType::Stack,
    );
    let result = resource_ir.emit_golang(context, &output, Option::None);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_reference_with_trailer() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let context = &mut GoContext::new(
        &schema,
        output.section(false),
        output.section(false),
        output.section(false),
        output.section(false),
        ClassType::Stack,
    );
    let reference = Reference {
        origin: Origin::Condition {},
        name: "origin".into(),
    };
    let result = reference.emit_golang(context, &output, Some(","));
    assert_eq!((), result.unwrap());
}

#[test]
fn test_boolean_primitive() {
    let schema = Cow::Borrowed(Schema::builtin());
    let primitive = Primitive::Boolean;
    let result = primitive.as_golang(&schema);
    assert_eq!(Cow::from("*bool"), result);
}

#[test]
fn test_string_primitive() {
    let schema = Cow::Borrowed(Schema::builtin());
    let primitive = Primitive::String;
    let result = primitive.as_golang(&schema);
    assert_eq!(Cow::from("*string"), result);
}

#[test]
fn test_timestamp_primitive() {
    let schema = Cow::Borrowed(Schema::builtin());
    let primitive = Primitive::Timestamp;
    let result = primitive.as_golang(&schema);
    assert_eq!(Cow::from("*time.Time"), result);
}

#[test]
fn test_json_primitive() {
    let schema = Cow::Borrowed(Schema::builtin());
    let primitive = Primitive::Json;
    let result = primitive.as_golang(&schema);
    assert_eq!(Cow::from("interface{}{"), result);
}

#[test]
fn test_unknown_primitive() {
    let schema = Cow::Borrowed(Schema::builtin());
    let primitive = Primitive::Unknown;
    let result = primitive.as_golang(&schema);
    assert_eq!(Cow::from("cdk.IResolvable"), result);
}

// Class type integration tests
use crate::ir::CloudformationProgramIr;
use crate::CloudformationParseTree;

const SIMPLE_TEMPLATE: &str = r#"{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Description": "Test template",
    "Resources": {
        "MyBucket": {
            "Type": "AWS::S3::Bucket",
            "Properties": {
                "BucketName": {"Fn::Sub": "${AWS::StackName}-bucket"}
            }
        }
    }
}"#;

#[test]
fn test_class_type_stack_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("go", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("cdk.StackProps"),
        "Props should embed cdk.StackProps"
    );
    assert!(code.contains("cdk.Stack"), "Struct should embed cdk.Stack");
    assert!(
        code.contains("cdk.NewStack(scope, &id, &sprops)"),
        "Should use cdk.NewStack"
    );
    assert!(
        code.contains("stack.StackName()"),
        "Should use stack.StackName() for pseudo-params"
    );
}

#[test]
fn test_class_type_construct_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("go", &mut output, "TestConstruct", ClassType::Construct)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        !code.contains("cdk.StackProps"),
        "Props should NOT embed cdk.StackProps"
    );
    assert!(
        code.contains("constructs.Construct"),
        "Struct should embed constructs.Construct"
    );
    assert!(
        code.contains("constructs.NewConstruct(scope, &id)"),
        "Should use constructs.NewConstruct"
    );
    assert!(
        code.contains("cdk.Stack_Of(construct).StackName()"),
        "Should use cdk.Stack_Of(construct) for pseudo-params"
    );
}

const TEMPLATE_WITH_TRANSFORM: &str = r#"{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Transform": "AWS::Serverless-2016-10-31",
    "Resources": {
        "MyBucket": {
            "Type": "AWS::S3::Bucket"
        }
    }
}"#;

#[test]
fn test_add_transform_stack_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(TEMPLATE_WITH_TRANSFORM).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("go", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("stack.AddTransform(jsii.String(\"AWS::Serverless-2016-10-31\"))"),
        "Stack mode should use stack.AddTransform"
    );
}

#[test]
fn test_add_transform_construct_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(TEMPLATE_WITH_TRANSFORM).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("go", &mut output, "TestConstruct", ClassType::Construct)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains(
            "cdk.Stack_Of(construct).AddTransform(jsii.String(\"AWS::Serverless-2016-10-31\"))"
        ),
        "Construct mode should use cdk.Stack_Of(stack).AddTransform"
    );
}

#[test]
fn test_class_type_default_is_stack() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("go", &mut output, "TestStack", ClassType::default())
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("cdk.NewStack"),
        "Default should use cdk.NewStack"
    );
}

#[test]
fn test_class_type_from_str_valid() {
    assert_eq!(ClassType::from_str("stack").unwrap(), ClassType::Stack);
    assert_eq!(
        ClassType::from_str("construct").unwrap(),
        ClassType::Construct
    );
}

#[test]
fn test_class_type_from_str_invalid() {
    let result = ClassType::from_str("invalid");
    assert!(result.is_err());
    assert_eq!(
        result.unwrap_err(),
        "Invalid class type: 'invalid'. Expected 'stack' or 'construct'"
    );
}
