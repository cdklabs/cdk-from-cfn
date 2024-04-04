from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_apigatewayv2 as apigatewayv2
from constructs import Construct

class ApiGatewayV2Stack(Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Resources
    myApi = apigatewayv2.CfnApi(self, 'MyApi',
          name = 'MyHttpApi',
          protocol_type = 'HTTP',
          description = 'My HTTP API',
        )

    defaultStage = apigatewayv2.CfnStage(self, 'DefaultStage',
          api_id = myApi.ref,
          stage_name = 'default',
          auto_deploy = True,
        )

    helloWorldIntegration = apigatewayv2.CfnIntegration(self, 'HelloWorldIntegration',
          api_id = myApi.ref,
          integration_type = 'HTTP_PROXY',
          integration_uri = 'https://jsonplaceholder.typicode.com/posts/1',
          integration_method = 'GET',
          payload_format_version = '1.0',
        )

    helloWorldRoute = apigatewayv2.CfnRoute(self, 'HelloWorldRoute',
          api_id = myApi.ref,
          route_key = 'GET /hello',
          target = '/'.join([
            'integrations',
            helloWorldIntegration.ref,
          ]),
        )

    # Outputs
    """
      Endpoint for the HTTP API
    """
    self.api_endpoint = f"""https://{myApi.ref}.execute-api.{self.region}.amazonaws.com/default"""
    cdk.CfnOutput(self, 'CfnOutputApiEndpoint', 
      key = 'ApiEndpoint',
      description = 'Endpoint for the HTTP API',
      value = str(self.api_endpoint),
    )



