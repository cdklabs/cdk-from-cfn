package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	batch "github.com/aws/aws-cdk-go/awscdk/v2/awsbatch"
	ec2 "github.com/aws/aws-cdk-go/awscdk/v2/awsec2"
	iam "github.com/aws/aws-cdk-go/awscdk/v2/awsiam"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type BatchStackProps struct {
	cdk.StackProps
}

/// AWS CloudFormation Sample Template Managed Single Batch Job Queue: This template demonstrates the usage of simple Job Queue and EC2 style Compute Environment.  **WARNING** You will be billed for the AWS resources used if you create a stack from this template.
type BatchStack struct {
	cdk.Stack
	ComputeEnvironmentArn interface{} // TODO: fix to appropriate type
	JobQueueArn interface{} // TODO: fix to appropriate type
	JobDefinitionArn interface{} // TODO: fix to appropriate type
}

func NewBatchStack(scope constructs.Construct, id string, props *BatchStackProps) *BatchStack {
	var sprops cdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := cdk.NewStack(scope, &id, &sprops)

	batchServiceRole := iam.NewCfnRole(
		stack,
		jsii.String("BatchServiceRole"),
		&iam.CfnRoleProps{
			AssumeRolePolicyDocument: map[string]interface{} {
				"Version": jsii.String("2012-10-17"),
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Effect": jsii.String("Allow"),
						"Principal": map[string]interface{} {
							"Service": jsii.String("batch.amazonaws.com"),
						},
						"Action": jsii.String("sts:AssumeRole"),
					},
				},
			},
			ManagedPolicyArns: &[]*string{
				jsii.String("arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"),
			},
		},
	)

	ecsInstanceRole := iam.NewCfnRole(
		stack,
		jsii.String("EcsInstanceRole"),
		&iam.CfnRoleProps{
			AssumeRolePolicyDocument: map[string]interface{} {
				"Version": jsii.String("2008-10-17"),
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Sid": jsii.String(""),
						"Effect": jsii.String("Allow"),
						"Principal": map[string]interface{} {
							"Service": jsii.String("ec2.amazonaws.com"),
						},
						"Action": jsii.String("sts:AssumeRole"),
					},
				},
			},
			ManagedPolicyArns: &[]*string{
				jsii.String("arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"),
			},
		},
	)

	internetGateway := ec2.NewCfnInternetGateway(
		stack,
		jsii.String("InternetGateway"),
		&ec2.CfnInternetGatewayProps{
		},
	)

	jobDefinition := batch.NewCfnJobDefinition(
		stack,
		jsii.String("JobDefinition"),
		&batch.CfnJobDefinitionProps{
			Type: jsii.String("container"),
			ContainerProperties: &ContainerPropertiesProperty{
				Image: cdk.Fn_Join(jsii.String(""), &[]*string{
					jsii.String("137112412989.dkr.ecr."),
					stack.Region(),
					jsii.String(".amazonaws.com/amazonlinux:latest"),
				}),
				Vcpus: jsii.Number(2),
				Memory: jsii.Number(2000),
				Command: &[]*string{
					jsii.String("echo"),
					jsii.String("Hello world"),
				},
			},
			RetryStrategy: &RetryStrategyProperty{
				Attempts: jsii.Number(1),
			},
		},
	)

	vpc := ec2.NewCfnVPC(
		stack,
		jsii.String("VPC"),
		&ec2.CfnVPCProps{
			CidrBlock: jsii.String("10.0.0.0/16"),
		},
	)

	iamInstanceProfile := iam.NewCfnInstanceProfile(
		stack,
		jsii.String("IamInstanceProfile"),
		&iam.CfnInstanceProfileProps{
			Roles: &[]*string{
				ecsInstanceRole.Ref(),
			},
		},
	)

	routeTable := ec2.NewCfnRouteTable(
		stack,
		jsii.String("RouteTable"),
		&ec2.CfnRouteTableProps{
			VpcId: vpc.Ref(),
		},
	)

	securityGroup := ec2.NewCfnSecurityGroup(
		stack,
		jsii.String("SecurityGroup"),
		&ec2.CfnSecurityGroupProps{
			GroupDescription: jsii.String("EC2 Security Group for instances launched in the VPC by Batch"),
			VpcId: vpc.Ref(),
		},
	)

	subnet := ec2.NewCfnSubnet(
		stack,
		jsii.String("Subnet"),
		&ec2.CfnSubnetProps{
			CidrBlock: jsii.String("10.0.0.0/24"),
			VpcId: vpc.Ref(),
			MapPublicIpOnLaunch: jsii.Bool(true),
		},
	)

	ec2.NewCfnVPCGatewayAttachment(
		stack,
		jsii.String("VPCGatewayAttachment"),
		&ec2.CfnVPCGatewayAttachmentProps{
			VpcId: vpc.Ref(),
			InternetGatewayId: internetGateway.Ref(),
		},
	)

	computeEnvironment := batch.NewCfnComputeEnvironment(
		stack,
		jsii.String("ComputeEnvironment"),
		&batch.CfnComputeEnvironmentProps{
			Type: jsii.String("MANAGED"),
			ComputeResources: &ComputeResourcesProperty{
				Type: jsii.String("EC2"),
				MinvCpus: jsii.Number(0),
				DesiredvCpus: jsii.Number(0),
				MaxvCpus: jsii.Number(64),
				InstanceTypes: &[]*string{
					jsii.String("optimal"),
				},
				Subnets: &[]*string{
					subnet.Ref(),
				},
				SecurityGroupIds: &[]*string{
					securityGroup.Ref(),
				},
				InstanceRole: iamInstanceProfile.Ref(),
			},
			ServiceRole: batchServiceRole.Ref(),
		},
	)

	ec2.NewCfnRoute(
		stack,
		jsii.String("Route"),
		&ec2.CfnRouteProps{
			RouteTableId: routeTable.Ref(),
			DestinationCidrBlock: jsii.String("0.0.0.0/0"),
			GatewayId: internetGateway.Ref(),
		},
	)

	ec2.NewCfnSubnetRouteTableAssociation(
		stack,
		jsii.String("SubnetRouteTableAssociation"),
		&ec2.CfnSubnetRouteTableAssociationProps{
			RouteTableId: routeTable.Ref(),
			SubnetId: subnet.Ref(),
		},
	)

	jobQueue := batch.NewCfnJobQueue(
		stack,
		jsii.String("JobQueue"),
		&batch.CfnJobQueueProps{
			Priority: jsii.Number(1),
			ComputeEnvironmentOrder: &[]interface{}{
				&ComputeEnvironmentOrderProperty{
					Order: jsii.Number(1),
					ComputeEnvironment: computeEnvironment.Ref(),
				},
			},
		},
	)

	return &BatchStack{
		Stack: stack,
		ComputeEnvironmentArn: computeEnvironment.Ref(),
		JobQueueArn: jobQueue.Ref(),
		JobDefinitionArn: jobDefinition.Ref(),
	}
}

