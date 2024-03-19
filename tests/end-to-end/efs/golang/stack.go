package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	efs "github.com/aws/aws-cdk-go/awscdk/v2/awsefs"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type EfsStackProps struct {
	cdk.StackProps
}

type EfsStack struct {
	cdk.Stack
}

func NewEfsStack(scope constructs.Construct, id string, props *EfsStackProps) *EfsStack {
	var sprops cdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := cdk.NewStack(scope, &id, &sprops)

	efs.NewCfnFileSystem(
		stack,
		jsii.String("FileSystem"),
		&efs.CfnFileSystemProps{
		},
	)

	return &EfsStack{
		Stack: stack,
	}
}

