// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use crate::config::{Language, TestName};

/// Represents a GitHub issue that causes a test to be skipped.
///
/// Contains issue number and description for tracking known problems
/// that prevent certain language implementations from working correctly.
#[derive(Clone, Copy)]
pub struct Issue {
    /// GitHub issue number
    pub number: u16,
    /// Brief description of the issue
    pub description: &'static str,
}

impl Issue {
    /// Creates a new issue reference.
    ///
    /// # Arguments
    /// * `number` - GitHub issue number
    /// * `description` - Brief description of the issue
    ///
    /// # Returns
    /// A new `Issue` instance
    pub const fn new(number: u16, description: &'static str) -> Self {
        Self {
            number,
            description,
        }
    }

    /// Generates a clickable link to the GitHub issue.
    ///
    /// # Returns
    /// Terminal-formatted clickable link to the issue
    pub fn as_link(&self) -> String {
        let url = format!(
            "https://github.com/aws/aws-cdk-from-cfn/issues/{}",
            self.number
        );
        format!("\x1b]8;;{}\x1b\\#{}\x1b]8;;\x1b\\", url, self.number)
    }
}

/// Configuration for skipping a specific language due to known issues.
///
/// Associates a programming language with one or more GitHub issues
/// that prevent the test from running successfully.
#[derive(Clone)]
pub struct TestSkip {
    /// Programming language to skip
    pub lang: String,
    /// List of issues causing the skip
    pub issues: Vec<Issue>,
}

impl AsRef<str> for TestSkip {
    fn as_ref(&self) -> &str {
        &self.lang
    }
}

impl TestSkip {
    /// Creates a new test skip configuration.
    ///
    /// # Arguments
    /// * `lang` - Programming language to skip
    /// * `issues` - List of issues causing the skip
    ///
    /// # Returns
    /// A new `TestSkip` instance
    pub fn new(lang: &str, issues: Vec<Issue>) -> Self {
        Self {
            lang: lang.to_string(),
            issues,
        }
    }

    /// Creates a test skip for a single language and issue.
    ///
    /// # Arguments
    /// * `lang` - Programming language to skip
    /// * `issue` - Issue causing the skip
    ///
    /// # Returns
    /// A new `TestSkip` instance
    fn single(lang: &str, issue: Issue) -> Self {
        Self::new(lang, vec![issue])
    }

    /// Creates test skips for all languages due to a common issue.
    ///
    /// # Arguments
    /// * `issue` - Issue affecting all languages
    ///
    /// # Returns
    /// Vector of `TestSkip` instances for all enabled languages
    fn all(issue: Issue) -> Vec<Self> {
        Language::get_enabled_languages()
            .into_iter()
            .map(|lang| Self::single(&lang, issue))
            .collect()
    }
}

/// Filter for determining which languages to skip or synthesize for a test.
///
/// Processes skip lists and enabled languages to create filtered lists
/// for synthesis and execution control.
#[derive(Clone)]
pub struct TestFilter {
    /// Original skip list with issue details
    skip_list: Vec<TestSkip>,
    /// Languages to skip (filtered by enabled languages)
    pub skip: Vec<String>,
    /// Languages to synthesize (enabled minus skipped)
    pub synth: Vec<String>,
    /// Name of the test being filtered
    test_name: String,
}

impl TestFilter {
    /// Creates a new test filter from a skip list.
    ///
    /// Filters the skip list to only include enabled languages and partitions
    /// all enabled languages into skip and synthesis lists.
    ///
    /// # Arguments
    /// * `skip_list` - List of languages to skip with reasons
    /// * `test_name` - Name of the test being filtered
    ///
    /// # Returns
    /// A new `TestFilter` instance
    pub fn new(skip_list: Vec<TestSkip>, test_name: &str) -> Self {
        let enabled_languages = Language::get_enabled_languages();
        let filtered_skip_list: Vec<TestSkip> = skip_list
            .into_iter()
            .filter(|skip| enabled_languages.contains(&skip.lang))
            .collect();

        let (skip, synth): (Vec<String>, Vec<String>) = enabled_languages
            .into_iter()
            .partition(|lang| filtered_skip_list.iter().any(|skip| skip.lang == *lang));

        Self {
            skip_list: filtered_skip_list,
            skip,
            synth,
            test_name: test_name.to_string(),
        }
    }

    /// Determines if a language should be synthesized.
    ///
    /// # Arguments
    /// * `lang` - Programming language to check
    ///
    /// # Returns
    /// `true` if the language should be synthesized, `false` if skipped
    pub fn should_synth(&self, lang: &str) -> bool {
        !self.skip.contains(&lang.to_string())
    }

    /// Prints skip reasons for filtered languages.
    ///
    /// Outputs formatted messages explaining why each language is being skipped,
    /// including clickable links to relevant GitHub issues.
    ///
    /// # Arguments
    /// * `context` - Context description (e.g., "CDK synth", "end-to-end test")
    pub fn print_skip_reasons(&self, context: &str) {
        self.skip_list.iter().for_each(|skip| {
            let issues_str = skip
                .issues
                .iter()
                .map(|issue| format!("{} ({})", issue.description, issue.as_link()))
                .collect::<Vec<_>>()
                .join(", ");
            eprintln!(
                "  ⏭️  Skipping {} for {}::{}: {}",
                context, self.test_name, skip.lang, issues_str
            );
        });
    }
}

/// Centralized skip list configuration for synthesis tests.
///
/// Maintains known issues and skip configurations for different test cases
/// across all supported programming languages.
pub struct SkipSynthList;

/// Macro for creating TestSkip instances with multiple issues.
macro_rules! skip {
    ($lang:expr, $($issue:expr),+ $(,)?) => {
        TestSkip::new($lang, vec![$($issue),+])
    };
}

impl SkipSynthList {
    const I626_GO_COMPILATION: Issue =
        Issue::new(626, "Go is an approximation at best. It does not compile");
    const I1022_CSHARP_MISSING_OUTPUTS: Issue = Issue::new(1022, "missing outputs section");
    const I1023_CSHARP_MISSING_CFN_OPTIONS: Issue = Issue::new(
        1023,
        "missing cfn options: metadata, dependencies, update policy, and deletion policy",
    );
    const I1024_JAVA_UPDATE_REPLACE: Issue = Issue::new(1024, "extra UpdateReplacePolicy key");
    const I1025_PYTHON_PARAMETER_CASING: Issue = Issue::new(
        1025,
        "parameter casing issue - camelCase instead of PascalCase",
    );
    const I1026_JAVA_MAPPING_CASING: Issue =
        Issue::new(1026, "mapping key casing - camelCase instead of PascalCase");
    const I1027_CSHARP_LAMBDA_SPACING: Issue =
        Issue::new(1027, "lambda handler spacing differences");
    const I1028_ALL_SPECIAL_CHARACTER_HANDLING: Issue = Issue::new(
        1028,
        "special characters in multiline strings aren't being handled properly",
    );
    const I1029_JAVA_NAMING_COLLISION: Issue = Issue::new(
        1029,
        "parameter sharing name with condition causes conflict",
    );

    /// Returns the skip list for a specific test case.
    ///
    /// Maps test names to their corresponding skip configurations,
    /// including the specific issues that cause each language to be skipped.
    ///
    /// # Arguments
    /// * `test_name` - Name of the test case
    ///
    /// # Returns
    /// Vector of skip configurations for the test
    pub fn get(test_name: &str) -> Vec<TestSkip> {
        match TestName::from_str(test_name) {
            TestName::Batch => vec![
                skip!(Language::CSHARP, Self::I1022_CSHARP_MISSING_OUTPUTS),
                skip!(Language::GOLANG, Self::I626_GO_COMPILATION),
            ],
            TestName::Cloudwatch => vec![skip!(Language::GOLANG, Self::I626_GO_COMPILATION)],
            TestName::Config => vec![
                skip!(
                    Language::CSHARP,
                    Self::I1022_CSHARP_MISSING_OUTPUTS,
                    Self::I1023_CSHARP_MISSING_CFN_OPTIONS
                ),
                skip!(Language::GOLANG, Self::I626_GO_COMPILATION),
            ],
            TestName::DocumentDb => vec![
                skip!(
                    Language::CSHARP,
                    Self::I1022_CSHARP_MISSING_OUTPUTS,
                    Self::I1023_CSHARP_MISSING_CFN_OPTIONS
                ),
                skip!(Language::JAVA, Self::I1024_JAVA_UPDATE_REPLACE),
                skip!(Language::PYTHON, Self::I1025_PYTHON_PARAMETER_CASING),
                skip!(Language::GOLANG, Self::I626_GO_COMPILATION),
            ],
            TestName::Ec2 => vec![skip!(Language::GOLANG, Self::I626_GO_COMPILATION)],
            TestName::Ec2Encryption => vec![
                skip!(Language::GOLANG, Self::I626_GO_COMPILATION),
                skip!(Language::JAVA, Self::I1029_JAVA_NAMING_COLLISION),
            ],
            TestName::Ecs => vec![skip!(Language::GOLANG, Self::I626_GO_COMPILATION)],
            TestName::Efs => vec![
                skip!(Language::CSHARP, Self::I1022_CSHARP_MISSING_OUTPUTS),
                skip!(Language::JAVA, Self::I1026_JAVA_MAPPING_CASING),
                skip!(Language::GOLANG, Self::I626_GO_COMPILATION),
            ],
            // Due to permissions issues this template will never deploy, but it's an interesting use case for this problem
            // Once this synths we should add functionality to synth but skip deploy.
            TestName::Groundstation => TestSkip::all(Self::I1028_ALL_SPECIAL_CHARACTER_HANDLING),
            TestName::ResourceWJsonTypeProperties => {
                vec![skip!(Language::GOLANG, Self::I626_GO_COMPILATION)]
            }
            TestName::SamNodejsLambda => {
                vec![skip!(Language::CSHARP, Self::I1027_CSHARP_LAMBDA_SPACING)]
            }
            TestName::SamNodejsLambdaArrTransform => {
                vec![skip!(Language::CSHARP, Self::I1027_CSHARP_LAMBDA_SPACING)]
            }
            TestName::Simple => vec![
                skip!(Language::CSHARP, Self::I1023_CSHARP_MISSING_CFN_OPTIONS),
                skip!(
                    Language::JAVA,
                    Self::I1026_JAVA_MAPPING_CASING,
                    Self::I1024_JAVA_UPDATE_REPLACE
                ),
                skip!(Language::PYTHON, Self::I1025_PYTHON_PARAMETER_CASING),
                skip!(Language::GOLANG, Self::I626_GO_COMPILATION),
            ],
            TestName::CustomResource => {
                vec![
                    skip!(Language::CSHARP, Self::I1027_CSHARP_LAMBDA_SPACING),
                    skip!(Language::GOLANG, Self::I626_GO_COMPILATION),
                    skip!(Language::JAVA, Self::I1024_JAVA_UPDATE_REPLACE),
                ]
            }
            TestName::Bucket | TestName::Vpc => vec![],
        }
    }
}
