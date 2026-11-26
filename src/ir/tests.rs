// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use crate::cdk::Schema;
use crate::ir::CloudformationProgramIr;
use crate::synthesizer::ClassType;
use crate::CloudformationParseTree;

const CDK_DEPLOYED_JSON: &str = r#"{
  "Parameters": {
    "BootstrapVersion": {
      "Type": "AWS::SSM::Parameter::Value<String>",
      "Default": "/cdk-bootstrap/hnb659fds/version",
      "Description": "Version of the CDK Bootstrap resources in this environment, automatically retrieved from SSM Parameter Store. [cdk:skip]"
    },
    "UserQueueName": {
      "Type": "String",
      "Default": "my-queue"
    }
  },
  "Conditions": {
    "CDKMetadataAvailable": {
      "Fn::Or": [
        { "Fn::Equals": [{ "Ref": "AWS::Region" }, "us-east-1"] },
        { "Fn::Equals": [{ "Ref": "AWS::Region" }, "us-west-2"] }
      ]
    },
    "CreateBackup": {
      "Fn::Equals": [{ "Ref": "UserQueueName" }, "prod"]
    }
  },
  "Resources": {
    "AppQueueFD3F4958": {
      "Type": "AWS::SQS::Queue",
      "Properties": {
        "VisibilityTimeout": 300
      },
      "Metadata": {
        "aws:cdk:path": "AppStack/AppQueue/Resource"
      }
    },
    "AnnotatedQueue": {
      "Type": "AWS::SQS::Queue",
      "Properties": {
        "QueueName": { "Ref": "UserQueueName" }
      },
      "Metadata": {
        "aws:cdk:path": "AppStack/AnnotatedQueue/Resource",
        "CustomKey": "CustomValue"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/zPSMzQ10DNQ"
      },
      "Metadata": {
        "aws:cdk:path": "AppStack/CDKMetadata/Default"
      },
      "Condition": "CDKMetadataAvailable"
    }
  },
  "Rules": {
    "CheckBootstrapVersion": {
      "Assertions": [
        {
          "Assert": {
            "Fn::Not": [
              {
                "Fn::Contains": [
                  ["1", "2", "3", "4", "5"],
                  { "Ref": "BootstrapVersion" }
                ]
              }
            ]
          },
          "AssertDescription": "CDK bootstrap stack version 6 required."
        }
      ]
    }
  }
}"#;

#[test]
fn skips_cdk_generated_elements_and_preserves_user_content() {
    let parse_tree: CloudformationParseTree = serde_json::from_str(CDK_DEPLOYED_JSON).unwrap();
    let ir = CloudformationProgramIr::from(parse_tree, Schema::builtin()).unwrap();

    assert_eq!(ir.constructor.inputs.len(), 1);
    assert_eq!(ir.constructor.inputs[0].name, "userQueueName");

    assert_eq!(ir.conditions.len(), 1);
    assert_eq!(ir.conditions[0].name, "CreateBackup");

    assert_eq!(ir.resources.len(), 2);
    let app_queue = ir
        .resources
        .iter()
        .find(|r| r.name == "AppQueueFD3F4958")
        .expect("AppQueueFD3F4958 should be preserved");
    assert_eq!(app_queue.metadata, None);

    let annotated_queue = ir
        .resources
        .iter()
        .find(|r| r.name == "AnnotatedQueue")
        .expect("AnnotatedQueue should be preserved");
    assert!(annotated_queue.metadata.is_some());

    assert!(!ir.resources.iter().any(|r| r.name == "CDKMetadata"));

    #[cfg(feature = "typescript")]
    {
        let mut out = Vec::new();
        ir.synthesize("typescript", &mut out, "AppStack", ClassType::Stack)
            .unwrap();
        let code = String::from_utf8(out).unwrap();
        assert!(code.contains("AppQueueFD3F4958"));
        assert!(code.contains("CustomKey: 'CustomValue'") || code.contains("CustomKey"));
        assert!(!code.contains("aws:cdk:path"));
        assert!(!code.contains("CDKMetadata"));
        assert!(!code.contains("cdkMetadataAvailable"));
        assert!(!code.contains("BootstrapVersion"));
    }
}

#[test]
fn skips_cdk_generated_elements_in_yaml_template() {
    let yaml_template = r#"
Parameters:
  BootstrapVersion:
    Type: AWS::SSM::Parameter::Value<String>
    Default: /cdk-bootstrap/hnb659fds/version
    Description: Version of the CDK Bootstrap resources in this environment. [cdk:skip]
Conditions:
  CDKMetadataAvailable:
    !Or
      - !Equals [!Ref "AWS::Region", "us-east-1"]
      - !Equals [!Ref "AWS::Region", "us-west-2"]
Resources:
  AppQueue:
    Type: AWS::SQS::Queue
    Metadata:
      aws:cdk:path: AppStack/AppQueue/Resource
    Properties:
      VisibilityTimeout: 300
  CustomMetadataResource:
    Type: AWS::CDK::Metadata
    Condition: CDKMetadataAvailable
    Properties:
      Analytics: v2:deflate64:abc
Rules:
  CheckBootstrapVersion:
    Assertions:
      - Assert: !Not [!Contains [["1", "2", "3"], !Ref BootstrapVersion]]
        AssertDescription: CDK bootstrap stack version 4 required.
"#;

    let parse_tree: CloudformationParseTree = serde_yaml::from_str(yaml_template).unwrap();
    let ir = CloudformationProgramIr::from(parse_tree, Schema::builtin()).unwrap();

    assert!(ir.constructor.inputs.is_empty());
    assert!(ir.conditions.is_empty());
    assert_eq!(ir.resources.len(), 1);
    assert_eq!(ir.resources[0].name, "AppQueue");
    assert_eq!(ir.resources[0].metadata, None);
}

#[test]
fn preserves_bootstrap_version_parameter_without_cdk_skip_marker() {
    let json = r#"{
      "Parameters": {
        "BootstrapVersion": {
          "Type": "String",
          "Default": "1",
          "Description": "Custom user bootstrap version"
        }
      },
      "Resources": {
        "AppQueue": {
          "Type": "AWS::SQS::Queue",
          "Properties": {
            "QueueName": { "Ref": "BootstrapVersion" }
          }
        }
      }
    }"#;

    let parse_tree: CloudformationParseTree = serde_json::from_str(json).unwrap();
    let ir = CloudformationProgramIr::from(parse_tree, Schema::builtin()).unwrap();

    assert_eq!(ir.constructor.inputs.len(), 1);
    assert_eq!(ir.constructor.inputs[0].name, "bootstrapVersion");
}
