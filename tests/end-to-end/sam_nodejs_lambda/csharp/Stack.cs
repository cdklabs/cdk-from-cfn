using Amazon.CDK;
using Amazon.CDK.AWS.SAM;
using Constructs;
using System.Collections.Generic;

namespace SAMNodeJSLambda
{
    public class SAMNodeJSLambdaProps : StackProps
    {
    }

    public class SAMNodeJSLambda : Stack
    {
        public SAMNodeJSLambda(Construct scope, string id, SAMNodeJSLambdaProps props = null) : base(scope, id, props)
        {
            // Transforms
            AddTransform("AWS::Serverless-2016-10-31");

            // Resources
            var myFunction = new CfnFunction(this, "MyFunction", new CfnFunctionProps
            {
                Runtime = "nodejs18.x",
                Handler = "index.handler",
                InlineCode = @"exports.handler = async (event) => {
                  console.log(event);
                }
                ",
            });
        }
    }
}
