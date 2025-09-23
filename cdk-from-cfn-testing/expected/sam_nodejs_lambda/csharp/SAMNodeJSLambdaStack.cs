using Amazon.CDK;
using Amazon.CDK.AWS.SAM;
using Constructs;
using System.Collections.Generic;

namespace SAMNodeJSLambdaStack
{
    public class SAMNodeJSLambdaStackProps : StackProps
    {
    }

    public class SAMNodeJSLambdaStack : Stack
    {
        public SAMNodeJSLambdaStack(Construct scope, string id, SAMNodeJSLambdaStackProps props = null) : base(scope, id, props)
        {
            // Transforms
            AddTransform("AWS::Serverless-2016-10-31");

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
