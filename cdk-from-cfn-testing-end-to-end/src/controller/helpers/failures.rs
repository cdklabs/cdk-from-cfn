// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use aws_sdk_cloudformation::operation::{
    describe_change_set::DescribeChangeSetOutput, describe_stack_events::DescribeStackEventsOutput,
};

use crate::controller::stack::TestFixtureController;

/// Represents a CloudFormation stack failure event.
///
/// Contains details about a specific resource failure during stack operations,
/// used for error analysis and automated failure handling.
#[derive(Debug)]
pub(crate) struct FailureEvent {
    /// The AWS resource type that failed (e.g., "AWS::S3::Bucket")
    pub resource_type: String,
    /// The physical ID of the failed resource
    pub physical_id: String,
    /// The reason for the resource failure
    pub resource_status_reason: String,
}

impl TestFixtureController<'_> {
    /// Searches stack events for the most recent failure event.
    ///
    /// # Arguments
    /// * `events` - Stack events from CloudFormation
    ///
    /// # Returns
    /// The most recent failure event, if any
    async fn look_for_stack_failure_event(
        events: DescribeStackEventsOutput,
    ) -> Option<FailureEvent> {
        events
            .stack_events()
            .iter()
            .filter(|event| {
                event
                    .resource_status()
                    .is_some_and(|status| status.as_str().contains("FAILED"))
            })
            .last()
            .map(|event| FailureEvent {
                resource_type: event.resource_type().unwrap_or("Unknown").to_string(),
                physical_id: event
                    .physical_resource_id()
                    .unwrap_or("Unknown")
                    .to_string(),
                resource_status_reason: event
                    .resource_status_reason()
                    .unwrap_or("Unknown")
                    .to_string(),
            })
    }

    /// Handles failures during change set execution.
    ///
    /// Provides detailed error information when change set execution fails,
    /// particularly for change sets in FAILED status.
    ///
    /// These failures mostly happen on create due to pre-existing resources
    /// colliding with resources in the test. In this case a error message is
    /// returned because we do not know if it is safe to delete those resources.
    ///
    /// # Arguments
    /// * `err` - Optional error message from the failed execution
    /// * `change_set_id` - ID of the failed change set
    ///
    /// # Returns
    /// Detailed error message for debugging
    pub async fn handle_change_set_execution_failed(
        &self,
        err: Option<String>,
        change_set_id: &str,
    ) -> String {
        if err
            .clone()
            .unwrap()
            .contains("cannot be executed in its current status of [FAILED]")
        {
            let description = self.describe_change_set(change_set_id).await;
            format!(
                "{}. You may need to manually delete these resources.",
                description.status_reason.unwrap()
            )
        } else {
            err.unwrap()
        }
    }

    /// Handles stack deletion failures by analyzing and resolving known issues.
    ///
    /// Currently handles S3 bucket deletion failures by emptying buckets before deletion.
    /// Can be extended to handle other types of deletion failures.
    ///
    /// # Panics
    /// Panics if no failure events are found or if the failure type is not handled
    pub async fn handle_delete_failed(&self) {
        let events = self.get_stack_events().await;
        let failure_event = Self::look_for_stack_failure_event(events).await;

        assert!(
            failure_event.is_some(),
            "❌ Stack deletion failed for {} in {} but no failure events were found",
            self.controller.client.region,
            &self.stack.name
        );
        let failure = failure_event.unwrap();
        // There may be additional reasons we can handle in the future,
        // but this is the only known one right now
        assert!(
            Self::is_s3_bucket_not_empty_error(&failure),
            "❌ Stack deletion failed for {} in {}:{} ",
            self.stack.name,
            self.controller.client.region,
            format!(
                "\n\tPhysical Id: {}\n\tResource Type: {}\n\tResource Status Reason: {}\n\n",
                failure.physical_id, failure.resource_type, failure.resource_status_reason
            ),
        );
        self.empty_and_delete_bucket(&failure.physical_id).await;
    }

    /// Retrieves stack events for failure analysis.
    ///
    /// # Returns
    /// Stack events from CloudFormation
    ///
    /// # Panics
    /// Panics if stack events cannot be retrieved
    async fn get_stack_events(&self) -> DescribeStackEventsOutput {
        let events = self
            .controller
            .client
            .describe_stack_events(&self.stack.name)
            .await;
        assert!(
            events.is_ok(),
            "❌ Could not retrieve stack events for {} in {} to determine the reason for the failure.{}",
            self.stack.name,
            self.controller.client.region,
            events.err().unwrap()
        );
        events.unwrap()
    }

    /// Describes a change set for failure analysis.
    ///
    /// # Arguments
    /// * `change_set_id` - ID of the change set to describe
    ///
    /// # Returns
    /// Change set description from CloudFormation
    ///
    /// # Panics
    /// Panics if change set description cannot be retrieved
    async fn describe_change_set(&self, change_set_id: &str) -> DescribeChangeSetOutput {
        let describe_change_set_result = self
            .controller
            .client
            .describe_change_set(&self.stack.name, change_set_id)
            .await;
        assert!(
            describe_change_set_result.is_ok(),
            "❌ Could not get change set details for {change_set_id} in {}: {}",
            self.controller.client.region,
            describe_change_set_result.err().unwrap()
        );

        describe_change_set_result.unwrap()
    }

    /// Determines if a failure event represents an S3 bucket not empty error.
    ///
    /// # Arguments
    /// * `failure` - The failure event to analyze
    ///
    /// # Returns
    /// `true` if this is an S3 bucket not empty error, `false` otherwise
    fn is_s3_bucket_not_empty_error(failure: &FailureEvent) -> bool {
        failure.resource_type == "AWS::S3::Bucket"
            && failure
                .resource_status_reason
                .contains("The bucket you tried to delete is not empty")
    }

    /// Empties and deletes an S3 bucket to resolve deletion failures.
    ///
    /// Continuously attempts to delete all objects in the bucket and then
    /// delete the bucket itself until successful or the bucket no longer exists.
    ///
    /// # Arguments
    /// * `bucket_name` - Name of the S3 bucket to empty and delete
    async fn empty_and_delete_bucket(&self, bucket_name: &str) {
        loop {
            match self.controller.client.list_objects_v2(bucket_name).await {
                Ok(output) => {
                    for object in output.contents() {
                        if let Some(tag_key) = object.key() {
                            match self
                                .controller
                                .client
                                .delete_object(bucket_name, tag_key)
                                .await
                            {
                                Ok(_) => {}
                                Err(_) => {
                                    continue;
                                }
                            }
                        }
                    }
                }
                Err(e) if e.contains("NoSuchBucket") => {
                    break;
                }
                Err(_) => {}
            }

            match self.controller.client.delete_bucket(bucket_name).await {
                Ok(_) => break,
                Err(e) if e.contains("NoSuchBucket") => {
                    break;
                }
                Err(_) => {
                    continue;
                }
            }
        }
    }
}
