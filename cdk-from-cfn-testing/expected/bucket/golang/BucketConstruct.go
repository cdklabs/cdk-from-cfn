package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	s3 "github.com/aws/aws-cdk-go/awscdk/v2/awss3"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type BucketConstructProps struct {
}

type BucketConstruct struct {
	constructs.Construct
}

func NewBucketConstruct(scope constructs.Construct, id string, props *BucketConstructProps) *BucketConstruct {
	construct := constructs.NewConstruct(scope, &id)

	s3.NewCfnBucket(
		construct,
		jsii.String("Bucket"),
		&s3.CfnBucketProps{
		},
	)

	return &BucketConstruct{
		Construct: construct,
	}
}

