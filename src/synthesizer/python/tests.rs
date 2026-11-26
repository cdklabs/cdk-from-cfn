// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use crate::cdk::Schema;
use crate::ir::CloudformationProgramIr;
use crate::ir::{conditions::ConditionIr, importer::ImportInstruction};
use crate::synthesizer::ClassType;
use crate::CloudformationParseTree;
use std::str::FromStr;

use super::synthesize_condition_recursive;

#[test]
fn test_invalid_organization() {
    let bad_org = "NotAws";
    let import_instruction = ImportInstruction {
        organization: bad_org.to_string(),
        service: Option::None,
    };
    let result = import_instruction.to_python().unwrap_err();
    let expected = format!("Expected organization to be AWS or Alexa. Found {bad_org}");
    assert_eq!(expected, result.to_string());
}

#[test]
fn test_alexa_org() {
    let import_instruction = ImportInstruction {
        organization: "Alexa".into(),
        service: Some("Ask".into()),
    };
    let result = import_instruction.to_python();
    assert_eq!("import alexa_ask as ask from ask", result.unwrap());
}

#[test]
fn test_condition_ir_not_simple() {
    let condition_ir = ConditionIr::Not(Box::new(ConditionIr::Condition("condition".into())));
    let result = synthesize_condition_recursive(&condition_ir, ClassType::Stack);
    assert_eq!("not (condition)", result);
}

#[test]
fn test_condition_ir_map() {
    let condition_ir = ConditionIr::Map(
        "ConditionIrMap".into(),
        Box::new(ConditionIr::Str("FirstLevelKey".into())),
        Box::new(ConditionIr::Str("SecondLevelKey".into())),
    );
    let result = synthesize_condition_recursive(&condition_ir, ClassType::Stack);
    assert_eq!(
        "condition_ir_map['FirstLevelKey']['SecondLevelKey']",
        result
    );
}

const SIMPLE_TEMPLATE: &str = r#"{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Description": "Test template",
    "Resources": {
        "MyBucket": {
            "Type": "AWS::S3::Bucket",
            "Properties": {
                "BucketName": {"Fn::Sub": "${AWS::StackName}-bucket"}
            }
        }
    }
}"#;

fn assert_conditional_resource_has_no_empty_guard(
    resource_type: &str,
    properties: serde_json::Value,
) {
    let template = serde_json::json!({
        "Conditions": {"CreateResource": {"Fn::Equals": ["yes", "yes"]}},
        "Resources": {
            "ConditionalResource": {
                "Type": resource_type,
                "Condition": "CreateResource",
                "Properties": properties
            }
        }
    });
    for class_type in [ClassType::Stack, ClassType::Construct] {
        let cfn: CloudformationParseTree = serde_json::from_value(template.clone()).unwrap();
        let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();
        let mut output = Vec::new();
        ir.synthesize("python", &mut output, "TestStack", class_type)
            .unwrap();
        let code = String::from_utf8(output).unwrap();

        assert!(
            !code
                .trim_end()
                .ends_with("if (conditionalResource is not None):"),
            "Conditional resource leaves an empty Python suite:\n{code}"
        );
    }
}

#[test]
fn test_conditional_resource_without_attributes() {
    assert_conditional_resource_has_no_empty_guard("AWS::S3::Bucket", serde_json::json!({}));
}

#[test]
fn test_conditional_cfn_custom_resource_without_attributes() {
    assert_conditional_resource_has_no_empty_guard(
        "AWS::CloudFormation::CustomResource",
        serde_json::json!({"ServiceToken": "arn:aws:lambda:us-east-1:123456789:function:handler"}),
    );
}

#[test]
fn test_conditional_resource_with_attributes_keeps_guard() {
    for attributes in [
        serde_json::json!({"Metadata": {"note": "test"}}),
        serde_json::json!({
            "UpdatePolicy": {"AutoScalingRollingUpdate": {"MinInstancesInService": 1}}
        }),
        serde_json::json!({"DeletionPolicy": "Retain"}),
        serde_json::json!({"DependsOn": ["OtherBucket"]}),
    ] {
        let mut resource = serde_json::json!({
            "Type": "AWS::S3::Bucket",
            "Condition": "CreateResource"
        });
        resource
            .as_object_mut()
            .unwrap()
            .extend(attributes.as_object().unwrap().clone());
        let template = serde_json::json!({
            "Conditions": {"CreateResource": {"Fn::Equals": ["yes", "yes"]}},
            "Resources": {
                "OtherBucket": {"Type": "AWS::S3::Bucket"},
                "ConditionalResource": resource
            }
        });
        for class_type in [ClassType::Stack, ClassType::Construct] {
            let cfn: CloudformationParseTree = serde_json::from_value(template.clone()).unwrap();
            let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();
            let mut output = Vec::new();
            ir.synthesize("python", &mut output, "TestStack", class_type)
                .unwrap();
            let code = String::from_utf8(output).unwrap();

            assert!(
                code.contains("if (conditionalResource is not None):\n      conditionalResource."),
                "Conditional resource attributes must stay inside the guard:\n{code}"
            );
        }
    }
}

#[test]
fn test_class_type_stack_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("class TestStack(Stack):"),
        "Should extend Stack"
    );
    assert!(
        code.contains("super().__init__(scope, construct_id, **kwargs)"),
        "Should call super with kwargs"
    );
    assert!(
        code.contains("self.stack_name"),
        "Should use self.stack_name for pseudo-params"
    );
}

#[test]
fn test_class_type_construct_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestConstruct", ClassType::Construct)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("class TestConstruct(Construct):"),
        "Should extend Construct"
    );
    assert!(
        code.contains("super().__init__(scope, construct_id)"),
        "Should call super without kwargs"
    );
    assert!(
        !code.contains("super().__init__(scope, construct_id, **kwargs)"),
        "Super call should not have kwargs"
    );
    assert!(
        code.contains("Stack.of(self).stack_name"),
        "Should use Stack.of(self) for pseudo-params"
    );
}

const TEMPLATE_WITH_TRANSFORM: &str = r#"{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Transform": "AWS::Serverless-2016-10-31",
    "Resources": {
        "MyBucket": {
            "Type": "AWS::S3::Bucket"
        }
    }
}"#;

#[test]
fn test_add_transform_stack_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(TEMPLATE_WITH_TRANSFORM).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("Stack.add_transform(self, 'AWS::Serverless-2016-10-31')"),
        "Stack mode should use Stack.add_transform(self, ...)"
    );
}

#[test]
fn test_add_transform_construct_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(TEMPLATE_WITH_TRANSFORM).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestConstruct", ClassType::Construct)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("Stack.of(self).add_transform('AWS::Serverless-2016-10-31')"),
        "Construct mode should use Stack.of(self).add_transform(...)"
    );
}

#[test]
fn test_class_type_default_is_stack() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", ClassType::default())
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("class TestStack(Stack):"),
        "Default should extend Stack"
    );
}

#[test]
fn test_class_type_from_str_valid() {
    assert_eq!(ClassType::from_str("stack").unwrap(), ClassType::Stack);
    assert_eq!(
        ClassType::from_str("construct").unwrap(),
        ClassType::Construct
    );
}

#[test]
fn test_class_type_from_str_invalid() {
    let result = ClassType::from_str("invalid");
    assert!(result.is_err());
    assert_eq!(
        result.unwrap_err(),
        "Invalid class type: 'invalid'. Expected 'stack' or 'construct'"
    );
}

const TEMPLATE_WITH_PARAMS: &str = r#"{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Parameters": {
        "BucketName": {
            "Type": "String",
            "Default": "my-bucket"
        },
        "EnableVersioning": {
            "Type": "String",
            "Default": "false"
        }
    },
    "Resources": {
        "MyBucket": {
            "Type": "AWS::S3::Bucket",
            "Properties": {
                "BucketName": {"Ref": "BucketName"}
            }
        }
    }
}"#;

#[test]
fn test_construct_mode_with_props() {
    let cfn: CloudformationParseTree = serde_json::from_str(TEMPLATE_WITH_PARAMS).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestConstruct", ClassType::Construct)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    // Should extend Construct
    assert!(
        code.contains("class TestConstruct(Construct):"),
        "Should extend Construct"
    );

    // Should have parameters in props
    assert!(
        code.contains("bucketName"),
        "Should have bucketName parameter"
    );
    assert!(
        code.contains("enableVersioning"),
        "Should have enableVersioning parameter"
    );

    // Should call super without kwargs
    assert!(
        code.contains("super().__init__(scope, construct_id)"),
        "Should call super without kwargs"
    );
}

#[test]
fn test_stack_mode_with_props() {
    let cfn: CloudformationParseTree = serde_json::from_str(TEMPLATE_WITH_PARAMS).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    // Should extend Stack
    assert!(
        code.contains("class TestStack(Stack):"),
        "Should extend Stack"
    );

    // Should have parameters in props
    assert!(
        code.contains("bucketName"),
        "Should have bucketName parameter"
    );
    assert!(
        code.contains("enableVersioning"),
        "Should have enableVersioning parameter"
    );

    // Should call super with kwargs
    assert!(
        code.contains("super().__init__(scope, construct_id, **kwargs)"),
        "Should call super with kwargs"
    );
}

// --- Custom Resource Tests ---

const CUSTOM_RESOURCE_BASIC_TEMPLATE: &str = r#"{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Resources": {
        "BackingLambda": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "Runtime": "python3.9",
                "Handler": "index.handler",
                "Role": "arn:aws:iam::123456789:role/role",
                "Code": { "S3Bucket": "bucket", "S3Key": "key.zip" }
            }
        },
        "MyCustomResource": {
            "Type": "Custom::DatabaseSetup",
            "DeletionPolicy": "Retain",
            "DependsOn": ["BackingLambda"],
            "Properties": {
                "ServiceToken": { "Fn::GetAtt": ["BackingLambda", "Arn"] },
                "DatabaseName": "mydb",
                "TableCount": 5
            }
        },
        "ConsumerLambda": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "Runtime": "python3.9",
                "Handler": "index.handler",
                "Role": "arn:aws:iam::123456789:role/role",
                "Code": { "S3Bucket": "bucket", "S3Key": "key.zip" },
                "Environment": {
                    "Variables": {
                        "DB_ENDPOINT": { "Fn::GetAtt": ["MyCustomResource", "Endpoint"] }
                    }
                }
            }
        }
    }
}"#;

#[test]
fn test_custom_resource_basic() {
    let cfn: CloudformationParseTree =
        serde_json::from_str(CUSTOM_RESOURCE_BASIC_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(code.contains("cdk.CfnCustomResource(self, 'MyCustomResource',"));
    assert!(code.contains("service_token = backingLambda.attr_arn,"));
    assert!(code.contains("myCustomResource.add_override('Type', 'Custom::DatabaseSetup')"));
    assert!(code.contains("myCustomResource.add_property_override('DatabaseName',"));
    assert!(code.contains("myCustomResource.add_property_override('TableCount',"));
    assert!(!code.contains("add_property_override('ServiceToken'"));
}

#[test]
fn test_custom_resource_getatt() {
    let cfn: CloudformationParseTree =
        serde_json::from_str(CUSTOM_RESOURCE_BASIC_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    // Custom resource GetAtt should use dynamic get_att().to_string()
    assert!(code.contains("myCustomResource.get_att('Endpoint').to_string()"));
    // Standard resource GetAtt should use typed accessor
    assert!(code.contains("backingLambda.attr_arn"));
}

const CUSTOM_RESOURCE_CONDITIONAL_TEMPLATE: &str = r#"{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Conditions": {
        "IsProduction": { "Fn::Equals": ["prod", "prod"] }
    },
    "Resources": {
        "MyCustomResource": {
            "Type": "Custom::Setup",
            "Condition": "IsProduction",
            "Properties": {
                "ServiceToken": "arn:aws:lambda:us-east-1:123456789:function:handler"
            }
        }
    }
}"#;

#[test]
fn test_custom_resource_conditional() {
    let cfn: CloudformationParseTree =
        serde_json::from_str(CUSTOM_RESOURCE_CONDITIONAL_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(code.contains("cdk.CfnCustomResource(self, 'MyCustomResource',"));
    assert!(code.contains("if is_production else None"));
    assert!(code.contains("if (myCustomResource is not None):"));
    assert!(code.contains("myCustomResource.add_override('Type', 'Custom::Setup')"));
}

// --- AWS::CloudFormation::CustomResource Tests ---

const CFN_CUSTOM_RESOURCE_TEMPLATE: &str = r#"{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Resources": {
        "BackingLambda": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "Runtime": "python3.9",
                "Handler": "index.handler",
                "Role": "arn:aws:iam::123456789:role/role",
                "Code": { "S3Bucket": "bucket", "S3Key": "key.zip" }
            }
        },
        "MyCustomResource": {
            "Type": "AWS::CloudFormation::CustomResource",
            "Properties": {
                "ServiceToken": { "Fn::GetAtt": ["BackingLambda", "Arn"] },
                "DatabaseName": "mydb"
            }
        },
        "ConsumerLambda": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "Runtime": "python3.9",
                "Handler": "index.handler",
                "Role": "arn:aws:iam::123456789:role/role",
                "Code": { "S3Bucket": "bucket", "S3Key": "key.zip" },
                "Environment": {
                    "Variables": {
                        "RESULT": { "Fn::GetAtt": ["MyCustomResource", "Endpoint"] }
                    }
                }
            }
        }
    }
}"#;

#[test]
fn test_cfn_custom_resource_no_type_override() {
    let cfn: CloudformationParseTree = serde_json::from_str(CFN_CUSTOM_RESOURCE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(code.contains("cdk.CfnCustomResource(self, 'MyCustomResource',"));
    assert!(code.contains("service_token = backingLambda.attr_arn,"));
    assert!(code.contains("myCustomResource.add_property_override('DatabaseName',"));
    assert!(!code.contains("add_override('Type',"));
    assert!(!code.contains("aws_cloudformation"));
    assert!(code.contains("myCustomResource.get_att('Endpoint').to_string()"));
}

// --- Condition tests ---

const NOT_EQUALS_PARAM_TEMPLATE: &str = r#"{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Parameters": {
        "PolicyName": { "Type": "String" }
    },
    "Conditions": {
        "ShouldEnable": {
            "Fn::Not": [{ "Fn::Equals": [{ "Ref": "PolicyName" }, "NONE"] }]
        }
    },
    "Resources": {
        "Queue": {
            "Type": "AWS::SQS::Queue",
            "Condition": "ShouldEnable"
        }
    }
}"#;

#[test]
fn test_not_equals_with_parameter_reference() {
    let cfn: CloudformationParseTree = serde_json::from_str(NOT_EQUALS_PARAM_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("should_enable = not (props['policyName'] == 'NONE')"),
        "Should reference the parameter through props, got:\n{code}"
    );
}

const SUB_SPECIAL_CHARACTERS_TEMPLATE: &str = r##"{
    "Resources": {
        "Topic": {
            "Type": "AWS::SNS::Topic",
            "Properties": {
                "DisplayName": {
                    "Fn::Sub": "#!/bin/bash\n\necho {} \\$(id) ${!Literal} ${AWS::Region}\n  indented \"quoted\""
                }
            }
        }
    }
}"##;

#[test]
fn test_sub_string_keeps_special_characters_and_line_starts() {
    let cfn: CloudformationParseTree =
        serde_json::from_str(SUB_SPECIAL_CHARACTERS_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains(
            "f\"\"\"#!/bin/bash\n\necho {{}} \\\\$(id) ${{Literal}} {self.region}\n  indented \\\"quoted\\\"\"\"\""
        ),
        "unexpected output:\n{code}"
    );
}

const SUB_WITH_VARIABLES_TEMPLATE: &str = r##"{
    "Resources": {
        "Queue": {
            "Type": "AWS::SQS::Queue"
        },
        "Topic": {
            "Type": "AWS::SNS::Topic",
            "Properties": {
                "DisplayName": {
                    "Fn::Sub": [
                        "line1\r\n${QueueArn}\r\n",
                        { "QueueArn": { "Fn::GetAtt": ["Queue", "Arn"] } }
                    ]
                }
            }
        }
    }
}"##;

#[test]
fn test_sub_string_with_variables_keeps_carriage_returns() {
    let cfn: CloudformationParseTree = serde_json::from_str(SUB_WITH_VARIABLES_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("f\"\"\"line1\\r\n{queue.attr_arn}\\r\n\"\"\""),
        "unexpected output:\n{code}"
    );
}

const AWS_TYPED_PARAMETERS_TEMPLATE: &str = r#"{
    "Parameters": {
        "VpcId": { "Type": "AWS::EC2::VPC::Id", "Description": "vpc" },
        "SubnetIds": { "Type": "List<AWS::EC2::Subnet::Id>", "Description": "subnets" }
    },
    "Resources": {
        "SecurityGroup": {
            "Type": "AWS::EC2::SecurityGroup",
            "Properties": {
                "GroupDescription": "test",
                "VpcId": { "Ref": "VpcId" }
            }
        },
        "SubnetGroup": {
            "Type": "AWS::RDS::DBSubnetGroup",
            "Properties": {
                "DBSubnetGroupDescription": "test",
                "SubnetIds": { "Ref": "SubnetIds" }
            }
        }
    }
}"#;

#[test]
fn test_aws_typed_parameters_are_unwrapped() {
    let cfn: CloudformationParseTree = serde_json::from_str(AWS_TYPED_PARAMETERS_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("description = 'vpc',\n      ).value_as_string,"),
        "unexpected output:\n{code}"
    );
    assert!(
        code.contains("description = 'subnets',\n      ).value_as_list,"),
        "unexpected output:\n{code}"
    );
    assert!(
        code.contains("vpc_id = props['vpcId'],"),
        "unexpected output:\n{code}"
    );
    assert!(
        code.contains("subnet_ids = props['subnetIds'],"),
        "unexpected output:\n{code}"
    );
}

const AWS_TYPED_NO_ECHO_PARAMETER_TEMPLATE: &str = r#"{
    "Parameters": {
        "TopicName": {
            "Type": "AWS::SSM::Parameter::Value<String>",
            "NoEcho": "True"
        }
    },
    "Resources": {
        "Topic": {
            "Type": "AWS::SNS::Topic",
            "Properties": {
                "TopicName": { "Ref": "TopicName" }
            }
        }
    }
}"#;

#[test]
fn test_aws_typed_no_echo_parameter_is_unwrapped_once() {
    let cfn: CloudformationParseTree =
        serde_json::from_str(AWS_TYPED_NO_ECHO_PARAMETER_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("topic_name = props['topicName'].value_as_string,"),
        "unexpected output:\n{code}"
    );
    assert_eq!(
        code.matches(".value_as_string").count(),
        1,
        "unexpected output:\n{code}"
    );
}

const NO_ECHO_STRING_PARAMETER_TEMPLATE: &str = r#"{
    "Parameters": {
        "TopicName": { "Type": "String", "NoEcho": "True", "Default": "abc" }
    },
    "Resources": {
        "Topic": {
            "Type": "AWS::SNS::Topic",
            "Properties": {
                "TopicName": { "Ref": "TopicName" }
            }
        }
    }
}"#;

#[test]
fn test_no_echo_string_parameter_is_a_cfn_parameter() {
    let cfn: CloudformationParseTree =
        serde_json::from_str(NO_ECHO_STRING_PARAMETER_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("python", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("'topicName': cdk.CfnParameter(self, 'TopicName',"),
        "unexpected output:\n{code}"
    );
    assert_eq!(
        code.matches(".value_as_string").count(),
        1,
        "unexpected output:\n{code}"
    );
}
