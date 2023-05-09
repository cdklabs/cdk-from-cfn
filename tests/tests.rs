use indexmap::IndexMap;
use noctilucent::parser::condition::{ConditionFunction, ConditionValue};
use noctilucent::parser::lookup_table::{MappingInnerValue, MappingTable};
use noctilucent::parser::parameters::{Parameter, ParameterType};
use noctilucent::parser::resource::{DeletionPolicy, IntrinsicFunction};
use noctilucent::parser::resource::{ResourceAttributes, ResourceValue};
use noctilucent::primitives::WrapperF64;
use noctilucent::CloudformationParseTree;
use serde_yaml::Value;
use std::vec;

mod json;

macro_rules! map{
    ($($key:expr => $value:expr),+) => {
        {
            let mut m = ::indexmap::IndexMap::<String, _, _>::default();
            $(
                m.insert($key.into(), $value);
            )+
            m
        }
     };
}

macro_rules! assert_resource_equal {
    ($name:expr => $val:expr, $resource:expr) => {
        let obj = ($val).as_mapping().unwrap();
        let resources: IndexMap<String, ResourceAttributes> =
            serde_yaml::from_value(serde_yaml::Value::Mapping(obj.clone())).unwrap();
        assert_eq!(resources[$name], ($resource))
    };
}

macro_rules! assert_template_equal {
    ($val:expr, $cfn_tree:expr) => {{
        let cfn_template: CloudformationParseTree = serde_yaml::from_value($val).unwrap();
        let cfn_tree = $cfn_tree;
        assert_eq!(cfn_template.parameters, cfn_tree.parameters);
        assert_eq!(cfn_template.mappings, cfn_tree.mappings);
        assert_eq!(cfn_template.outputs, cfn_tree.outputs);
        assert_eq!(cfn_template.conditions, cfn_tree.conditions);
        assert_eq!(cfn_template.resources, cfn_tree.resources);
    }};
}

#[test]
fn test_parse_tree_basics() {
    let a = json!({
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
    assert_resource_equal!("LogicalResource" => a, resource);
}

#[test]
fn test_basic_parse_tree_with_condition() {
    let a: Value = json!({
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
    assert_resource_equal!("LogicalResource" => a, resource);
}

#[test]
fn test_basic_parse_tree_with_metadata() {
    let a: Value = json!({
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
    assert_resource_equal!("LogicalResource" => a, resource);
}

#[test]
fn test_parse_tree_basics_with_deletion_policy() {
    let a: Value = json!({
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

    assert_resource_equal!("LogicalResource" => a, resource);
}

#[test]
fn test_parse_tree_sub_str() {
    let a = json!({
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
    assert_resource_equal!("LogicalResource" => a, resource);
}

#[test]
fn test_parse_tree_yaml_codes() {
    let a = json!({
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
    assert_resource_equal!("LogicalResource" => a, resource);
}
#[test]
fn test_parse_get_attr_shorthand() {
    let a = json!({
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
            "RoleName" => IntrinsicFunction::GetAtt{logical_name:"Foo".into(), attribute_name:"Bar".into()}.into()
        },
    };
    assert_resource_equal!("LogicalResource" => a, resource);
}

#[test]
fn test_parse_tree_sub_list() {
    let a = json!({
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

    let resource = ResourceAttributes {
        condition: Option::None,
        resource_type: "AWS::IAM::Role".into(),
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::None,
        depends_on: vec![],
        properties: map! {
            "RoleName" => IntrinsicFunction::Sub{
                string: "bobs-role-${Region}".into(),
                replaces: Some(ResourceValue::Object(map!{
                    "Region" =>  IntrinsicFunction::Ref("AWS::Region".into()).into()
                }))
            }.into()
        },
    };
    assert_resource_equal!("LogicalResource" => a, resource);
}

#[test]
fn test_parse_simple_json_template() {
    let cfn_template = json!({
        "Resources": {
            "EC2Instance": {
                "Type": "AWS::EC2::Instance",
                "Properties": {
                    "ImageId": "ami-0c55b159cbfafe1f0",
                    "InstanceType": "t2.micro",
                    "KeyName": "my-key-pair",
                    "BlockDeviceMappings": [
                    {
                        "DeviceName": "/dev/xvda",
                        "Ebs": {
                            "VolumeSize": 8,
                            "VolumeType": "gp2"
                        }
                    }
                    ]
                }
            },
            "EBSVolume": {
                "Type": "AWS::EC2::Volume",
                "Properties": {
                    "Size": 10,
                    "AvailabilityZone": "us-east-1a",
                    "VolumeType": "gp2"
                }
            },
            "VolumeAttachment": {
                "Type": "AWS::EC2::VolumeAttachment",
                "Properties": {
                    "InstanceId": null,
                    "VolumeId": null,
                    "Device": "/dev/xvdf"
                }
            }
        }
    });

    let resources = IndexMap::from([
        (
            "EC2Instance".into(),
            ResourceAttributes {
                condition: Option::None,
                resource_type: "AWS::EC2::Instance".into(),
                metadata: Option::None,
                update_policy: Option::None,
                deletion_policy: Option::None,
                depends_on: vec![],
                properties: map! {
                    "ImageId" => ResourceValue::String("ami-0c55b159cbfafe1f0".into()),
                    "InstanceType" => ResourceValue::String("t2.micro".into()),
                    "KeyName" => ResourceValue::String("my-key-pair".into()),
                    "BlockDeviceMappings" => ResourceValue::Array(vec![
                        ResourceValue::Object(map!{
                            "DeviceName" => ResourceValue::String("/dev/xvda".into()),
                            "Ebs" => ResourceValue::Object(map!{
                                "VolumeSize" => ResourceValue::Number(8),
                                "VolumeType" => ResourceValue::String("gp2".into())
                            })
                        })
                    ])
                },
            },
        ),
        (
            "EBSVolume".into(),
            ResourceAttributes {
                condition: Option::None,
                resource_type: "AWS::EC2::Volume".into(),
                metadata: Option::None,
                update_policy: Option::None,
                deletion_policy: Option::None,
                depends_on: vec![],
                properties: map! {
                    "Size" => ResourceValue::Number(10),
                    "AvailabilityZone" => ResourceValue::String("us-east-1a".into()),
                    "VolumeType" => ResourceValue::String("gp2".into())
                },
            },
        ),
        (
            "VolumeAttachment".into(),
            ResourceAttributes {
                condition: Option::None,
                resource_type: "AWS::EC2::VolumeAttachment".into(),
                metadata: Option::None,
                update_policy: Option::None,
                deletion_policy: Option::None,
                depends_on: vec![],
                properties: map! {
                    "InstanceId" => ResourceValue::Null,
                    "VolumeId" => ResourceValue::Null,
                    "Device" => ResourceValue::String("/dev/xvdf".into())
                },
            },
        ),
    ]);

    let cfn_tree = CloudformationParseTree {
        description: None,
        transforms: vec![],
        parameters: IndexMap::default(),
        mappings: IndexMap::default(),
        conditions: IndexMap::default(),
        resources,
        outputs: IndexMap::default(),
    };

    assert_template_equal!(cfn_template, cfn_tree)
}

#[test]
fn test_parse_tree_with_fnjoin() {
    let a = json!({
            "MyBucket": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": {
                        "Fn::Join": [
                            "-",
                            [
                                "my-bucket-prefix",
                                { "Ref": "AWS::Region" },
                                { "Ref": "AWS::AccountId" }
                            ]
                        ]
                    }
                }
            }
    });
    let resource = ResourceAttributes {
        condition: Option::None,
        resource_type: "AWS::S3::Bucket".into(),
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::None,
        depends_on: vec![],
        properties: map! {
            "BucketName" => IntrinsicFunction::Join{
                sep: "-".into(),
                list: ResourceValue::Array(vec![
                    ResourceValue::String("my-bucket-prefix".into()),
                    IntrinsicFunction::Ref("AWS::Region".into()).into(),
                    IntrinsicFunction::Ref("AWS::AccountId".into()).into()
                ])
            }.into()
        },
    };
    assert_resource_equal!("MyBucket" => a, resource);
}

#[test]
fn test_parse_tree_with_fnfindinmap() {
    let cfn_template = json!(
        {
            "Resources": {
                "MyInstance": {
                    "Type": "AWS::EC2::Instance",
                    "Properties": {
                        "InstanceType": { "Fn::FindInMap": [ "InstanceTypes", { "Ref": "Region" }, "t2.micro" ] },
                        "ImageId": { "Fn::FindInMap": [ "AMIIds", { "Ref": "Region" }, "AmazonLinuxAMI" ] }
                    }
                }
            },
            "Mappings": {
                "InstanceTypes": {
                    "us-east-1": {
                        "t2.micro": "t2.micro",
                        "t2.small": "t2.small"
                    },
                    "us-west-2": {
                        "t2.micro": "t2.nano",
                        "t2.small": "t2.micro"
                    }
                },
                "AMIIds": {
                    "us-east-1": {
                        "AmazonLinuxAMI": "ami-0ff8a91507f77f867",
                        "UbuntuAMI": "ami-0c55b159cbfafe1f0"
                    },
                    "us-west-2": {
                        "AmazonLinuxAMI": "ami-0323c3dd2da7fb37d",
                        "UbuntuAMI": "ami-0bdb1d6c15a40392c"
                    }
                }
            }
        }

    );

    let resources = IndexMap::from([(
        "MyInstance".into(),
        ResourceAttributes {
            condition: Option::None,
            resource_type: "AWS::EC2::Instance".into(),
            metadata: Option::None,
            update_policy: Option::None,
            deletion_policy: Option::None,
            depends_on: vec![],
            properties: map! {
                "InstanceType" => IntrinsicFunction::FindInMap{
                    map_name:ResourceValue::String("InstanceTypes".into()),
                    top_level_key:IntrinsicFunction::Ref("Region".into()).into(),
                    second_level_key:ResourceValue::String("t2.micro".into()),
                }.into(),
                "ImageId" => IntrinsicFunction::FindInMap{
                    map_name:ResourceValue::String("AMIIds".into()),
                    top_level_key:IntrinsicFunction::Ref("Region".into()).into(),
                    second_level_key: ResourceValue::String("AmazonLinuxAMI".into()),
                }.into()
            },
        },
    )]);

    let cfn_tree = CloudformationParseTree {
        description: None,
        transforms: vec![],
        parameters: IndexMap::default(),
        mappings: map! {
            "InstanceTypes" => MappingTable {
                mappings: map! {
                        "us-east-1" => map! {
                            "t2.micro" => MappingInnerValue::String("t2.micro".into()),
                            "t2.small" => MappingInnerValue::String("t2.small".into())
                        },
                        "us-west-2" => map! {
                            "t2.micro" => MappingInnerValue::String("t2.nano".into()),
                            "t2.small" => MappingInnerValue::String("t2.micro".into())
                        }
                },
            },
            "AMIIds" => MappingTable {
                mappings: map! {
                        "us-east-1" => map! {
                            "AmazonLinuxAMI" => MappingInnerValue::String("ami-0ff8a91507f77f867".into()),
                            "UbuntuAMI" => MappingInnerValue::String("ami-0c55b159cbfafe1f0".into())
                        },
                        "us-west-2" => map! {
                            "AmazonLinuxAMI" => MappingInnerValue::String("ami-0323c3dd2da7fb37d".into()),
                            "UbuntuAMI" => MappingInnerValue::String("ami-0bdb1d6c15a40392c".into())
                        }
                },
            }
        },
        conditions: IndexMap::default(),
        resources,
        outputs: IndexMap::default(),
    };

    assert_template_equal!(cfn_template, cfn_tree)
}

#[test]
fn test_parse_tree_resource_with_floats() {
    let a = json!({
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

    let resource = ResourceAttributes {
        condition: Option::None,
        resource_type: "AWS::CloudWatch::Alarm".into(),
        metadata: Option::None,
        update_policy: Option::None,
        deletion_policy: Option::None,
        depends_on: vec![],
        properties: map! {
            "AlarmName" => IntrinsicFunction::Sub{
                string: "${Tag}-FrontendDistributedCacheTrafficImbalanceAlarm".into(),
                replaces: Some(ResourceValue::Object(map!{
                    "Tag" =>  IntrinsicFunction::Ref("AWS::Region".into()).into()
                }))
            }.into(),
            "ComparisonOperator" => ResourceValue::String("GreaterThanOrEqualToThreshold".to_string()),
            "Threshold" => ResourceValue::Double(WrapperF64::new(3.5))
        },
    };
    assert_resource_equal!("Alarm" => a, resource);
}

#[test]
fn test_parse_tree_resource_with_fn_and() {
    let cfn_template = json!({
        "Conditions": {
            "IsProduction": {
                "Fn::Equals": [
                    { "Ref": "Environment" },
                    "prod"
                ]
            },
            "HasDatabase": {
                "Fn::Equals": [
                    { "Ref": "DatabaseType" },
                    "mysql"
                ]
            },
            "UseEncryption": {
                "Fn::And": [
                    { "Condition": "IsProduction" },
                    { "Condition": "HasDatabase" },
                ]
            }
        },
        "Resources": {
            "MyApp": {
                "Type": "AWS::EC2::Instance",
                "Properties": {
                    "ImageId": {
                        "Fn::If": [
                            "UseEncryption",
                            { "Ref": "EncryptedAmi" },
                            { "Ref": "UnencryptedAmi" }
                        ]
                    }
                }
            }
        },
        "Parameters": {
            "Environment": {
                "Type": "String",
                "AllowedValues": [ "dev", "test", "prod" ],
                "Default": "dev"
            },
            "DatabaseType": {
                "Type": "String",
                "AllowedValues": [ "mysql", "postgresql" ],
                "Default": "postgresql"
            },
            "UseEncryption": {
                "Type": "String",
                "AllowedValues": [ "true", "false" ],
                "Default": "false"
            },
            "EncryptedAmi": {
                "Type": "String",
                "Default": "ami-1234567890abcdef0"
            },
            "UnencryptedAmi": {
                "Type": "String",
                "Default": "ami-0987654321fedcba0"
            }
        }
    });

    let resources = IndexMap::from([(
        "MyApp".into(),
        ResourceAttributes {
            condition: Option::None,
            resource_type: "AWS::EC2::Instance".into(),
            metadata: Option::None,
            update_policy: Option::None,
            deletion_policy: Option::None,
            depends_on: vec![],
            properties: map! {
                "ImageId" => IntrinsicFunction::If{
                    condition_name: "UseEncryption".into(),
                        value_if_true: IntrinsicFunction::Ref("EncryptedAmi".into()).into(),
                        value_if_false: IntrinsicFunction::Ref("UnencryptedAmi".into()).into(),
                }.into()
            },
        },
    )]);

    let cfn_tree = CloudformationParseTree {
        parameters: IndexMap::from([
            (
                "Environment".into(),
                Parameter {
                    parameter_type: ParameterType::String,
                    description: Option::None,
                    allowed_values: Option::Some(vec!["dev".into(), "test".into(), "prod".into()]),
                    default: Option::Some("dev".into()),
                },
            ),
            (
                "DatabaseType".into(),
                Parameter {
                    parameter_type: ParameterType::String,
                    description: Option::None,
                    allowed_values: Option::Some(vec!["mysql".into(), "postgresql".into()]),
                    default: Option::Some("postgresql".into()),
                },
            ),
            (
                "UseEncryption".into(),
                Parameter {
                    parameter_type: ParameterType::String,
                    description: Option::None,
                    allowed_values: Option::Some(vec!["true".into(), "false".into()]),
                    default: Option::Some("false".into()),
                },
            ),
            (
                "EncryptedAmi".into(),
                Parameter {
                    parameter_type: ParameterType::String,
                    description: Option::None,
                    allowed_values: Option::None,
                    default: Option::Some("ami-1234567890abcdef0".into()),
                },
            ),
            (
                "UnencryptedAmi".into(),
                Parameter {
                    parameter_type: ParameterType::String,
                    description: Option::None,
                    allowed_values: Option::None,
                    default: Option::Some("ami-0987654321fedcba0".into()),
                },
            ),
        ]),
        mappings: IndexMap::default(),
        conditions: map! {
            "IsProduction" => ConditionFunction::Equals(ConditionValue::Ref("Environment".into()), ConditionValue::String("prod".into())),
            "HasDatabase" => ConditionFunction::Equals(ConditionValue::Ref("DatabaseType".into()), ConditionValue::String("mysql".into())),
            "UseEncryption" => ConditionFunction::And(vec![
                ConditionValue::Condition("IsProduction".into()),
                ConditionValue::Condition("HasDatabase".into())
            ])
        },
        resources,
        outputs: IndexMap::default(),
        description: Option::None,
        transforms: vec![],
    };

    assert_template_equal!(cfn_template, cfn_tree)
}
