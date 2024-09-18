// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use crate::CloudformationParseTree;

use super::*;

#[test]
pub fn none() {
    assert_eq!(
        OutputInstruction::from(
            IndexMap::default(),
            Schema::builtin(),
            &ReferenceOrigins::new(&CloudformationParseTree {
                description: None,
                transforms: vec![],
                conditions: IndexMap::default(),
                mappings: IndexMap::default(),
                outputs: IndexMap::default(),
                parameters: IndexMap::default(),
                resources: IndexMap::default()
            })
        )
        .unwrap(),
        vec![]
    );
}
