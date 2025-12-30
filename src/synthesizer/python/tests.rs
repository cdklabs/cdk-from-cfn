// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use crate::cdk::Schema;
use crate::ir::CloudformationProgramIr;
use crate::ir::{conditions::ConditionIr, importer::ImportInstruction};
use crate::synthesizer::StackType;
use crate::CloudformationParseTree;
use std::str::FromStr;

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
    let condition_ir = ConditionIr::Not(Box::new(ConditionIr::Condition("condition".into())));
    let result = synthesize_condition_recursive(&condition_ir, StackType::Stack);
    assert_eq!("not (condition)", result);
}

#[test]
fn test_condition_ir_map() {
    let condition_ir = ConditionIr::Map(
        "ConditionIrMap".into(),
        Box::new(ConditionIr::Str("FirstLevelKey".into())),
        Box::new(ConditionIr::Str("SecondLevelKey".into())),
    );
    let result = synthesize_condition_recursive(&condition_ir, StackType::Stack);
    assert_eq!(
        "condition_ir_map['FirstLevelKey']['SecondLevelKey']",
        result
    );
}

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
fn test_stack_type_stack_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", StackType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("class TestStack(Stack):"),
        "Should extend Stack"
    );
    assert!(
        code.contains("super().__init__(scope, construct_id, **kwargs)"),
        "Should call super with kwargs"
    );
    assert!(
        code.contains("self.stack_name"),
        "Should use self.stack_name for pseudo-params"
    );
}

#[test]
fn test_stack_type_construct_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", StackType::Construct)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("class TestStack(Construct):"),
        "Should extend Construct"
    );
    assert!(
        code.contains("super().__init__(scope, construct_id)"),
        "Should call super without kwargs"
    );
    assert!(
        !code.contains("super().__init__(scope, construct_id, **kwargs)"),
        "Super call should not have kwargs"
    );
    assert!(
        code.contains("Stack.of(self).stack_name"),
        "Should use Stack.of(self) for pseudo-params"
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
    ir.synthesize("python", &mut output, "TestStack", StackType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("Stack.add_transform(self, 'AWS::Serverless-2016-10-31')"),
        "Stack mode should use Stack.add_transform(self, ...)"
    );
}

#[test]
fn test_add_transform_construct_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(TEMPLATE_WITH_TRANSFORM).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", StackType::Construct)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("Stack.of(self).add_transform('AWS::Serverless-2016-10-31')"),
        "Construct mode should use Stack.of(self).add_transform(...)"
    );
}

#[test]
fn test_stack_type_default_is_stack() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", StackType::default())
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("class TestStack(Stack):"),
        "Default should extend Stack"
    );
}

#[test]
fn test_stack_type_from_str_valid() {
    assert_eq!(StackType::from_str("stack").unwrap(), StackType::Stack);
    assert_eq!(
        StackType::from_str("construct").unwrap(),
        StackType::Construct
    );
}

#[test]
fn test_stack_type_from_str_invalid() {
    let result = StackType::from_str("invalid");
    assert!(result.is_err());
    assert_eq!(
        result.unwrap_err(),
        "Invalid stack type: 'invalid'. Expected 'stack' or 'construct'"
    );
}
