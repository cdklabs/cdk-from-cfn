package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	ec2 "github.com/aws/aws-cdk-go/awscdk/v2/awsec2"
	efs "github.com/aws/aws-cdk-go/awscdk/v2/awsefs"
	iam "github.com/aws/aws-cdk-go/awscdk/v2/awsiam"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type EfsStackProps struct {
	cdk.StackProps
	/// WebServer EC2 instance type
	InstanceType *string
	/// Maximum size and initial desired capacity of Auto Scaling Group
	AsgMaxSize *string
	/// The IP address range that can be used to connect to the EC2 instances by using SSH
	SshLocation *string
	/// The name to be used for the EFS volume
	VolumeName *string
	/// The Linux mount point for the EFS volume
	MountPoint *string
}

/// This template creates an Amazon EFS file system and mount target and associates it with Amazon EC2 instances in an Auto Scaling group. **WARNING** This template creates Amazon EC2 instances and related resources. You will be billed for the AWS resources used if you create a stack from this template.
type EfsStack struct {
	cdk.Stack
	/// Mount target ID
	MountTargetId interface{} // TODO: fix to appropriate type
	/// File system ID
	FileSystemId interface{} // TODO: fix to appropriate type
}

func NewEfsStack(scope constructs.Construct, id string, props *EfsStackProps) *EfsStack {
	/*
	awsInstanceType2Arch := map[*string]map[*string]*string{
		jsii.String("t1.micro"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("t2.nano"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("t2.micro"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("t2.small"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("t2.medium"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("t2.large"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m1.small"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m1.medium"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m1.large"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m1.xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m2.xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m2.2xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m2.4xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m3.medium"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m3.large"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m3.xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m3.2xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m4.large"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m4.xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m4.2xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m4.4xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("m4.10xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("c1.medium"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("c1.xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("c3.large"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("c3.xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("c3.2xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("c3.4xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("c3.8xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("c4.large"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("c4.xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("c4.2xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("c4.4xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("c4.8xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("g2.2xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVMG2"),
		},
		jsii.String("g2.8xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVMG2"),
		},
		jsii.String("r3.large"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("r3.xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("r3.2xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("r3.4xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("r3.8xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("i2.xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("i2.2xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("i2.4xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("i2.8xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("d2.xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("d2.2xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("d2.4xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("d2.8xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("hi1.4xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("hs1.8xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("cr1.8xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
		jsii.String("cc2.8xlarge"): map[*string]*string{
			jsii.String("Arch"): jsii.String("HVM64"),
		},
	}
	*/

	/*
	awsRegionArch2Ami := map[*string]map[*string]*string{
		jsii.String("us-east-1"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-0ff8a91507f77f867"),
			jsii.String("HVMG2"): jsii.String("ami-0a584ac55a7631c0c"),
		},
		jsii.String("us-west-2"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-a0cfeed8"),
			jsii.String("HVMG2"): jsii.String("ami-0e09505bc235aa82d"),
		},
		jsii.String("us-west-1"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-0bdb828fd58c52235"),
			jsii.String("HVMG2"): jsii.String("ami-066ee5fd4a9ef77f1"),
		},
		jsii.String("eu-west-1"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-047bb4163c506cd98"),
			jsii.String("HVMG2"): jsii.String("ami-0a7c483d527806435"),
		},
		jsii.String("eu-west-2"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-f976839e"),
			jsii.String("HVMG2"): jsii.String("NOT_SUPPORTED"),
		},
		jsii.String("eu-west-3"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-0ebc281c20e89ba4b"),
			jsii.String("HVMG2"): jsii.String("NOT_SUPPORTED"),
		},
		jsii.String("eu-central-1"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-0233214e13e500f77"),
			jsii.String("HVMG2"): jsii.String("ami-06223d46a6d0661c7"),
		},
		jsii.String("ap-northeast-1"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-06cd52961ce9f0d85"),
			jsii.String("HVMG2"): jsii.String("ami-053cdd503598e4a9d"),
		},
		jsii.String("ap-northeast-2"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-0a10b2721688ce9d2"),
			jsii.String("HVMG2"): jsii.String("NOT_SUPPORTED"),
		},
		jsii.String("ap-northeast-3"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-0d98120a9fb693f07"),
			jsii.String("HVMG2"): jsii.String("NOT_SUPPORTED"),
		},
		jsii.String("ap-southeast-1"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-08569b978cc4dfa10"),
			jsii.String("HVMG2"): jsii.String("ami-0be9df32ae9f92309"),
		},
		jsii.String("ap-southeast-2"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-09b42976632b27e9b"),
			jsii.String("HVMG2"): jsii.String("ami-0a9ce9fecc3d1daf8"),
		},
		jsii.String("ap-south-1"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-0912f71e06545ad88"),
			jsii.String("HVMG2"): jsii.String("ami-097b15e89dbdcfcf4"),
		},
		jsii.String("us-east-2"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-0b59bfac6be064b78"),
			jsii.String("HVMG2"): jsii.String("NOT_SUPPORTED"),
		},
		jsii.String("ca-central-1"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-0b18956f"),
			jsii.String("HVMG2"): jsii.String("NOT_SUPPORTED"),
		},
		jsii.String("sa-east-1"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-07b14488da8ea02a0"),
			jsii.String("HVMG2"): jsii.String("NOT_SUPPORTED"),
		},
		jsii.String("cn-north-1"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-0a4eaf6c4454eda75"),
			jsii.String("HVMG2"): jsii.String("NOT_SUPPORTED"),
		},
		jsii.String("cn-northwest-1"): map[*string]*string{
			jsii.String("HVM64"): jsii.String("ami-6b6a7d09"),
			jsii.String("HVMG2"): jsii.String("NOT_SUPPORTED"),
		},
	}
	*/

	var sprops cdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := cdk.NewStack(scope, &id, &sprops)

	cloudWatchPutMetricsRole := iam.NewCfnRole(
		stack,
		jsii.String("CloudWatchPutMetricsRole"),
		&iam.CfnRoleProps{
			AssumeRolePolicyDocument: map[string]interface{} {
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Effect": jsii.String("Allow"),
						"Principal": map[string]interface{} {
							"Service": &[]interface{}{
								jsii.String("ec2.amazonaws.com"),
							},
						},
						"Action": &[]interface{}{
							jsii.String("sts:AssumeRole"),
						},
					},
				},
			},
			Path: jsii.String("/"),
		},
	)

	fileSystem := efs.NewCfnFileSystem(
		stack,
		jsii.String("FileSystem"),
		&efs.CfnFileSystemProps{
			PerformanceMode: jsii.String("generalPurpose"),
			FileSystemTags: &[]interface{}{
				&ElasticFileSystemTagProperty{
					Key: jsii.String("Name"),
					Value: props.VolumeName,
				},
			},
		},
	)

	internetGateway := ec2.NewCfnInternetGateway(
		stack,
		jsii.String("InternetGateway"),
		&ec2.CfnInternetGatewayProps{
			Tags: &[]*cdk.CfnTag{
				&cdk.CfnTag{
					Key: jsii.String("Application"),
					Value: stack.StackName(),
				},
				&cdk.CfnTag{
					Key: jsii.String("Network"),
					Value: jsii.String("Public"),
				},
			},
		},
	)

	vpc := ec2.NewCfnVPC(
		stack,
		jsii.String("VPC"),
		&ec2.CfnVPCProps{
			EnableDnsSupport: jsii.Bool(true),
			EnableDnsHostnames: jsii.Bool(true),
			CidrBlock: jsii.String("10.0.0.0/16"),
			Tags: &[]*cdk.CfnTag{
				&cdk.CfnTag{
					Key: jsii.String("Application"),
					Value: stack.StackId(),
				},
			},
		},
	)

	iam.NewCfnInstanceProfile(
		stack,
		jsii.String("CloudWatchPutMetricsInstanceProfile"),
		&iam.CfnInstanceProfileProps{
			Path: jsii.String("/"),
			Roles: &[]*string{
				cloudWatchPutMetricsRole.Ref(),
			},
		},
	)

	iam.NewCfnPolicy(
		stack,
		jsii.String("CloudWatchPutMetricsRolePolicy"),
		&iam.CfnPolicyProps{
			PolicyName: jsii.String("CloudWatch_PutMetricData"),
			PolicyDocument: map[string]interface{} {
				"Version": jsii.String("2012-10-17"),
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Sid": jsii.String("CloudWatchPutMetricData"),
						"Effect": jsii.String("Allow"),
						"Action": &[]interface{}{
							jsii.String("cloudwatch:PutMetricData"),
						},
						"Resource": &[]interface{}{
							jsii.String("*"),
						},
					},
				},
			},
			Roles: &[]*string{
				cloudWatchPutMetricsRole.Ref(),
			},
		},
	)

	ec2.NewCfnVPCGatewayAttachment(
		stack,
		jsii.String("GatewayToInternet"),
		&ec2.CfnVPCGatewayAttachmentProps{
			VpcId: vpc.Ref(),
			InternetGatewayId: internetGateway.Ref(),
		},
	)

	ec2.NewCfnSecurityGroup(
		stack,
		jsii.String("InstanceSecurityGroup"),
		&ec2.CfnSecurityGroupProps{
			VpcId: vpc.Ref(),
			GroupDescription: jsii.String("Enable SSH access via port 22"),
			SecurityGroupIngress: &[]interface{}{
				&IngressProperty{
					IpProtocol: jsii.String("tcp"),
					FromPort: jsii.Number(22),
					ToPort: jsii.Number(22),
					CidrIp: props.SshLocation,
				},
				&IngressProperty{
					IpProtocol: jsii.String("tcp"),
					FromPort: jsii.Number(80),
					ToPort: jsii.Number(80),
					CidrIp: jsii.String("0.0.0.0/0"),
				},
			},
		},
	)

	mountTargetSecurityGroup := ec2.NewCfnSecurityGroup(
		stack,
		jsii.String("MountTargetSecurityGroup"),
		&ec2.CfnSecurityGroupProps{
			VpcId: vpc.Ref(),
			GroupDescription: jsii.String("Security group for mount target"),
			SecurityGroupIngress: &[]interface{}{
				&IngressProperty{
					IpProtocol: jsii.String("tcp"),
					FromPort: jsii.Number(2049),
					ToPort: jsii.Number(2049),
					CidrIp: jsii.String("0.0.0.0/0"),
				},
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

	subnet := ec2.NewCfnSubnet(
		stack,
		jsii.String("Subnet"),
		&ec2.CfnSubnetProps{
			VpcId: vpc.Ref(),
			CidrBlock: jsii.String("10.0.0.0/24"),
			Tags: &[]*cdk.CfnTag{
				&cdk.CfnTag{
					Key: jsii.String("Application"),
					Value: stack.StackId(),
				},
			},
		},
	)

	ec2.NewCfnRoute(
		stack,
		jsii.String("InternetGatewayRoute"),
		&ec2.CfnRouteProps{
			DestinationCidrBlock: jsii.String("0.0.0.0/0"),
			RouteTableId: routeTable.Ref(),
			GatewayId: internetGateway.Ref(),
		},
	)

	mountTarget := efs.NewCfnMountTarget(
		stack,
		jsii.String("MountTarget"),
		&efs.CfnMountTargetProps{
			FileSystemId: fileSystem.Ref(),
			SubnetId: subnet.Ref(),
			SecurityGroups: &[]*string{
				mountTargetSecurityGroup.Ref(),
			},
		},
	)

	ec2.NewCfnSubnetRouteTableAssociation(
		stack,
		jsii.String("SubnetRouteTableAssoc"),
		&ec2.CfnSubnetRouteTableAssociationProps{
			RouteTableId: routeTable.Ref(),
			SubnetId: subnet.Ref(),
		},
	)

	return &EfsStack{
		Stack: stack,
		MountTargetId: mountTarget.Ref(),
		FileSystemId: fileSystem.Ref(),
	}
}

