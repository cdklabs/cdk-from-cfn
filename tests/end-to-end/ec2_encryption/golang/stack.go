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
}

type Ec2EncryptionStack struct {
	cdk.Stack
}

func NewEc2EncryptionStack(scope constructs.Construct, id string, props *Ec2EncryptionStackProps) *Ec2EncryptionStack {
	var sprops cdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := cdk.NewStack(scope, &id, &sprops)

	hasDatabase := props.DatabaseType == jsii.String("mysql")

	isProduction := props.Environment == jsii.String("prod")

	useEncryption := isProduction && hasDatabase

	ec2.NewCfnInstance(
		stack,
		jsii.String("MyApp"),
		&ec2.CfnInstanceProps{
			ImageId: ifCondition(
				useEncryption,
				props.EncryptedAmi,
				props.UnencryptedAmi,
			),
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
