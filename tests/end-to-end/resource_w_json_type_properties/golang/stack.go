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

