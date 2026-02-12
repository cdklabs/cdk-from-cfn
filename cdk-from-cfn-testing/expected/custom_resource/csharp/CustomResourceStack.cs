using Amazon.CDK;
using Amazon.CDK.AWS.IAM;
using Amazon.CDK.AWS.Lambda;
using Constructs;
using System.Collections.Generic;

namespace CustomResourceStack
{
    public class CustomResourceStackProps : StackProps
    {
    }

    /// <summary>
    /// Test Custom Resource conversion
    /// </summary>
    public class CustomResourceStack : Stack
    {
        public CustomResourceStack(Construct scope, string id, CustomResourceStackProps props = null) : base(scope, id, props)
        {

            // Resources
            var lambdaRole = new CfnRole(this, "LambdaRole", new CfnRoleProps
            {
                AssumeRolePolicyDocument = new Dictionary<string, object>
                {
                    { "Version", "2012-10-17"},
                    { "Statement", new []
                    {
                        new Dictionary<string, object>
                        {
                            { "Effect", "Allow"},
                            { "Principal", new Dictionary<string, object>
                            {
                                { "Service", "lambda.amazonaws.com"},
                            }},
                            { "Action", "sts:AssumeRole"},
                        },
                    }},
                },
            });
            var backingLambda = new CfnFunction(this, "BackingLambda", new CfnFunctionProps
            {
                Runtime = "python3.9",
                Handler = "index.handler",
                Role = lambdaRole.AttrArn,
                Code = new CfnFunction.CodeProperty
                {
                    ZipFile = @"def handler(event, context):
                      return {'Status': 'SUCCESS', 'Data': {'Endpoint': 'test-endpoint'}}
                    ",
                },
            });
            var myCustomResource = new CfnCustomResource(this, "MyCustomResource", new CfnCustomResourceProps
            {
                ServiceToken = backingLambda.AttrArn,
            });
            myCustomResource.AddOverride("Type", "Custom::DatabaseSetup");
            myCustomResource.AddPropertyOverride("DatabaseName", "mydb");
            myCustomResource.AddPropertyOverride("TableCount", 5);
            myCustomResource.AddPropertyOverride("EnableLogging", "true");
            myCustomResource.AddPropertyOverride("Tags", new []
            {
                "prod",
                "critical",
            });
            myCustomResource.CfnOptions.DeletionPolicy = CfnDeletionPolicy.RETAIN;
            myCustomResource.AddDependency(backingLambda);
            var consumerLambda = new CfnFunction(this, "ConsumerLambda", new CfnFunctionProps
            {
                Runtime = "python3.9",
                Handler = "index.handler",
                Role = lambdaRole.AttrArn,
                Code = new CfnFunction.CodeProperty
                {
                    ZipFile = @"def handler(event, context):
                      pass
                    ",
                },
                Environment = new CfnFunction.EnvironmentProperty
                {
                    Variables = new Dictionary<string, string>
                    {
                        { "DB_ENDPOINT", myCustomResource.GetAtt("Endpoint").ToString()},
                    },
                },
            });
        }
    }
}
