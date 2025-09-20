// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use aws_sdk_cloudformation::operation::describe_change_set::DescribeChangeSetOutput;

/// Utility for extracting and formatting differences from CloudFormation change sets.
/// 
/// This struct provides methods to analyze change sets and generate human-readable
/// diff output for debugging and validation purposes.
pub struct Diff;

impl Diff {
    /// Extracts and formats differences from a CloudFormation change set.
    /// 
    /// Analyzes the change set to identify resource changes, including actions
    /// (Create, Update, Delete) and specific property modifications.
    /// 
    /// # Arguments
    /// * `change_set` - CloudFormation change set description
    /// 
    /// # Returns
    /// `Some(String)` containing formatted diff if changes exist, `None` if no changes
    pub fn get_change_set_diff(change_set: DescribeChangeSetOutput) -> Option<String> {
        let mut result = String::new();
        if let Some(changes) = change_set.changes {
            for change in changes {
                if let Some(resource_change) = change.resource_change {
                    let action = resource_change.action.unwrap_or("Unknown".into());
                    let logical_id = resource_change
                        .logical_resource_id
                        .unwrap_or("Unknown".into());
                    let resource_type = resource_change.resource_type.unwrap_or("Unknown".into());

                    result.push_str(&format!(
                        "    Action: {} for {} ({})\n",
                        action, logical_id, resource_type
                    ));

                    if let Some(details) = resource_change.details {
                        for detail in details {
                            if let Some(target) = detail.target {
                                let attribute = target.attribute.unwrap_or("Unknown".into());
                                let before = target.before_value.unwrap_or("<none>".into());
                                let after = target.after_value.unwrap_or("<none>".into());
                                result.push_str(&format!(
                                    "      {}: {} → {}\n",
                                    attribute, before, after
                                ));
                            }
                        }
                    }
                }
            }
        }
        if result.is_empty() {
            None
        } else {
            Some(result)
        }
    }
}
