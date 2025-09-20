// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

/// Test scope containing metadata about a specific test case and language combination.
/// 
/// Provides normalized identifiers for organizing test cases across different
/// programming languages and test modules.
#[derive(Clone, Debug)]
pub struct Scope {
    /// Module name extracted from the test path
    pub module: String,
    /// Test name extracted from the test path
    pub test: String,
    /// Programming language for this test scope
    pub lang: String,
    /// Normalized identifier combining test and language
    pub normalized: String,
}

impl Scope {
    /// Creates a new test scope from a test path and programming language.
    /// 
    /// Parses the test path to extract module and test names, then creates
    /// a normalized identifier for consistent test organization.
    /// 
    /// # Arguments
    /// * `test_path` - Full path identifying the test case
    /// * `lang` - Programming language for this scope
    /// 
    /// # Returns
    /// A new `Scope` instance with parsed metadata
    pub fn new(test_path: &str, lang: &str) -> Self {
        let normalized = Self::normalize(test_path, lang);
        let parts = normalized
            .split("::")
            .map(|s| s.to_string())
            .collect::<Vec<String>>();
        Self {
            module: parts[0].clone(),
            test: parts[1].clone(),
            lang: lang.to_string(),
            normalized,
        }
    }

    /// Extracts just the test name from a test path.
    /// 
    /// # Arguments
    /// * `test_path` - Full path identifying the test case
    /// 
    /// # Returns
    /// The test name component of the path
    pub fn test_name(test_path: &str) -> String {
        Self::new(test_path, "").test
    }

    /// Normalizes a test path by filtering out common test-related components.
    /// 
    /// Removes test framework artifacts, crate names, language names, and other
    /// noise from the test path to create a clean identifier.
    /// 
    /// # Arguments
    /// * `test_path` - Full path identifying the test case
    /// * `lang` - Optional language to filter out of the path
    /// 
    /// # Returns
    /// Normalized test path with noise components removed
    fn normalize_test(test_path: &str, lang: Option<&str>) -> String {
        use crate::Language;
        let all_languages = Language::get_enabled_languages();
        test_path
            .split("::")
            .filter(|s| !s.contains("test"))
            .filter(|s| !env!("CARGO_CRATE_NAME").contains(s))
            .filter(|s| *s != lang.unwrap_or(""))
            .filter(|s| !all_languages.contains(&s.to_string()))
            .map(|s| s.to_string())
            .collect::<Vec<String>>()
            .join("::")
    }

    /// Creates a normalized identifier combining test path and language.
    /// 
    /// # Arguments
    /// * `test_path` - Full path identifying the test case
    /// * `lang` - Programming language for this scope
    /// 
    /// # Returns
    /// Normalized identifier in the format "test::language"
    pub fn normalize(test_path: &str, lang: &str) -> String {
        [&Self::normalize_test(test_path, Some(lang)), lang].join("::")
    }
}
