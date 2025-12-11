// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use pretty_assertions::assert_eq;
use serde_json::Value;

use crate::{
    filesystem::{Files, Zip},
    validation::json::JSON,
};

/// Advanced JSON diff utility for CloudFormation template comparison.
///
/// Provides semantic comparison of JSON structures with detailed reporting
/// of differences, acceptable diff management, and multi-template validation.
pub struct TemplateDiff;

impl TemplateDiff {
    /// Generates a detailed diff report showing specific differences between JSON structures.
    ///
    /// Recursively compares JSON values and produces human-readable output
    /// highlighting missing keys, extra keys, and value mismatches.
    ///
    /// # Arguments
    /// * `expected` - Expected JSON structure
    /// * `actual` - Actual JSON structure
    ///
    /// # Returns
    /// Formatted string describing all differences found
    pub fn report(expected: &Value, actual: &Value) -> String {
        let mut diff_lines = Vec::new();
        Self::find_differences(expected, actual, "", &mut diff_lines);

        if diff_lines.is_empty() {
            "No differences found".to_string()
        } else {
            format!("Differences found:\n{}", diff_lines.join("\n\n"))
        }
    }

    /// Recursively traverses JSON structures to identify all differences.
    ///
    /// Handles objects, arrays, and primitive values, tracking the path
    /// to each difference for detailed reporting.
    ///
    /// # Arguments
    /// * `expected` - Expected JSON value
    /// * `actual` - Actual JSON value
    /// * `path` - Current path in the JSON structure
    /// * `diff_lines` - Accumulator for difference descriptions
    fn find_differences(
        expected: &Value,
        actual: &Value,
        path: &str,
        diff_lines: &mut Vec<String>,
    ) {
        match (expected, actual) {
            (Value::Object(exp_map), Value::Object(act_map)) => {
                for (key, exp_val) in exp_map {
                    let current_path = Self::build_path(path, key);
                    match act_map.get(key) {
                        Some(act_val) => {
                            Self::find_differences(exp_val, act_val, &current_path, diff_lines)
                        }
                        None => {
                            Self::add_missing_key_diff(&current_path, exp_val, diff_lines);
                        }
                    }
                }
                for key in act_map.keys() {
                    if !exp_map.contains_key(key) {
                        let current_path = Self::build_path(path, key);
                        Self::add_extra_key_diff(
                            &current_path,
                            act_map.get(key).unwrap(),
                            diff_lines,
                        );
                    }
                }
            }
            (Value::Array(exp_arr), Value::Array(act_arr)) => {
                if exp_arr.len() != act_arr.len() {
                    diff_lines.push(format!(
                        "Array length mismatch at {}: expected {}, got {}",
                        path,
                        exp_arr.len(),
                        act_arr.len()
                    ));
                }
                for (i, (exp_item, act_item)) in exp_arr.iter().zip(act_arr.iter()).enumerate() {
                    let current_path = format!("{}[{}]", path, i);
                    Self::find_differences(exp_item, act_item, &current_path, diff_lines);
                }
            }
            (exp, act) if exp != act => {
                Self::add_value_mismatch_diff(path, exp, act, diff_lines);
            }
            _ => {}
        }
    }

    /// Constructs a dot-notation path for nested JSON keys.
    ///
    /// # Arguments
    /// * `base` - Base path (empty for root level)
    /// * `key` - Key to append to the path
    ///
    /// # Returns
    /// Dot-notation path string
    fn build_path(base: &str, key: &str) -> String {
        if base.is_empty() {
            key.to_string()
        } else {
            format!("{}.{}", base, key)
        }
    }

    /// Formats JSON values for human-readable output.
    ///
    /// # Arguments
    /// * `value` - JSON value to format
    ///
    /// # Returns
    /// Pretty-printed JSON string with fallback to debug format
    fn pretty_print_json(value: &Value) -> String {
        serde_json::to_string_pretty(value).unwrap_or_else(|_| format!("{:?}", value))
    }

    /// Adds consistent indentation to multi-line text.
    ///
    /// # Arguments
    /// * `text` - Text to indent
    /// * `spaces` - Number of spaces for indentation
    ///
    /// # Returns
    /// Indented text with specified spacing
    fn indent(text: &str, spaces: usize) -> String {
        let indent_str = " ".repeat(spaces);
        text.lines()
            .map(|line| format!("{}{}", indent_str, line))
            .collect::<Vec<_>>()
            .join("\n")
    }

    /// Records a missing key difference in the diff report.
    ///
    /// # Arguments
    /// * `path` - Path to the missing key
    /// * `value` - Expected value that was missing
    /// * `diff_lines` - Accumulator for difference descriptions
    fn add_missing_key_diff(path: &str, value: &Value, diff_lines: &mut Vec<String>) {
        let pretty = Self::pretty_print_json(value);
        diff_lines.push(format!(
            "- Missing key: {}\n  Expected:\n{}",
            path,
            Self::indent(&pretty, 4)
        ));
    }

    /// Records an extra key difference in the diff report.
    ///
    /// # Arguments
    /// * `path` - Path to the extra key
    /// * `value` - Actual value that was unexpected
    /// * `diff_lines` - Accumulator for difference descriptions
    fn add_extra_key_diff(path: &str, value: &Value, diff_lines: &mut Vec<String>) {
        let pretty = Self::pretty_print_json(value);
        diff_lines.push(format!(
            "+ Extra key: {}\n  Actual:\n{}",
            path,
            Self::indent(&pretty, 4)
        ));
    }

    /// Records a value mismatch difference in the diff report.
    ///
    /// # Arguments
    /// * `path` - Path to the mismatched value
    /// * `expected` - Expected value
    /// * `actual` - Actual value
    /// * `diff_lines` - Accumulator for difference descriptions
    fn add_value_mismatch_diff(
        path: &str,
        expected: &Value,
        actual: &Value,
        diff_lines: &mut Vec<String>,
    ) {
        let exp_pretty = Self::pretty_print_json(expected);
        let act_pretty = Self::pretty_print_json(actual);
        diff_lines.push(format!(
            "Value mismatch at {}:\n  Expected:\n{}\n  Actual:\n{}",
            path,
            Self::indent(&exp_pretty, 4),
            Self::indent(&act_pretty, 4)
        ));
    }

    /// Performs semantic comparison of CloudFormation templates with acceptable diff support.
    ///
    /// Normalizes both templates and compares them semantically. Supports acceptable
    /// diff files for known differences and snapshot updating during development.
    ///
    /// # Arguments
    /// * `expected_content` - Expected template content
    /// * `actual_content` - Actual template content
    /// * `test_name` - Name of the test for diff file management
    ///
    /// # Returns
    /// Success reason string describing the comparison result
    ///
    /// # Panics
    /// Panics if templates differ and differences are not acceptable
    pub fn compare<'a>(
        expected_content: &'a str,
        actual_content: &'a str,
        test_name: &'a str,
    ) -> &'a str {
        let expected_json = Self::normalize_content(expected_content, "expected");
        let actual_json = Self::normalize_content(actual_content, "actual");

        // First check to see if the normalized templates are the exact same
        if expected_json == actual_json {
            if Files::acceptable_diff_exists(test_name) {
                Files::delete_acceptable_diff(test_name);
            }
            return SuccessReasons::MATCHES.as_str();
        }

        // Generates a report of the diff between the two normalized templates
        let current_diff = TemplateDiff::report(&expected_json, &actual_json);

        // Update diff file when update_snapshots is enabled
        if cfg!(feature = "update-snapshots") {
            Files::write_acceptable_diff(test_name, &current_diff);
            return SuccessReasons::UPDATED.as_str();
        }

        // Check if existing diff matches current diff
        Self::check_diff_acceptable(test_name, &current_diff).as_str()
    }

    /// Validates that multiple templates are semantically identical.
    ///
    /// Compares the first template against all others to ensure consistency
    /// across different language implementations.
    ///
    /// # Arguments
    /// * `templates` - Vector of (language, template_content) pairs
    ///
    /// # Panics
    /// Panics if any template differs from the first one
    pub fn compare_multiple_templates(templates: &Vec<(String, String)>) {
        let (first_lang, first_template) = match templates.first() {
            Some(first) => first,
            None => return,
        };

        let first_json = TemplateDiff::normalize_content(first_template, first_lang);
        for (lang, template) in templates.iter().skip(1) {
            let current_json = TemplateDiff::normalize_content(template, lang);

            assert!(
                first_json == current_json,
                "  ❌ Synthesized CDK apps do not match between {} and {}:\n{}",
                first_lang,
                lang,
                TemplateDiff::report(&first_json, &current_json)
            );
        }
    }

    /// Normalizes template content for semantic comparison.
    ///
    /// # Arguments
    /// * `content` - Template content to normalize
    /// * `context` - Context description for error reporting
    ///
    /// # Returns
    /// Normalized JSON value ready for comparison
    ///
    /// # Panics
    /// Panics if the content cannot be parsed as valid JSON
    pub fn normalize_content(content: &str, context: &str) -> Value {
        let result = JSON::parse(content);
        assert!(
            result.is_ok(),
            "❌ Template from {context} could not be parsed: {:?}",
            result.err().unwrap()
        );
        result.unwrap()
    }

    /// Checks if current differences match the acceptable diff file.
    ///
    /// # Arguments
    /// * `test_name` - Name of the test to check
    /// * `current_diff` - Current diff content to validate
    ///
    /// # Returns
    /// Success reason indicating acceptable differences
    ///
    /// # Panics
    /// Panics if no acceptable diff exists or current diff doesn't match
    fn check_diff_acceptable(test_name: &str, current_diff: &str) -> SuccessReasons {
        let acceptable_diff = Zip::extract_acceptable_diff(test_name);
        assert!(
            acceptable_diff.is_ok(),
            "❌ Template differences found (no acceptable diff file):\n{current_diff}"
        );

        // This is showing a diff of a diff. Mind bending!
        assert_eq!(
            acceptable_diff.unwrap().trim(),
            current_diff.trim(),
            "❌ Template differences are not acceptable:",
        );

        SuccessReasons::ACCEPTABLE
    }
}

/// Enumeration of possible success reasons for template comparison.
///
/// Indicates why a template comparison succeeded, providing context
/// for different validation scenarios.
enum SuccessReasons {
    /// Templates match exactly with no differences
    MATCHES,
    /// Acceptable diff file was updated during snapshot mode
    UPDATED,
    /// Differences exist but are documented as acceptable
    ACCEPTABLE,
}

impl SuccessReasons {
    /// Returns a human-readable description of the success reason.
    ///
    /// # Returns
    /// Static string describing why the comparison succeeded
    fn as_str(&self) -> &'static str {
        match self {
            SuccessReasons::MATCHES => "templates match exactly",
            SuccessReasons::UPDATED => "acceptable diff was updated",
            SuccessReasons::ACCEPTABLE => "all differences are acceptable",
        }
    }
}
