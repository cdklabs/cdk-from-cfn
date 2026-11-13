// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use std::{io::Write, path::Path, process::{Command, Stdio}};

use crate::{filesystem::{Files, Paths, Zip}, Language};

use super::Scope;

/// Configuration for a CloudFormation stack used in testing.
/// 
/// Contains all necessary information to deploy and manage a CloudFormation stack,
/// including the template content and identification tags.
#[derive(Clone)]
pub struct Stack {
    /// Name of the CloudFormation stack
    pub name: String,
    /// CloudFormation template content as JSON/YAML string
    pub template: String,
    /// Tag key used to identify test resources
    pub tag_key: String,
}

/// Configuration for end-to-end testing including main stack and optional dependencies.
/// 
/// Represents a complete test scenario that may include both a primary stack
/// and dependency stacks that must be deployed in the correct order.
#[derive(Clone)]
pub struct EndToEndTestStack {
    /// Primary stack configuration for the test
    pub stack: Stack,
    /// Optional dependency stack that must be deployed first
    pub dependency: Option<Stack>,
}

impl Stack {
    /// Creates an end-to-end test stack configuration from test metadata.
    /// 
    /// Extracts templates from test archives and creates stack configurations
    /// with appropriate naming and tagging for end-to-end testing.
    /// 
    /// # Arguments
    /// * `stack_name` - Base name for the CloudFormation stack
    /// * `test_name` - Unique identifier for this test run
    /// 
    /// # Returns
    /// Complete end-to-end test stack configuration with main and dependency stacks
    pub fn for_end_to_end(stack_name: &str, test_name: &str) -> EndToEndTestStack {
        EndToEndTestStack {
            stack: Stack {
                name: Paths::e2e_name(stack_name),
                template: Zip::extract_template(test_name),
                tag_key: Paths::E2E_TAG.to_string(),
            },
            dependency: if let Some(template) = Zip::extract_dependency_template(test_name) {
                Some(Stack {
                    name: Paths::dependency_name(stack_name),
                    template,
                    tag_key: Paths::E2E_DEPENDENCY_TAG.to_string(),
                })
            } else {
                None
            },
        }
    }

    /// Loads the synthesized CDK template for a specific programming language.
    /// 
    /// # Arguments
    /// * `scope` - Test scope containing language and test metadata
    /// 
    /// # Returns
    /// CDK-synthesized CloudFormation template for the specified language
    pub fn for_lang(self, scope: &Scope) -> String {
        let name = self.name.split("-").into_iter().last().unwrap();
        Files::load_actual_synthesized_template(scope, name)
    }
}

/// Trait for generating CDK stacks from CloudFormation templates.
/// 
/// Provides the interface for converting CloudFormation templates into
/// CDK code using the cdk-from-cfn tool.
pub trait CdkFromCfnStack {
    /// Generates CDK stack code from a CloudFormation template.
    /// 
    /// # Arguments
    /// * `bin` - Path to the cdk-from-cfn binary
    /// * `template` - CloudFormation template as JSON/YAML string
    /// * `lang` - Target programming language for CDK code
    /// * `stack_name` - Name for the generated CDK stack
    /// 
    /// # Returns
    /// Generated CDK code as bytes
    fn generate_stack(bin: &Path, template: &str, lang: &str, stack_name: &str) -> Vec<u8>;
}

impl CdkFromCfnStack for Stack {
    /// Generates CDK stack code using the cdk-from-cfn binary.
    /// 
    /// Executes the cdk-from-cfn tool as a subprocess to convert the CloudFormation
    /// template into CDK code for the specified language.
    /// 
    /// # Arguments
    /// * `bin` - Path to the cdk-from-cfn binary
    /// * `template` - CloudFormation template as JSON/YAML string
    /// * `lang` - Target programming language for CDK code
    /// * `stack_name` - Name for the generated CDK stack
    /// 
    /// # Returns
    /// Generated CDK code as bytes
    /// 
    /// # Panics
    /// Panics if the cdk-from-cfn tool execution fails or returns non-zero exit code
    fn generate_stack(bin: &Path, template: &str, lang: &str, stack_name: &str) -> Vec<u8> {
        let mut child = match Command::new(bin)
            .args([
                "-",
                "--language",
                // Accounts for golang/go usage. We allow different versions in different places
                Language::lang_arg(lang),
                "--stack-name",
                stack_name,
            ])
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
        {
            Ok(child) => child,
            Err(e) => panic!("Failed to execute cdk-from-cfn: {}", e),
        };

        if let Some(stdin) = child.stdin.as_mut() {
            if let Err(e) = stdin.write_all(template.as_bytes()) {
                panic!("Failed to write to stdin: {}", e);
            }
        }

        let output = child.wait_with_output().expect("Failed to read output");

        assert!(output.status.success(), 
            "❌ Stack file could not be generated. {}", 
            format!("An error occurred while running 'cdk-from-cfn --language {lang} --stack-name {stack_name}. {}: {:?}'", 
                output.status.code().expect("Unknown Error"),
                output.stderr)
            );

        output.stdout
    }
}

/// Trait for generating CDK constructs from CloudFormation templates.
/// 
/// Provides the interface for converting CloudFormation templates into
/// CDK construct code using the cdk-from-cfn tool with `--as construct` flag.
pub trait CdkFromCfnConstruct {
    /// Generates CDK construct code from a CloudFormation template.
    /// 
    /// # Arguments
    /// * `bin` - Path to the cdk-from-cfn binary
    /// * `template` - CloudFormation template as JSON/YAML string
    /// * `lang` - Target programming language for CDK code
    /// * `construct_name` - Name for the generated CDK construct
    /// 
    /// # Returns
    /// Generated CDK code as bytes
    fn generate_construct(bin: &Path, template: &str, lang: &str, construct_name: &str) -> Vec<u8>;
}

impl CdkFromCfnConstruct for Stack {
    /// Generates CDK construct code using the cdk-from-cfn binary with `--as construct`.
    /// 
    /// # Arguments
    /// * `bin` - Path to the cdk-from-cfn binary
    /// * `template` - CloudFormation template as JSON/YAML string
    /// * `lang` - Target programming language for CDK code
    /// * `construct_name` - Name for the generated CDK construct
    /// 
    /// # Returns
    /// Generated CDK code as bytes
    /// 
    /// # Panics
    /// Panics if the cdk-from-cfn tool execution fails or returns non-zero exit code
    fn generate_construct(bin: &Path, template: &str, lang: &str, construct_name: &str) -> Vec<u8> {
        let mut child = match Command::new(bin)
            .args([
                "-",
                "--language",
                Language::lang_arg(lang),
                "--stack-name",
                construct_name,
                "--as",
                "construct",
            ])
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
        {
            Ok(child) => child,
            Err(e) => panic!("Failed to execute cdk-from-cfn: {}", e),
        };

        if let Some(stdin) = child.stdin.as_mut() {
            if let Err(e) = stdin.write_all(template.as_bytes()) {
                panic!("Failed to write to stdin: {}", e);
            }
        }

        let output = child.wait_with_output().expect("Failed to read output");

        assert!(output.status.success(), 
            "❌ Construct file could not be generated. {}", 
            format!("An error occurred while running 'cdk-from-cfn --language {lang} --stack-name {construct_name} --as construct. {}: {:?}'", 
                output.status.code().expect("Unknown Error"),
                output.stderr)
            );

        output.stdout
    }
}

/// Runs the cdk-from-cfn CLI with custom arguments.
/// 
/// # Arguments
/// * `bin` - Path to the cdk-from-cfn binary
/// * `args` - Command line arguments to pass to the binary
/// * `stdin_input` - Optional input to write to stdin
/// 
/// # Returns
/// Tuple of (exit_code, stdout, stderr)
pub fn run_cli_with_args(bin: &Path, args: &[&str], stdin_input: Option<&str>) -> (Option<i32>, Vec<u8>, Vec<u8>) {
    let mut child = match Command::new(bin)
        .args(args)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
    {
        Ok(child) => child,
        Err(e) => panic!("Failed to execute cdk-from-cfn: {}", e),
    };

    if let Some(input) = stdin_input {
        if let Some(stdin) = child.stdin.as_mut() {
            let _ = stdin.write_all(input.as_bytes());
        }
    }

    let output = child.wait_with_output().expect("Failed to read output");
    (output.status.code(), output.stdout, output.stderr)
}
