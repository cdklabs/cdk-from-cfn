import * as cdk from 'aws-cdk-lib';
import * as apigatewayv2 from 'aws-cdk-lib/aws-apigatewayv2';

export interface ApiGatewayV2StackProps extends cdk.StackProps {
}

export class ApiGatewayV2Stack extends cdk.Stack {
  /**
   * Endpoint for the HTTP API
   */
  public readonly apiEndpoint;

  public constructor(scope: cdk.App, id: string, props: ApiGatewayV2StackProps = {}) {
    super(scope, id, props);

    // Resources
    const myApi = new apigatewayv2.CfnApi(this, 'MyApi', {
      name: 'MyHttpApi',
      protocolType: 'HTTP',
      description: 'My HTTP API',
    });

    const defaultStage = new apigatewayv2.CfnStage(this, 'DefaultStage', {
      apiId: myApi.ref,
      stageName: 'default',
      autoDeploy: true,
    });

    const helloWorldIntegration = new apigatewayv2.CfnIntegration(this, 'HelloWorldIntegration', {
      apiId: myApi.ref,
      integrationType: 'HTTP_PROXY',
      integrationUri: 'https://jsonplaceholder.typicode.com/posts/1',
      integrationMethod: 'GET',
      payloadFormatVersion: '1.0',
    });

    const helloWorldRoute = new apigatewayv2.CfnRoute(this, 'HelloWorldRoute', {
      apiId: myApi.ref,
      routeKey: 'GET /hello',
      target: [
        'integrations',
        helloWorldIntegration.ref,
      ].join('/'),
    });

    // Outputs
    this.apiEndpoint = `https://${myApi.ref}.execute-api.${this.region}.amazonaws.com/default`;
    new cdk.CfnOutput(this, 'CfnOutputApiEndpoint', {
      key: 'ApiEndpoint',
      description: 'Endpoint for the HTTP API',
      value: this.apiEndpoint!.toString(),
    });
  }
}
