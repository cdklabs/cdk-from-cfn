// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use std::{env::var, io::Write, path::PathBuf, process::{Command, Stdio}};

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
    /// * `template` - CloudFormation template as JSON/YAML string
    /// * `lang` - Target programming language for CDK code
    /// * `stack_name` - Name for the generated CDK stack
    /// 
    /// # Returns
    /// Generated CDK code as bytes
    fn generate_stack(template: &str, lang: &str, stack_name: &str) -> Vec<u8>;
}

impl CdkFromCfnStack for Stack {
    /// Generates CDK stack code using the cdk-from-cfn binary.
    /// 
    /// Executes the cdk-from-cfn tool as a subprocess to convert the CloudFormation
    /// template into CDK code for the specified language.
    /// 
    /// # Arguments
    /// * `template` - CloudFormation template as JSON/YAML string
    /// * `lang` - Target programming language for CDK code
    /// * `stack_name` - Name for the generated CDK stack
    /// 
    /// # Returns
    /// Generated CDK code as bytes
    /// 
    /// # Panics
    /// Panics if the cdk-from-cfn tool execution fails or returns non-zero exit code
    fn generate_stack(template: &str, lang: &str, stack_name: &str) -> Vec<u8> {
        let mut child = match Command::new(&get_cdk_from_cfn_binary_path())
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

/// Determines the path to the cdk-from-cfn binary for the current build.
/// 
/// Attempts to locate the binary in the target directory based on the build
/// environment, falling back to a default path if necessary.
/// 
/// # Returns
/// Path to the cdk-from-cfn binary
fn get_cdk_from_cfn_binary_path() -> PathBuf {
    // OUT_DIR is target/debug/build/{crate}-{hash}/out
    // We need target/<potentially-something>/debug
    var("OUT_DIR")
        .ok()
        .and_then(|out_dir| {
            PathBuf::from(out_dir)
                .parent()? // remove /out
                .parent()? // remove /{crate}-{hash}
                .parent() // remove /build
                .map(|p| p.join(Paths::crate_name()))
        })
        .unwrap_or_else(|| PathBuf::from("target/debug/cdk-from-cfn"))
    }

