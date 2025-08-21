package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	ec2 "github.com/aws/aws-cdk-go/awscdk/v2/awsec2"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type Ec2EncryptionStackProps struct {
	cdk.StackProps
	Environment *string
	DatabaseType *string
	UseEncryption *bool
	EncryptedAmi *string
	UnencryptedAmi *string
	SubnetType *string
	EnableMonitoringParameter *bool
}

type Ec2EncryptionStack struct {
	cdk.Stack
}

func NewEc2EncryptionStack(scope constructs.Construct, id string, props *Ec2EncryptionStackProps) *Ec2EncryptionStack {
	regionToAmi := map[*string]map[*string]*string{
		jsii.String("us-east-1"): map[*string]*string{
			jsii.String("AMI"): jsii.String("ami-0c02fb55956c7d316"),
		},
		jsii.String("us-west-2"): map[*string]*string{
			jsii.String("AMI"): jsii.String("ami-008fe2fc65df48dac"),
		},
		jsii.String("eu-west-1"): map[*string]*string{
			jsii.String("AMI"): jsii.String("ami-0c9c942bd7bf113a2"),
		},
		jsii.String("ap-southeast-1"): map[*string]*string{
			jsii.String("AMI"): jsii.String("ami-0c802847a7dd848c0"),
		},
		jsii.String("us-east-2"): map[*string]*string{
			jsii.String("AMI"): jsii.String("ami-0900fe555666598a2"),
		},
	}

	var sprops cdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := cdk.NewStack(scope, &id, &sprops)

	hasDatabase := props.DatabaseType == jsii.String("mysql")

	isProduction := props.Environment == jsii.String("prod")

	usePrivateSecurityGroup := props.SubnetType == jsii.String("Private1") || props.SubnetType == jsii.String("Private2")

	keyPairProd := !isProduction

	useEncryption := isProduction && hasDatabase

	privateSecurityGroup := ec2.NewCfnSecurityGroup(
		stack,
		jsii.String("PrivateSecurityGroup"),
		&ec2.CfnSecurityGroupProps{
			GroupDescription: jsii.String("Private security group"),
		},
	)

	publicSecurityGroup := ec2.NewCfnSecurityGroup(
		stack,
		jsii.String("PublicSecurityGroup"),
		&ec2.CfnSecurityGroupProps{
			GroupDescription: jsii.String("Public security group"),
		},
	)

	ec2.NewCfnInstance(
		stack,
		jsii.String("MyApp"),
		&ec2.CfnInstanceProps{
			ImageId: regionToAmi[stack.Region()][jsii.String("AMI")],
			InstanceType: jsii.String("t3.micro"),
			Tags: &[]*cdk.CfnTag{
				&cdk.CfnTag{
					Key: jsii.String("Name"),
					Value: cdk.Fn_Select(jsii.Number(1), cdk.Fn_Split(jsii.String("-"), jsii.String("My-EC2-Instance"))),
				},
			},
			SecurityGroups: &[]*string{
				ifCondition(
					usePrivateSecurityGroup,
					privateSecurityGroup.Ref(),
					publicSecurityGroup.Ref(),
				),
			},
		},
	)

	return &Ec2EncryptionStack{
		Stack: stack,
	}
}

/// ifCondition is a helper function that replicates the ternary
/// operator that can be found in other languages. It is conceptually
/// equivalent to writing `cond ? whenTrue : whenFalse`, meaning it
/// returns `whenTrue` if `cond` is `true`, and `whenFalse` otherwise.
func ifCondition[T any](cond bool, whenTrue T, whenFalse T) T {
	if cond {
		return whenTrue
	}
	return whenFalse
}

