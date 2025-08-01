package main

import (
	"fmt"

	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	apigatewayv2 "github.com/aws/aws-cdk-go/awscdk/v2/awsapigatewayv2"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type ApiGatewayV2StackProps struct {
	cdk.StackProps
}

type ApiGatewayV2Stack struct {
	cdk.Stack
	/// Endpoint for the HTTP API
	ApiEndpoint interface{} // TODO: fix to appropriate type
}

func NewApiGatewayV2Stack(scope constructs.Construct, id string, props *ApiGatewayV2StackProps) *ApiGatewayV2Stack {
	var sprops cdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := cdk.NewStack(scope, &id, &sprops)

	myApi := api_gateway_v2.NewCfnApi(
		stack,
		jsii.String("MyApi"),
		&api_gateway_v2.CfnApiProps{
			Name: jsii.String("MyHttpApi"),
			ProtocolType: jsii.String("HTTP"),
			Description: jsii.String("My HTTP API"),
		},
	)

	api_gateway_v2.NewCfnStage(
		stack,
		jsii.String("DefaultStage"),
		&api_gateway_v2.CfnStageProps{
			ApiId: myApi.Ref(),
			StageName: jsii.String("default"),
			AutoDeploy: jsii.Bool(true),
		},
	)

	helloWorldIntegration := api_gateway_v2.NewCfnIntegration(
		stack,
		jsii.String("HelloWorldIntegration"),
		&api_gateway_v2.CfnIntegrationProps{
			ApiId: myApi.Ref(),
			IntegrationType: jsii.String("HTTP_PROXY"),
			IntegrationUri: jsii.String("https://jsonplaceholder.typicode.com/posts/1"),
			IntegrationMethod: jsii.String("GET"),
			PayloadFormatVersion: jsii.String("1.0"),
		},
	)

	api_gateway_v2.NewCfnRoute(
		stack,
		jsii.String("HelloWorldRoute"),
		&api_gateway_v2.CfnRouteProps{
			ApiId: myApi.Ref(),
			RouteKey: jsii.String("GET /hello"),
			Target: cdk.Fn_Join(jsii.String("/"), &[]*string{
				jsii.String("integrations"),
				helloWorldIntegration.Ref(),
			}),
		},
	)

	return &ApiGatewayV2Stack{
		Stack: stack,
		ApiEndpoint: jsii.String(fmt.Sprintf("https://%v.execute-api.%v.amazonaws.com/default", myApi.Ref(), stack.Region())),
	}
}

