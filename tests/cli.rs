// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

//! CLI integration tests for cdk-from-cfn binary.
//!
//! Tests the command-line interface including:
//! - Default mode (no --as flag, defaults to stack)
//! - Explicit --as stack mode
//! - Explicit --as construct mode
//! - Invalid command handling

use std::path::Path;

use cdk_from_cfn_testing::{run_cli_with_args, CdkFromCfnConstruct, CdkFromCfnStack, Stack};

/// Path to the cdk-from-cfn binary, built by Cargo for these tests.
fn bin() -> &'static Path {
    Path::new(env!("CARGO_BIN_EXE_cdk-from-cfn"))
}

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
        bin(),
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
        bin(),
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
        bin(),
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
        bin(),
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
        bin(),
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
    let output = Stack::generate_stack(bin(), TEST_TEMPLATE, "typescript", "TestStack");
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
    let output = Stack::generate_construct(bin(), TEST_TEMPLATE, "typescript", "TestConstruct");
    let code = String::from_utf8(output).expect("Output should be valid UTF-8");

    assert!(
        code.contains("extends Construct"),
        "CdkFromCfnConstruct should generate Construct. Output:\n{}",
        code
    );
}

/// Test that --name sets the name of the generated class and is not deprecated
#[test]
fn name_option_sets_the_generated_class_name() {
    let (exit_code, stdout, stderr) = run_cli_with_args(
        bin(),
        &["-", "--language", "typescript", "--name", "TestStack"],
        Some(TEST_TEMPLATE),
    );

    assert_eq!(exit_code, Some(0), "CLI should exit successfully");

    let output = String::from_utf8(stdout).expect("Output should be valid UTF-8");
    assert!(
        output.contains("TestStackProps extends cdk.StackProps"),
        "--name should name the generated class. Output:\n{}",
        output
    );

    let error = String::from_utf8(stderr).expect("Stderr should be valid UTF-8");
    assert!(
        !error.contains("deprecated"),
        "--name should not print a deprecation warning. Stderr:\n{}",
        error
    );
}

/// Test that --name names a construct when combined with --as construct
#[test]
fn name_option_names_a_construct() {
    let (exit_code, stdout, _stderr) = run_cli_with_args(
        bin(),
        &[
            "-",
            "--language",
            "typescript",
            "--name",
            "TestConstruct",
            "--as",
            "construct",
        ],
        Some(TEST_TEMPLATE),
    );

    assert_eq!(exit_code, Some(0), "CLI should exit successfully");

    let output = String::from_utf8(stdout).expect("Output should be valid UTF-8");
    assert!(
        output.contains("interface TestConstructProps"),
        "--name should name the generated construct. Output:\n{}",
        output
    );
}

/// Test that the short flag -s keeps working without a warning
#[test]
fn name_option_short_flag_still_works() {
    let (exit_code, stdout, stderr) = run_cli_with_args(
        bin(),
        &["-", "--language", "typescript", "-s", "TestStack"],
        Some(TEST_TEMPLATE),
    );

    assert_eq!(exit_code, Some(0), "CLI should exit successfully");

    let output = String::from_utf8(stdout).expect("Output should be valid UTF-8");
    assert!(
        output.contains("TestStackProps extends cdk.StackProps"),
        "-s should name the generated class. Output:\n{}",
        output
    );

    let error = String::from_utf8(stderr).expect("Stderr should be valid UTF-8");
    assert!(
        !error.contains("deprecated"),
        "-s should not print a deprecation warning. Stderr:\n{}",
        error
    );
}

/// Test that the deprecated --stack-name still works but points to --name
#[test]
fn name_option_stack_name_is_deprecated_but_works() {
    let (exit_code, stdout, stderr) = run_cli_with_args(
        bin(),
        &["-", "--language", "typescript", "--stack-name", "TestStack"],
        Some(TEST_TEMPLATE),
    );

    assert_eq!(exit_code, Some(0), "CLI should exit successfully");

    let output = String::from_utf8(stdout).expect("Output should be valid UTF-8");
    assert!(
        output.contains("TestStackProps extends cdk.StackProps"),
        "--stack-name should still name the generated class. Output:\n{}",
        output
    );

    let error = String::from_utf8(stderr).expect("Stderr should be valid UTF-8");
    assert!(
        error.contains("--stack-name") && error.contains("deprecated") && error.contains("--name"),
        "--stack-name should warn that it is deprecated in favor of --name. Stderr:\n{}",
        error
    );
}

/// Test that --name and the deprecated --stack-name cannot be combined
#[test]
fn name_option_conflicts_with_deprecated_stack_name() {
    let (exit_code, stdout, stderr) = run_cli_with_args(
        bin(),
        &[
            "-",
            "--language",
            "typescript",
            "--name",
            "One",
            "--stack-name",
            "Two",
        ],
        Some(TEST_TEMPLATE),
    );

    assert_ne!(
        exit_code,
        Some(0),
        "CLI should reject --name together with --stack-name"
    );
    assert!(stdout.is_empty(), "No code should be generated");

    let error = String::from_utf8(stderr).expect("Stderr should be valid UTF-8");
    assert!(
        error.contains("cannot be used with"),
        "Error message should explain the conflict. Stderr:\n{}",
        error
    );
}

const CDK_DEPLOYED_TEMPLATE: &str = r#"{
    "Parameters": {
        "BootstrapVersion": {
            "Type": "AWS::SSM::Parameter::Value<String>",
            "Default": "/cdk-bootstrap/hnb659fds/version",
            "Description": "Version of the CDK Bootstrap resources in this environment, automatically retrieved from SSM Parameter Store. [cdk:skip]"
        }
    },
    "Conditions": {
        "CDKMetadataAvailable": {
            "Fn::Or": [
                { "Fn::Equals": [{ "Ref": "AWS::Region" }, "us-east-1"] },
                { "Fn::Equals": [{ "Ref": "AWS::Region" }, "us-west-2"] }
            ]
        }
    },
    "Resources": {
        "AppQueueFD3F4958": {
            "Type": "AWS::SQS::Queue",
            "Properties": {
                "VisibilityTimeout": 300
            },
            "Metadata": {
                "aws:cdk:path": "AppStack/AppQueue/Resource"
            }
        },
        "CustomMetaQueue": {
            "Type": "AWS::SQS::Queue",
            "Properties": {
                "VisibilityTimeout": 60
            },
            "Metadata": {
                "aws:cdk:path": "AppStack/CustomMetaQueue/Resource",
                "Owner": "platform"
            }
        },
        "CDKMetadata": {
            "Type": "AWS::CDK::Metadata",
            "Properties": {
                "Analytics": "v2:deflate64:H4sIAAAAAAAA/zPSMzQ10DNQ"
            },
            "Metadata": {
                "aws:cdk:path": "AppStack/CDKMetadata/Default"
            },
            "Condition": "CDKMetadataAvailable"
        }
    },
    "Rules": {
        "CheckBootstrapVersion": {
            "Assertions": [
                {
                    "Assert": {
                        "Fn::Not": [
                            {
                                "Fn::Contains": [
                                    ["1", "2", "3", "4", "5"],
                                    { "Ref": "BootstrapVersion" }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }
}"#;

/// Test that CDK-generated elements are skipped cleanly and logged to stderr
#[test]
fn cli_skips_cdk_generated_elements_and_logs_messages() {
    let (exit_code, stdout, stderr) = run_cli_with_args(
        bin(),
        &["-", "--language", "typescript", "--name", "AppStack"],
        Some(CDK_DEPLOYED_TEMPLATE),
    );

    assert_eq!(exit_code, Some(0), "CLI should exit successfully");

    let output = String::from_utf8(stdout).expect("Output should be valid UTF-8");
    assert!(
        output.contains("AppQueueFD3F4958"),
        "User resource should be generated. Output:\n{}",
        output
    );
    assert!(
        output.contains("Owner: 'platform'"),
        "User metadata should be preserved when aws:cdk:path is stripped. Output:\n{}",
        output
    );
    for omitted in [
        "CDKMetadata",
        "AWS::CDK::Metadata",
        "CDKMetadataAvailable",
        "cdkMetadataAvailable",
        "aws:cdk:path",
        "BootstrapVersion",
        "bootstrapVersion",
        "CheckBootstrapVersion",
    ] {
        assert!(
            !output.contains(omitted),
            "Generated output must omit {omitted}. Output:\n{}",
            output
        );
    }

    // Verify AppQueueFD3F4958 specifically has no empty cfnOptions.metadata block
    assert!(
        !output.contains("appQueueFd3f4958.cfnOptions.metadata"),
        "Resource with only aws:cdk:path must not emit empty metadata. Output:\n{}",
        output
    );

    let stderr_str = String::from_utf8(stderr).expect("Stderr should be valid UTF-8");
    for expected in [
        "AWS::CDK::Metadata",
        "CDKMetadata",
        "CDKMetadataAvailable",
        "aws:cdk:path",
        "BootstrapVersion",
        "CheckBootstrapVersion",
    ] {
        assert!(
            stderr_str.contains(expected),
            "Stderr should report skipping {expected}. Stderr:\n{}",
            stderr_str
        );
    }
}

/// Test that YAML CDK-deployed templates with short tags in Rules are handled cleanly
#[test]
fn cli_skips_cdk_generated_elements_in_yaml_template() {
    let yaml = r#"
Parameters:
  BootstrapVersion:
    Type: AWS::SSM::Parameter::Value<String>
    Default: /cdk-bootstrap/hnb659fds/version
    Description: Version of the CDK Bootstrap resources in this environment. [cdk:skip]
Resources:
  AppQueue:
    Type: AWS::SQS::Queue
    Metadata:
      aws:cdk:path: AppStack/AppQueue/Resource
    Properties:
      VisibilityTimeout: 300
  CDKMetadata:
    Type: AWS::CDK::Metadata
    Properties:
      Analytics: v2:deflate64:abc
Rules:
  CheckBootstrapVersion:
    Assertions:
      - Assert: !Not [!Contains [["1", "2", "3"], !Ref BootstrapVersion]]
        AssertDescription: CDK bootstrap stack version 4 required.
"#;

    let (exit_code, stdout, stderr) = run_cli_with_args(
        bin(),
        &["-", "--language", "typescript", "--name", "YamlStack"],
        Some(yaml),
    );

    assert_eq!(exit_code, Some(0), "CLI should exit successfully");

    let output = String::from_utf8(stdout).expect("Output should be valid UTF-8");
    assert!(output.contains("AppQueue"));
    assert!(!output.contains("CDKMetadata"));
    assert!(!output.contains("aws:cdk:path"));
    assert!(!output.contains("BootstrapVersion"));
    assert!(!output.contains("bootstrapVersion"));

    let stderr_str = String::from_utf8(stderr).expect("Stderr should be valid UTF-8");
    assert!(stderr_str.contains("BootstrapVersion"));
    assert!(stderr_str.contains("CheckBootstrapVersion"));
    assert!(stderr_str.contains("AWS::CDK::Metadata"));
    assert!(stderr_str.contains("aws:cdk:path"));
}
