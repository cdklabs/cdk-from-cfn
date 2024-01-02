using Amazon.CDK;
using Amazon.CDK.AWS.Config;
using Amazon.CDK.AWS.EC2;
using Amazon.CDK.AWS.IAM;
using Amazon.CDK.AWS.Lambda;
using Amazon.CDK.AWS.S3;
using Amazon.CDK.AWS.SNS;
using Constructs;
using System.Collections.Generic;

namespace ConfigStack
{
    public class ConfigStackProps : StackProps
    {
        public bool? Ec2VolumeAutoEnableIo { get; set; }

        public string Ec2VolumeTagKey { get; set; }

    }

    /// <summary>
    /// AWS CloudFormation Sample Template Config: This template demonstrates the usage of AWS Config resources.  **WARNING** You will be billed for the AWS resources used if you create a stack from this template.
    /// </summary>
    public class ConfigStack : Stack
    {
        public object ConfigRuleForVolumeTagsArn { get; } 

        public object ConfigRuleForVolumeTagsConfigRuleId { get; } 

        public object ConfigRuleForVolumeAutoEnableIOComplianceType { get; } 

        public ConfigStack(Construct scope, string id, ConfigStackProps props = null) : base(scope, id, props)
        {
            // Applying default props
            props ??= new ConfigStackProps();
            props.Ec2VolumeAutoEnableIo ??= false;
            props.Ec2VolumeTagKey ??= "CostCenter";


            // Resources
            var configBucket = new CfnBucket(this, "ConfigBucket", new CfnBucketProps
            {
            });
            var configTopic = new CfnTopic(this, "ConfigTopic", new CfnTopicProps
            {
            });
            var ec2Volume = new CfnVolume(this, "Ec2Volume", new CfnVolumeProps
            {
                AutoEnableIo = props.Ec2VolumeAutoEnableIo,
                Size = 5,
                AvailabilityZone = Fn.Select(0, Fn.GetAzs("")),
                Tags = new []
                {
                    new CfnTag
                    {
                        Key = props.Ec2VolumeTagKey,
                        Value = "Ec2VolumeTagValue",
                    },
                },
            });
            var lambdaExecutionRole = new CfnRole(this, "LambdaExecutionRole", new CfnRoleProps
            {
                AssumeRolePolicyDocument = new Dictionary<string, object>
                {
                    { "Version", "2012-10-17"},
                    { "Statement", new []
                    {
                        new Dictionary<string, object>
                        {
                            { "Effect", "Allow"},
                            { "Principal", new Dictionary<string, object>
                            {
                                { "Service", new []
                                {
                                    "lambda.amazonaws.com",
                                }},
                            }},
                            { "Action", new []
                            {
                                "sts:AssumeRole",
                            }},
                        },
                    }},
                },
                Policies = new []
                {
                    new CfnRole.PolicyProperty
                    {
                        PolicyName = "root",
                        PolicyDocument = new Dictionary<string, object>
                        {
                            { "Version", "2012-10-17"},
                            { "Statement", new []
                            {
                                new Dictionary<string, object>
                                {
                                    { "Effect", "Allow"},
                                    { "Action", new []
                                    {
                                        "logs:*",
                                        "config:PutEvaluations",
                                        "ec2:DescribeVolumeAttribute",
                                    }},
                                    { "Resource", "*"},
                                },
                            }},
                        },
                    },
                },
            });
            var configRole = new CfnRole(this, "ConfigRole", new CfnRoleProps
            {
                AssumeRolePolicyDocument = new Dictionary<string, object>
                {
                    { "Version", "2012-10-17"},
                    { "Statement", new []
                    {
                        new Dictionary<string, object>
                        {
                            { "Effect", "Allow"},
                            { "Principal", new Dictionary<string, object>
                            {
                                { "Service", new []
                                {
                                    "config.amazonaws.com",
                                }},
                            }},
                            { "Action", new []
                            {
                                "sts:AssumeRole",
                            }},
                        },
                    }},
                },
                ManagedPolicyArns = new []
                {
                    "arn:aws:iam::aws:policy/service-role/AWSConfigRole",
                },
                Policies = new []
                {
                    new CfnRole.PolicyProperty
                    {
                        PolicyName = "root",
                        PolicyDocument = new Dictionary<string, object>
                        {
                            { "Version", "2012-10-17"},
                            { "Statement", new []
                            {
                                new Dictionary<string, object>
                                {
                                    { "Effect", "Allow"},
                                    { "Action", "s3:GetBucketAcl"},
                                    { "Resource", string.Join("", new []
                                    {
                                        "arn:aws:s3:::",
                                        configBucket.Ref,
                                    })},
                                },
                                new Dictionary<string, object>
                                {
                                    { "Effect", "Allow"},
                                    { "Action", "s3:PutObject"},
                                    { "Resource", string.Join("", new []
                                    {
                                        "arn:aws:s3:::",
                                        configBucket.Ref,
                                        "/AWSLogs/",
                                        Account,
                                        "/*",
                                    })},
                                    { "Condition", new Dictionary<string, object>
                                    {
                                        { "StringEquals", new Dictionary<string, object>
                                        {
                                            { "s3:x-amz-acl", "bucket-owner-full-control"},
                                        }},
                                    }},
                                },
                                new Dictionary<string, object>
                                {
                                    { "Effect", "Allow"},
                                    { "Action", "config:Put*"},
                                    { "Resource", "*"},
                                },
                            }},
                        },
                    },
                },
            });
            var configTopicPolicy = new CfnTopicPolicy(this, "ConfigTopicPolicy", new CfnTopicPolicyProps
            {
                PolicyDocument = new Dictionary<string, object>
                {
                    { "Id", "ConfigTopicPolicy"},
                    { "Version", "2012-10-17"},
                    { "Statement", new []
                    {
                        new Dictionary<string, object>
                        {
                            { "Effect", "Allow"},
                            { "Principal", new Dictionary<string, object>
                            {
                                { "Service", "config.amazonaws.com"},
                            }},
                            { "Action", "SNS:Publish"},
                            { "Resource", "*"},
                        },
                    }},
                },
                Topics = new []
                {
                    configTopic.Ref,
                },
            });
            var deliveryChannel = new CfnDeliveryChannel(this, "DeliveryChannel", new CfnDeliveryChannelProps
            {
                ConfigSnapshotDeliveryProperties = new CfnDeliveryChannel.ConfigSnapshotDeliveryPropertiesProperty
                {
                    DeliveryFrequency = "Six_Hours",
                },
                S3BucketName = configBucket.Ref,
                SnsTopicArn = configTopic.Ref,
            });
            var volumeAutoEnableIoComplianceCheck = new CfnFunction(this, "VolumeAutoEnableIOComplianceCheck", new CfnFunctionProps
            {
                Code = new CfnFunction.CodeProperty
                {
                    ZipFile = string.Join("\n", new []
                    {
                        "var aws  = require('aws-sdk');",
                        "var config = new aws.ConfigService();",
                        "var ec2 = new aws.EC2();",
                        "exports.handler = function(event, context) {",
                        "    compliance = evaluateCompliance(event, function(compliance, event) {",
                        "        var configurationItem = JSON.parse(event.invokingEvent).configurationItem;",
                        "        var putEvaluationsRequest = {",
                        "            Evaluations: [{",
                        "                ComplianceResourceType: configurationItem.resourceType,",
                        "                ComplianceResourceId: configurationItem.resourceId,",
                        "                ComplianceType: compliance,",
                        "                OrderingTimestamp: configurationItem.configurationItemCaptureTime",
                        "            }],",
                        "            ResultToken: event.resultToken",
                        "        };",
                        "        config.putEvaluations(putEvaluationsRequest, function(err, data) {",
                        "            if (err) context.fail(err);",
                        "            else context.succeed(data);",
                        "        });",
                        "    });",
                        "};",
                        "function evaluateCompliance(event, doReturn) {",
                        "    var configurationItem = JSON.parse(event.invokingEvent).configurationItem;",
                        "    var status = configurationItem.configurationItemStatus;",
                        "    if (configurationItem.resourceType !== 'AWS::EC2::Volume' || event.eventLeftScope || (status !== 'OK' && status !== 'ResourceDiscovered'))",
                        "        doReturn('NOT_APPLICABLE', event);",
                        "    else ec2.describeVolumeAttribute({VolumeId: configurationItem.resourceId, Attribute: 'autoEnableIO'}, function(err, data) {",
                        "        if (err) context.fail(err);",
                        "        else if (data.AutoEnableIO.Value) doReturn('COMPLIANT', event);",
                        "        else doReturn('NON_COMPLIANT', event);",
                        "    });",
                        "}",
                    }),
                },
                Handler = "index.handler",
                Runtime = "nodejs",
                Timeout = 30,
                Role = lambdaExecutionRole.AttrArn,
            });
            var configPermissionToCallLambda = new CfnPermission(this, "ConfigPermissionToCallLambda", new CfnPermissionProps
            {
                FunctionName = volumeAutoEnableIoComplianceCheck.AttrArn,
                Action = "lambda:InvokeFunction",
                Principal = "config.amazonaws.com",
            });
            var configRecorder = new CfnConfigurationRecorder(this, "ConfigRecorder", new CfnConfigurationRecorderProps
            {
                Name = "default",
                RecordingGroup = new CfnConfigurationRecorder.RecordingGroupProperty
                {
                    ResourceTypes = new []
                    {
                        "AWS::EC2::Volume",
                    },
                },
                RoleArn = configRole.AttrArn,
            });
            var configRuleForVolumeAutoEnableIo = new CfnConfigRule(this, "ConfigRuleForVolumeAutoEnableIO", new CfnConfigRuleProps
            {
                ConfigRuleName = "ConfigRuleForVolumeAutoEnableIO",
                Scope = new CfnConfigRule.ScopeProperty
                {
                    ComplianceResourceId = ec2Volume.Ref,
                    ComplianceResourceTypes = new []
                    {
                        "AWS::EC2::Volume",
                    },
                },
                Source = new CfnConfigRule.SourceProperty
                {
                    Owner = "CUSTOM_LAMBDA",
                    SourceDetails = new []
                    {
                        new CfnConfigRule.SourceDetailProperty
                        {
                            EventSource = "aws.config",
                            MessageType = "ConfigurationItemChangeNotification",
                        },
                    },
                    SourceIdentifier = volumeAutoEnableIoComplianceCheck.AttrArn,
                },
            });
            var configRuleForVolumeTags = new CfnConfigRule(this, "ConfigRuleForVolumeTags", new CfnConfigRuleProps
            {
                InputParameters = new Dictionary<string, object>
                {
                    { "tag1Key", "CostCenter"},
                },
                Scope = new CfnConfigRule.ScopeProperty
                {
                    ComplianceResourceTypes = new []
                    {
                        "AWS::EC2::Volume",
                    },
                },
                Source = new CfnConfigRule.SourceProperty
                {
                    Owner = "AWS",
                    SourceIdentifier = "REQUIRED_TAGS",
                },
            });

            // Outputs
            ConfigRuleForVolumeTagsArn = configRuleForVolumeTags.AttrArn;
            ConfigRuleForVolumeTagsConfigRuleId = configRuleForVolumeTags.AttrConfigRuleId;
            ConfigRuleForVolumeAutoEnableIOComplianceType = configRuleForVolumeAutoEnableIo.AttrComplianceType;
        }
    }
}
