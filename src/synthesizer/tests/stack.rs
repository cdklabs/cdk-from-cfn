// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use crate::cdk::Schema;
use crate::ir::CloudformationProgramIr;
use crate::CloudformationParseTree;
use crate::synthesizer::StackType;
use cdk_from_cfn_testing::{Language, Stack};

/// Trait for generating CDK stacks directly from CloudFormation templates using the IR (Intermediate Representation).
///
/// This trait provides an alternative to the binary-based approach by using the internal
/// CloudformationProgramIr directly for stack generation, bypassing subprocess execution.
pub trait IrStack {
    /// Generates CDK stack code from a CloudFormation template using the internal IR.
    ///
    /// # Arguments
    /// * `template` - CloudFormation template as JSON/YAML string
    /// * `lang` - Target programming language for CDK code
    /// * `stack_name` - Name for the generated CDK stack
    ///
    /// # Returns
    /// Generated CDK code as bytes
    fn generate_stack(template: &str, lang: &str, stack_name: &str) -> Vec<u8>;
}

impl IrStack for Stack {
    /// Generates CDK stack code using the CloudformationProgramIr directly.
    ///
    /// Parses the CloudFormation template into the internal IR representation
    /// and synthesizes CDK code for the specified language without external process execution.
    ///
    /// # Arguments
    /// * `template` - CloudFormation template as JSON string
    /// * `lang` - Target programming language for CDK code
    /// * `stack_name` - Name for the generated CDK stack
    ///
    /// # Returns
    /// Generated CDK code as bytes
    ///
    /// # Panics
    /// Panics if template parsing fails or IR synthesis encounters an error
    fn generate_stack(template: &str, lang: &str, stack_name: &str) -> Vec<u8> {
        let cfn: CloudformationParseTree = serde_json::from_str(template).unwrap();
        let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

        let mut output = Vec::new();
        let ir_lang = Language::lang_arg(lang);
        let result = ir.synthesize(ir_lang, &mut output, stack_name,StackType::default());
        assert!(
            result.is_ok(),
            "❌ Stack file could not be generated. An error occurred in the CloudformationProgramIr synthesis. {:?}", result.err()
        );

        output
    }
}
