package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	ec2 "github.com/aws/aws-cdk-go/awscdk/v2/awsec2"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type VpcStackProps struct {
	cdk.StackProps
}

type VpcStack struct {
	cdk.Stack
}

func NewVpcStack(scope constructs.Construct, id string, props *VpcStackProps) *VpcStack {
	var sprops cdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := cdk.NewStack(scope, &id, &sprops)

	vpc := ec2.NewCfnVPC(
		stack,
		jsii.String("VPC"),
		&ec2.CfnVPCProps{
			CidrBlock: jsii.String("10.42.0.0/16"),
			EnableDnsSupport: jsii.Bool(true),
			EnableDnsHostnames: jsii.Bool(true),
			Tags: &[]*cdk.CfnTag{
				&cdk.CfnTag{
					Key: jsii.String("cost-center"),
					Value: jsii.String("1337"),
				},
			},
		},
	)

	ec2.NewCfnSubnet(
		stack,
		jsii.String("Subnet1"),
		&ec2.CfnSubnetProps{
			AvailabilityZone: cdk.Fn_Select(jsii.Number(0), cdk.Fn_GetAzs(jsii.String(""))),
			CidrBlock: cdk.Fn_Select(jsii.Number(0), cdk.Fn_Cidr(vpc.AttrCidrBlock(), jsii.Number(6), jsii.String("8"))),
			VpcId: vpc.Ref(),
		},
	)

	ec2.NewCfnSubnet(
		stack,
		jsii.String("Subnet2"),
		&ec2.CfnSubnetProps{
			AvailabilityZone: cdk.Fn_Select(jsii.Number(1), cdk.Fn_GetAzs(jsii.String(""))),
			CidrBlock: cdk.Fn_Select(jsii.Number(1), cdk.Fn_Cidr(vpc.AttrCidrBlock(), jsii.Number(6), jsii.String("8"))),
			VpcId: vpc.Ref(),
		},
	)

	ec2.NewCfnSubnet(
		stack,
		jsii.String("Subnet3"),
		&ec2.CfnSubnetProps{
			AvailabilityZone: cdk.Fn_Select(jsii.Number(2), cdk.Fn_GetAzs(jsii.String(""))),
			CidrBlock: cdk.Fn_Select(jsii.Number(2), cdk.Fn_Cidr(vpc.AttrCidrBlock(), jsii.Number(6), jsii.String("8"))),
			VpcId: vpc.Ref(),
		},
	)

	return &VpcStack{
		Stack: stack,
	}
}

