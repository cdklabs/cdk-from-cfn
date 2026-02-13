package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	iam "github.com/aws/aws-cdk-go/awscdk/v2/awsiam"
	lambda "github.com/aws/aws-cdk-go/awscdk/v2/awslambda"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type CustomResourceConstructProps struct {
}

/// Test Custom Resource conversion
type CustomResourceConstruct struct {
	constructs.Construct
}

func NewCustomResourceConstruct(scope constructs.Construct, id string, props *CustomResourceConstructProps) *CustomResourceConstruct {
	construct := constructs.NewConstruct(scope, &id)

	lambdaRole := iam.NewCfnRole(
		construct,
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
		construct,
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

	myCustomResource := cdk.NewCfnCustomResource(construct, jsii.String("MyCustomResource"), &cdk.CfnCustomResourceProps{
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
		construct,
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
				},
			},
		},
	)

	return &CustomResourceConstruct{
		Construct: construct,
	}
}

