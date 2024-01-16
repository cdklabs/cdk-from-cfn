package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	sam "github.com/aws/aws-cdk-go/awscdk/v2/awssam"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type SAMNodeJSLambdaProps struct {
	cdk.StackProps
}

type SAMNodeJSLambda struct {
	cdk.Stack
}

func NewSAMNodeJSLambda(scope constructs.Construct, id string, props *SAMNodeJSLambdaProps) *SAMNodeJSLambda {
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
			Runtime: jsii.String("nodejs18.x"),
			Handler: jsii.String("index.handler"),
			InlineCode: jsii.String("exports.handler = async (event) => {\n  console.log(event);\n}\n"),
		},
	)

	return &SAMNodeJSLambda{
		Stack: stack,
	}
}

func main() {
	defer jsii.Close()

	app := cdk.NewApp(nil)

	NewSAMNodeJSLambda(app, "SAMNodeJSLambda", SAMNodeJSLambdaProps{
		cdk.StackProps{
			Env: env(),
		},
	})

	app.Synth(nil)
}

// env determines the AWS environment (account+region) in which our stack is to
// be deployed. For more information see: https://docs.aws.amazon.com/cdk/latest/guide/environments.html
func env() *cdk.Environment {
	// If unspecified, this stack will be "environment-agnostic".
	// Account/Region-dependent features and context lookups will not work, but a
	// single synthesized template can be deployed anywhere.
	//---------------------------------------------------------------------------
	return nil

	// Uncomment if you know exactly what account and region you want to deploy
	// the stack to. This is the recommendation for production stacks.
	//---------------------------------------------------------------------------
	// return &cdk.Environment{
	//  Account: jsii.String("123456789012"),
	//  Region:  jsii.String("us-east-1"),
	// }

	// Uncomment to specialize this stack for the AWS Account and Region that are
	// implied by the current CLI configuration. This is recommended for dev
	// stacks.
	//---------------------------------------------------------------------------
	// return &cdk.Environment{
	//  Account: jsii.String(os.Getenv("CDK_DEFAULT_ACCOUNT")),
	//  Region:  jsii.String(os.Getenv("CDK_DEFAULT_REGION")),
	// }
}
