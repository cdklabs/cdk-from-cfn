// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use similar::{ChangeTag, TextDiff};

/// Text-based diff utility for comparing CDK class files.
///
/// Provides line-by-line comparison of generated CDK code against expected
/// reference implementations, highlighting specific differences.
pub struct ClassDiff<'a> {
    /// Expected class content from reference implementation
    expected_class: &'a str,
    /// Generated class content from CDK conversion
    generated_class: &'a str,
}

impl<'a> ClassDiff<'a> {
    /// Creates a new class diff comparison.
    ///
    /// # Arguments
    /// * `expected_class` - Expected class content
    /// * `generated_class` - Generated class content
    ///
    /// # Returns
    /// A new `classDiff` instance ready for comparison
    pub fn new(expected_class: &'a str, generated_class: &'a str) -> Self {
        Self {
            expected_class,
            generated_class,
        }
    }

    /// Compares class contents and reports differences if found.
    ///
    /// Performs exact string comparison and generates detailed diff output
    /// showing added and removed lines if the classes don't match.
    ///
    /// # Panics
    /// Panics if the classes don't match, displaying the detailed diff
    pub fn compare_and_report(&self) {
        assert!(
            self.expected_class == self.generated_class,
            "{}",
            self.print()
        );
    }

    /// Generates a formatted diff report showing line-by-line differences.
    ///
    /// Uses the `similar` crate to compute text differences and formats them
    /// with + and - prefixes for added and removed lines.
    ///
    /// # Returns
    /// Formatted string containing the diff report
    fn print(&self) -> String {
        let diff = TextDiff::from_lines(self.expected_class, self.generated_class);
        let differences: Vec<String> = diff
            .iter_all_changes()
            .filter_map(|change| match change.tag() {
                ChangeTag::Delete => Some(format!("- {}", change.value().trim_end())),
                ChangeTag::Insert => Some(format!("+ {}", change.value().trim_end())),
                ChangeTag::Equal => None,
            })
            .collect();

        format!(
            "❌ Template output does not match expected\n\nFound {} difference(s) between expected and actual output\n\n===== DIFFERENCES =====\n\n{}\n\n",
            differences.len(),
            differences.join("\n")
        )
    }
}
