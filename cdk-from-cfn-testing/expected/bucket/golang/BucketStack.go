package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	s3 "github.com/aws/aws-cdk-go/awscdk/v2/awss3"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type BucketStackProps struct {
	cdk.StackProps
}

type BucketStack struct {
	cdk.Stack
}

func NewBucketStack(scope constructs.Construct, id string, props *BucketStackProps) *BucketStack {
	var sprops cdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := cdk.NewStack(scope, &id, &sprops)

	s3.NewCfnBucket(
		stack,
		jsii.String("Bucket"),
		&s3.CfnBucketProps{
		},
	)

	return &BucketStack{
		Stack: stack,
	}
}

