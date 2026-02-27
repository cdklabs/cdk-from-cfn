package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	iam "github.com/aws/aws-cdk-go/awscdk/v2/awsiam"
	lambda "github.com/aws/aws-cdk-go/awscdk/v2/awslambda"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type CustomResourceStackProps struct {
	cdk.StackProps
}

/// Test Custom Resource conversion
type CustomResourceStack struct {
	cdk.Stack
}

func NewCustomResourceStack(scope constructs.Construct, id string, props *CustomResourceStackProps) *CustomResourceStack {
	var sprops cdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := cdk.NewStack(scope, &id, &sprops)

	lambdaRole := iam.NewCfnRole(
		stack,
		jsii.String("LambdaRole"),
		&iam.CfnRoleProps{
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
		},
	)

	backingLambda := lambda.NewCfnFunction(
		stack,
		jsii.String("BackingLambda"),
		&lambda.CfnFunctionProps{
			Runtime: jsii.String("python3.9"),
			Handler: jsii.String("index.handler"),
			Role: lambdaRole.AttrArn(),
			Code: &CodeProperty{
				ZipFile: jsii.String("def handler(event, context):\n  return {'Status': 'SUCCESS', 'Data': {'Endpoint': 'test-endpoint'}}\n"),
			},
		},
	)

	cfnCustomResource := cdk.NewCfnCustomResource(stack, jsii.String("CfnCustomResource"), &cdk.CfnCustomResourceProps{
		ServiceToken: backingLambda.AttrArn(),
	})
	cfnCustomResource.AddPropertyOverride(jsii.String("Region"), jsii.String("us-west-2"))

	myCustomResource := cdk.NewCfnCustomResource(stack, jsii.String("MyCustomResource"), &cdk.CfnCustomResourceProps{
		ServiceToken: backingLambda.AttrArn(),
	})
	myCustomResource.AddOverride(jsii.String("Type"), jsii.String("Custom::DatabaseSetup"))
	myCustomResource.AddPropertyOverride(jsii.String("DatabaseName"), jsii.String("mydb"))
	myCustomResource.AddPropertyOverride(jsii.String("TableCount"), jsii.Number(5))
	myCustomResource.AddPropertyOverride(jsii.String("EnableLogging"), jsii.String("true"))
	myCustomResource.AddPropertyOverride(jsii.String("Tags"), &[]interface{}{
		jsii.String("prod"),
		jsii.String("critical"),
	})
	myCustomResource.CfnOptions().SetDeletionPolicy(cdk.CfnDeletionPolicy_RETAIN)
	myCustomResource.AddDependency(backingLambda)

	lambda.NewCfnFunction(
		stack,
		jsii.String("ConsumerLambda"),
		&lambda.CfnFunctionProps{
			Runtime: jsii.String("python3.9"),
			Handler: jsii.String("index.handler"),
			Role: lambdaRole.AttrArn(),
			Code: &CodeProperty{
				ZipFile: jsii.String("def handler(event, context):\n  pass\n"),
			},
			Environment: &EnvironmentProperty{
				Variables: map[string]interface{} {
					"DB_ENDPOINT": myCustomResource.GetAtt(jsii.String("Endpoint")).ToString(),
					"CFN_RESULT": cfnCustomResource.GetAtt(jsii.String("Result")).ToString(),
				},
			},
		},
	)

	return &CustomResourceStack{
		Stack: stack,
	}
}

