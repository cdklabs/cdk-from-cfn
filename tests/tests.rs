use noctilucent::parser::resource::{build_resources, ResourceParseTree, ResourceValue};
use noctilucent::primitives::WrapperF64;
use serde_json::Value;

macro_rules! map(
    { $($key:expr => $value:expr),+ } => {
        {
            let mut m = ::std::collections::HashMap::new();
            $(
                m.insert($key.to_string(), $value);
            )+
            m
        }
     };
);

#[test]
fn test_parse_tree_basics() {
    let a = serde_json::json!({
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

    let resource = ResourceParseTree {
        name: "LogicalResource".into(),
        condition: Option::None,
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::None,
        dependencies: vec![],
        resource_type: "AWS::IAM::Role".into(),
        properties: map! {
            "RoleName" => ResourceValue::String("bob".into()),
            "AssumeTime" => ResourceValue::Number(20),
            "Bool" => ResourceValue::Bool(true),
            "NotExistent" => ResourceValue::Null,
            "Array" => ResourceValue::Array(vec![ResourceValue::String("hi".into()), ResourceValue::String("there".into())])
        },
    };
    assert_resource_equal(a, resource);
}

#[test]
fn test_basic_parse_tree_with_condition() {
    let a: Value = serde_json::json!({
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

    let resource = ResourceParseTree {
        name: "LogicalResource".into(),
        condition: Option::Some("SomeCondition".into()),
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::None,
        dependencies: vec![],
        resource_type: "AWS::IAM::Role".into(),
        properties: map! {
            "RoleName" => ResourceValue::String("bob".into()),
            "AssumeTime" => ResourceValue::Number(20),
            "Bool" => ResourceValue::Bool(true),
            "NotExistent" => ResourceValue::Null,
            "Array" => ResourceValue::Array(vec![ResourceValue::String("hi".into()), ResourceValue::String("there".into())])
        },
    };
    assert_resource_equal(a, resource);
}

#[test]
fn test_basic_parse_tree_with_metadata() {
    let a: Value = serde_json::json!({
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

    let resource = ResourceParseTree {
        name: "LogicalResource".into(),
        condition: Option::None,
        metadata: Option::Some(ResourceValue::Object(map! {
            "myArbitrary" => ResourceValue::String("objectData".into())
        })),
        update_policy: Option::None,
        deletion_policy: Option::None,
        dependencies: vec![],
        resource_type: "AWS::IAM::Role".into(),
        properties: map! {
            "RoleName" => ResourceValue::String("bob".into()),
            "AssumeTime" => ResourceValue::Number(20),
            "Bool" => ResourceValue::Bool(true),
            "NotExistent" => ResourceValue::Null,
            "Array" => ResourceValue::Array(vec![ResourceValue::String("hi".into()), ResourceValue::String("there".into())])
        },
    };
    assert_resource_equal(a, resource);
}   

#[test]
fn test_parse_tree_basics_with_deletion_policy() {
    let a: Value = serde_json::json!({
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

    let resource: ResourceParseTree = ResourceParseTree {
        name: "LogicalResource".into(),
        condition: Option::None,
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::Some("Retain".into()),
        dependencies: vec![],
        resource_type: "AWS::IAM::Role".into(),
        properties: map! {
            "RoleName" => ResourceValue::String("bob".into()),
            "AssumeTime" => ResourceValue::Number(20),
            "Bool" => ResourceValue::Bool(true),
            "NotExistent" => ResourceValue::Null,
            "Array" => ResourceValue::Array(vec![ResourceValue::String("hi".into()), ResourceValue::String("there".into())])
        },
    };

    assert_resource_equal(a, resource);
}


#[test]
fn test_parse_tree_sub_str() {
    let a = serde_json::json!({
        "LogicalResource": {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "RoleName": {
                    "Fn::Sub": "bobs-role-${AWS::Region}"
                }
            }
        }
    });

    let resource = ResourceParseTree {
        name: "LogicalResource".into(),
        condition: Option::None,
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::None,
        dependencies: vec![],
        resource_type: "AWS::IAM::Role".into(),
        properties: map! {
            "RoleName" => ResourceValue::Sub(vec![ResourceValue::String("bobs-role-${AWS::Region}".into())])
        },
    };
    assert_resource_equal(a, resource);
}

#[test]
fn test_parse_tree_yaml_codes() {
    let a = serde_json::json!({
        "LogicalResource": {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "RoleName": {
                    "!Sub": "bobs-role-${AWS::Region}"
                }
            }
        }
    });

    let resource = ResourceParseTree {
        name: "LogicalResource".into(),
        condition: Option::None,
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::None,
        dependencies: vec![],
        resource_type: "AWS::IAM::Role".into(),
        properties: map! {
            "RoleName" => ResourceValue::Sub(vec![ResourceValue::String("bobs-role-${AWS::Region}".into())])
        },
    };
    assert_resource_equal(a, resource);
}
#[test]
fn test_parse_get_attr_shorthand() {
    let a = serde_json::json!({
        "LogicalResource": {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "RoleName": {
                    "Fn::GetAtt": "Foo.Bar"
                }
            }
        }
    });

    let resource = ResourceParseTree {
        name: "LogicalResource".into(),
        condition: Option::None,
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::None,
        dependencies: vec![],
        resource_type: "AWS::IAM::Role".into(),
        properties: map! {
            "RoleName" => ResourceValue::GetAtt(Box::new(ResourceValue::String("Foo".to_string())), Box::new(ResourceValue::String("Bar".to_string())))
        },
    };
    assert_resource_equal(a, resource);
}

#[test]
fn test_parse_tree_sub_list() {
    let a = serde_json::json!({
        "LogicalResource": {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "RoleName": {
                    "Fn::Sub": [
                        "bobs-role-${Region}",
                        {
                            "Region": {
                               "Ref": "AWS::Region"
                            }
                        }
                    ]
                }
            }
        }
    });

    let resource = ResourceParseTree {
        name: "LogicalResource".into(),
        condition: Option::None,
        resource_type: "AWS::IAM::Role".into(),
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::None,
        dependencies: vec![],
        properties: map! {
            "RoleName" => ResourceValue::Sub(vec![
                ResourceValue::String("bobs-role-${Region}".into()),
                ResourceValue::Object(map!{
                    "Region" =>  ResourceValue::Ref("AWS::Region".into())
                })
            ])
        },
    };
    assert_resource_equal(a, resource);
}

#[test]
fn test_parse_tree_resource_with_floats() {
    let a = serde_json::json!({
        "Alarm": {
            "Type": "AWS::CloudWatch::Alarm",
            "Properties": {
                "ComparisonOperator": "GreaterThanOrEqualToThreshold",
                "AlarmName": {
                    "Fn::Sub": [
                        "${Tag}-FrontendDistributedCacheTrafficImbalanceAlarm",
                        {
                            "Tag": {
                               "Ref": "AWS::Region"
                            }
                        }
                    ]
                },
                "Threshold": 3.5
            }
        }
    });

    let resource = ResourceParseTree {
        name: "Alarm".into(),
        condition: Option::None,
        resource_type: "AWS::CloudWatch::Alarm".into(),
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::None,
        dependencies: vec![],
        properties: map! {
            "AlarmName" => ResourceValue::Sub(vec![
                ResourceValue::String("${Tag}-FrontendDistributedCacheTrafficImbalanceAlarm".into()),
                ResourceValue::Object(map!{
                    "Tag" =>  ResourceValue::Ref("AWS::Region".into())
                })
            ]),
            "ComparisonOperator" => ResourceValue::String("GreaterThanOrEqualToThreshold".to_string()),
            "Threshold" => ResourceValue::Double(WrapperF64::new(3.5))
        },
    };
    assert_resource_equal(a, resource);
}

fn assert_resource_equal(val: Value, resource: ResourceParseTree) {
    let obj = val.as_object().unwrap();
    let resources = build_resources(obj).unwrap();
    assert_eq!(resources.resources[0], resource)
}
