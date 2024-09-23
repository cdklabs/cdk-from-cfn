// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use indexmap::IndexMap;

use crate::parser::resource::ResourceAttributes;

use super::ImportInstruction;

#[test]
fn test_invalid_resource_type_name() {
    let resource_attributes = ResourceAttributes {
        resource_type: "AWS:Invalid:Resource:Type".to_string(),
        condition: Option::None,
        metadata: Option::None,
        depends_on: vec![],
        update_policy: Option::None,
        deletion_policy: Option::None,
        properties: IndexMap::new(),
    };
    let parse_tree = IndexMap::from([("Resource".to_string(), resource_attributes)]);
    let import_instruction = ImportInstruction::from(&parse_tree).unwrap_err();
    assert_eq!(
        "Invalid resource type name: AWS:Invalid:Resource:Type",
        import_instruction.to_string()
    );
}
