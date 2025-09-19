// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use aws_sdk_cloudformation::{
    operation::{
        describe_change_set::DescribeChangeSetOutput, describe_stacks::DescribeStacksOutput,
    },
    types::{ChangeSetType, OnStackFailure, StackStatus, Tag},
};

use cdk_from_cfn_testing::Stack;

use crate::{
    client::AwsClient,
    controller::helpers::{Diff, Template},
};

/// Base controller providing core AWS operations and test metadata.
///
/// This controller encapsulates the AWS client and test identification,
/// serving as the foundation for more specialized controllers.
#[derive(Clone)]
pub struct BaseController {
    /// AWS client for CloudFormation and S3 operations
    pub client: AwsClient,
    /// Unique identifier for the current test
    pub test_name: String,
}

impl BaseController {
    /// Creates a new base controller with the specified AWS client and test name.
    ///
    /// # Arguments
    /// * `client` - Configured AWS client for API operations
    /// * `test_name` - Unique identifier for this test run
    ///
    /// # Returns
    /// A new `BaseController` instance
    pub fn new(client: AwsClient, test_name: &str) -> Self {
        Self {
            client,
            test_name: test_name.to_string(),
        }
    }

    /// Creates a CloudFormation change set and waits for it to complete.
    ///
    /// # Arguments
    /// * `stack` - Stack configuration containing name and template
    /// * `change_set_type` - Type of change set (Create or Update)
    /// * `change_set_name` - Name for the change set
    /// * `on_stack_failure` - Action to take if stack creation fails
    /// * `tag` - Tag to apply to the stack for identification
    ///
    /// # Returns
    /// Description of the completed change set
    ///
    /// # Panics
    /// Panics if change set creation or completion fails
    async fn create_change_set(
        &self,
        stack: &Stack,
        change_set_type: ChangeSetType,
        change_set_name: &str,
        on_stack_failure: OnStackFailure,
        tag: Tag,
    ) -> DescribeChangeSetOutput {
        let create_change_set_result = self
            .client
            .create_change_set(
                &stack.name,
                &stack.template,
                tag,
                change_set_type,
                change_set_name,
                on_stack_failure,
            )
            .await;
        assert!(
            create_change_set_result.is_ok(),
            "❌ Change set could not be created for {} in {} due to error: {}",
            stack.name,
            self.client.region,
            create_change_set_result.clone().err().unwrap()
        );

        let change_set_create_complete_result = self
            .client
            .wait_for_change_set_create_complete(&stack.name, change_set_name)
            .await;
        assert!(
            change_set_create_complete_result.is_ok(),
            "❌ Change set could not be created for {} in {} due to error: {:?}",
            stack.name,
            self.client.region,
            change_set_create_complete_result.clone().err().unwrap()
        );

        change_set_create_complete_result.unwrap()
    }
}

/// Controller for testing CloudFormation change sets against CDK-generated templates.
///
/// This controller creates change sets to detect differences between deployed CloudFormation
/// stacks and CDK-generated templates, ensuring consistency across language implementations.
pub struct ChangeSetTestController<'a> {
    /// Test fixture controller managing the stack under test
    fixture: &'a TestFixtureController<'a>,
    /// Programming language being tested
    lang: &'a str,
}

impl<'a> ChangeSetTestController<'a> {
    /// Creates a new change set test controller.
    ///
    /// # Arguments
    /// * `fixture` - Test fixture controller for the stack
    /// * `lang` - Programming language being tested
    ///
    /// # Returns
    /// A new `ChangeSetTestController` instance
    pub fn new(fixture: &'a TestFixtureController, lang: &'a str) -> Self {
        Self { fixture, lang }
    }

    /// Executes the workflow to check for stack updates using change sets.
    ///
    /// Creates an update change set and verifies that no changes are detected,
    /// confirming that the deployed CloudFormation stack matches the CDK-generated template.
    ///
    /// # Panics
    /// Panics if any differences are detected between the deployed stack and CDK template
    pub async fn check_for_stack_updates_workflow(&self) {
        let change_set_name = format!("{}-update-{}", self.lang, self.fixture.stack.name);
        let change_set = self
            .fixture
            .controller
            .create_change_set(
                self.fixture.stack,
                ChangeSetType::Update,
                &change_set_name,
                OnStackFailure::DoNothing,
                self.fixture.tag.clone(),
            )
            .await;
        let diff = Diff::get_change_set_diff(change_set);
        assert!(
            diff.is_none(),
            "❌ Changes detected in change set for {}::{} in {}:\n{}",
            self.fixture.controller.test_name,
            self.lang,
            self.fixture.controller.client.region,
            diff.unwrap(),
        );
        eprintln!("  ✨ No changes detected in change set. Deployed CFN stack matches CDK stack for {}::{} in {}", self.fixture.controller.test_name, self.lang, self.fixture.controller.client.region);
    }
}

/// Controller for managing individual CloudFormation stack test fixtures.
///
/// This controller handles the complete lifecycle of a test stack, including creation,
/// validation, and cleanup. It ensures proper tagging and handles various failure scenarios.
pub struct TestFixtureController<'a> {
    /// Base controller providing AWS operations and test metadata
    pub(crate) controller: &'a BaseController,
    /// Stack configuration being managed
    pub(crate) stack: &'a Stack,
    /// CloudFormation tag for identifying test resources
    pub(crate) tag: Tag,
}

impl<'a> TestFixtureController<'a> {
    /// Creates a new test fixture controller for the specified stack.
    ///
    /// # Arguments
    /// * `controller` - Base controller providing AWS operations
    /// * `stack` - Stack configuration to manage
    ///
    /// # Returns
    /// A new `TestFixtureController` instance with appropriate tagging
    pub fn new(controller: &'a BaseController, stack: &'a Stack) -> Self {
        let tag = Tag::builder()
            .key(&stack.tag_key)
            .value(&controller.test_name)
            .build();
        Self {
            controller,
            stack,
            tag,
        }
    }

    /// Executes the complete stack deletion workflow.
    ///
    /// Validates stack ownership through tags, updates retention policies to allow deletion,
    /// and handles various failure scenarios during deletion. Ensures clean resource cleanup.
    ///
    /// # Returns
    /// Returns early if the stack doesn't exist or isn't owned by this test
    pub async fn delete_stack_workflow(&self) {
        let Ok(stacks_output) = self
            .controller
            .client
            .describe_stacks(&self.stack.name)
            .await
        else {
            return;
        };

        let Some(stack) = stacks_output.stacks().first() else {
            return;
        };

        // Verify stack tags unless it's stuck in ReviewInProgress (which is broken)
        if let Some(status) = stack.stack_status() {
            if status != &StackStatus::ReviewInProgress {
                self.stack_has_test_tags(stacks_output).await;
            }
        }

        // Some tests have retain policies. Update these so no orphaned resources are left behind
        self.ensure_retention_policies_are_delete().await;

        self.delete_stack().await;
    }

    /// Executes the complete stack creation workflow.
    ///
    /// Creates a change set for stack creation, executes it, and waits for completion.
    /// Provides detailed logging of the deployment process.
    ///
    /// # Panics
    /// Panics if stack creation fails at any stage
    pub async fn create_stack_workflow(&self) {
        eprintln!(
            "  🌩️  Starting deployment for {} for {} in {}",
            self.controller.test_name, self.controller.client.region, self.stack.name
        );
        let change_set = self
            .controller
            .create_change_set(
                self.stack,
                ChangeSetType::Create,
                format!("{}-create", self.stack.name).as_str(),
                OnStackFailure::Delete,
                self.tag.clone(),
            )
            .await;

        self.execute_change_set(change_set.change_set_id().unwrap())
            .await;

        eprintln!(
            "  🚀 {} successfully created in {}",
            self.stack.name, self.controller.client.region
        );
    }

    /// Executes a CloudFormation change set and waits for stack creation to complete.
    ///
    /// # Arguments
    /// * `change_set_id` - ID of the change set to execute
    ///
    /// # Panics
    /// Panics if change set execution or stack creation fails
    async fn execute_change_set(&self, change_set_id: &str) {
        let execute_change_set_result = self
            .controller
            .client
            .execute_change_set(&self.stack.name, change_set_id)
            .await;

        assert!(
            execute_change_set_result.is_ok(),
            "❌ {} set could not be executed in {} due to error: {}",
            change_set_id,
            self.controller.client.region,
            format!(
                "{}",
                self.handle_change_set_execution_failed(
                    execute_change_set_result.err(),
                    change_set_id
                )
                .await
            )
        );
        let stack_create_result = self
            .controller
            .client
            .wait_for_stack_create_complete(&self.stack.name)
            .await;
        assert!(
            stack_create_result.is_ok(),
            "❌ {} could not be created in {} due to error: {}",
            self.stack.name,
            self.controller.client.region,
            stack_create_result.clone().err().unwrap()
        )
    }

    /// Validates that the stack has the required test tags for safe deletion.
    ///
    /// Prevents accidental deletion of stacks not owned by this test run.
    ///
    /// # Arguments
    /// * `stacks` - Stack description output from AWS
    ///
    /// # Panics
    /// Panics if the stack doesn't have the required test tags
    async fn stack_has_test_tags(&self, stacks: DescribeStacksOutput) {
        let stack_tags = stacks.stacks().first().unwrap().tags();
        assert!(
            stack_tags
                .iter()
                .any(|tag| { tag.key() == self.tag.key() && tag.value() == self.tag.value() }),
            "❌ {} in {} does not have the required tag [{:?}]. The stack will not be deleted. {}",
            self.stack.name,
            self.controller.client.region,
            self.tag,
            format!(
                "The test cannot proceed as there is a naming collision with an existing stack."
            )
        )
    }

    /// Deletes the CloudFormation stack and handles deletion failures.
    ///
    /// Recursively handles deletion failures, particularly S3 bucket cleanup issues.
    /// Will retry deletion after handling known failure scenarios.
    async fn delete_stack(&self) {
        self.controller
            .client
            .delete_stack(&self.stack.name)
            .await
            .ok();
        if let Err(err) = self
            .controller
            .client
            .wait_for_stack_delete_complete(&self.stack.name)
            .await
        {
            // We might have a FailureEvent we can handle. Fail anything else
            assert!(
                err.contains("FailureEvent"),
                "❌ Stack deletion of {} failed in {} due to error: {}",
                self.stack.name,
                self.controller.client.region,
                err
            );

            self.handle_delete_failed().await;
            // All failures we can handle have been handled at this point.
            // If there are more failures, one of the asserts will fail so this won't go into an infinite loop
            Box::pin(self.delete_stack()).await;
        }
    }

    /// Updates stack resources to use Delete retention policies.
    ///
    /// Modifies the CloudFormation template to change all retention policies to Delete,
    /// preventing orphaned resources during test cleanup.
    async fn ensure_retention_policies_are_delete(&self) {
        let template = Template::new(&self.stack.template);
        if !template.has_non_delete_policies() {
            return;
        }
        let updated_template = template.modify_template_retention_policies();
        let update_result = self
            .controller
            .client
            .update_stack(&self.stack.name, &updated_template)
            .await;
        assert!(
            update_result.is_ok(),
            "❌ {} in {} could not be updated with new deletion policies due to error: {}",
            self.stack.name,
            self.controller.client.region,
            update_result.clone().err().unwrap()
        );
        let update_waiter_result = self
            .controller
            .client
            .wait_for_stack_update_complete(&self.stack.name)
            .await;
        assert!(
            update_waiter_result.is_ok(),
            "❌ {} in {} could not be updated with new deletion policies due to error: {}",
            self.stack.name,
            self.controller.client.region,
            update_waiter_result.clone().err().unwrap()
        );
    }
}
