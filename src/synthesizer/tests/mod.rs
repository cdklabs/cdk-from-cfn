// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

#[cfg(test)]
use crate::ir_synthesizer_test;
use cdk_from_cfn_macros::generate_ir_tests;
#[cfg(test)]
use cdk_from_cfn_testing::{Stack, StackTestCase};

mod stack;
mod test;
use stack::IrStack;

generate_ir_tests!();
