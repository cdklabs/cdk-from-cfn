// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use std::time::Duration;

use aws_config::{load_defaults, timeout::TimeoutConfig, BehaviorVersion, Region};
use aws_sdk_cloudformation::{
    client::Waiters,
    operation::{
        create_change_set::CreateChangeSetOutput, delete_stack::DeleteStackOutput,
        describe_change_set::DescribeChangeSetOutput,
        describe_stack_events::DescribeStackEventsOutput, describe_stacks::DescribeStacksOutput,
        execute_change_set::ExecuteChangeSetOutput, update_stack::UpdateStackOutput,
    },
    types::{Capability, ChangeSetType, OnStackFailure, StackStatus, Tag},
    Client as CloudFormationClient,
};
use aws_sdk_s3::{
    operation::{
        delete_bucket::DeleteBucketOutput, delete_object::DeleteObjectOutput,
        list_objects_v2::ListObjectsV2Output,
    },
    Client as S3Client,
};
use tokio::time::timeout;

mod errors;
use errors::{extract_error_metadata, extract_s3_error_metadata, extract_waiter_result};

/// AWS client wrapper providing CloudFormation and S3 operations for testing.
///
/// This client encapsulates AWS SDK clients with appropriate timeouts, retry policies,
/// and error handling for end-to-end testing scenarios.
#[derive(Clone)]
pub struct AwsClient {
    /// CloudFormation client for stack operations
    cloudformation: CloudFormationClient,
    /// S3 client for bucket operations during cleanup
    s3: S3Client,
    /// AWS region where operations are performed
    pub region: String,
}

impl AwsClient {
    /// Creates a new AWS client configured for the specified region.
    ///
    /// Configures clients with appropriate timeouts and retry policies for testing:
    /// - 30 second config loading timeout
    /// - 60 second operation timeout
    /// - 30 second operation attempt timeout
    /// - Adaptive retry with 3 max attempts
    ///
    /// # Arguments
    /// * `region` - AWS region for client operations
    ///
    /// # Returns
    /// A new `AwsClient` instance
    ///
    /// # Panics
    /// Panics if AWS configuration loading times out
    pub async fn new(region: &str) -> Self {
        let config_with_timeout_result = timeout(
            Duration::from_secs(30),
            load_defaults(BehaviorVersion::latest()),
        )
        .await;

        // If we can't generate a client the test cannot continue so using assert to cause an immediate failure
        assert!(
            config_with_timeout_result.is_ok(),
            "❌ AWS config loading timed out after 30 seconds: {:?}",
            config_with_timeout_result.err().unwrap()
        );

        let config = config_with_timeout_result
            .unwrap()
            .into_builder()
            .region(Region::new(region.to_string()))
            .timeout_config(
                TimeoutConfig::builder()
                    .operation_timeout(Duration::from_secs(60))
                    .operation_attempt_timeout(Duration::from_secs(30))
                    .build(),
            )
            .retry_config(aws_config::retry::RetryConfig::adaptive().with_max_attempts(3))
            .build();

        Self {
            cloudformation: CloudFormationClient::new(&config),
            s3: S3Client::new(&config),
            region: region.to_string(),
        }
    }

    /// Creates a CloudFormation change set with full capabilities enabled.
    ///
    /// # Arguments
    /// * `stack_name` - Name of the CloudFormation stack
    /// * `template_body` - CloudFormation template JSON/YAML content
    /// * `tag` - Tag to apply to the stack
    /// * `change_set_type` - Type of change set (Create or Update)
    /// * `change_set_name` - Name for the change set
    /// * `on_stack_failure` - Action to take if stack creation fails
    ///
    /// # Returns
    /// Result containing change set creation output or error message
    pub async fn create_change_set(
        &self,
        stack_name: &str,
        template_body: &str,
        tag: Tag,
        change_set_type: ChangeSetType,
        change_set_name: &str,
        on_stack_failure: OnStackFailure,
    ) -> Result<CreateChangeSetOutput, String> {
        extract_error_metadata(
            self.cloudformation
                .create_change_set()
                .change_set_name(change_set_name)
                .stack_name(stack_name)
                .template_body(template_body)
                .change_set_type(change_set_type)
                .capabilities(Capability::CapabilityIam)
                .capabilities(Capability::CapabilityNamedIam)
                .capabilities(Capability::CapabilityAutoExpand)
                .tags(tag)
                .import_existing_resources(true)
                .on_stack_failure(on_stack_failure)
                .send()
                .await,
        )
    }

    /// Waits for a change set to reach CREATE_COMPLETE status.
    ///
    /// # Arguments
    /// * `stack_name` - Name of the CloudFormation stack
    /// * `change_set_name` - Name of the change set to wait for
    ///
    /// # Returns
    /// Result containing change set description or error message
    pub async fn wait_for_change_set_create_complete(
        &self,
        stack_name: &str,
        change_set_name: &str,
    ) -> Result<DescribeChangeSetOutput, String> {
        extract_waiter_result(
            self.cloudformation
                .wait_until_change_set_create_complete()
                .stack_name(stack_name)
                .change_set_name(change_set_name)
                .include_property_values(true)
                .wait(Duration::from_secs(300))
                .await,
        )
    }

    /// Waits for a stack to reach CREATE_COMPLETE status.
    ///
    /// # Arguments
    /// * `stack_name` - Name of the CloudFormation stack
    ///
    /// # Returns
    /// Result containing stack description or error message
    pub async fn wait_for_stack_create_complete(
        &self,
        stack_name: &str,
    ) -> Result<DescribeStacksOutput, String> {
        extract_waiter_result(
            self.cloudformation
                .wait_until_stack_create_complete()
                .stack_name(stack_name)
                .wait(Duration::from_secs(1800))
                .await,
        )
    }

    /// Waits for a stack to reach UPDATE_COMPLETE status.
    ///
    /// # Arguments
    /// * `stack_name` - Name of the CloudFormation stack
    ///
    /// # Returns
    /// Result containing stack description or error message
    pub async fn wait_for_stack_update_complete(
        &self,
        stack_name: &str,
    ) -> Result<DescribeStacksOutput, String> {
        extract_waiter_result(
            self.cloudformation
                .wait_until_stack_update_complete()
                .stack_name(stack_name)
                .wait(Duration::from_secs(1800))
                .await,
        )
    }

    /// Waits for a stack to reach DELETE_COMPLETE status or be deleted.
    ///
    /// Handles cases where the stack no longer exists and treats deletion failures
    /// as recoverable errors that can be handled by the caller.
    ///
    /// When the deletion is complete, this typically returns an err so that gets translated
    /// into Ok(()). Failure Events are handled.
    ///
    /// # Arguments
    /// * `stack_name` - Name of the CloudFormation stack
    ///
    /// # Returns
    /// Result indicating successful deletion or error details for handling
    pub async fn wait_for_stack_delete_complete(&self, stack_name: &str) -> Result<(), String> {
        match extract_waiter_result(
            self.cloudformation
                .wait_until_stack_delete_complete()
                .stack_name(stack_name)
                .wait(Duration::from_secs(1800))
                .await,
        ) {
            Err(e) => {
                if e.contains("does not exist") {
                    Ok(())
                } else {
                    Err(e)
                }
            }
            Ok(output) => {
                let stacks = output.stacks.clone().unwrap();
                let stack = stacks.first().unwrap();
                if stack.stack_status.clone().unwrap() != StackStatus::DeleteComplete {
                    let failure = stack.stack_status_reason.clone().unwrap();
                    Err(format!("FailureEvent: {}", failure))
                } else {
                    Ok(())
                }
            }
        }
    }

    /// Executes a CloudFormation change set.
    ///
    /// # Arguments
    /// * `stack_name` - Name of the CloudFormation stack
    /// * `change_set_name` - Name of the change set to execute
    ///
    /// # Returns
    /// Result containing execution output or error message
    pub async fn execute_change_set(
        &self,
        stack_name: &str,
        change_set_name: &str,
    ) -> Result<ExecuteChangeSetOutput, String> {
        extract_error_metadata(
            self.cloudformation
                .execute_change_set()
                .change_set_name(change_set_name)
                .retain_except_on_create(true)
                .stack_name(stack_name)
                .send()
                .await,
        )
    }

    /// Describes a CloudFormation stack.
    ///
    /// # Arguments
    /// * `stack_name` - Name of the CloudFormation stack
    ///
    /// # Returns
    /// Result containing stack description or error message
    pub async fn describe_stacks(&self, stack_name: &str) -> Result<DescribeStacksOutput, String> {
        extract_error_metadata(
            self.cloudformation
                .describe_stacks()
                .stack_name(stack_name)
                .send()
                .await,
        )
    }

    /// Initiates deletion of a CloudFormation stack.
    ///
    /// # Arguments
    /// * `stack_name` - Name of the CloudFormation stack
    ///
    /// # Returns
    /// Result containing deletion output or error message
    pub async fn delete_stack(&self, stack_name: &str) -> Result<DeleteStackOutput, String> {
        extract_error_metadata(
            self.cloudformation
                .delete_stack()
                .stack_name(stack_name)
                .send()
                .await,
        )
    }

    /// Updates a CloudFormation stack with a new template.
    ///
    /// # Arguments
    /// * `stack_name` - Name of the CloudFormation stack
    /// * `template_body` - New CloudFormation template JSON/YAML content
    ///
    /// # Returns
    /// Result containing update output or error message
    pub async fn update_stack(
        &self,
        stack_name: &str,
        template_body: &str,
    ) -> Result<UpdateStackOutput, String> {
        extract_error_metadata(
            self.cloudformation
                .update_stack()
                .stack_name(stack_name)
                .template_body(template_body)
                .capabilities(Capability::CapabilityIam)
                .capabilities(Capability::CapabilityNamedIam)
                .capabilities(Capability::CapabilityAutoExpand)
                .send()
                .await,
        )
    }

    /// Retrieves events for a CloudFormation stack.
    ///
    /// # Arguments
    /// * `stack_name` - Name of the CloudFormation stack
    ///
    /// # Returns
    /// Result containing stack events or error message
    pub async fn describe_stack_events(
        &self,
        stack_name: &str,
    ) -> Result<DescribeStackEventsOutput, String> {
        extract_error_metadata(
            self.cloudformation
                .describe_stack_events()
                .stack_name(stack_name)
                .send()
                .await,
        )
    }

    /// Lists objects in an S3 bucket.
    ///
    /// # Arguments
    /// * `bucket_name` - Name of the S3 bucket
    ///
    /// # Returns
    /// Result containing object list or error message
    pub async fn list_objects_v2(&self, bucket_name: &str) -> Result<ListObjectsV2Output, String> {
        extract_s3_error_metadata(self.s3.list_objects_v2().bucket(bucket_name).send().await)
    }

    /// Deletes an object from an S3 bucket.
    ///
    /// # Arguments
    /// * `bucket_name` - Name of the S3 bucket
    /// * `key` - Key of the object to delete
    ///
    /// # Returns
    /// Result containing deletion output or error message
    pub async fn delete_object(
        &self,
        bucket_name: &str,
        key: &str,
    ) -> Result<DeleteObjectOutput, String> {
        extract_s3_error_metadata(
            self.s3
                .delete_object()
                .bucket(bucket_name)
                .key(key)
                .send()
                .await,
        )
    }

    /// Deletes an S3 bucket.
    ///
    /// # Arguments
    /// * `bucket_name` - Name of the S3 bucket to delete
    ///
    /// # Returns
    /// Result containing deletion output or error message
    pub async fn delete_bucket(&self, bucket_name: &str) -> Result<DeleteBucketOutput, String> {
        extract_s3_error_metadata(self.s3.delete_bucket().bucket(bucket_name).send().await)
    }

    /// Describes a CloudFormation change set.
    ///
    /// # Arguments
    /// * `stack_name` - Name of the CloudFormation stack
    /// * `change_set_name` - Name of the change set to describe
    ///
    /// # Returns
    /// Result containing change set description or error message
    pub async fn describe_change_set(
        &self,
        stack_name: &str,
        change_set_name: &str,
    ) -> Result<DescribeChangeSetOutput, String> {
        extract_error_metadata(
            self.cloudformation
                .describe_change_set()
                .stack_name(stack_name)
                .change_set_name(change_set_name)
                .send()
                .await,
        )
    }
}
