// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use std::env::current_dir;
use std::path::PathBuf;

use crate::Language;
/// Path constants and utilities for test file organization.
///
/// Provides standardized paths for test files, directories, and naming conventions
/// used throughout the testing framework.
///
/// Is it overkill? Potentially, but these tests use a lot of filepaths and any updates to that
/// structure can be very difficult to troubleshoot when it's not all in once place.
pub struct Paths;

impl Paths {
    /// Directory name for actual generated test output
    pub const ACTUAL_DIR: &'static str = "actual";
    /// Directory name for test case definitions
    pub const CASES_DIR: &'static str = "cases";
    /// Directory name for expected test output
    pub const EXPECTED_DIR: &'static str = "expected";

    /// CloudFormation template file name
    pub const TEMPLATE: &'static str = "template.json";
    /// CDK output directory name
    pub const CDK_OUT_DIR: &'static str = "cdk.out";
    /// Acceptable diff file name
    pub const ACCEPTABLE_DIFF: &'static str = "Stack.diff";

    /// Go module cache directory name
    pub const GO_CACHE_DIR: &'static str = "go-mod-cache";
    /// Node.js modules directory name
    pub const NODE_MODULES: &'static str = "node_modules";
    /// Python virtual environment directory name
    pub const PYTHON_VENV: &'static str = ".python-venv";
    /// Binary directory name
    pub const BIN: &'static str = "bin";
    /// CDK binary name
    pub const CDK: &'static str = "cdk";

    /// Dependency stack template file name
    pub const DEPENDENCY_TEMPLATE: &'static str = "dependency_stack_template.json";
    /// Tag for end-to-end test stacks
    pub const E2E_TAG: &'static str = "cdk-from-cfn-e2e-test";
    /// Tag for end-to-end test dependency stacks
    pub const E2E_DEPENDENCY_TAG: &'static str = "cdk-from-cfn-e2e-test-dependency-stack";
    /// Boilerplate files directory name
    pub const BOILERPLATE_DIR: &'static str = "boilerplate";

    /// Returns the current project root directory.
    ///
    /// # Returns
    /// Path to the project root
    ///
    /// # Panics
    /// Panics if the current directory cannot be determined
    pub fn project_root() -> PathBuf {
        current_dir().unwrap_or_else(|e| panic!("Failed to get current directory: {}", e))
    }

    /// Returns the current crate name as a path.
    ///
    /// # Returns
    /// Path containing the crate name
    pub fn crate_name() -> PathBuf {
        PathBuf::from(Self::project_root().file_name().unwrap())
    }

    /// Returns the testing crate directory path.
    ///
    /// # Returns
    /// Path to the testing crate directory
    fn testing_crate_dir() -> PathBuf {
        Self::project_root().join(env!("CARGO_PKG_NAME"))
    }

    /// Returns the expected output directory path.
    ///
    /// # Returns
    /// Path to the expected test output directory
    pub fn expected_dir() -> PathBuf {
        Self::testing_crate_dir().join(Self::EXPECTED_DIR)
    }

    /// Returns the actual output directory path.
    ///
    /// # Returns
    /// Path to the actual test output directory
    pub fn actual_dir() -> PathBuf {
        Self::testing_crate_dir().join(Self::ACTUAL_DIR)
    }

    /// Returns the test cases directory path for a specific test.
    ///
    /// # Arguments
    /// * `test` - Name of the test
    ///
    /// # Returns
    /// Path to the test case directory
    pub fn cases_dir(test: &str) -> PathBuf {
        Self::testing_crate_dir().join(Self::CASES_DIR).join(test)
    }

    /// Returns the acceptable diff file path for a test.
    ///
    /// # Arguments
    /// * `test` - Name of the test
    ///
    /// # Returns
    /// Path to the acceptable diff file
    pub fn acceptable_diff_path(test: &str) -> PathBuf {
        Self::cases_dir(test).join(Self::ACCEPTABLE_DIFF)
    }

    /// Returns the actual output directory path for a normalized test identifier.
    ///
    /// # Arguments
    /// * `normalized` - Normalized test identifier
    ///
    /// # Returns
    /// Path to the test's actual output directory
    pub fn actual_dir_path(normalized: &str) -> PathBuf {
        Self::actual_dir().join(normalized)
    }

    /// Returns the application file path for a test and language.
    ///
    /// # Arguments
    /// * `normalized` - Normalized test identifier
    /// * `lang` - Programming language
    ///
    /// # Returns
    /// Path to the application file
    pub fn app(normalized: &str, lang: &str) -> PathBuf {
        Self::actual_dir_path(normalized).join(Language::app_name(lang))
    }

    /// Returns the expected stack file path.
    ///
    /// # Arguments
    /// * `test` - Name of the test
    /// * `lang` - Programming language
    /// * `stack_name` - Name of the stack
    ///
    /// # Returns
    /// Path to the expected stack file
    pub fn expected_stack_path(test: &str, lang: &str, stack_name: &str) -> PathBuf {
        let filename = Language::stack_filename(lang, stack_name);
        Self::expected_dir().join(test).join(lang).join(filename)
    }

    /// Returns the actual stack file path.
    ///
    /// # Arguments
    /// * `normalized` - Normalized test identifier
    /// * `lang` - Programming language
    /// * `stack_name` - Name of the stack
    ///
    /// # Returns
    /// Path to the actual stack file
    pub fn actual_stack_path(normalized: &str, lang: &str, stack_name: &str) -> PathBuf {
        let filename = Language::stack_filename(lang, stack_name);
        Self::actual_dir_path(normalized).join(filename)
    }

    /// Returns the CDK-synthesized template path.
    ///
    /// # Arguments
    /// * `normalized` - Normalized test identifier
    /// * `stack_name` - Name of the stack
    ///
    /// # Returns
    /// Path to the synthesized CloudFormation template
    pub fn synthesized_template_path(normalized: &str, stack_name: &str) -> PathBuf {
        Self::actual_dir_path(normalized)
            .join(Self::CDK_OUT_DIR)
            .join(format!("{}.{}", Self::e2e_name(stack_name), Self::TEMPLATE))
    }

    /// Generates an end-to-end test stack name.
    ///
    /// # Arguments
    /// * `name` - Base stack name
    ///
    /// # Returns
    /// Formatted end-to-end stack name with prefix
    pub fn e2e_name(name: &str) -> String {
        format!("{}-{}", Self::E2E_TAG, name)
    }

    /// Generates a dependency stack name.
    ///
    /// # Arguments
    /// * `name` - Base stack name
    ///
    /// # Returns
    /// Formatted dependency stack name with prefix
    pub fn dependency_name(name: &str) -> String {
        format!("{}-{}", Self::E2E_DEPENDENCY_TAG, name)
    }

    /// Returns the ZIP path for an application writer template.
    ///
    /// # Arguments
    /// * `lang` - Programming language
    ///
    /// # Returns
    /// ZIP archive path to the application writer template
    pub fn zip_app_writer_path(lang: &str) -> String {
        PathBuf::from(Self::BOILERPLATE_DIR)
            .join(lang)
            .join(format!("{}.template", Language::app_name(lang)))
            .to_string_lossy()
            .to_string()
    }

    /// Returns the ZIP path for expected output directory.
    ///
    /// # Arguments
    /// * `test` - Name of the test
    /// * `lang` - Programming language
    ///
    /// # Returns
    /// ZIP archive path to the expected output directory
    pub fn zip_expected_dir(test: &str, lang: &str) -> String {
        format!(
            "{}/",
            PathBuf::from(Self::EXPECTED_DIR)
                .join(test)
                .join(lang)
                .display()
        )
    }

    /// Returns the ZIP path for a test case file.
    ///
    /// # Arguments
    /// * `test` - Name of the test
    /// * `file` - Name of the file
    ///
    /// # Returns
    /// ZIP archive path to the test case file
    pub fn zip_case_path(test: &str, file: &str) -> String {
        PathBuf::from(Self::CASES_DIR)
            .join(test)
            .join(file)
            .display()
            .to_string()
    }

    /// Returns the ZIP path for boilerplate files directory.
    ///
    /// # Arguments
    /// * `lang` - Programming language
    ///
    /// # Returns
    /// ZIP archive path to the boilerplate files directory
    pub fn zip_boilerplate_dir(lang: &str) -> String {
        format!("{}/{}/", Self::BOILERPLATE_DIR, lang)
    }
}
