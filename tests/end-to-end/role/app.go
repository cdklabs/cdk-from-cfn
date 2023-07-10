package role

import (
	"fmt"

	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	iam "github.com/aws/aws-cdk-go/awscdk/v2/awsiam"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type NoctStackProps struct {
	cdk.StackProps
}

type NoctStack struct {
	cdk.Stack
}

func NewNoctStack(scope constructs.Construct, id string, props NoctStackProps) *NoctStack {
	stack := cdk.NewStack(scope, &id, &props.StackProps)

	iam.NewCfnRole(
		stack,
		jsii.String("MyRole"),
		&iam.CfnRoleProps{
			AssumeRolePolicyDocument: interface{}{
				Statement: &[]interface{}{
					interface{}{
						Action: &[]interface{}{
							jsii.String("sts:AssumeRole"),
						},
						Condition: interface{}{
							StringLike: interface{}{
								Kms:ViaService: jsii.String(fmt.Sprintf("s3.us-east-1.amazonaws.com")),
							},
						},
						Effect: jsii.String("Allow"),
						Principal: interface{}{
							Service: &[]interface{}{
								jsii.String("lambda.amazonaws.com"),
							},
						},
					},
				},
				Version: jsii.String("2012-10-17"),
			},
		},
	)

	return &NoctStack{
		Stack: stack,
	}
}