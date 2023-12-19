package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	iam "github.com/aws/aws-cdk-go/awscdk/v2/awsiam"
	sqs "github.com/aws/aws-cdk-go/awscdk/v2/awssqs"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type JsonPropsStackProps struct {
	cdk.StackProps
}

type JsonPropsStack struct {
	cdk.Stack
}

func NewJsonPropsStack(scope constructs.Construct, id string, props *JsonPropsStackProps) *JsonPropsStack {
	var sprops cdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := cdk.NewStack(scope, &id, &sprops)

	myQueue1 := sqs.NewCfnQueue(
		stack,
		jsii.String("MyQueue1"),
		&sqs.CfnQueueProps{
		},
	)

	myQueue2 := sqs.NewCfnQueue(
		stack,
		jsii.String("MyQueue2"),
		&sqs.CfnQueueProps{
		},
	)

	iam.NewCfnGroup(
		stack,
		jsii.String("MyRDMessageQueueGroup"),
		&iam.CfnGroupProps{
			Policies: &[]*Policy /* FIXME */{
				&Policy/* FIXME */{
					PolicyName: jsii.String("MyQueueGroupPolicy"),
					PolicyDocument: map[string]interface{} {
						"Statement": &[]interface{}{
							map[string]interface{} {
								"Effect": jsii.String("Allow"),
								"Action": &[]interface{}{
									jsii.String("sqs:DeleteMessage"),
									jsii.String("sqs:ReceiveMessage"),
								},
								"Resource": &[]interface{}{
									myQueue1.AttrArn(),
									myQueue2.AttrArn(),
								},
							},
						},
					},
				},
			},
		},
	)

	return &JsonPropsStack{
		Stack: stack,
	}
}

func main() {
	defer jsii.Close()

	app := cdk.NewApp(nil)

	NewJsonPropsStack(app, "JsonProps", JsonPropsStackProps{
		cdk.StackProps{
			Env: env(),
		},
	})

	app.Synth(nil)
}

// env determines the AWS environment (account+region) in which our stack is to
// be deployed. For more information see: https://docs.aws.amazon.com/cdk/latest/guide/environments.html
func env() *cdk.Environment {
	// If unspecified, this stack will be "environment-agnostic".
	// Account/Region-dependent features and context lookups will not work, but a
	// single synthesized template can be deployed anywhere.
	//---------------------------------------------------------------------------
	return nil

	// Uncomment if you know exactly what account and region you want to deploy
	// the stack to. This is the recommendation for production stacks.
	//---------------------------------------------------------------------------
	// return &cdk.Environment{
	//  Account: jsii.String("123456789012"),
	//  Region:  jsii.String("us-east-1"),
	// }

	// Uncomment to specialize this stack for the AWS Account and Region that are
	// implied by the current CLI configuration. This is recommended for dev
	// stacks.
	//---------------------------------------------------------------------------
	// return &cdk.Environment{
	//  Account: jsii.String(os.Getenv("CDK_DEFAULT_ACCOUNT")),
	//  Region:  jsii.String(os.Getenv("CDK_DEFAULT_REGION")),
	// }
}
