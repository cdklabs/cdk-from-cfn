using Amazon.CDK;
using Amazon.CDK.AWS.SAM;
using Constructs;
using System.Collections.Generic;

namespace SAMNodeJSLambdaConstruct
{
    public class SAMNodeJSLambdaConstructProps
    {
    }

    public class SAMNodeJSLambdaConstruct : Construct
    {
        public SAMNodeJSLambdaConstruct(Construct scope, string id, SAMNodeJSLambdaConstructProps props = null) : base(scope, id)
        {
            // Transforms
            Stack.Of(this).AddTransform("AWS::Serverless-2016-10-31");

            // Resources
            var myFunction = new CfnFunction(this, "MyFunction", new CfnFunctionProps
            {
                Runtime = "nodejs20.x",
                Handler = "index.handler",
                InlineCode = @"exports.handler = async (event) => {
                  console.log(event);
                }
                ",
            });
        }
    }
}
