use noctilucent::parser::lookup_table::{
    build_mappings, MappingInnerValue, MappingParseTree, MappingsParseTree,
};
use noctilucent::parser::resource::{
    build_resources, ResourceParseTree, ResourceValue, WrapperF64,
};
use serde_json::Value;
use std::collections::HashMap;

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

#[test]
fn test_parse_mapping_tree_with_numbers() {
    let mapping = serde_json::json!({
        "FooMap": {
            "BarOuterKey": {
                "innerKey1": 1,
                "innerKey2": 2,
                "innerKey3": 3
            }
        }
    });

    let mut mapping_parsed = MappingsParseTree::new();
    let mut outer_mapping = MappingParseTree::new();
    let mut key_value_pairs: HashMap<String, MappingInnerValue> = HashMap::new();
    key_value_pairs.insert("innerKey1".to_string(), MappingInnerValue::Number(1));
    key_value_pairs.insert("innerKey2".to_string(), MappingInnerValue::Number(2));
    key_value_pairs.insert("innerKey3".to_string(), MappingInnerValue::Number(3));
    outer_mapping.insert("BarOuterKey".to_string(), key_value_pairs);
    mapping_parsed.insert("FooMap".to_string(), outer_mapping);

    assert_mapping_equal(mapping, mapping_parsed)
}

fn assert_resource_equal(val: Value, resource: ResourceParseTree) {
    let obj = val.as_object().unwrap();
    let resources = build_resources(obj).unwrap();
    assert_eq!(resources.resources[0], resource)
}

fn assert_mapping_equal(val: Value, mapping: MappingsParseTree) {
    let obj = val.as_object().unwrap();
    let mappings = build_mappings(obj).unwrap();
    assert_eq!(mappings, mapping);
}
