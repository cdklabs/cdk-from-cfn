// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

mod helpers;
mod stack;

use crate::client::AwsClient;
use cdk_from_cfn_testing::{EndToEndTestStack, Scope, Stack};

use self::stack::{BaseController, ChangeSetTestController, TestFixtureController};

/// Controller for managing end-to-end CloudFormation stack testing workflows.
/// 
/// This controller orchestrates the deployment, testing, and cleanup of CloudFormation stacks
/// generated from CDK code across multiple programming languages. It handles both main stacks
/// and their dependencies, ensuring proper ordering and cleanup.
#[derive(Clone)]
pub struct EndToEndController {
    /// The test stack configuration including main stack and optional dependency stack
    stack: EndToEndTestStack,
    /// Base controller providing AWS client operations and test metadata
    controller: BaseController,
}

impl EndToEndController {
    /// Creates a new end-to-end test controller.
    /// 
    /// # Arguments
    /// * `stack_name` - Base name for the CloudFormation stack
    /// * `region` - AWS region where stacks will be deployed
    /// * `test_name` - Unique identifier for this test run
    /// 
    /// # Returns
    /// A new `EndToEndController` instance configured for the specified test
    pub async fn new(stack_name: &str, region: &str, test_name: &str) -> Self {
        let stack = Stack::for_end_to_end(stack_name, test_name);
        let controller = BaseController::new(AwsClient::new(region).await, test_name);
        Self { stack, controller }
    }

    /// Tests a specific programming language by comparing CDK-generated stack with deployed CloudFormation.
    /// 
    /// Creates a change set to detect any differences between the deployed CloudFormation stack
    /// and the CDK-generated template for the specified language. Fails if differences are found.
    /// 
    /// # Arguments
    /// * `scope` - Test scope containing language and test metadata
    pub async fn test_language(&self, scope: &Scope) {
        let stack = Stack {
            tag_key: self.stack.stack.tag_key.clone(),
            template: self.stack.stack.clone().for_lang(scope),
            name: self.stack.stack.name.clone(),
        };
        ChangeSetTestController::new(
            &TestFixtureController::new(&self.controller, &stack),
            &scope.lang,
        )
        .check_for_stack_updates_workflow()
        .await;
    }

    /// Deletes all test stacks in the correct order.
    /// 
    /// Deletes the main stack first, followed by any dependency stacks.
    /// This ensures proper cleanup without dependency conflicts.
    pub async fn delete_stacks(&self) {
        // Main stacks first
        TestFixtureController::new(&self.controller, &self.stack.stack)
            .delete_stack_workflow()
            .await;

        if let Some(dependency) = &self.stack.dependency {
            TestFixtureController::new(&self.controller, &dependency)
                .delete_stack_workflow()
                .await;
        }
    }

    /// Deploys all test stacks in the correct order.
    /// 
    /// Deploys dependency stacks first, followed by the main stack.
    /// This ensures proper deployment order to satisfy dependencies.
    pub async fn deploy_stacks(&self) {
        // Dependency stacks first
        if let Some(dependency) = &self.stack.dependency {
            TestFixtureController::new(&self.controller, &dependency)
                .create_stack_workflow()
                .await;
        }

        // Main stack next
        TestFixtureController::new(&self.controller, &self.stack.stack)
            .create_stack_workflow()
            .await;
    }
}
