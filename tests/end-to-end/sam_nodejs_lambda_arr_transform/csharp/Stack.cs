using Amazon.CDK;
using Amazon.CDK.AWS.SAM;
using Constructs;
using System.Collections.Generic;

namespace SAMNodeJSLambdaArr
{
    public class SAMNodeJSLambdaArrProps : StackProps
    {
    }

    public class SAMNodeJSLambdaArr : Stack
    {
        public SAMNodeJSLambdaArr(Construct scope, string id, SAMNodeJSLambdaArrProps props = null) : base(scope, id, props)
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
