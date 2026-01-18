// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use indexmap::IndexMap;

use super::*;

use std::borrow::Cow;
use std::str::FromStr;

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
    let result = emit_java(
        resource_ir,
        &output,
        Option::None,
        &schema,
        ClassType::Stack,
    );
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_number() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Number(10);
    let result = emit_java(
        resource_ir,
        &output,
        Option::None,
        &schema,
        ClassType::Stack,
    );
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_double() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Double(WrapperF64::new(2.0));
    let result = emit_java(
        resource_ir,
        &output,
        Option::None,
        &schema,
        ClassType::Stack,
    );
    assert_eq!((), result.unwrap());
}

#[test]
fn test_tag_value_resource_ir_bool() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Bool(true);
    let result = emit_tag_value(
        resource_ir,
        &output,
        Option::None,
        &schema,
        ClassType::Stack,
    );
    assert_eq!((), result.unwrap());
}

#[test]
fn test_tag_value_resource_ir_double() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Double(WrapperF64::new(2.0));
    let result = emit_tag_value(
        resource_ir,
        &output,
        Option::None,
        &schema,
        ClassType::Stack,
    );
    assert_eq!((), result.unwrap());
}

#[test]
fn test_tag_value_resource_ir_number() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Number(10);
    let result = emit_tag_value(
        resource_ir,
        &output,
        Option::None,
        &schema,
        ClassType::Stack,
    );
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
    let result = emit_tag_value(
        resource_ir,
        &output,
        Option::None,
        &schema,
        ClassType::Stack,
    )
    .unwrap_err();
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
    let result = emit_java(
        resource_ir,
        &output,
        Option::None,
        &schema,
        ClassType::Stack,
    );
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_split_non_string() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Split("-".to_string(), Box::new(ResourceIr::Null));
    let result = emit_java(
        resource_ir,
        &output,
        Option::None,
        &schema,
        ClassType::Stack,
    );
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
    let result = emit_java(
        resource_ir,
        &output,
        Option::None,
        &schema,
        ClassType::Stack,
    );
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
    let result = emit_java(
        resource_ir,
        &output,
        Option::None,
        &schema,
        ClassType::Stack,
    );
    assert_eq!((), result.unwrap());
}

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
    ir.synthesize("java", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("class TestStack extends Stack"),
        "Should extend Stack"
    );
    assert!(
        code.contains("this.getStackName()"),
        "Should use this.getStackName() for pseudo-params"
    );
}

#[test]
fn test_class_type_construct_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("java", &mut output, "TestConstruct", ClassType::Construct)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("class TestConstruct extends Construct"),
        "Should extend Construct"
    );
    assert!(
        code.contains("super(scope, id);"),
        "Should call super without props"
    );
    assert!(
        code.contains("Stack.of(this).getStackName()"),
        "Should use Stack.of(this) for pseudo-params"
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
    ir.synthesize("java", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("this.addTransform(\"AWS::Serverless-2016-10-31\")"),
        "Stack mode should use this.addTransform"
    );
}

#[test]
fn test_add_transform_construct_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(TEMPLATE_WITH_TRANSFORM).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("java", &mut output, "TestConstruct", ClassType::Construct)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("Stack.of(this).addTransform(\"AWS::Serverless-2016-10-31\")"),
        "Construct mode should use Stack.of(this).addTransform"
    );
}

#[test]
fn test_class_type_default_is_stack() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("java", &mut output, "TestStack", ClassType::default())
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("extends Stack"),
        "Default should extend Stack"
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

const TEMPLATE_WITH_PARAMS: &str = r#"{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Parameters": {
        "BucketName": {
            "Type": "String",
            "Default": "my-bucket"
        },
        "EnableVersioning": {
            "Type": "String",
            "Default": "false"
        }
    },
    "Resources": {
        "MyBucket": {
            "Type": "AWS::S3::Bucket",
            "Properties": {
                "BucketName": {"Ref": "BucketName"}
            }
        }
    }
}"#;

#[test]
fn test_construct_mode_with_props() {
    let cfn: CloudformationParseTree = serde_json::from_str(TEMPLATE_WITH_PARAMS).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("java", &mut output, "TestConstruct", ClassType::Construct)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    // Should extend Construct
    assert!(
        code.contains("class TestConstruct extends Construct"),
        "Should extend Construct"
    );

    // Should have no-args constructor that delegates
    assert!(
        code.contains("public TestConstruct(final Construct scope, final String id) {"),
        "Should have no-args constructor"
    );
    assert!(
        code.contains("this(scope, id, null, null);"),
        "No-args constructor should delegate with nulls for each prop"
    );

    // Should have constructor with props
    assert!(
        code.contains("public TestConstruct(final Construct scope, final String id,"),
        "Should have props constructor signature"
    );
    assert!(
        code.contains("String bucketName"),
        "Should have bucketName parameter"
    );
    assert!(
        code.contains("String enableVersioning"),
        "Should have enableVersioning parameter"
    );

    // Props constructor should call super(scope, id) without StackProps
    let super_calls: Vec<_> = code.match_indices("super(scope, id);").collect();
    assert!(
        !super_calls.is_empty(),
        "Props constructor should call super(scope, id)"
    );
}

#[test]
fn test_stack_mode_with_props() {
    let cfn: CloudformationParseTree = serde_json::from_str(TEMPLATE_WITH_PARAMS).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("java", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    // Should extend Stack
    assert!(
        code.contains("class TestStack extends Stack"),
        "Should extend Stack"
    );

    // Should have StackProps in constructor
    assert!(
        code.contains("final StackProps props"),
        "Stack mode should have StackProps parameter"
    );

    // Should call super with props
    assert!(
        code.contains("super(scope, id, props);"),
        "Stack mode should call super with props"
    );
}
