// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use serde_json::{from_str, to_string, Map, Value};

const DELETION_POLICY: &'static str = "DeletionPolicy";
const UPDATE_REPLACE_POLICY: &'static str = "UpdateReplacePolicy";
const RESOURCES: &'static str = "Resources";
const DELETE: &'static str = "Delete";

/// Utility for parsing and modifying CloudFormation templates.
/// 
/// This struct provides methods to analyze and modify CloudFormation templates,
/// particularly for updating retention policies to ensure clean resource deletion.
pub struct Template {
    /// The CloudFormation template as a JSON string
    template: String,
}

impl Template {
    /// Creates a new Template instance from a CloudFormation template string.
    /// 
    /// # Arguments
    /// * `template` - CloudFormation template as JSON/YAML string
    /// 
    /// # Returns
    /// A new `Template` instance
    pub fn new(template: &str) -> Self {
        Self {
            template: template.to_string(),
        }
    }
    
    /// Modifies the template to set all retention policies to Delete.
    /// 
    /// Updates both DeletionPolicy and UpdateReplacePolicy for all resources
    /// to ensure clean deletion during test cleanup.
    /// 
    /// # Returns
    /// Modified template as a JSON string with updated retention policies
    /// 
    /// # Panics
    /// Panics if template parsing or serialization fails
    pub fn modify_template_retention_policies(&self) -> String {
        let mut template_json: Value = self.parse_template();

        if let Some(resources) = template_json
            .get_mut(RESOURCES)
            .and_then(|r| r.as_object_mut())
        {
            for resource in resources.values_mut() {
                if let Some(resource_obj) = resource.as_object_mut() {
                    Self::update_retention_policy(resource_obj, DELETION_POLICY);
                    Self::update_retention_policy(resource_obj, UPDATE_REPLACE_POLICY);
                }
            }
        }

        Self::serialize_template(&template_json)
    }

    /// Parses the CloudFormation template from JSON string to Value.
    /// 
    /// # Returns
    /// Parsed JSON value representing the template
    /// 
    /// # Panics
    /// Panics if the template cannot be parsed as valid JSON
    fn parse_template(&self) -> Value {
        let result = from_str(&self.template);
        assert!(
            result.is_ok(),
            "❌ Failed to parse template: {:?}",
            result.err()
        );
        result.unwrap()
    }

    /// Serializes a JSON value back to a CloudFormation template string.
    /// 
    /// # Arguments
    /// * `template_json` - JSON value representing the template
    /// 
    /// # Returns
    /// Serialized template as a JSON string
    /// 
    /// # Panics
    /// Panics if the template cannot be serialized to JSON
    fn serialize_template(template_json: &Value) -> String {
        let result = to_string(template_json);
        assert!(
            result.is_ok(),
            "❌ Failed to serialize template: {:?}",
            result.err()
        );
        result.unwrap()
    }

    /// Updates a specific retention policy for a resource to Delete.
    /// 
    /// # Arguments
    /// * `resource_obj` - Mutable reference to the resource object
    /// * `policy_key` - The policy key to update (DeletionPolicy or UpdateReplacePolicy)
    fn update_retention_policy(resource_obj: &mut Map<String, Value>, policy_key: &str) {
        if resource_obj.contains_key(policy_key) {
            resource_obj.insert(policy_key.to_string(), Value::String(DELETE.to_string()));
        }
    }

    /// Checks if the template contains any non-Delete retention policies.
    /// 
    /// Scans all resources in the template to determine if any have retention
    /// policies other than Delete, which would prevent clean resource deletion.
    /// 
    /// # Returns
    /// `true` if any resources have non-Delete retention policies, `false` otherwise
    pub fn has_non_delete_policies(&self) -> bool {
        if let Ok(template_json) = from_str::<Value>(&self.template) {
            if let Some(resources) = template_json.get(RESOURCES).and_then(|r| r.as_object()) {
                return resources.values().any(|resource| {
                    resource
                        .get(DELETION_POLICY)
                        .and_then(|p| p.as_str())
                        .is_some_and(|p| p != DELETE)
                        || resource
                            .get(UPDATE_REPLACE_POLICY)
                            .and_then(|p| p.as_str())
                            .is_some_and(|p| p != DELETE)
                });
            }
        }
        false
    }
}
