using Amazon.CDK;
using Amazon.CDK.AWS.Batch;
using Amazon.CDK.AWS.EC2;
using Amazon.CDK.AWS.IAM;
using Constructs;
using System.Collections.Generic;

namespace BatchStack
{
    public class BatchStackProps : StackProps
    {
        public double MaxCpus { get; set; }

    }

    /// <summary>
    /// AWS CloudFormation Sample Template Managed Single Batch Job Queue: This template demonstrates the usage of simple Job Queue and EC2 style Compute Environment.  **WARNING** You will be billed for the AWS resources used if you create a stack from this template.
    /// </summary>
    public class BatchStack : Stack
    {
        public object ComputeEnvironmentArn { get; } 

        public object JobQueueArn { get; } 

        public object JobDefinitionArn { get; } 

        public BatchStack(Construct scope, string id, BatchStackProps props = null) : base(scope, id, props)
        {
            // Applying default props
            props ??= new BatchStackProps();
            props.MaxCpus = new CfnParameter(this, "MaxCpus", new CfnParameterProps
            {
                Type = "Number",
                Default = props.MaxCpus.ToString() ?? "64",
                NoEcho = true,
            }).ValueAsNumber;


            // Resources
            var batchServiceRole = new CfnRole(this, "BatchServiceRole", new CfnRoleProps
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
                                { "Service", "batch.amazonaws.com"},
                            }},
                            { "Action", "sts:AssumeRole"},
                        },
                    }},
                },
                ManagedPolicyArns = new []
                {
                    "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole",
                },
            });
            var ecsInstanceRole = new CfnRole(this, "EcsInstanceRole", new CfnRoleProps
            {
                AssumeRolePolicyDocument = new Dictionary<string, object>
                {
                    { "Version", "2008-10-17"},
                    { "Statement", new []
                    {
                        new Dictionary<string, object>
                        {
                            { "Sid", ""},
                            { "Effect", "Allow"},
                            { "Principal", new Dictionary<string, object>
                            {
                                { "Service", "ec2.amazonaws.com"},
                            }},
                            { "Action", "sts:AssumeRole"},
                        },
                    }},
                },
                ManagedPolicyArns = new []
                {
                    "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role",
                },
            });
            var internetGateway = new CfnInternetGateway(this, "InternetGateway", new CfnInternetGatewayProps
            {
            });
            var jobDefinition = new CfnJobDefinition(this, "JobDefinition", new CfnJobDefinitionProps
            {
                Type = "container",
                ContainerProperties = new CfnJobDefinition.ContainerPropertiesProperty
                {
                    Image = string.Join("", new []
                    {
                        "137112412989.dkr.ecr.",
                        Region,
                        ".amazonaws.com/amazonlinux:latest",
                    }),
                    Vcpus = 2,
                    Memory = 2000,
                    Command = new []
                    {
                        "echo",
                        "Hello world",
                    },
                },
                RetryStrategy = new CfnJobDefinition.RetryStrategyProperty
                {
                    Attempts = 1,
                },
            });
            var vpc = new CfnVPC(this, "VPC", new CfnVPCProps
            {
                CidrBlock = "10.0.0.0/16",
            });
            var iamInstanceProfile = new CfnInstanceProfile(this, "IamInstanceProfile", new CfnInstanceProfileProps
            {
                Roles = new []
                {
                    ecsInstanceRole.Ref,
                },
            });
            var routeTable = new CfnRouteTable(this, "RouteTable", new CfnRouteTableProps
            {
                VpcId = vpc.Ref,
            });
            var securityGroup = new CfnSecurityGroup(this, "SecurityGroup", new CfnSecurityGroupProps
            {
                GroupDescription = "EC2 Security Group for instances launched in the VPC by Batch",
                VpcId = vpc.Ref,
            });
            var subnet = new CfnSubnet(this, "Subnet", new CfnSubnetProps
            {
                CidrBlock = "10.0.0.0/24",
                VpcId = vpc.Ref,
                MapPublicIpOnLaunch = true,
            });
            var vpcGatewayAttachment = new CfnVPCGatewayAttachment(this, "VPCGatewayAttachment", new CfnVPCGatewayAttachmentProps
            {
                VpcId = vpc.Ref,
                InternetGatewayId = internetGateway.Ref,
            });
            var computeEnvironment = new CfnComputeEnvironment(this, "ComputeEnvironment", new CfnComputeEnvironmentProps
            {
                Type = "MANAGED",
                ComputeResources = new CfnComputeEnvironment.ComputeResourcesProperty
                {
                    Type = "EC2",
                    MinvCpus = 0,
                    DesiredvCpus = 0,
                    MaxvCpus = props.MaxCpus,
                    InstanceTypes = new []
                    {
                        "optimal",
                    },
                    Subnets = new []
                    {
                        subnet.Ref,
                    },
                    SecurityGroupIds = new []
                    {
                        securityGroup.Ref,
                    },
                    InstanceRole = iamInstanceProfile.Ref,
                },
                ServiceRole = batchServiceRole.Ref,
            });
            var route = new CfnRoute(this, "Route", new CfnRouteProps
            {
                RouteTableId = routeTable.Ref,
                DestinationCidrBlock = "0.0.0.0/0",
                GatewayId = internetGateway.Ref,
            });
            var subnetRouteTableAssociation = new CfnSubnetRouteTableAssociation(this, "SubnetRouteTableAssociation", new CfnSubnetRouteTableAssociationProps
            {
                RouteTableId = routeTable.Ref,
                SubnetId = subnet.Ref,
            });
            var jobQueue = new CfnJobQueue(this, "JobQueue", new CfnJobQueueProps
            {
                Priority = 1,
                ComputeEnvironmentOrder = new []
                {
                    new CfnJobQueue.ComputeEnvironmentOrderProperty
                    {
                        Order = 1,
                        ComputeEnvironment = computeEnvironment.Ref,
                    },
                },
            });

            // Outputs
            ComputeEnvironmentArn = computeEnvironment.Ref;
            JobQueueArn = jobQueue.Ref;
            JobDefinitionArn = jobDefinition.Ref;
        }
    }
}
