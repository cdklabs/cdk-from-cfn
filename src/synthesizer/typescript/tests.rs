// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use super::*;
use crate::cdk::Schema;
use crate::ir::CloudformationProgramIr;
use crate::CloudformationParseTree;
use std::str::FromStr;

#[test]
fn pretty_name_fixes() {
    assert_eq!("vpc", pretty_name("VPC"));
    assert_eq!("vpcs", pretty_name("VPCs"));
    assert_eq!("objectAccess", pretty_name("GetObject"));
    assert_eq!("equalTo", pretty_name("Equals"));
    assert_eq!("providerArns", pretty_name("ProviderARNs"));
    assert_eq!("targetAZs", pretty_name("TargetAZs"));
    assert_eq!("diskSizeMBs", pretty_name("DiskSizeMBs"));
}

#[test]
fn test_invalid_organization() {
    let bad_org = "NotAws";
    let import_instruction = ImportInstruction {
        organization: bad_org.to_string(),
        service: Option::None,
    };
    let result = import_instruction.to_typescript().unwrap_err();
    let expected = format!("Expected organization to be AWS or Alexa. Found {bad_org}");
    assert_eq!(expected, result.to_string());
}

#[test]
fn test_alexa_organization() {
    let import_instruction = ImportInstruction {
        organization: "Alexa".to_string(),
        service: Some("ASK".to_string()),
    };
    let result = import_instruction.to_typescript();
    assert_eq!(
        "import * as ask from 'aws-cdk-lib/alexa-ask';",
        result.unwrap()
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

#[test]
fn test_class_type_stack_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("extends cdk.Stack"),
        "Should extend cdk.Stack"
    );
    assert!(
        code.contains("scope: cdk.App"),
        "Should have scope: cdk.App"
    );
    assert!(
        code.contains("super(scope, id, props)"),
        "Should call super with props"
    );
    assert!(
        !code.contains("import { Construct }"),
        "Should not import Construct"
    );
}

#[test]
fn test_class_type_construct_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize(
        "typescript",
        &mut output,
        "TestConstruct",
        ClassType::Construct,
    )
    .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("extends Construct"),
        "Should extend Construct"
    );
    assert!(
        code.contains("scope: Construct"),
        "Should have scope: Construct"
    );
    assert!(
        code.contains("super(scope, id)"),
        "Should call super without props"
    );
    assert!(
        code.contains("import { Construct } from 'constructs'"),
        "Should import Construct"
    );
    assert!(
        code.contains("cdk.Stack.of(this).stackName"),
        "Should use cdk.Stack.of(this) for pseudo-params"
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
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("this.addTransform('AWS::Serverless-2016-10-31')"),
        "Stack mode should use this.addTransform"
    );
}

#[test]
fn test_add_transform_construct_mode() {
    let cfn: CloudformationParseTree = serde_json::from_str(TEMPLATE_WITH_TRANSFORM).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize(
        "typescript",
        &mut output,
        "TestConstruct",
        ClassType::Construct,
    )
    .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("cdk.Stack.of(this).addTransform('AWS::Serverless-2016-10-31')"),
        "Construct mode should use cdk.Stack.of(this).addTransform"
    );
}

#[test]
fn test_class_type_default_is_stack() {
    let cfn: CloudformationParseTree = serde_json::from_str(SIMPLE_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::default())
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("extends cdk.Stack"),
        "Default should extend cdk.Stack"
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
    ir.synthesize(
        "typescript",
        &mut output,
        "TestConstruct",
        ClassType::Construct,
    )
    .unwrap();
    let code = String::from_utf8(output).unwrap();

    // Should extend Construct
    assert!(
        code.contains("extends Construct"),
        "Should extend Construct"
    );

    // Should have props interface with parameters
    assert!(
        code.contains("bucketName"),
        "Should have bucketName parameter"
    );
    assert!(
        code.contains("enableVersioning"),
        "Should have enableVersioning parameter"
    );

    // Should call super without props
    assert!(
        code.contains("super(scope, id)"),
        "Should call super without props"
    );

    // Should import Construct
    assert!(
        code.contains("import { Construct } from 'constructs'"),
        "Should import Construct"
    );
}

#[test]
fn test_stack_mode_with_props() {
    let cfn: CloudformationParseTree = serde_json::from_str(TEMPLATE_WITH_PARAMS).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    // Should extend Stack
    assert!(
        code.contains("extends cdk.Stack"),
        "Should extend cdk.Stack"
    );

    // Should have props interface with parameters
    assert!(
        code.contains("bucketName"),
        "Should have bucketName parameter"
    );
    assert!(
        code.contains("enableVersioning"),
        "Should have enableVersioning parameter"
    );

    // Should call super with props
    assert!(
        code.contains("super(scope, id, props)"),
        "Should call super with props"
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
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(code.contains("new cdk.CfnCustomResource(this, 'MyCustomResource', {"));
    assert!(code.contains("serviceToken: backingLambda.attrArn,"));
    assert!(code.contains("myCustomResource.addOverride('Type', 'Custom::DatabaseSetup');"));
    assert!(code.contains("myCustomResource.addPropertyOverride('DatabaseName',"));
    assert!(code.contains("myCustomResource.addPropertyOverride('TableCount',"));
    assert!(!code.contains("addPropertyOverride('ServiceToken'"));
}

#[test]
fn test_custom_resource_getatt() {
    let cfn: CloudformationParseTree =
        serde_json::from_str(CUSTOM_RESOURCE_BASIC_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    // Custom resource GetAtt should use dynamic getAtt().toString()
    assert!(code.contains("myCustomResource.getAtt('Endpoint').toString()"));
    // Standard resource GetAtt should use typed accessor
    assert!(code.contains("backingLambda.attrArn"));
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
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(code.contains("? new cdk.CfnCustomResource(this, 'MyCustomResource', {"));
    assert!(code.contains(": undefined;"));
    assert!(code.contains("?.addOverride('Type', 'Custom::Setup');"));
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
            "DeletionPolicy": "Retain",
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
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(code.contains("new cdk.CfnCustomResource(this, 'MyCustomResource', {"));
    assert!(code.contains("serviceToken: backingLambda.attrArn,"));
    assert!(code.contains("myCustomResource.addPropertyOverride('DatabaseName',"));
    // Should NOT have addOverride('Type', ...) since type is already correct
    assert!(!code.contains("addOverride('Type',"));
    // Should NOT import aws-cloudformation
    assert!(!code.contains("aws-cloudformation"));
    // GetAtt should use dynamic lookup
    assert!(code.contains("myCustomResource.getAtt('Endpoint').toString()"));
    // DeletionPolicy should still work
    assert!(code.contains("cfnOptions.deletionPolicy = cdk.CfnDeletionPolicy.RETAIN"));
}

const FIND_IN_MAP_TEMPLATE: &str = r#"{
    "Parameters": {
        "Stage": { "Type": "String", "Default": "dev" }
    },
    "Mappings": {
        "EnvMap": {
            "dev": { "Size": 1 },
            "prod": { "Size": 3 }
        },
        "RegionMapping": {
            "us-east-1": { "Name": "east" },
            "us-west-2": { "Name": "west" }
        }
    },
    "Resources": {
        "Queue": {
            "Type": "AWS::SQS::Queue",
            "Properties": {
                "DelaySeconds": { "Fn::FindInMap": ["EnvMap", { "Ref": "Stage" }, "Size"] },
                "QueueName": { "Fn::FindInMap": ["RegionMapping", { "Ref": "AWS::Region" }, "Name"] }
            }
        }
    }
}"#;

fn synthesize_find_in_map(class_type: ClassType) -> String {
    let cfn: CloudformationParseTree = serde_json::from_str(FIND_IN_MAP_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();
    let mut output = Vec::new();
    ir.synthesize("typescript", &mut output, "FindInMap", class_type)
        .unwrap();
    String::from_utf8(output).unwrap()
}

#[test]
fn find_in_map_with_parameter_key_uses_dictionary() {
    let code = synthesize_find_in_map(ClassType::Stack);
    assert!(code.contains("delaySeconds: envMap[props.stage!]['Size'],"));
    assert!(!code.contains("envMapCfnMapping"));
}

#[test]
fn find_in_map_with_token_key_uses_cfn_mapping() {
    let code = synthesize_find_in_map(ClassType::Stack);
    assert!(code.contains(
        "const regionMappingCfnMapping = new cdk.CfnMapping(this, 'RegionMapping', { mapping: regionMapping });"
    ));
    assert!(code.contains("queueName: regionMappingCfnMapping.findInMap(this.region, 'Name'),"));

    // In a construct the CfnMapping gets a generated logical id, so lookups must go through the
    // CfnMapping object rather than a hard-coded mapping name.
    let code = synthesize_find_in_map(ClassType::Construct);
    assert!(code.contains(
        "queueName: regionMappingCfnMapping.findInMap(cdk.Stack.of(this).region, 'Name'),"
    ));
    assert!(!code.contains("Fn.findInMap"));
}

const SUB_SPECIAL_CHARACTERS_TEMPLATE: &str = r##"{
    "Resources": {
        "Topic": {
            "Type": "AWS::SNS::Topic",
            "Properties": {
                "DisplayName": {
                    "Fn::Sub": "#!/bin/bash\n\necho `date` \\$(id) ${!Literal} ${AWS::Region}\n  indented\n"
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
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains(
            "`#!/bin/bash\n\necho \\`date\\` \\\\$(id) \\${Literal} ${this.region}\n  indented\n`"
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
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("`line1\\r\n${queue.attrArn}\\r\n`"),
        "unexpected output:\n{code}"
    );
}

const METADATA_SPECIAL_KEYS_TEMPLATE: &str = r#"{
    "Resources": {
        "MyBucket": {
            "Type": "AWS::S3::Bucket",
            "Metadata": {
                "AWS::CloudFormation::Init": {
                    "configSets": {
                        "MountConfig": ["setup"]
                    },
                    "setup": {
                        "packages": {
                            "yum": {
                                "nfs-utils": []
                            }
                        },
                        "files": {
                            "/home/ec2-user/post_nfsstat": {
                                "mode": "000755"
                            }
                        }
                    }
                },
                "CostCenter": 1337,
                "cfn-lint": {
                    "it's": "ignored",
                    "": "empty-key"
                }
            }
        }
    }
}"#;

#[test]
fn test_metadata_quotes_non_identifier_keys() {
    let cfn: CloudformationParseTree =
        serde_json::from_str(METADATA_SPECIAL_KEYS_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(code.contains("'AWS::CloudFormation::Init': {"), "{code}");
    assert!(code.contains("configSets: {"), "{code}");
    assert!(code.contains("'nfs-utils': ["), "{code}");
    assert!(code.contains("'/home/ec2-user/post_nfsstat': {"), "{code}");
    assert!(code.contains("CostCenter: 1337,"), "{code}");
    assert!(code.contains("'cfn-lint': {"), "{code}");
    assert!(code.contains("'it\\'s': 'ignored',"), "{code}");
    assert!(code.contains("'': 'empty-key',"), "{code}");
}

const MAP_SPECIAL_KEYS_TEMPLATE: &str = r#"{
    "Resources": {
        "MyFunction": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "Code": {
                    "S3Bucket": "my-bucket",
                    "S3Key": "code.zip"
                },
                "Role": "arn:aws:iam::123456789012:role/lambda-role",
                "Handler": "index.handler",
                "Runtime": "nodejs20.x",
                "Environment": {
                    "Variables": {
                        "SIMPLE_KEY": "ok",
                        "hyphen-key": "val",
                        "it's": "quoted",
                        "": "empty"
                    }
                }
            }
        }
    }
}"#;

#[test]
fn test_map_property_quotes_and_escapes_special_keys() {
    let cfn: CloudformationParseTree = serde_json::from_str(MAP_SPECIAL_KEYS_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(code.contains("'SIMPLE_KEY': 'ok',"), "{code}");
    assert!(code.contains("'hyphen-key': 'val',"), "{code}");
    assert!(code.contains("'it\\'s': 'quoted',"), "{code}");
    assert!(code.contains("'': 'empty',"), "{code}");
}

const PARAMETER_LOGICAL_IDS_TEMPLATE: &str = r#"{
    "Parameters": {
        "SSHKeyName": { "Type": "AWS::EC2::KeyPair::KeyName", "Default": "my-key" },
        "DBPassword": { "Type": "String", "NoEcho": "true", "Default": "secret" }
    },
    "Resources": {
        "Instance": {
            "Type": "AWS::EC2::Instance",
            "Properties": {
                "KeyName": { "Ref": "SSHKeyName" }
            }
        }
    }
}"#;

#[test]
fn test_cfn_parameter_keeps_logical_id() {
    let cfn: CloudformationParseTree =
        serde_json::from_str(PARAMETER_LOGICAL_IDS_TEMPLATE).unwrap();
    let ir = CloudformationProgramIr::from(cfn, Schema::builtin()).unwrap();

    let mut output = Vec::new();
    ir.synthesize("typescript", &mut output, "TestStack", ClassType::Stack)
        .unwrap();
    let code = String::from_utf8(output).unwrap();

    assert!(
        code.contains("sshKeyName: new cdk.CfnParameter(this, 'SSHKeyName', {"),
        "unexpected output:\n{code}"
    );
    assert!(
        code.contains("dbPassword: new cdk.CfnParameter(this, 'DBPassword', {"),
        "unexpected output:\n{code}"
    );
}
