package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	sam "github.com/aws/aws-cdk-go/awscdk/v2/awssam"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type SAMNodeJSLambdaConstructProps struct {
}

type SAMNodeJSLambdaConstruct struct {
	constructs.Construct
}

func NewSAMNodeJSLambdaConstruct(scope constructs.Construct, id string, props *SAMNodeJSLambdaConstructProps) *SAMNodeJSLambdaConstruct {
	construct := constructs.NewConstruct(scope, &id)

	cdk.Stack_Of(construct).AddTransform(jsii.String("AWS::Serverless-2016-10-31"))

	sam.NewCfnFunction(
		construct,
		jsii.String("MyFunction"),
		&sam.CfnFunctionProps{
			Runtime: jsii.String("nodejs20.x"),
			Handler: jsii.String("index.handler"),
			InlineCode: jsii.String("exports.handler = async (event) => {\n  console.log(event);\n}\n"),
		},
	)

	return &SAMNodeJSLambdaConstruct{
		Construct: construct,
	}
}

