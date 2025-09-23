// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use std::collections::HashMap;

/// Template engine for generating CDK application files with variable substitution.
/// 
/// Provides a simple templating system that supports variable replacement and
/// conditional blocks for generating language-specific CDK application boilerplate.
pub struct AppFile {
    /// Map of template variables to their values
    variables: HashMap<String, String>,
}

impl AppFile {
    /// Creates a new empty AppFile template engine.
    /// 
    /// # Returns
    /// A new `AppFile` instance with no variables set
    pub fn new() -> Self {
        Self {
            variables: HashMap::new(),
        }
    }

    /// Sets a string variable for template substitution.
    /// 
    /// # Arguments
    /// * `key` - Variable name to use in templates (without braces)
    /// * `value` - String value to substitute
    /// 
    /// # Returns
    /// Mutable reference to self for method chaining
    pub fn set(&mut self, key: &str, value: &str) -> &mut Self {
        self.variables.insert(key.to_string(), value.to_string());
        self
    }

    /// Sets a boolean variable for template substitution and conditionals.
    /// 
    /// # Arguments
    /// * `key` - Variable name to use in templates and conditionals
    /// * `value` - Boolean value (converted to "true"/"false" string)
    /// 
    /// # Returns
    /// Mutable reference to self for method chaining
    pub fn set_bool(&mut self, key: &str, value: bool) -> &mut Self {
        self.variables.insert(key.to_string(), value.to_string());
        self
    }

    /// Renders a template string by substituting variables and processing conditionals.
    /// 
    /// Supports two types of template syntax:
    /// - Variable substitution: `{{VARIABLE_NAME}}`
    /// - Conditional blocks: `{{#if VARIABLE_NAME}} content {{else}} alt {{/if}}`
    /// 
    /// # Arguments
    /// * `writer` - Template string containing variables and conditionals
    /// 
    /// # Returns
    /// Rendered string with all variables substituted and conditionals processed
    pub fn render(&self, writer: &str) -> String {
        let mut result = writer.to_string();

        // Handle conditional blocks {{#if VAR}} ... {{/if}} first
        result = self.process_conditionals(result);

        // Replace simple variables {{VAR}}
        for (key, value) in &self.variables {
            let placeholder = format!("{{{{{}}}}}", key);
            result = result.replace(&placeholder, value);
        }

        result
    }

    /// Processes conditional blocks in the template.
    /// 
    /// Handles `{{#if VAR}} ... {{else}} ... {{/if}}` syntax by evaluating
    /// boolean variables and including/excluding content accordingly.
    /// 
    /// # Arguments
    /// * `writer` - Template string potentially containing conditional blocks
    /// 
    /// # Returns
    /// Template string with conditional blocks resolved
    fn process_conditionals(&self, mut writer: String) -> String {
        while let Some(start) = writer.find("{{#if ") {
            if let Some(end_pos) = writer.find("{{/if}}") {
                let condition_end = writer[start..].find("}}").unwrap() + start + 2;
                let condition_name = writer[start + 6..condition_end - 2].trim();

                let should_include = self
                    .variables
                    .get(condition_name)
                    .map(|v| v == "true")
                    .unwrap_or(false);

                let replacement = if let Some(else_pos) = writer[start..end_pos].find("{{else}}") {
                    let else_pos = start + else_pos;
                    // Has else block
                    let if_content = &writer[condition_end..else_pos];
                    let else_content = &writer[else_pos + 8..end_pos];

                    if should_include {
                        if_content.to_string()
                    } else {
                        else_content.to_string()
                    }
                } else {
                    // No else block
                    let content = &writer[condition_end..end_pos];
                    if should_include {
                        content.to_string()
                    } else {
                        String::new()
                    }
                };

                writer.replace_range(start..end_pos + 7, &replacement);
            } else {
                break;
            }
        }

        writer
    }
}
