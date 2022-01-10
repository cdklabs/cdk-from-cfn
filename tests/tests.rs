use noctilucent::parser::condition::{ConditionParseTree, ConditionValue};
use noctilucent::parser::resource::{build_resources, ResourceParseTree, ResourceValue};
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
        resource_type: "AWS::IAM::Role".into(),
        properties: map! {
            "RoleName" => ResourceValue::Sub(vec![ResourceValue::String("bobs-role-${AWS::Region}".into())])
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

fn assert_resource_equal(val: Value, resource: ResourceParseTree) {
    let obj = val.as_object().unwrap();
    let resources = build_resources(obj).unwrap();
    assert_eq!(resources.resources[0], resource)
}
