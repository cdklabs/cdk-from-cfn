package main

import (
	"fmt"

	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	s3 "github.com/aws/aws-cdk-go/awscdk/v2/awss3"
	sqs "github.com/aws/aws-cdk-go/awscdk/v2/awssqs"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type SimpleStackProps struct {
	cdk.StackProps
	/// The prefix for the bucket name
	BucketNamePrefix *string
	LogDestinationBucketName interface{/* AWS::SSM::Parameter::Value<String> */}
}

/// An example stack that uses many of the syntax elements permitted in a
/// CloudFormation template, but does not attempt to represent a realistic stack.
type SimpleStack struct {
	cdk.Stack
	/// The ARN of the bucket in this template!
	BucketArn interface{} // TODO: fix to appropriate type
	/// The ARN of the SQS Queue
	QueueArn interface{} // TODO: fix to appropriate type
	/// Whether this is a large region or not
	IsLarge interface{} // TODO: fix to appropriate type
}

func NewSimpleStack(scope constructs.Construct, id string, props *SimpleStackProps) *SimpleStack {
	/*
	booleans := map[*string]map[*string]*bool{
		jsii.String("True"): map[*string]*bool{
			jsii.String("true"): jsii.Bool(true),
		},
		jsii.String("False"): map[*string]*bool{
			jsii.String("false"): jsii.Bool(false),
		},
	}
	*/

	/*
	lists := map[*string]map[*string][]*string{
		jsii.String("Candidates"): map[*string][]*string{
			jsii.String("Empty"): []*string{
			},
			jsii.String("Singleton"): []*string{
				jsii.String("One"),
			},
			jsii.String("Pair"): []*string{
				jsii.String("One"),
				jsii.String("Two"),
			},
		},
	}
	*/

	/*
	numbers := map[*string]map[*string]*float64{
		jsii.String("Prime"): map[*string]*float64{
			jsii.String("Eleven"): jsii.Number(11),
			jsii.String("Thirteen"): jsii.Number(13),
			jsii.String("Seventeen"): jsii.Number(17),
		},
	}
	*/

	strings := map[*string]map[*string]*string{
		jsii.String("Foos"): map[*string]*string{
			jsii.String("Foo1"): jsii.String("Foo1"),
			jsii.String("Foo2"): jsii.String("Foo2"),
		},
		jsii.String("Bars"): map[*string]*string{
			jsii.String("Bar"): jsii.String("Bar"),
		},
	}

	table := map[*string]map[*string]interface{}{
		jsii.String("Values"): map[*string]interface{}{
			jsii.String("Boolean"): jsii.Bool(true),
			jsii.String("Float"): jsii.Number(3.14),
			jsii.String("List"): []*string{
				jsii.String("1"),
				jsii.String("2"),
				jsii.String("3"),
			},
			jsii.String("Number"): jsii.Number(42),
			jsii.String("String"): jsii.String("Baz"),
		},
	}

	var sprops cdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := cdk.NewStack(scope, &id, &sprops)

	isUs := cdk.Fn_Select(jsii.Number(0), cdk.Fn_Split(jsii.String("-"), stack.Region())) == jsii.String("us")

	isUsEast1 := stack.Region() == jsii.String("us-east-1")

	isLargeRegion := isUsEast1

	queue := sqs.NewCfnQueue(
		stack,
		jsii.String("Queue"),
		&sqs.CfnQueueProps{
			DelaySeconds: jsii.Number(42),
			SqsManagedSseEnabled: jsii.Bool(false),
			KmsMasterKeyId: cdk.Fn_ImportValue(jsii.String("Shared-KmsKeyArn")),
			QueueName: cdk.Fn_Join(jsii.String("-"), &[]*string{
				stack.StackName(),
				strings[jsii.String("Bars")][jsii.String("Bar")],
				cdk.Fn_Select(jsii.Number(1), cdk.Fn_GetAzs(stack.Region())),
			}),
			RedrivePolicy: nil,
			VisibilityTimeout: jsii.Number(120),
		},
	)

	bucket := s3.NewCfnBucket(
		stack,
		jsii.String("Bucket"),
		&s3.CfnBucketProps{
			AccessControl: jsii.String("Private"),
			BucketName: jsii.String(fmt.Sprintf("%v-%v-bucket", props.BucketNamePrefix, stack.Region())),
			LoggingConfiguration: &LoggingConfiguration/* FIXME */{
				DestinationBucketName: props.LogDestinationBucketName,
			},
			WebsiteConfiguration: &WebsiteConfiguration/* FIXME */{
				RedirectAllRequestsTo: &RedirectAllRequestsTo/* FIXME */{
					HostName: jsii.String("example.com"),
					Protocol: jsii.String("https"),
				},
			},
			Tags: &[]*cdk.CfnTag{
				&cdk.CfnTag{
					Key: jsii.String("FancyTag"),
					Value: ifCondition(
						isUsEast1,
						cdk.Fn_Base64(table[jsii.String("Values")][jsii.String("String")]),
						cdk.Fn_Base64(jsii.String("8CiMvAo=")),
					),
				},
			},
		},
	)

	cdk.NewCfnOutput(stack, jsii.String("CfnOutputBucketArn"), &cdk.CfnOutputProps{
		Key: jsii.String("BucketArn"),
		Description: jsii.String("The ARN of the bucket in this template!"),
		ExportName: jsii.String("ExportName"),
		Value: bucket.AttrArn(),
	})

	return &SimpleStack{
		Stack: stack,
		BucketArn: bucket.AttrArn(),
		QueueArn: queue.Ref(),
		IsLarge: ifCondition(
			isLargeRegion,
			jsii.Bool(true),
			jsii.Bool(false),
		),
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

