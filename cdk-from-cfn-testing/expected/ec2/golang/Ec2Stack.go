package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	ec2 "github.com/aws/aws-cdk-go/awscdk/v2/awsec2"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type Ec2StackProps struct {
	cdk.StackProps
}

type Ec2Stack struct {
	cdk.Stack
}

func NewEc2Stack(scope constructs.Construct, id string, props *Ec2StackProps) *Ec2Stack {
	var sprops cdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := cdk.NewStack(scope, &id, &sprops)

	testVpc := ec2.NewCfnVPC(
		stack,
		jsii.String("TestVPC"),
		&ec2.CfnVPCProps{
			CidrBlock: jsii.String("10.0.0.0/16"),
		},
	)

	ec2.NewCfnSecurityGroup(
		stack,
		jsii.String("SG1"),
		&ec2.CfnSecurityGroupProps{
			GroupDescription: jsii.String("SG2"),
			VpcId: testVpc.Ref(),
			SecurityGroupEgress: &[]interface{}{
				&EgressProperty{
					IpProtocol: jsii.String("TCP"),
					FromPort: jsii.Number(10000),
					ToPort: jsii.Number(10000),
					CidrIp: jsii.String("10.0.0.0/16"),
				},
			},
		},
	)

	return &Ec2Stack{
		Stack: stack,
	}
}

