// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

//! CLI integration tests for cdk-from-cfn binary.
//!
//! Tests the command-line interface including:
//! - Default mode (no --as flag, defaults to stack)
//! - Explicit --as stack mode
//! - Explicit --as construct mode
//! - Invalid command handling

use cdk_from_cfn_testing::{run_cli_with_args, CdkFromCfnConstruct, CdkFromCfnStack, Stack};

const TEST_TEMPLATE: &str = r#"{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Description": "Test template for CLI integration tests",
    "Parameters": {
        "BucketName": {
            "Type": "String",
            "Default": "my-test-bucket",
            "Description": "Name of the S3 bucket"
        },
        "Environment": {
            "Type": "String",
            "Default": "dev",
            "AllowedValues": ["dev", "prod"],
            "Description": "Environment type"
        }
    },
    "Conditions": {
        "IsProd": {
            "Fn::Equals": [{"Ref": "Environment"}, "prod"]
        }
    },
    "Resources": {
        "MyBucket": {
            "Type": "AWS::S3::Bucket",
            "Properties": {
                "BucketName": {"Ref": "BucketName"},
                "Tags": [
                    {
                        "Key": "Environment",
                        "Value": {"Ref": "Environment"}
                    }
                ]
            }
        },
        "ProdOnlyBucket": {
            "Type": "AWS::S3::Bucket",
            "Condition": "IsProd",
            "Properties": {
                "BucketName": {"Fn::Sub": "${BucketName}-prod-backup"}
            }
        }
    },
    "Outputs": {
        "BucketArn": {
            "Description": "ARN of the created bucket",
            "Value": {"Fn::GetAtt": ["MyBucket", "Arn"]},
            "Export": {
                "Name": {"Fn::Sub": "${AWS::StackName}-BucketArn"}
            }
        }
    }
}"#;

/// Test that default mode (no --as flag) generates a Stack
#[test]
fn test_cli_default_mode_generates_stack() {
    let (exit_code, stdout, _stderr) = run_cli_with_args(
        &["-", "--language", "typescript", "--stack-name", "TestStack"],
        Some(TEST_TEMPLATE),
    );

    assert_eq!(exit_code, Some(0), "CLI should exit successfully");

    let output = String::from_utf8(stdout).expect("Output should be valid UTF-8");

    // Stack-specific assertions
    assert!(
        output.contains("extends cdk.Stack"),
        "Default mode should generate a Stack class. Output:\n{}",
        output
    );
    assert!(
        output.contains("TestStackProps extends cdk.StackProps"),
        "Stack props should extend StackProps"
    );
    assert!(
        output.contains("scope: cdk.App"),
        "Stack constructor should accept cdk.App as scope"
    );

    // Should NOT have Construct-specific patterns
    assert!(
        !output.contains("extends Construct"),
        "Default mode should not generate a Construct class"
    );
    assert!(
        !output.contains("import { Construct } from 'constructs'"),
        "Should not import Construct directly for Stack mode"
    );
}

/// Test that explicit --as stack mode generates a Stack
#[test]
fn test_cli_explicit_stack_mode() {
    let (exit_code, stdout, _stderr) = run_cli_with_args(
        &[
            "-",
            "--language",
            "typescript",
            "--stack-name",
            "TestStack",
            "--as",
            "stack",
        ],
        Some(TEST_TEMPLATE),
    );

    assert_eq!(exit_code, Some(0), "CLI should exit successfully");

    let output = String::from_utf8(stdout).expect("Output should be valid UTF-8");

    // Stack-specific assertions
    assert!(
        output.contains("extends cdk.Stack"),
        "Stack mode should generate a Stack class. Output:\n{}",
        output
    );
    assert!(
        output.contains("TestStackProps extends cdk.StackProps"),
        "Stack props should extend StackProps"
    );
    assert!(
        output.contains("scope: cdk.App"),
        "Stack constructor should accept cdk.App as scope"
    );
}

/// Test that --as construct mode generates a Construct
#[test]
fn test_cli_construct_mode() {
    let (exit_code, stdout, _stderr) = run_cli_with_args(
        &[
            "-",
            "--language",
            "typescript",
            "--stack-name",
            "TestConstruct",
            "--as",
            "construct",
        ],
        Some(TEST_TEMPLATE),
    );

    assert_eq!(exit_code, Some(0), "CLI should exit successfully");

    let output = String::from_utf8(stdout).expect("Output should be valid UTF-8");

    // Construct-specific assertions
    assert!(
        output.contains("extends Construct"),
        "Construct mode should generate a Construct class. Output:\n{}",
        output
    );
    assert!(
        output.contains("import { Construct } from 'constructs'"),
        "Should import Construct from constructs package"
    );
    assert!(
        output.contains("scope: Construct"),
        "Construct constructor should accept Construct as scope"
    );
    assert!(
        output.contains("interface TestConstructProps"),
        "Should generate props interface without extending StackProps"
    );

    // Should NOT have Stack-specific patterns
    assert!(
        !output.contains("extends cdk.Stack"),
        "Construct mode should not generate a Stack class"
    );
    assert!(
        !output.contains("extends cdk.StackProps"),
        "Construct props should not extend StackProps"
    );
}

/// Test that invalid --as value is rejected
#[test]
fn test_cli_invalid_as_value() {
    let (exit_code, _stdout, stderr) = run_cli_with_args(
        &[
            "-",
            "--language",
            "typescript",
            "--stack-name",
            "TestStack",
            "--as",
            "invalid",
        ],
        Some(TEST_TEMPLATE),
    );

    assert_ne!(
        exit_code,
        Some(0),
        "CLI should fail with invalid --as value"
    );

    let error = String::from_utf8(stderr).expect("Stderr should be valid UTF-8");
    assert!(
        error.contains("invalid") || error.contains("Invalid"),
        "Error message should mention invalid value. Stderr:\n{}",
        error
    );
}

/// Test that invalid language is rejected
#[test]
fn test_cli_invalid_language() {
    let (exit_code, _stdout, stderr) = run_cli_with_args(
        &[
            "-",
            "--language",
            "invalid_lang",
            "--stack-name",
            "TestStack",
        ],
        Some(TEST_TEMPLATE),
    );

    assert_ne!(exit_code, Some(0), "CLI should fail with invalid language");

    let error = String::from_utf8(stderr).expect("Stderr should be valid UTF-8");
    assert!(
        error.contains("invalid") || error.contains("Invalid") || error.contains("invalid_lang"),
        "Error message should mention invalid language. Stderr:\n{}",
        error
    );
}

/// Test CdkFromCfnStack trait generates stack code
#[test]
fn test_cdk_from_cfn_stack_trait() {
    let output = Stack::generate_stack(TEST_TEMPLATE, "typescript", "TestStack");
    let code = String::from_utf8(output).expect("Output should be valid UTF-8");

    assert!(
        code.contains("extends cdk.Stack"),
        "CdkFromCfnStack should generate Stack. Output:\n{}",
        code
    );
}

/// Test CdkFromCfnConstruct trait generates construct code
#[test]
fn test_cdk_from_cfn_construct_trait() {
    let output = Stack::generate_construct(TEST_TEMPLATE, "typescript", "TestConstruct");
    let code = String::from_utf8(output).expect("Output should be valid UTF-8");

    assert!(
        code.contains("extends Construct"),
        "CdkFromCfnConstruct should generate Construct. Output:\n{}",
        code
    );
}
