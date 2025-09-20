// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use similar::{ChangeTag, TextDiff};

/// Text-based diff utility for comparing CDK stack files.
/// 
/// Provides line-by-line comparison of generated CDK code against expected
/// reference implementations, highlighting specific differences.
pub struct StackDiff<'a> {
    /// Expected stack content from reference implementation
    expected_stack: &'a str,
    /// Generated stack content from CDK conversion
    generated_stack: &'a str,
}

impl<'a> StackDiff<'a> {
    /// Creates a new stack diff comparison.
    /// 
    /// # Arguments
    /// * `expected_stack` - Expected stack content
    /// * `generated_stack` - Generated stack content
    /// 
    /// # Returns
    /// A new `StackDiff` instance ready for comparison
    pub fn new(expected_stack: &'a str, generated_stack: &'a str) -> Self {
        Self {
            expected_stack,
            generated_stack,
        }
    }

    /// Compares stack contents and reports differences if found.
    /// 
    /// Performs exact string comparison and generates detailed diff output
    /// showing added and removed lines if the stacks don't match.
    /// 
    /// # Panics
    /// Panics if the stacks don't match, displaying the detailed diff
    pub fn compare_and_report(&self) {
        assert!(
            self.expected_stack == self.generated_stack,
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
        let diff = TextDiff::from_lines(self.expected_stack, self.generated_stack);
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
