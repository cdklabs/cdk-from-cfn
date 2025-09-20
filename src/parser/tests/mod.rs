// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use crate::parser::resource::{DeletionPolicy, IntrinsicFunction};
use crate::parser::resource::{ResourceAttributes, ResourceValue};
use crate::{assert_resource_equal, json, json_internal_vec, map};
use indexmap::IndexMap;

mod util;

#[test]
fn test_parse_tree_basics() {
    let resource_template = json!({
        "LogicalResource": {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "RoleName": "bob",
                "AssumeTime": 20,
                "Bool": true,
                "NotExistent": {"Ref": "AWS::NoValue"},
                "Array": ["hi", "there"]
            }
        }
    });

    let resource = ResourceAttributes {
        condition: Option::None,
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::None,
        depends_on: vec![],
        resource_type: "AWS::IAM::Role".into(),
        properties: map! {
            "RoleName" => ResourceValue::String("bob".into()),
            "AssumeTime" => ResourceValue::Number(20),
            "Bool" => ResourceValue::Bool(true),
            "NotExistent" => ResourceValue::Null,
            "Array" => ResourceValue::Array(vec![ResourceValue::String("hi".into()), ResourceValue::String("there".into())])
        },
    };
    assert_resource_equal!("LogicalResource" => resource_template, resource);
}

#[test]
fn test_basic_parse_tree_with_condition() {
    let resource_template = json!({
        "LogicalResource": {
            "Type": "AWS::IAM::Role",
            "Condition": "SomeCondition",
            "Properties": {
                "RoleName": "bob",
                "AssumeTime": 20,
                "Bool": true,
                "NotExistent": {"Ref": "AWS::NoValue"},
                "Array": ["hi", "there"]
            }
        }
    });

    let resource = ResourceAttributes {
        condition: Option::Some("SomeCondition".into()),
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::None,
        depends_on: vec![],
        resource_type: "AWS::IAM::Role".into(),
        properties: map! {
            "RoleName" => ResourceValue::String("bob".into()),
            "AssumeTime" => ResourceValue::Number(20),
            "Bool" => ResourceValue::Bool(true),
            "NotExistent" => ResourceValue::Null,
            "Array" => ResourceValue::Array(vec![ResourceValue::String("hi".into()), ResourceValue::String("there".into())])
        },
    };
    assert_resource_equal!("LogicalResource" => resource_template, resource);
}

#[test]
fn test_basic_parse_tree_with_metadata() {
    let resource_template = json!({
        "LogicalResource": {
            "Type": "AWS::IAM::Role",
            "Metadata": {
                "myArbitrary": "objectData"
            },
            "Properties": {
                "RoleName": "bob",
                "AssumeTime": 20,
                "Bool": true,
                "NotExistent": {"Ref": "AWS::NoValue"},
                "Array": ["hi", "there"]
            }
        }
    });

    let resource = ResourceAttributes {
        condition: Option::None,
        metadata: Option::Some(ResourceValue::Object(map! {
            "myArbitrary" => ResourceValue::String("objectData".into())
        })),
        update_policy: Option::None,
        deletion_policy: Option::None,
        depends_on: vec![],
        resource_type: "AWS::IAM::Role".into(),
        properties: map! {
            "RoleName" => ResourceValue::String("bob".into()),
            "AssumeTime" => ResourceValue::Number(20),
            "Bool" => ResourceValue::Bool(true),
            "NotExistent" => ResourceValue::Null,
            "Array" => ResourceValue::Array(vec![ResourceValue::String("hi".into()), ResourceValue::String("there".into())])
        },
    };
    assert_resource_equal!("LogicalResource" => resource_template, resource);
}

#[test]
fn test_parse_tree_basics_with_deletion_policy() {
    let resource_template = json!({
        "LogicalResource": {
            "Type": "AWS::IAM::Role",
            "DeletionPolicy": "Retain",
            "Properties": {
                "RoleName": "bob",
                "AssumeTime": 20,
                "Bool": true,
                "NotExistent": {"Ref": "AWS::NoValue"},
                "Array": ["hi", "there"]
            }
        }
    });

    let resource: ResourceAttributes = ResourceAttributes {
        condition: Option::None,
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::Some(DeletionPolicy::Retain),
        depends_on: vec![],
        resource_type: "AWS::IAM::Role".into(),
        properties: map! {
            "RoleName" => ResourceValue::String("bob".into()),
            "AssumeTime" => ResourceValue::Number(20),
            "Bool" => ResourceValue::Bool(true),
            "NotExistent" => ResourceValue::Null,
            "Array" => ResourceValue::Array(vec![ResourceValue::String("hi".into()), ResourceValue::String("there".into())])
        },
    };

    assert_resource_equal!("LogicalResource" => resource_template, resource);
}

#[test]
fn test_parse_tree_sub_str() {
    let resource_template = json!({
        "LogicalResource": {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "RoleName": {
                    "Fn::Sub": "bobs-role-${AWS::Region}"
                }
            }
        }
    });

    let resource = ResourceAttributes {
        condition: Option::None,
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::None,
        depends_on: vec![],
        resource_type: "AWS::IAM::Role".into(),
        properties: map! {
            "RoleName" => IntrinsicFunction::Sub{ string:"bobs-role-${AWS::Region}".into(), replaces: None }.into()
        },
    };
    assert_resource_equal!("LogicalResource" => resource_template, resource);
}

#[test]
fn test_parse_tree_yaml_codes() {
    let resource_template = json!({
        "LogicalResource": {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "RoleName": {
                    "!Sub": "bobs-role-${AWS::Region}"
                }
            }
        }
    });

    let resource = ResourceAttributes {
        condition: Option::None,
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::None,
        depends_on: vec![],
        resource_type: "AWS::IAM::Role".into(),
        properties: map! {
            "RoleName" => IntrinsicFunction::Sub{ string: "bobs-role-${AWS::Region}".into(), replaces: None }.into()
        },
    };
    assert_resource_equal!("LogicalResource" => resource_template, resource);
}

#[test]
fn test_parse_get_attr_shorthand() {
    let resource_template = json!({
        "LogicalResource": {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "RoleName": {
                    "Fn::GetAtt": "Foo.Bar"
                }
            }
        }
    });

    let resource = ResourceAttributes {
        condition: Option::None,
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::None,
        depends_on: vec![],
        resource_type: "AWS::IAM::Role".into(),
        properties: map! {
            "RoleName" => IntrinsicFunction::GetAtt{ logical_name: "Foo".into(), attribute_name: "Bar".into() }.into()
        },
    };
    assert_resource_equal!("LogicalResource" => resource_template, resource);
}
