// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

mod client;
mod controller;

use cdk_from_cfn_testing::{CdkAppTestGroup, Scope};
use controller::EndToEndController;

/// End-to-end test orchestrator for CDK stack validation.
/// 
/// Manages the complete lifecycle of end-to-end testing including stack deployment,
/// language-specific testing, and cleanup operations.
#[derive(Clone)]
pub struct EndToEndTest<'a> {
    /// Controller for AWS CloudFormation operations
    controller: EndToEndController,
    /// Whether to skip stack operations (when no synthesis filters are set)
    skip: bool,
    /// Unique identifier for this test run
    test_name: String,
    /// Name of the stack being tested
    stack_name: &'a str,
    /// AWS region where the test is running
    region: &'static str,
}

impl<'a> EndToEndTest<'a> {
    /// Generates a new end-to-end test from a CDK application test group.
    /// 
    /// Sets up the test environment by deploying CloudFormation stacks if synthesis
    /// filters are configured, otherwise skips stack operations for faster testing.
    /// 
    /// # Arguments
    /// * `app` - CDK application test group configuration
    /// 
    /// # Returns
    /// A new `EndToEndTest` instance ready for language testing
    pub async fn generate(app: &CdkAppTestGroup<'a>) -> Self {
        let controller = EndToEndController::new(app.stack_name, app.region, &app.test_name).await;
        let skip = app.test_filter.synth.len() == 0;

        if !skip {
            controller.delete_stacks().await;
            controller.deploy_stacks().await;
        }
        Self {
            controller,
            skip,
            test_name: app.test_name.clone(),
            stack_name: app.stack_name,
            region: app.region,
        }
    }

    /// Runs the end-to-end test for a specific programming language.
    /// 
    /// Compares the CDK-generated template with the deployed CloudFormation stack
    /// to ensure consistency across language implementations.
    /// 
    /// # Arguments
    /// * `scope` - Test scope containing language and test metadata
    pub async fn run(&self, scope: &Scope) {
        self.controller.test_language(scope).await;
    }

    /// Cleans up AWS resources created during the test.
    /// 
    /// Deletes CloudFormation stacks and associated resources if they were deployed.
    /// Skips cleanup if stack operations were skipped during generation.
    pub async fn clean(&self) {
        if !self.skip {
            eprintln!(
                "  🌩️  Starting cleanup for {} for {} in {}",
                self.test_name, self.stack_name, self.region
            );
            self.controller.delete_stacks().await;
        }
    }
}
