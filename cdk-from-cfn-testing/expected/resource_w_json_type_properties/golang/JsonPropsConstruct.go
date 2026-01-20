package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	iam "github.com/aws/aws-cdk-go/awscdk/v2/awsiam"
	sqs "github.com/aws/aws-cdk-go/awscdk/v2/awssqs"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type JsonPropsConstructProps struct {
}

type JsonPropsConstruct struct {
	constructs.Construct
}

func NewJsonPropsConstruct(scope constructs.Construct, id string, props *JsonPropsConstructProps) *JsonPropsConstruct {
	construct := constructs.NewConstruct(scope, &id)

	myQueue1 := sqs.NewCfnQueue(
		construct,
		jsii.String("MyQueue1"),
		&sqs.CfnQueueProps{
		},
	)

	myQueue2 := sqs.NewCfnQueue(
		construct,
		jsii.String("MyQueue2"),
		&sqs.CfnQueueProps{
		},
	)

	iam.NewCfnGroup(
		construct,
		jsii.String("MyRDMessageQueueGroup"),
		&iam.CfnGroupProps{
			Policies: &[]interface{}{
				&PolicyProperty{
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

	return &JsonPropsConstruct{
		Construct: construct,
	}
}

