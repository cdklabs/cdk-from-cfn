// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use super::*;
use crate::cdk::Schema;
use crate::ir::CloudformationProgramIr;
use crate::CloudformationParseTree;
use std::str::FromStr;

#[test]
fn pretty_name_fixes() {
    assert_eq!("vpc", pretty_name("VPC"));
    assert_eq!("vpcs", pretty_name("VPCs"));
    assert_eq!("objectAccess", pretty_name("GetObject"));
    assert_eq!("equalTo", pretty_name("Equals"));
    assert_eq!("providerArns", pretty_name("ProviderARNs"));
    assert_eq!("targetAZs", pretty_name("TargetAZs"));
    assert_eq!("diskSizeMBs", pretty_name("DiskSizeMBs"));
}

#[test]
fn test_invalid_organization() {
    let bad_org = "NotAws";
    let import_instruction = ImportInstruction {
        organization: bad_org.to_string(),
        service: Option::None,
    };
    let result = import_instruction.to_typescript().unwrap_err();
    let expected = format!("Expected organization to be AWS or Alexa. Found {bad_org}");
    assert_eq!(expected, result.to_string());
}

#[test]
fn test_alexa_organization() {
    let import_instruction = ImportInstruction {
        organization: "Alexa".to_string(),
        service: Some("ASK".to_string()),
    };
    let result = import_instruction.to_typescript();
    assert_eq!(
        "import * as ask from 'aws-cdk-lib/alexa-ask';",
        result.unwrap()
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
fn test_class_type_stack_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("extends cdk.Stack"),
        "Should extend cdk.Stack"
    );
    assert!(
        code.contains("scope: cdk.App"),
        "Should have scope: cdk.App"
    );
    assert!(
        code.contains("super(scope, id, props)"),
        "Should call super with props"
    );
    assert!(
        !code.contains("import { Construct }"),
        "Should not import Construct"
    );
}

#[test]
fn test_class_type_construct_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize(
        "typescript",
        &mut output,
        "TestConstruct",
        ClassType::Construct,
    )
    .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("extends Construct"),
        "Should extend Construct"
    );
    assert!(
        code.contains("scope: Construct"),
        "Should have scope: Construct"
    );
    assert!(
        code.contains("super(scope, id)"),
        "Should call super without props"
    );
    assert!(
        code.contains("import { Construct } from 'constructs'"),
        "Should import Construct"
    );
    assert!(
        code.contains("cdk.Stack.of(this).stackName"),
        "Should use cdk.Stack.of(this) for pseudo-params"
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
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("this.addTransform('AWS::Serverless-2016-10-31')"),
        "Stack mode should use this.addTransform"
    );
}

#[test]
fn test_add_transform_construct_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(TEMPLATE_WITH_TRANSFORM).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize(
        "typescript",
        &mut output,
        "TestConstruct",
        ClassType::Construct,
    )
    .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("cdk.Stack.of(this).addTransform('AWS::Serverless-2016-10-31')"),
        "Construct mode should use cdk.Stack.of(this).addTransform"
    );
}

#[test]
fn test_class_type_default_is_stack() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::default())
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("extends cdk.Stack"),
        "Default should extend cdk.Stack"
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
    ir.synthesize(
        "typescript",
        &mut output,
        "TestConstruct",
        ClassType::Construct,
    )
    .unwrap();
    let code = String::from_utf8(output).unwrap();

    // Should extend Construct
    assert!(
        code.contains("extends Construct"),
        "Should extend Construct"
    );

    // Should have props interface with parameters
    assert!(
        code.contains("bucketName"),
        "Should have bucketName parameter"
    );
    assert!(
        code.contains("enableVersioning"),
        "Should have enableVersioning parameter"
    );

    // Should call super without props
    assert!(
        code.contains("super(scope, id)"),
        "Should call super without props"
    );

    // Should import Construct
    assert!(
        code.contains("import { Construct } from 'constructs'"),
        "Should import Construct"
    );
}

#[test]
fn test_stack_mode_with_props() {
    let cfn: CloudformationParseTree = serde_json::from_str(TEMPLATE_WITH_PARAMS).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    // Should extend Stack
    assert!(
        code.contains("extends cdk.Stack"),
        "Should extend cdk.Stack"
    );

    // Should have props interface with parameters
    assert!(
        code.contains("bucketName"),
        "Should have bucketName parameter"
    );
    assert!(
        code.contains("enableVersioning"),
        "Should have enableVersioning parameter"
    );

    // Should call super with props
    assert!(
        code.contains("super(scope, id, props)"),
        "Should call super with props"
    );
}
