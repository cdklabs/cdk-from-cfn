// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use super::TemplateDiff;
use crate::{
    filesystem::{Files, Zip},
    Scope,
};

/// Template validation utilities for CDK synthesis verification.
/// 
/// Provides methods to validate that CDK-synthesized CloudFormation templates
/// match expected templates and that templates are consistent across languages.
pub struct Templates;

impl Templates {
    /// Validates that a synthesized CDK template matches the expected CloudFormation template.
    /// 
    /// Compares the CDK-synthesized template with the original CloudFormation template
    /// to ensure the CDK code generates equivalent infrastructure definitions.
    /// 
    /// # Arguments
    /// * `scope` - Test scope containing language and test metadata
    /// * `stack_name` - Name of the stack to validate
    /// 
    /// # Panics
    /// Panics if templates don't match and differences are not acceptable
    pub fn validate(scope: &Scope, stack_name: &str) {
        let expected_content = Zip::extract_template(&scope.test);
        let actual_content = Files::load_actual_synthesized_template(scope, stack_name);

        eprintln!(
            "  ✨ Synthesized App {}::{} passed ({})",
            scope.test,
            scope.lang,
            TemplateDiff::compare(
                expected_content.as_str(),
                actual_content.as_str(),
                &scope.test,
            ),
        );
    }

    /// Validates that synthesized templates are consistent across all specified languages.
    /// 
    /// Ensures that CDK synthesis produces identical CloudFormation templates
    /// regardless of the programming language used to generate the CDK code.
    /// 
    /// # Arguments
    /// * `languages` - List of programming languages to compare
    /// * `scope` - Test scope containing test metadata
    /// * `stack_name` - Name of the stack to validate
    /// 
    /// # Panics
    /// Panics if templates differ between languages
    pub fn validate_all(languages: &Vec<String>, scope: &Scope, stack_name: &str) {
        let templates = Self::get_synthesized_templates(languages, scope, stack_name);
        TemplateDiff::compare_multiple_templates(&templates);
        eprintln!(
            "  ✨ Synthesized App {}::[{}] matches all other apps",
            scope.test,
            languages.join(", ")
        );
    }

    /// Loads synthesized templates for all specified languages.
    /// 
    /// # Arguments
    /// * `languages` - List of programming languages to load templates for
    /// * `scope` - Test scope containing test metadata
    /// * `stack_name` - Name of the stack to load
    /// 
    /// # Returns
    /// Vector of tuples containing (language, template_content) pairs
    fn get_synthesized_templates(
        languages: &Vec<String>,
        scope: &Scope,
        stack_name: &str,
    ) -> Vec<(String, String)> {
        let mut templates = Vec::new();
        for lang in languages {
            let scope = Scope::new(&scope.normalized, &lang);
            templates.push((
                lang.clone(),
                Files::load_actual_synthesized_template(&scope, &stack_name),
            ));
        }
        templates
    }
}
