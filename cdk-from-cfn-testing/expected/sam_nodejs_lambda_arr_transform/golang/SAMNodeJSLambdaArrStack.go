package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	sam "github.com/aws/aws-cdk-go/awscdk/v2/awssam"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type SAMNodeJSLambdaArrStackProps struct {
	cdk.StackProps
}

type SAMNodeJSLambdaArrStack struct {
	cdk.Stack
}

func NewSAMNodeJSLambdaArrStack(scope constructs.Construct, id string, props *SAMNodeJSLambdaArrStackProps) *SAMNodeJSLambdaArrStack {
	var sprops cdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := cdk.NewStack(scope, &id, &sprops)

	stack.AddTransform(jsii.String("AWS::Serverless-2016-10-31"))

	sam.NewCfnFunction(
		stack,
		jsii.String("MyFunction"),
		&sam.CfnFunctionProps{
			Runtime: jsii.String("nodejs20.x"),
			Handler: jsii.String("index.handler"),
			InlineCode: jsii.String("exports.handler = async (event) => {\n  console.log(event);\n}\n"),
		},
	)

	return &SAMNodeJSLambdaArrStack{
		Stack: stack,
	}
}

