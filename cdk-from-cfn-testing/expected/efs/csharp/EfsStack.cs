using Amazon.CDK;
using Amazon.CDK.AWS.EC2;
using Amazon.CDK.AWS.EFS;
using Amazon.CDK.AWS.IAM;
using Constructs;
using System.Collections.Generic;

namespace EfsStack
{
    public class EfsStackProps : StackProps
    {
        /// <summary>
        /// WebServer EC2 instance type
        /// </summary>
        public string InstanceType { get; set; }

        /// <summary>
        /// Maximum size and initial desired capacity of Auto Scaling Group
        /// </summary>
        public string AsgMaxSize { get; set; }

        /// <summary>
        /// The IP address range that can be used to connect to the EC2 instances by using SSH
        /// </summary>
        public string SshLocation { get; set; }

        /// <summary>
        /// The name to be used for the EFS volume
        /// </summary>
        public string VolumeName { get; set; }

        /// <summary>
        /// The Linux mount point for the EFS volume
        /// </summary>
        public string MountPoint { get; set; }

    }

    /// <summary>
    /// This template creates an Amazon EFS file system and mount target and associates it with Amazon EC2 instances in an Auto Scaling group. **WARNING** This template creates Amazon EC2 instances and related resources. You will be billed for the AWS resources used if you create a stack from this template.
    /// </summary>
    public class EfsStack : Stack
    {
        /// <summary>
        /// Mount target ID
        /// </summary>
        public object MountTargetID { get; } 

        /// <summary>
        /// File system ID
        /// </summary>
        public object FileSystemID { get; } 

        public EfsStack(Construct scope, string id, EfsStackProps props = null) : base(scope, id, props)
        {
            // Applying default props
            props ??= new EfsStackProps();
            props.InstanceType ??= "t2.small";
            props.AsgMaxSize ??= "2";
            props.SshLocation ??= "0.0.0.0/0";
            props.VolumeName ??= "myEFSvolume";
            props.MountPoint ??= "myEFSvolume";

            // Mappings
            var awsInstanceType2Arch = new Dictionary<string, Dictionary<string,string>> 
            {
                ["t1.micro"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["t2.nano"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["t2.micro"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["t2.small"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["t2.medium"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["t2.large"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m1.small"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m1.medium"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m1.large"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m1.xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m2.xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m2.2xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m2.4xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m3.medium"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m3.large"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m3.xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m3.2xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m4.large"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m4.xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m4.2xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m4.4xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["m4.10xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["c1.medium"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["c1.xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["c3.large"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["c3.xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["c3.2xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["c3.4xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["c3.8xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["c4.large"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["c4.xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["c4.2xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["c4.4xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["c4.8xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["g2.2xlarge"] = new Dictionary<string, string> {["Arch"] = "HVMG2", },
                ["g2.8xlarge"] = new Dictionary<string, string> {["Arch"] = "HVMG2", },
                ["r3.large"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["r3.xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["r3.2xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["r3.4xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["r3.8xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["i2.xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["i2.2xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["i2.4xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["i2.8xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["d2.xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["d2.2xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["d2.4xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["d2.8xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["hi1.4xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["hs1.8xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["cr1.8xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
                ["cc2.8xlarge"] = new Dictionary<string, string> {["Arch"] = "HVM64", },
            };
            var awsRegionArch2Ami = new Dictionary<string, Dictionary<string,string>> 
            {
                ["us-east-1"] = new Dictionary<string, string> {["HVM64"] = "ami-0ff8a91507f77f867", ["HVMG2"] = "ami-0a584ac55a7631c0c", },
                ["us-west-2"] = new Dictionary<string, string> {["HVM64"] = "ami-a0cfeed8", ["HVMG2"] = "ami-0e09505bc235aa82d", },
                ["us-west-1"] = new Dictionary<string, string> {["HVM64"] = "ami-0bdb828fd58c52235", ["HVMG2"] = "ami-066ee5fd4a9ef77f1", },
                ["eu-west-1"] = new Dictionary<string, string> {["HVM64"] = "ami-047bb4163c506cd98", ["HVMG2"] = "ami-0a7c483d527806435", },
                ["eu-west-2"] = new Dictionary<string, string> {["HVM64"] = "ami-f976839e", ["HVMG2"] = "NOT_SUPPORTED", },
                ["eu-west-3"] = new Dictionary<string, string> {["HVM64"] = "ami-0ebc281c20e89ba4b", ["HVMG2"] = "NOT_SUPPORTED", },
                ["eu-central-1"] = new Dictionary<string, string> {["HVM64"] = "ami-0233214e13e500f77", ["HVMG2"] = "ami-06223d46a6d0661c7", },
                ["ap-northeast-1"] = new Dictionary<string, string> {["HVM64"] = "ami-06cd52961ce9f0d85", ["HVMG2"] = "ami-053cdd503598e4a9d", },
                ["ap-northeast-2"] = new Dictionary<string, string> {["HVM64"] = "ami-0a10b2721688ce9d2", ["HVMG2"] = "NOT_SUPPORTED", },
                ["ap-northeast-3"] = new Dictionary<string, string> {["HVM64"] = "ami-0d98120a9fb693f07", ["HVMG2"] = "NOT_SUPPORTED", },
                ["ap-southeast-1"] = new Dictionary<string, string> {["HVM64"] = "ami-08569b978cc4dfa10", ["HVMG2"] = "ami-0be9df32ae9f92309", },
                ["ap-southeast-2"] = new Dictionary<string, string> {["HVM64"] = "ami-09b42976632b27e9b", ["HVMG2"] = "ami-0a9ce9fecc3d1daf8", },
                ["ap-south-1"] = new Dictionary<string, string> {["HVM64"] = "ami-0912f71e06545ad88", ["HVMG2"] = "ami-097b15e89dbdcfcf4", },
                ["us-east-2"] = new Dictionary<string, string> {["HVM64"] = "ami-0b59bfac6be064b78", ["HVMG2"] = "NOT_SUPPORTED", },
                ["ca-central-1"] = new Dictionary<string, string> {["HVM64"] = "ami-0b18956f", ["HVMG2"] = "NOT_SUPPORTED", },
                ["sa-east-1"] = new Dictionary<string, string> {["HVM64"] = "ami-07b14488da8ea02a0", ["HVMG2"] = "NOT_SUPPORTED", },
                ["cn-north-1"] = new Dictionary<string, string> {["HVM64"] = "ami-0a4eaf6c4454eda75", ["HVMG2"] = "NOT_SUPPORTED", },
                ["cn-northwest-1"] = new Dictionary<string, string> {["HVM64"] = "ami-6b6a7d09", ["HVMG2"] = "NOT_SUPPORTED", },
            };

            // Resources
            var cloudWatchPutMetricsRole = new CfnRole(this, "CloudWatchPutMetricsRole", new CfnRoleProps
            {
                AssumeRolePolicyDocument = new Dictionary<string, object>
                {
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
            });
            var fileSystem = new CfnFileSystem(this, "FileSystem", new CfnFileSystemProps
            {
                PerformanceMode = "generalPurpose",
                FileSystemTags = new []
                {
                    new CfnFileSystem.ElasticFileSystemTagProperty
                    {
                        Key = "Name",
                        Value = props.VolumeName,
                    },
                },
            });
            var internetGateway = new CfnInternetGateway(this, "InternetGateway", new CfnInternetGatewayProps
            {
                Tags = new []
                {
                    new CfnTag
                    {
                        Key = "Application",
                        Value = StackName,
                    },
                    new CfnTag
                    {
                        Key = "Network",
                        Value = "Public",
                    },
                },
            });
            var vpc = new CfnVPC(this, "VPC", new CfnVPCProps
            {
                EnableDnsSupport = true,
                EnableDnsHostnames = true,
                CidrBlock = "10.0.0.0/16",
                Tags = new []
                {
                    new CfnTag
                    {
                        Key = "Application",
                        Value = StackId,
                    },
                },
            });
            var cloudWatchPutMetricsInstanceProfile = new CfnInstanceProfile(this, "CloudWatchPutMetricsInstanceProfile", new CfnInstanceProfileProps
            {
                Path = "/",
                Roles = new []
                {
                    cloudWatchPutMetricsRole.Ref,
                },
            });
            var cloudWatchPutMetricsRolePolicy = new CfnPolicy(this, "CloudWatchPutMetricsRolePolicy", new CfnPolicyProps
            {
                PolicyName = "CloudWatch_PutMetricData",
                PolicyDocument = new Dictionary<string, object>
                {
                    { "Version", "2012-10-17"},
                    { "Statement", new []
                    {
                        new Dictionary<string, object>
                        {
                            { "Sid", "CloudWatchPutMetricData"},
                            { "Effect", "Allow"},
                            { "Action", new []
                            {
                                "cloudwatch:PutMetricData",
                            }},
                            { "Resource", new []
                            {
                                "*",
                            }},
                        },
                    }},
                },
                Roles = new []
                {
                    cloudWatchPutMetricsRole.Ref,
                },
            });
            var gatewayToInternet = new CfnVPCGatewayAttachment(this, "GatewayToInternet", new CfnVPCGatewayAttachmentProps
            {
                VpcId = vpc.Ref,
                InternetGatewayId = internetGateway.Ref,
            });
            var instanceSecurityGroup = new CfnSecurityGroup(this, "InstanceSecurityGroup", new CfnSecurityGroupProps
            {
                VpcId = vpc.Ref,
                GroupDescription = "Enable SSH access via port 22",
                SecurityGroupIngress = new []
                {
                    new CfnSecurityGroup.IngressProperty
                    {
                        IpProtocol = "tcp",
                        FromPort = 22,
                        ToPort = 22,
                        CidrIp = props.SshLocation,
                    },
                    new CfnSecurityGroup.IngressProperty
                    {
                        IpProtocol = "tcp",
                        FromPort = 80,
                        ToPort = 80,
                        CidrIp = "0.0.0.0/0",
                    },
                },
            });
            var mountTargetSecurityGroup = new CfnSecurityGroup(this, "MountTargetSecurityGroup", new CfnSecurityGroupProps
            {
                VpcId = vpc.Ref,
                GroupDescription = "Security group for mount target",
                SecurityGroupIngress = new []
                {
                    new CfnSecurityGroup.IngressProperty
                    {
                        IpProtocol = "tcp",
                        FromPort = 2049,
                        ToPort = 2049,
                        CidrIp = "0.0.0.0/0",
                    },
                },
            });
            var routeTable = new CfnRouteTable(this, "RouteTable", new CfnRouteTableProps
            {
                VpcId = vpc.Ref,
            });
            var subnet = new CfnSubnet(this, "Subnet", new CfnSubnetProps
            {
                VpcId = vpc.Ref,
                CidrBlock = "10.0.0.0/24",
                Tags = new []
                {
                    new CfnTag
                    {
                        Key = "Application",
                        Value = StackId,
                    },
                },
            });
            var internetGatewayRoute = new CfnRoute(this, "InternetGatewayRoute", new CfnRouteProps
            {
                DestinationCidrBlock = "0.0.0.0/0",
                RouteTableId = routeTable.Ref,
                GatewayId = internetGateway.Ref,
            });
            var mountTarget = new CfnMountTarget(this, "MountTarget", new CfnMountTargetProps
            {
                FileSystemId = fileSystem.Ref,
                SubnetId = subnet.Ref,
                SecurityGroups = new []
                {
                    mountTargetSecurityGroup.Ref,
                },
            });
            var subnetRouteTableAssoc = new CfnSubnetRouteTableAssociation(this, "SubnetRouteTableAssoc", new CfnSubnetRouteTableAssociationProps
            {
                RouteTableId = routeTable.Ref,
                SubnetId = subnet.Ref,
            });

            // Outputs
            MountTargetID = mountTarget.Ref;
            FileSystemID = fileSystem.Ref;
        }
    }
}
