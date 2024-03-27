package main

import (
	"fmt"

	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	iam "github.com/aws/aws-cdk-go/awscdk/v2/awsiam"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type StackSetStackProps struct {
	cdk.StackProps
	ModuleName *string
	RoleName *string
	RolePath *string
}

/// Deploy required components for StackSet custom resources in this region.  Lambda ARN is exported as StackSetCustomResource
type StackSetStack struct {
	cdk.Stack
}

func NewStackSetStack(scope constructs.Construct, id string, props *StackSetStackProps) *StackSetStack {
	var sprops cdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := cdk.NewStack(scope, &id, &sprops)

	useRoleName := !props.RoleName == jsii.String("")

	useRolePath := !props.RolePath == jsii.String("")

	iam.NewCfnRole(
		stack,
		jsii.String("StackSetResourceRole"),
		&iam.CfnRoleProps{
			RoleName: ifCondition(
				useRoleName,
				props.RoleName,
				nil,
			),
			Path: ifCondition(
				useRolePath,
				props.RolePath,
				jsii.String("/"),
			),
			AssumeRolePolicyDocument: map[string]interface{} {
				"Version": jsii.String("2012-10-17"),
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Effect": jsii.String("Allow"),
						"Principal": map[string]interface{} {
							"Service": jsii.String("lambda.amazonaws.com"),
						},
						"Action": jsii.String("sts:AssumeRole"),
					},
				},
			},
			Policies: &[]interface{}{
				&PolicyProperty{
					PolicyName: jsii.String("IAMPassRolePermissions"),
					PolicyDocument: map[string]interface{} {
						"Version": jsii.String("2012-10-17"),
						"Statement": &[]interface{}{
							map[string]interface{} {
								"Effect": jsii.String("Allow"),
								"Action": jsii.String("iam:PassRole"),
								"Resource": jsii.String("*"),
							},
						},
					},
				},
				&PolicyProperty{
					PolicyName: jsii.String("CloudFormationPermissions"),
					PolicyDocument: map[string]interface{} {
						"Version": jsii.String("2012-10-17"),
						"Statement": &[]interface{}{
							map[string]interface{} {
								"Effect": jsii.String("Allow"),
								"Action": jsii.String("cloudformation:*"),
								"Resource": jsii.String("*"),
							},
						},
					},
				},
				&PolicyProperty{
					PolicyName: jsii.String("LambdaPermissions"),
					PolicyDocument: map[string]interface{} {
						"Version": jsii.String("2012-10-17"),
						"Statement": &[]interface{}{
							map[string]interface{} {
								"Effect": jsii.String("Allow"),
								"Action": jsii.String("logs:CreateLogGroup"),
								"Resource": &[]interface{}{
									jsii.String(fmt.Sprintf("arn:aws:logs:%v:%v:*", stack.Region(), stack.Account())),
								},
							},
							map[string]interface{} {
								"Effect": jsii.String("Allow"),
								"Action": &[]interface{}{
									jsii.String("logs:CreateLogStream"),
									jsii.String("logs:PutLogEvents"),
								},
								"Resource": &[]interface{}{
									jsii.String(fmt.Sprintf("arn:aws:logs:%v:%v:log-group:/aws/lambda/*", stack.Region(), stack.Account())),
								},
							},
						},
					},
				},
				&PolicyProperty{
					PolicyName: jsii.String("S3Permissions"),
					PolicyDocument: map[string]interface{} {
						"Version": jsii.String("2012-10-17"),
						"Statement": &[]interface{}{
							map[string]interface{} {
								"Effect": jsii.String("Allow"),
								"Action": &[]interface{}{
									jsii.String("s3:Get*"),
									jsii.String("s3:List*"),
								},
								"Resource": jsii.String("*"),
							},
						},
					},
				},
			},
		},
	)

	return &StackSetStack{
		Stack: stack,
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

