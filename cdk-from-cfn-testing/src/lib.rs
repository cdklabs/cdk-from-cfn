// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

mod bootstrap;
mod config;
mod filesystem;
mod synth;
mod validation;

pub use config::{
    run_cli_with_args, CdkFromCfnConstruct, CdkFromCfnStack, EndToEndTestStack, Language, Scope,
    Stack,
};
pub use synth::{CdkAppTestCase, CdkAppTestGroup};

// Re-export synth types
pub use synth::{SkipSynthList, TestFilter};

use self::{
    filesystem::{Files, Zip},
    validation::ClassDiff,
};

/// Test case for validating CDK code generation against expected output.
///
/// This struct manages the comparison between generated CDK code and expected
/// reference implementations, handling file I/O and validation workflows and is
/// shared across both sets of tests that test code generation.
#[derive(Clone)]
pub struct ClassTestCase<'a> {
    /// Test scope containing language and test metadata
    pub scope: Scope,
    /// Expected code content from reference implementation
    pub(crate) expected_code: String,
    /// Generated code content from CDK conversion
    pub(crate) generated_code: String,
    /// Name of the class being tested (stack or construct)
    pub(crate) class_name: &'a str,
}

impl<'a> ClassTestCase<'a> {
    /// Creates a new class test case by generating and comparing class output.
    ///
    /// # Arguments
    /// * `test_path` - Path identifying the test case
    /// * `lang` - Programming language for class generation
    /// * `class_name` - Name of the class to generate (stack or construct)
    /// * `generator` - Function to generate code from template
    ///
    /// # Returns
    /// A new `ClassTestCase` instance ready for validation
    ///
    /// # Type Parameters
    /// * `F` - Function type that generates code bytes from template, language, and name
    pub fn new<F>(test_path: &str, lang: &'a str, class_name: &'a str, generator: F) -> Self
    where
        F: Fn(&str, &str, &str) -> Vec<u8>,
    {
        let scope = Scope::new(test_path, lang);
        let template = Zip::extract_template(&scope.test);
        let output = generator(&template, lang, class_name);
        let generated_code = Self::get_valid_generated_class(output, lang);
        let expected_code = if cfg!(feature = "update-snapshots") {
            // Write the new/updated test case to expected in cdk-from-cfn-testing
            Files::write_expected_class(&scope, class_name, &generated_code);
            generated_code.clone()
        } else {
            Zip::extract_class_file(&scope.test, lang, class_name)
        };
        Files::write_actual_class(&scope, class_name, &generated_code);
        Self {
            scope,
            generated_code,
            expected_code,
            class_name,
        }
    }

    /// Creates a test case from an existing scope and class name.
    ///
    /// Loads previously generated files for comparison without regeneration.
    ///
    /// # Arguments
    /// * `scope` - Test scope containing language and test metadata
    /// * `class_name` - Name of the class to load (stack or construct)
    ///
    /// # Returns
    /// A new `CLassTestCase` instance with loaded content
    pub fn from_scope(scope: &Scope, class_name: &'a str) -> Self {
        let expected_code = if cfg!(feature = "update-snapshots") {
            Files::load_expected_class(&scope.test, &scope.lang, class_name)
        } else {
            Zip::extract_class_file(&scope.test, &scope.lang, class_name)
        };
        Self {
            scope: scope.clone(),
            generated_code: Files::load_actual_class(scope, class_name),
            expected_code,
            class_name,
        }
    }

    /// Validates that the generated code matches the expected output.
    ///
    /// Performs detailed comparison between generated and expected code content,
    /// providing clear error messages if differences are found.
    ///
    /// # Panics
    /// Panics if the generated code doesn't match the expected output
    pub fn generated_class_file_matches_expected(&self) {
        ClassDiff::new(&self.expected_code, &self.generated_code).compare_and_report();
        // Only prints on a success
        eprintln!(
            "  ✨ Class files match expected for {} ({})",
            self.scope.test, self.scope.lang
        );
    }

    /// Cleans up temporary files created during testing.
    ///
    /// Removes generated class files and other test artifacts to maintain
    /// a clean testing environment. Failed test artifacts will remain after
    /// each test run. for troubleshooting. This can also be skipped with the
    /// "skip-clean" feature.
    pub fn clean(&self) {
        Files::cleanup_test(&self.scope);
    }

    /// Converts generated class bytes to a valid UTF-8 string with post-processing.
    ///
    /// # Arguments
    /// * `class_output` - Raw bytes from class generation
    /// * `lang` - Programming language for post-processing
    ///
    /// # Returns
    /// Valid UTF-8 string with language-specific post-processing applied
    ///
    /// # Panics
    /// Panics if the class output cannot be converted to valid UTF-8
    fn get_valid_generated_class(class_output: Vec<u8>, lang: &str) -> String {
        let class_result = String::from_utf8(class_output);
        assert!(
            class_result.is_ok(),
            "❌ Generated class could not be translated into utf-8: {:?}",
            class_result.err()
        );
        Language::post_process_output(lang, class_result.unwrap())
    }
}
