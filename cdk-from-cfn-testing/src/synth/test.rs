// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use crate::bootstrap::Install;
use crate::config::{CdkFromCfnStack, Environment};
use crate::filesystem::Files;
use crate::validation::Templates;
use crate::{Language, Scope, Stack, StackTestCase};

use super::{Synthesizer, TestFilter, TestSkip};

/// Individual CDK application test case for a specific language.
/// 
/// Represents a single language implementation of a CDK application test,
/// including synthesis status and validation capabilities.
#[derive(Clone)]
pub struct CdkAppTestCase<'a> {
    /// List of languages that were synthesized for this test group
    languages: Vec<String>,
    /// Whether CDK synthesis was performed for this language
    pub did_synth: bool,
    /// Underlying stack test case for validation
    pub test_case: StackTestCase<'a>,
}

/// Group of CDK application test cases across multiple languages.
/// 
/// Orchestrates testing across all enabled programming languages,
/// managing synthesis, filtering, and regional configuration.
pub struct CdkAppTestGroup<'a> {
    /// AWS region where tests are executed
    pub region: &'static str,
    /// Filter configuration for skipping languages
    pub test_filter: TestFilter,
    /// Test scopes for all languages
    pub scopes: Vec<Scope>,
    /// Name of the stack being tested
    pub stack_name: &'a str,
    /// Unique identifier for this test
    pub test_name: String,
}

impl<'a> CdkAppTestCase<'a> {
    /// Creates a new CDK application test group with synthesis across all enabled languages.
    /// 
    /// Generates CDK code for all enabled languages, installs boilerplate files,
    /// creates application files, and performs CDK synthesis for non-skipped languages.
    /// 
    /// # Arguments
    /// * `test_path` - Path identifying the test case
    /// * `stack_name` - Name of the stack to generate
    /// * `skip_list` - List of languages to skip with reasons
    /// 
    /// # Returns
    /// A new `CdkAppTestGroup` with all languages processed
    pub fn new(
        test_path: &str,
        stack_name: &'a str,
        skip_list: Vec<TestSkip>,
    ) -> CdkAppTestGroup<'a> {
        let all_languages = Language::get_enabled_languages();
        let test_name = Scope::test_name(test_path);
        let region = Environment::region_for_test(&test_name);
        let test_filter = TestFilter::new(skip_list, &test_name);
        test_filter.print_skip_reasons("CDK synth");
        let mut scopes = Vec::new();
        for lang in all_languages {
            let scope = Scope::new(test_path, &lang);
            scopes.push(scope.clone());
            let test_case = StackTestCase::new(
                test_path,
                &lang,
                stack_name,
                &<Stack as CdkFromCfnStack>::generate_stack,
            );

            if test_filter.should_synth(&lang) {
                let install = Install::new(&scope);
                install.boilerplate_files();
                install.app_file(
                    &test_case.stack_name,
                    Environment::is_env_dependent(&test_name),
                );
                let mut synthesizer = Synthesizer::new(&scope, region);
                synthesizer.synth();
            }
        }

        CdkAppTestGroup {
            region,
            test_filter,
            scopes,
            stack_name,
            test_name,
        }
    }

    /// Creates a CDK application test case from an existing scope and test group.
    /// 
    /// # Arguments
    /// * `scope` - Test scope for a specific language
    /// * `app` - Test group containing configuration and filters
    /// 
    /// # Returns
    /// A new `CdkAppTestCase` for the specified language
    pub fn from_scope(scope: &Scope, app: &CdkAppTestGroup<'a>) -> Self {
        let did_synth = app.test_filter.should_synth(&scope.lang);
        let test_case = StackTestCase::from_scope(scope, app.stack_name);
        Self {
            languages: app.test_filter.synth.clone(),
            test_case,
            did_synth,
        }
    }

    /// Cleans up test files and directories for a specific scope.
    /// 
    /// # Arguments
    /// * `scope` - Test scope to clean up
    pub fn clean(scope: &Scope) {
        Files::cleanup_test(scope);
    }

    /// Validates that CDK synthesis output matches the original CloudFormation template.
    /// 
    /// Compares the synthesized CloudFormation template with the original template
    /// to ensure CDK code generation produces equivalent infrastructure.
    pub fn cdk_out_matches_cfn_stack_file(&self) {
        Templates::validate(&self.test_case.scope, self.test_case.stack_name);
    }

    /// Validates that all synthesized applications produce identical CloudFormation templates.
    /// 
    /// Compares synthesized templates across all languages to ensure consistency
    /// in the generated infrastructure definitions.
    pub fn synthesized_apps_match_each_other(&self) {
        Templates::validate_all(
            &self.languages,
            &self.test_case.scope,
            self.test_case.stack_name,
        );
    }

    /// Validates that the generated stack file matches the expected reference implementation.
    /// 
    /// Compares the generated CDK code with the expected output to ensure
    /// code generation produces the correct language-specific implementation.
    pub fn generated_stack_file_matches_expected(&self) {
        self.test_case.generated_stack_file_matches_expected();
    }
}
