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
	UseEncryption interface{/* Boolean */}
	EncryptedAmi *string
	UnencryptedAmi *string
	SubnetType *string
	EnableMonitoringParameter interface{/* Boolean */}
}

type Ec2EncryptionStack struct {
	cdk.Stack
}

func NewEc2EncryptionStack(scope constructs.Construct, id string, props *Ec2EncryptionStackProps) *Ec2EncryptionStack {
	regionToAmi := map[*string]map[*string]*string{
		jsii.String("us-east-1"): map[*string]*string{
			jsii.String("AMI"): jsii.String("ami-12345678"),
		},
		jsii.String("us-west-2"): map[*string]*string{
			jsii.String("AMI"): jsii.String("ami-87654321"),
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
			VpcId: jsii.String("vpc-xxxxxxxx"),
		},
	)

	publicSecurityGroup := ec2.NewCfnSecurityGroup(
		stack,
		jsii.String("PublicSecurityGroup"),
		&ec2.CfnSecurityGroupProps{
			GroupDescription: jsii.String("Public security group"),
			VpcId: jsii.String("vpc-xxxxxxxx"),
		},
	)

	ec2.NewCfnInstance(
		stack,
		jsii.String("MyApp"),
		&ec2.CfnInstanceProps{
			ImageId: regionToAmi[jsii.String("us-east-1")][jsii.String("AMI")],
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

