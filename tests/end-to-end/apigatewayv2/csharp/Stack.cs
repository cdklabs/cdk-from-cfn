using Amazon.CDK;
using Amazon.CDK.AWS.ApiGatewayV2;
using Constructs;
using System.Collections.Generic;

namespace ApiGatewayV2Stack
{
    public class ApiGatewayV2StackProps : StackProps
    {
    }

    public class ApiGatewayV2Stack : Stack
    {
        /// <summary>
        /// Endpoint for the HTTP API
        /// </summary>
        public object ApiEndpoint { get; } 

        public ApiGatewayV2Stack(Construct scope, string id, ApiGatewayV2StackProps props = null) : base(scope, id, props)
        {

            // Resources
            var myApi = new CfnApi(this, "MyApi", new CfnApiProps
            {
                Name = "MyHttpApi",
                ProtocolType = "HTTP",
                Description = "My HTTP API",
            });
            var defaultStage = new CfnStage(this, "DefaultStage", new CfnStageProps
            {
                ApiId = myApi.Ref,
                StageName = "default",
                AutoDeploy = true,
            });
            var helloWorldIntegration = new CfnIntegration(this, "HelloWorldIntegration", new CfnIntegrationProps
            {
                ApiId = myApi.Ref,
                IntegrationType = "HTTP_PROXY",
                IntegrationUri = "https://jsonplaceholder.typicode.com/posts/1",
                IntegrationMethod = "GET",
                PayloadFormatVersion = "1.0",
            });
            var helloWorldRoute = new CfnRoute(this, "HelloWorldRoute", new CfnRouteProps
            {
                ApiId = myApi.Ref,
                RouteKey = "GET /hello",
                Target = string.Join("/", new []
                {
                    "integrations",
                    helloWorldIntegration.Ref,
                }),
            });

            // Outputs
            ApiEndpoint = $"https://{myApi.Ref}.execute-api.{Region}.amazonaws.com/default";
        }
    }
}
