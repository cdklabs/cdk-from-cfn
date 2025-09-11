// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

mod bootstrap;
mod config;
mod filesystem;
mod synth;
mod validation;

pub use config::{EndToEndTestStack, Language, Scope, Stack};
pub use synth::{CdkAppTestCase, CdkAppTestGroup};

// Re-export synth types
pub use synth::{SkipSynthList, TestFilter};

use self::{
    filesystem::{Files, Zip},
    validation::StackDiff,
};

/// Test case for validating CDK stack generation against expected output.
///
/// This struct manages the comparison between generated CDK stacks and expected
/// reference implementations, handling file I/O and validation workflows and is
/// shared across both sets of tests that test stack generation.
#[derive(Clone)]
pub struct StackTestCase<'a> {
    /// Test scope containing language and test metadata
    pub scope: Scope,
    /// Expected stack content from reference implementation
    pub(crate) expected_stack: String,
    /// Generated stack content from CDK conversion
    pub(crate) generated_stack: String,
    /// Name of the stack being tested
    pub(crate) stack_name: &'a str,
}

impl<'a> StackTestCase<'a> {
    /// Creates a new stack test case by generating and comparing stack output.
    ///
    /// # Arguments
    /// * `test_path` - Path identifying the test case
    /// * `lang` - Programming language for stack generation
    /// * `stack_name` - Name of the stack to generate
    /// * `generate_stack` - Function to generate stack from template
    ///
    /// # Returns
    /// A new `StackTestCase` instance ready for validation
    ///
    /// # Type Parameters
    /// * `F` - Function type that generates stack bytes from template, language, and name
    pub fn new<F>(test_path: &str, lang: &'a str, stack_name: &'a str, generate_stack: F) -> Self
    where
        F: Fn(&str, &str, &str) -> Vec<u8>,
    {
        let scope = Scope::new(test_path, lang);
        let template = Zip::extract_template(&scope.test);
        let stack_output = generate_stack(&template, lang, stack_name);
        let generated_stack = Self::get_valid_generated_stack(stack_output, lang);
        let expected_stack = if cfg!(feature = "update-snapshots") {
            // Write the new/updated test case stack to expected in cdk-from-cfn-testing
            Files::write_expected_stack(&scope, stack_name, &generated_stack);
            generated_stack.clone()
        } else {
            Zip::extract_stack_file(&scope.test, lang)
        };
        Files::write_actual_stack(&scope, stack_name, &generated_stack);
        Self {
            scope,
            generated_stack,
            expected_stack,
            stack_name,
        }
    }

    /// Creates a stack test case from an existing scope and stack name.
    ///
    /// Loads previously generated stack files for comparison without regeneration.
    ///
    /// # Arguments
    /// * `scope` - Test scope containing language and test metadata
    /// * `stack_name` - Name of the stack to load
    ///
    /// # Returns
    /// A new `StackTestCase` instance with loaded stack content
    pub fn from_scope(scope: &Scope, stack_name: &'a str) -> Self {
        let expected_stack = if cfg!(feature = "update-snapshots") {
            Files::load_expected_stack(&scope.test, &scope.lang)
        } else {
            Zip::extract_stack_file(&scope.test, &scope.lang)
        };
        Self {
            scope: scope.clone(),
            generated_stack: Files::load_actual_stack(scope, stack_name),
            expected_stack,
            stack_name,
        }
    }

    /// Validates that the generated stack matches the expected output.
    ///
    /// Performs detailed comparison between generated and expected stack content,
    /// providing clear error messages if differences are found.
    ///
    /// # Panics
    /// Panics if the generated stack doesn't match the expected output
    pub fn generated_stack_file_matches_expected(&self) {
        StackDiff::new(&self.expected_stack, &self.generated_stack).compare_and_report();
        // Only prints on a success
        eprintln!(
            "  ✨ Stack files match expected for {} ({})",
            self.scope.test, self.scope.lang
        );
    }

    /// Cleans up temporary files created during testing.
    ///
    /// Removes generated stack files and other test artifacts to maintain
    /// a clean testing environment. Failed test artifacts will remain after
    /// each test run. for troubleshooting. This can also be skipped with the
    /// "skip-clean" feature.
    pub fn clean(&self) {
        Files::cleanup_test(&self.scope);
    }

    /// Converts generated stack bytes to a valid UTF-8 string with post-processing.
    ///
    /// # Arguments
    /// * `stack_output` - Raw bytes from stack generation
    /// * `lang` - Programming language for post-processing
    ///
    /// # Returns
    /// Valid UTF-8 string with language-specific post-processing applied
    ///
    /// # Panics
    /// Panics if the stack output cannot be converted to valid UTF-8
    fn get_valid_generated_stack(stack_output: Vec<u8>, lang: &str) -> String {
        let stack_result = String::from_utf8(stack_output);
        assert!(
            stack_result.is_ok(),
            "❌ Generated stack could not be translated into utf-8: {:?}",
            stack_result.err()
        );
        Language::post_process_output(lang, stack_result.unwrap())
    }
}
