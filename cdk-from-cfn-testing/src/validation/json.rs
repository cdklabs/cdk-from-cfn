// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use std::collections::BTreeMap;

use serde_json::{Error, Value};

/// JSON normalization utilities for CloudFormation template comparison.
/// 
/// Provides methods to normalize JSON structures for semantic comparison,
/// ignoring irrelevant differences like key ordering and certain metadata fields.
pub struct JSON;

impl JSON {
    /// Determines if a JSON key should be ignored during template comparisons.
    /// 
    /// Ignores CloudFormation metadata fields that don't affect infrastructure:
    /// - AWSTemplateFormatVersion: Version specification
    /// - Description: Template description text
    /// 
    /// # Arguments
    /// * `key` - JSON key to check
    /// 
    /// # Returns
    /// `true` if the key should be ignored, `false` otherwise
    pub fn is_ignored_key(key: &str) -> bool {
        key == "AWSTemplateFormatVersion" || key == "Description"
    }
}

impl JSON {
    /// Recursively normalizes JSON values with depth-aware key filtering.
    /// 
    /// Sorts object keys alphabetically and applies filtering rules based on
    /// whether the value is at the top level of the template.
    /// 
    /// # Arguments
    /// * `value` - JSON value to normalize
    /// * `is_top_level` - Whether this is a top-level template field
    /// 
    /// # Returns
    /// Normalized JSON value with sorted keys and filtered fields
    fn normalize_with_depth(value: &Value, is_top_level: bool) -> Value {
        match value {
            Value::Object(map) => {
                let mut sorted_map = BTreeMap::new();
                for (k, v) in map {
                    let should_ignore = if is_top_level {
                        Self::is_ignored_key(k)
                    } else {
                        k == "AWSTemplateFormatVersion"
                    };
                    if !should_ignore {
                        sorted_map.insert(k.clone(), Self::normalize_with_depth(v, false));
                    }
                }
                Value::Object(sorted_map.into_iter().collect())
            }
            Value::Array(arr) => Value::Array(arr.iter().map(|v| Self::normalize_with_depth(v, false)).collect()),
            _ => value.clone(),
        }
    }

    /// Normalizes a JSON value starting from the top level.
    /// 
    /// # Arguments
    /// * `value` - JSON value to normalize
    /// 
    /// # Returns
    /// Normalized JSON value
    fn normalize(value: &Value) -> Value {
        Self::normalize_with_depth(value, true)
    }

    /// Parses and normalizes a JSON string for template comparison.
    /// 
    /// Parses the JSON string and applies normalization to ensure consistent
    /// structure for semantic comparison, ignoring formatting and key order.
    /// 
    /// # Arguments
    /// * `json` - JSON string to parse and normalize
    /// 
    /// # Returns
    /// Result containing normalized JSON value or parsing error
    pub fn parse(json: &str) -> Result<Value, Error> {
        let from_str: Value = serde_json::from_str(json)?;
        Ok(Self::normalize(&from_str))
    }
}
