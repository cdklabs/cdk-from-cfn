using Amazon.CDK;
using Amazon.CDK.AWS.EC2;
using Amazon.CDK.AWS.Events;
using Amazon.CDK.AWS.GroundStation;
using Amazon.CDK.AWS.IAM;
using Amazon.CDK.AWS.Lambda;
using Amazon.CDK.AWS.S3;
using Amazon.CDK.AWS.SNS;
using Constructs;
using System.Collections.Generic;

namespace GroundStationStack
{
    public class GroundStationStackProps : StackProps
    {
        /// <summary>
        /// This bucket will be created. Data will be delivered to this S3 bucket. Name must start with "aws-groundstation-"
        /// </summary>
        public string GroundStationS3DataDeliveryBucketName { get; set; }

        /// <summary>
        /// Email address to receive contact updates
        /// </summary>
        public string NotificationEmail { get; set; }

        /// <summary>
        /// Used for data processing task
        /// </summary>
        public string SatelliteName { get; set; }

        /// <summary>
        /// RT-STPS Software
        /// </summary>
        public string SoftwareS3Bucket { get; set; }

        /// <summary>
        /// The CIDR Block that the security group will allow ssh access to an instance. The CIDR Block has the form x.x.x.x/x.
        /// </summary>
        public string SshCidrBlock { get; set; }

        /// <summary>
        /// Name of the ssh key used to access ec2 hosts. Set this up ahead of time.
        /// </summary>
        public string SshKeyName { get; set; }

        /// <summary>
        /// VPC to launch instances in.
        /// </summary>
        public string VpcId { get; set; }

        /// <summary>
        /// Subnet to launch instances in
        /// </summary>
        public string SubnetId { get; set; }

    }

    /// <summary>
    /// Ground Station S3 Data Delivery stack for JPSS1
    /// </summary>
    public class GroundStationStack : Stack
    {
        public object SnsTopicArn { get; } 

        public GroundStationStack(Construct scope, string id, GroundStationStackProps props = null) : base(scope, id, props)
        {
            // Applying default props
            props ??= new GroundStationStackProps();
            props.GroundStationS3DataDeliveryBucketName ??= "aws-groundstation-s3dd-your-bucket";
            props.NotificationEmail ??= "someone@somewhere.com";
            props.SatelliteName ??= "JPSS1";
            props.SoftwareS3Bucket ??= "your-software-bucket";
            props.SshCidrBlock ??= "15.16.17.18/32";
            props.SshKeyName = new CfnParameter(this, "SshKeyName", new CfnParameterProps
            {
                Type = "AWS::EC2::KeyPair::KeyName",
                Default = props.SshKeyName ?? "",
                Description = "Name of the ssh key used to access ec2 hosts. Set this up ahead of time.",
            }).ValueAsString;
            props.VpcId = new CfnParameter(this, "VpcId", new CfnParameterProps
            {
                Type = "AWS::EC2::VPC::Id",
                Default = props.VpcId ?? "",
                Description = "VPC to launch instances in.",
            }).ValueAsString;
            props.SubnetId = new CfnParameter(this, "SubnetId", new CfnParameterProps
            {
                Type = "AWS::EC2::Subnet::Id",
                Default = props.SubnetId ?? "",
                Description = "Subnet to launch instances in",
            }).ValueAsString;

            // Transforms
            AddTransform("AWS::Serverless-2016-10-31");
            // Mappings
            var amiMap = new Dictionary<string, Dictionary<string,string>> 
            {
                ["eu-north-1"] = new Dictionary<string, string> {["ami"] = "ami-0abb1aa57ecf6a060", },
                ["eu-west-1"] = new Dictionary<string, string> {["ami"] = "ami-082af980f9f5514f8", },
                ["me-south-1"] = new Dictionary<string, string> {["ami"] = "ami-0687a5f8dac57444e", },
                ["us-east-1"] = new Dictionary<string, string> {["ami"] = "ami-03c7d01cf4dedc891", },
                ["us-east-2"] = new Dictionary<string, string> {["ami"] = "ami-06d5c50c30a35fb88", },
                ["us-west-2"] = new Dictionary<string, string> {["ami"] = "ami-0ac64ad8517166fb1", },
                ["ap-southeast-2"] = new Dictionary<string, string> {["ami"] = "ami-0074f30ddebf60493", },
                ["af-south-1"] = new Dictionary<string, string> {["ami"] = "ami-0764fb4fffa117039", },
                ["ap-northeast-2"] = new Dictionary<string, string> {["ami"] = "ami-03db74b70e1da9c56", },
                ["ap-southeast-1"] = new Dictionary<string, string> {["ami"] = "ami-0b3a4110c36b9a5f0", },
                ["eu-central-1"] = new Dictionary<string, string> {["ami"] = "ami-0adbcf08fdd664fed", },
                ["sa-east-1"] = new Dictionary<string, string> {["ami"] = "ami-0c5cdf1548242305d", },
            };

            // Resources
            var groundStationS3DataDeliveryBucket = new CfnBucket(this, "GroundStationS3DataDeliveryBucket", new CfnBucketProps
            {
                BucketName = props.GroundStationS3DataDeliveryBucketName,
            });
            var groundStationS3DataDeliveryRole = new CfnRole(this, "GroundStationS3DataDeliveryRole", new CfnRoleProps
            {
                AssumeRolePolicyDocument = new Dictionary<string, object>
                {
                    { "Statement", new []
                    {
                        new Dictionary<string, object>
                        {
                            { "Action", new []
                            {
                                "sts:AssumeRole",
                            }},
                            { "Effect", "Allow"},
                            { "Principal", new Dictionary<string, object>
                            {
                                { "Service", new []
                                {
                                    "groundstation.amazonaws.com",
                                }},
                            }},
                            { "Condition", new Dictionary<string, object>
                            {
                                { "StringEquals", new Dictionary<string, object>
                                {
                                    { "aws:SourceAccount", Account},
                                }},
                                { "ArnLike", new Dictionary<string, object>
                                {
                                    { "aws:SourceArn", $"arn:aws:groundstation:{Region}:{Account}:config/s3-recording/*"},
                                }},
                            }},
                        },
                    }},
                },
            });
            var instanceEip = new CfnEIP(this, "InstanceEIP", new CfnEIPProps
            {
                Domain = "vpc",
            });
            var instanceRole = new CfnRole(this, "InstanceRole", new CfnRoleProps
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
                                    "ec2.amazonaws.com",
                                }},
                            }},
                            { "Action", new []
                            {
                                "sts:AssumeRole",
                            }},
                        },
                    }},
                },
                Path = "/",
                ManagedPolicyArns = new []
                {
                    "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy",
                    "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM",
                },
            });
            var instanceSecurityGroup = new CfnSecurityGroup(this, "InstanceSecurityGroup", new CfnSecurityGroupProps
            {
                GroupDescription = "AWS Ground Station receiver instance security group.",
                VpcId = props.VpcId,
                SecurityGroupIngress = new []
                {
                    new CfnSecurityGroup.IngressProperty
                    {
                        IpProtocol = "tcp",
                        FromPort = 22,
                        ToPort = 22,
                        CidrIp = props.SshCidrBlock,
                        Description = "Inbound SSH access",
                    },
                },
            });
            var snppJpssDownlinkDemodDecodeAntennaConfig = new CfnConfig(this, "SnppJpssDownlinkDemodDecodeAntennaConfig", new CfnConfigProps
            {
                Name = "JPSS1 Downlink Demod Decode Antenna Config",
                ConfigData = new CfnConfig.ConfigDataProperty
                {
                    AntennaDownlinkDemodDecodeConfig = new CfnConfig.AntennaDownlinkDemodDecodeConfigProperty
                    {
                        SpectrumConfig = new CfnConfig.SpectrumConfigProperty
                        {
                            CenterFrequency = new CfnConfig.FrequencyProperty
                            {
                                Value = 7812,
                                Units = "MHz",
                            },
                            Polarization = "RIGHT_HAND",
                            Bandwidth = new CfnConfig.FrequencyBandwidthProperty
                            {
                                Value = 30,
                                Units = "MHz",
                            },
                        },
                        DemodulationConfig = new CfnConfig.DemodulationConfigProperty
                        {
                            UnvalidatedJSON = "{ "type":"QPSK", "qpsk":{ "carrierFrequencyRecovery":{ "centerFrequency":{ "value":7812, "units":"MHz" }, "range":{ "value":250, "units":"kHz" } }, "symbolTimingRecovery":{ "symbolRate":{ "value":15, "units":"Msps" }, "range":{ "value":0.75, "units":"ksps" }, "matchedFilter":{ "type":"ROOT_RAISED_COSINE", "rolloffFactor":0.5 } } } }",
                        },
                        DecodeConfig = new CfnConfig.DecodeConfigProperty
                        {
                            UnvalidatedJSON = "{ "edges":[ { "from":"I-Ingress", "to":"IQ-Recombiner" }, { "from":"Q-Ingress", "to":"IQ-Recombiner" }, { "from":"IQ-Recombiner", "to":"CcsdsViterbiDecoder" }, { "from":"CcsdsViterbiDecoder", "to":"NrzmDecoder" }, { "from":"NrzmDecoder", "to":"UncodedFramesEgress" } ], "nodeConfigs":{ "I-Ingress":{ "type":"CODED_SYMBOLS_INGRESS", "codedSymbolsIngress":{ "source":"I" } }, "Q-Ingress":{ "type":"CODED_SYMBOLS_INGRESS", "codedSymbolsIngress":{ "source":"Q" } }, "IQ-Recombiner":{ "type":"IQ_RECOMBINER" }, "CcsdsViterbiDecoder":{ "type":"CCSDS_171_133_VITERBI_DECODER", "ccsds171133ViterbiDecoder":{ "codeRate":"ONE_HALF" } }, "NrzmDecoder":{ "type":"NRZ_M_DECODER" }, "UncodedFramesEgress":{ "type":"UNCODED_FRAMES_EGRESS" } } }",
                        },
                    },
                },
            });
            var trackingConfig = new CfnConfig(this, "TrackingConfig", new CfnConfigProps
            {
                Name = "JPSS1 Tracking Config",
                ConfigData = new CfnConfig.ConfigDataProperty
                {
                    TrackingConfig = new CfnConfig.TrackingConfigProperty
                    {
                        Autotrack = "PREFERRED",
                    },
                },
            });
            var snsTopic = new CfnTopic(this, "snsTopic", new CfnTopicProps
            {
                DisplayName = string.Join("-", new []
                {
                    "GS-S3-Data-Delivery",
                    props.SatelliteName,
                }),
                Subscription = new []
                {
                    new CfnTopic.SubscriptionProperty
                    {
                        Endpoint = props.NotificationEmail,
                        Protocol = "email",
                    },
                },
            });
            var generalInstanceProfile = new CfnInstanceProfile(this, "GeneralInstanceProfile", new CfnInstanceProfileProps
            {
                Roles = new []
                {
                    instanceRole.Ref,
                },
            });
            var groundStationS3DataDeliveryIamPolicy = new CfnPolicy(this, "GroundStationS3DataDeliveryIamPolicy", new CfnPolicyProps
            {
                PolicyDocument = new Dictionary<string, object>
                {
                    { "Version", "2012-10-17"},
                    { "Statement", new []
                    {
                        new Dictionary<string, object>
                        {
                            { "Action", new []
                            {
                                "s3:GetBucketLocation",
                            }},
                            { "Effect", "Allow"},
                            { "Resource", new []
                            {
                                string.Join("", new []
                                {
                                    "arn:aws:s3:::",
                                    props.GroundStationS3DataDeliveryBucketName,
                                }),
                            }},
                        },
                        new Dictionary<string, object>
                        {
                            { "Action", new []
                            {
                                "s3:PutObject",
                            }},
                            { "Effect", "Allow"},
                            { "Resource", new []
                            {
                                string.Join("", new []
                                {
                                    "arn:aws:s3:::",
                                    props.GroundStationS3DataDeliveryBucketName,
                                    "/*",
                                }),
                            }},
                        },
                    }},
                },
                PolicyName = "GroundStationS3DataDeliveryPolicy",
                Roles = new []
                {
                    groundStationS3DataDeliveryRole.Ref,
                },
            });
            var instanceRoleEc2Policy = new CfnManagedPolicy(this, "InstanceRoleEC2Policy", new CfnManagedPolicyProps
            {
                PolicyDocument = new Dictionary<string, object>
                {
                    { "Version", "2012-10-17"},
                    { "Statement", new []
                    {
                        new Dictionary<string, object>
                        {
                            { "Action", new []
                            {
                                "ec2:DescribeTags",
                            }},
                            { "Effect", "Allow"},
                            { "Resource", "*"},
                        },
                    }},
                },
                Roles = new []
                {
                    instanceRole.Ref,
                },
            });
            var instanceRoleS3Policy = new CfnManagedPolicy(this, "InstanceRoleS3Policy", new CfnManagedPolicyProps
            {
                PolicyDocument = new Dictionary<string, object>
                {
                    { "Version", "2012-10-17"},
                    { "Statement", new []
                    {
                        new Dictionary<string, object>
                        {
                            { "Action", new []
                            {
                                "s3:PutObject",
                                "s3:GetObject",
                            }},
                            { "Effect", "Allow"},
                            { "Resource", string.Join("", new []
                            {
                                "arn:aws:s3:::",
                                props.SoftwareS3Bucket,
                                "/*",
                            })},
                        },
                        new Dictionary<string, object>
                        {
                            { "Action", new []
                            {
                                "s3:GetObject",
                            }},
                            { "Effect", "Allow"},
                            { "Resource", string.Join("", new []
                            {
                                "arn:aws:s3:::",
                                "space-solutions-",
                                "eu-west-1",
                                "/*",
                            })},
                        },
                        new Dictionary<string, object>
                        {
                            { "Action", new []
                            {
                                "s3:PutObject",
                                "s3:GetObject",
                            }},
                            { "Effect", "Allow"},
                            { "Resource", string.Join("", new []
                            {
                                "arn:aws:s3:::",
                                groundStationS3DataDeliveryBucket.Ref,
                                "/*",
                            })},
                        },
                        new Dictionary<string, object>
                        {
                            { "Action", new []
                            {
                                "s3:ListBucket",
                            }},
                            { "Effect", "Allow"},
                            { "Resource", string.Join("", new []
                            {
                                "arn:aws:s3:::",
                                props.SoftwareS3Bucket,
                            })},
                        },
                        new Dictionary<string, object>
                        {
                            { "Action", new []
                            {
                                "s3:ListBucket",
                            }},
                            { "Effect", "Allow"},
                            { "Resource", string.Join("", new []
                            {
                                "arn:aws:s3:::",
                                "space-solutions-",
                                "eu-west-1",
                                "/*",
                            })},
                        },
                        new Dictionary<string, object>
                        {
                            { "Action", new []
                            {
                                "s3:ListBucket",
                            }},
                            { "Effect", "Allow"},
                            { "Resource", string.Join("", new []
                            {
                                "arn:aws:s3:::",
                                groundStationS3DataDeliveryBucket.Ref,
                            })},
                        },
                    }},
                },
                Roles = new []
                {
                    instanceRole.Ref,
                },
            });
            var instanceRoleSnsPolicy = new CfnManagedPolicy(this, "InstanceRoleSNSPolicy", new CfnManagedPolicyProps
            {
                PolicyDocument = new Dictionary<string, object>
                {
                    { "Version", "2012-10-17"},
                    { "Statement", new []
                    {
                        new Dictionary<string, object>
                        {
                            { "Action", new []
                            {
                                "sns:Publish",
                            }},
                            { "Effect", "Allow"},
                            { "Resource", snsTopic.Ref},
                        },
                    }},
                },
                Roles = new []
                {
                    instanceRole.Ref,
                },
            });
            var receiverInstanceNetworkInterfacePublic = new CfnNetworkInterface(this, "ReceiverInstanceNetworkInterfacePublic", new CfnNetworkInterfaceProps
            {
                Description = "Public network interface for troubleshooting",
                GroupSet = new []
                {
                    instanceSecurityGroup.Ref,
                },
                SubnetId = props.SubnetId,
            });
            var instanceEipAsscociation = new CfnEIPAssociation(this, "InstanceEIPAsscociation", new CfnEIPAssociationProps
            {
                AllocationId = instanceEip.AttrAllocationId,
                NetworkInterfaceId = receiverInstanceNetworkInterfacePublic.Ref,
            });
            var receiverInstance = new CfnInstance(this, "ReceiverInstance", new CfnInstanceProps
            {
                DisableApiTermination = false,
                IamInstanceProfile = generalInstanceProfile.Ref,
                ImageId = amiMap[Region]["ami"],
                InstanceType = "c5.4xlarge",
                KeyName = props.SshKeyName,
                Monitoring = true,
                NetworkInterfaces = new []
                {
                    new CfnInstance.NetworkInterfaceProperty
                    {
                        NetworkInterfaceId = receiverInstanceNetworkInterfacePublic.Ref,
                        DeviceIndex = 0,
                        DeleteOnTermination = false,
                    },
                },
                BlockDeviceMappings = new []
                {
                    new CfnInstance.BlockDeviceMappingProperty
                    {
                        DeviceName = "/dev/xvda",
                        Ebs = new CfnInstance.EbsProperty
                        {
                            VolumeType = "gp2",
                            VolumeSize = 100,
                        },
                    },
                },
                Tags = new []
                {
                    new CfnTag
                    {
                        Key = "Name",
                        Value = string.Join("-", new []
                        {
                            "Receiver",
                            StackName,
                        }),
                    },
                },
                UserData = Fn.Base64($"#!/bin/bash

                exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
                echo `date +'%F %R:%S'` "INFO: Logging Setup" >&2

                echo "Setting instance hostname"
                export INSTANCE=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
                export HOSTNAME=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE" "Name=key,Values=Name" --region={Region} --output=text |cut -f5)
                echo $HOSTNAME > /etc/hostname
                hostname $HOSTNAME

                echo "Installing RT-STPS pre-reqs"
                yum update -y && yum install -y wget java python3

                GROUND_STATION_DIR="/opt/aws/groundstation"
                GROUND_STATION_BIN_DIR="$GROUND_STATION_DIR/bin"
                PROCESS_SCRIPT="$GROUND_STATION_BIN_DIR/rt-stps-process.sh"

                echo "Creating $GROUND_STATION_BIN_DIR"
                mkdir -p "$GROUND_STATION_BIN_DIR"

                echo "Getting Assets from S3"
                aws s3 cp --region {Region} "s3://{props.SoftwareS3Bucket}/software/RT-STPS/rt-stps-process.sh" "$PROCESS_SCRIPT"
                chmod +x "$PROCESS_SCRIPT"
                chown ec2-user:ec2-user "$PROCESS_SCRIPT"

                echo "Adding call to $PROCESS_SCRIPT into /etc/rc.local"
                echo "TIMESTR=\$(date '+%Y%m%d-%H%M')" >> /etc/rc.local
                echo "$PROCESS_SCRIPT {props.SatelliteName} {props.SoftwareS3Bucket} {props.GroundStationS3DataDeliveryBucketName} 2>&1 | tee $GROUND_STATION_BIN_DIR/data-capture_\$TIMESTR.log" >> /etc/rc.local
                chmod +x /etc/rc.d/rc.local

                echo "Creating /opt/aws/groundstation/bin/getSNSTopic.sh"
                echo "export SNS_TOPIC={snsTopic.Ref}" > /opt/aws/groundstation/bin/getSNSTopic.sh
                chmod +x /opt/aws/groundstation/bin/getSNSTopic.sh

                echo "Sending completion SNS notification"
                export MESSAGE="GroundStation setup is complete for Satellite: {props.SatelliteName}.  The RT-STPS processor EC2 instance is all setup and ready to go! It will be automatically started after data from a satellite pass has been deposited in your S3 bucket.  Data will be processed using RT-STPS, then copied to the following S3 Bucket: {props.GroundStationS3DataDeliveryBucketName}.  A summary of the contact will be emailed to {props.NotificationEmail}. The EC2 instance will now be stopped."
                aws sns publish --topic-arn {snsTopic.Ref} --message "$MESSAGE" --region {Region}

                echo "Shutting down the EC2 instance"
                shutdown -h now

                exit 0
                " as string),
            });
            var s3RecordingConfig = new CfnConfig(this, "S3RecordingConfig", new CfnConfigProps
            {
                Name = "JPSS1 Recording Config",
                ConfigData = new CfnConfig.ConfigDataProperty
                {
                    S3RecordingConfig = new CfnConfig.S3RecordingConfigProperty
                    {
                        BucketArn = string.Join("", new []
                        {
                            "arn:aws:s3:::",
                            props.GroundStationS3DataDeliveryBucketName,
                        }),
                        RoleArn = groundStationS3DataDeliveryRole.AttrArn,
                        Prefix = "data/JPSS1/{year}/{month}/{day}",
                    },
                },
            });
            var groundStationS3ddLambdaRolePolicy = new CfnManagedPolicy(this, "GroundStationS3ddLambdaRolePolicy", new CfnManagedPolicyProps
            {
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
                                "ec2:StartInstances",
                                "ec2:StopInstances",
                                "ec2:CreateTags",
                            }},
                            { "Resource", new []
                            {
                                $"arn:aws:ec2:{Region}:{Account}:instance/{receiverInstance.Ref}",
                            }},
                        },
                        new Dictionary<string, object>
                        {
                            { "Effect", "Allow"},
                            { "Action", new []
                            {
                                "ec2:DescribeInstanceStatus",
                                "ec2:DescribeNetworkInterfaces",
                            }},
                            { "Resource", new []
                            {
                                "*",
                            }},
                        },
                        new Dictionary<string, object>
                        {
                            { "Effect", "Allow"},
                            { "Action", new []
                            {
                                "sns:Publish",
                            }},
                            { "Resource", snsTopic.Ref},
                        },
                        new Dictionary<string, object>
                        {
                            { "Effect", "Allow"},
                            { "Action", new []
                            {
                                "s3:PutObject",
                                "s3:PutObjectAcl",
                                "s3:GetObject",
                                "s3:DeleteObjectVersion",
                                "s3:DeleteObject",
                            }},
                            { "Resource", new []
                            {
                                string.Join("", new []
                                {
                                    "arn:aws:s3:::",
                                    props.GroundStationS3DataDeliveryBucketName,
                                    "/*",
                                }),
                            }},
                        },
                        new Dictionary<string, object>
                        {
                            { "Effect", "Allow"},
                            { "Action", new []
                            {
                                "s3:ListBucket",
                            }},
                            { "Resource", new []
                            {
                                string.Join("", new []
                                {
                                    "arn:aws:s3:::",
                                    props.GroundStationS3DataDeliveryBucketName,
                                }),
                            }},
                        },
                    }},
                },
            });
            var snppJpssDemodDecodeMissionProfile = new CfnMissionProfile(this, "SnppJpssDemodDecodeMissionProfile", new CfnMissionProfileProps
            {
                Name = "43013 JPSS1 Demod Decode to S3",
                ContactPrePassDurationSeconds = 120,
                ContactPostPassDurationSeconds = 120,
                MinimumViableContactDurationSeconds = 180,
                TrackingConfigArn = trackingConfig.Ref,
                DataflowEdges = new []
                {
                    new CfnMissionProfile.DataflowEdgeProperty
                    {
                        Source = string.Join("/", new []
                        {
                            snppJpssDownlinkDemodDecodeAntennaConfig.Ref,
                            "UncodedFramesEgress",
                        }),
                        Destination = s3RecordingConfig.Ref,
                    },
                },
            });
            var groundStationS3ddLambdaRole = new CfnRole(this, "GroundStationS3ddLambdaRole", new CfnRoleProps
            {
                Path = "/",
                ManagedPolicyArns = new []
                {
                    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
                    groundStationS3ddLambdaRolePolicy.Ref,
                },
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
                                { "Service", "lambda.amazonaws.com"},
                            }},
                            { "Action", new []
                            {
                                "sts:AssumeRole",
                            }},
                        },
                    }},
                },
            });
            var lambdaFunctionStartRtstps = new CfnFunction(this, "LambdaFunctionStartRtstps", new CfnFunctionProps
            {
                Environment = new CfnFunction.EnvironmentProperty
                {
                    Variables = new Dictionary<string, string>
                    {
                        { "RtstpsInstance", receiverInstance.Ref},
                    },
                },
                Handler = "index.handle_cloudwatch_event",
                Runtime = "python3.9",
                MemorySize = 512,
                Timeout = 300,
                Role = groundStationS3ddLambdaRole.AttrArn,
                Code = new CfnFunction.CodeProperty
                {
                    S3Bucket = props.SoftwareS3Bucket,
                    S3Key = "software/RT-STPS/lambda.zip",
                },
            });
            var s3ContactCompleteEventRule = new CfnRule(this, "S3ContactCompleteEventRule", new CfnRuleProps
            {
                Description = "Triggered when all files have been uploaded for a Ground Station S3 data delivery contact",
                EventPattern = new Dictionary<string, object>
                {
                    { "source", new []
                    {
                        "aws.groundstation",
                    }},
                    { "detail-type", new []
                    {
                        "Ground Station S3 Upload Complete",
                    }},
                },
                State = "ENABLED",
                Targets = new []
                {
                    new CfnRule.TargetProperty
                    {
                        Arn = lambdaFunctionStartRtstps.AttrArn,
                        Id = "LambdaFunctionStartRtstps",
                    },
                },
            });
            var permissionForGroundStationCloudWatchEventsToInvokeLambda = new CfnPermission(this, "PermissionForGroundStationCloudWatchEventsToInvokeLambda", new CfnPermissionProps
            {
                FunctionName = lambdaFunctionStartRtstps.Ref,
                Action = "lambda:InvokeFunction",
                Principal = "events.amazonaws.com",
                SourceArn = s3ContactCompleteEventRule.AttrArn,
            });

            // Outputs
            SnsTopicArn = snsTopic.Ref;
            new CfnOutput(this, "CfnOutputSnsTopicArn", new CfnOutputProps {
                Key = "SnsTopicArn",
                ExportName = $"{StackName}-SnsTopicArn",
                Value = SnsTopicArn as string,
            });
        }
    }
}
