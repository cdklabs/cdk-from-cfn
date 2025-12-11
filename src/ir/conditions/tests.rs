// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use indexmap::IndexMap;

use crate::ir::conditions::{determine_order, ConditionIr};
use crate::ir::reference::{Origin, PseudoParameter, Reference};
use crate::parser::condition::{ConditionFunction, ConditionValue};

#[test]
fn test_eq_translation() {
    let condition_structure = ConditionFunction::Equals(
        ConditionValue::String("us-west-2".into()),
        ConditionValue::Ref("AWS::Region".into()),
    );

    let condition_ir = condition_structure.into_ir();
    assert_eq!(
        ConditionIr::Equals(
            Box::new(ConditionIr::Str("us-west-2".into())),
            Box::new(ConditionIr::Ref(Reference::new(
                "AWS::Region",
                Origin::PseudoParameter(PseudoParameter::Region)
            )))
        ),
        condition_ir
    );
}

#[test]
fn test_sorting() {
    let a = ConditionFunction::Equals(
        ConditionValue::Ref("Foo".into()),
        ConditionValue::Ref("Bar".into()),
    );

    let b = ConditionFunction::Not(ConditionValue::Condition("A".into()));

    let hash = IndexMap::from([("A".into(), a), ("B".into(), b)]);
    let ordered = determine_order(&hash).unwrap();

    assert_eq!(ordered, vec!["A", "B"]);
}

#[test]
fn test_condition_translation() {
    let condition_structure: ConditionValue = ConditionValue::Condition("other".into());
    let condition_ir = condition_structure.into_ir();
    assert_eq!(
        (ConditionIr::Ref(Reference::new("other", Origin::Condition))),
        condition_ir
    );
}

#[test]
fn test_simple() {
    assert_eq!(
        ConditionIr::Str("hi".into()),
        ConditionValue::String("hi".into()).into_ir()
    );
}
