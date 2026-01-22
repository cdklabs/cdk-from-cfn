using Amazon.CDK;
using Amazon.CDK.AWS.IAM;
using Amazon.CDK.AWS.SQS;
using Constructs;
using System.Collections.Generic;

namespace JsonPropsConstruct
{
    public class JsonPropsConstructProps
    {
    }

    public class JsonPropsConstruct : Construct
    {
        public JsonPropsConstruct(Construct scope, string id, JsonPropsConstructProps props = null) : base(scope, id)
        {

            // Resources
            var myQueue1 = new CfnQueue(this, "MyQueue1", new CfnQueueProps
            {
            });
            var myQueue2 = new CfnQueue(this, "MyQueue2", new CfnQueueProps
            {
            });
            var myRdMessageQueueGroup = new CfnGroup(this, "MyRDMessageQueueGroup", new CfnGroupProps
            {
                Policies = new []
                {
                    new CfnGroup.PolicyProperty
                    {
                        PolicyName = "MyQueueGroupPolicy",
                        PolicyDocument = new Dictionary<string, object>
                        {
                            { "Statement", new []
                            {
                                new Dictionary<string, object>
                                {
                                    { "Effect", "Allow"},
                                    { "Action", new []
                                    {
                                        "sqs:DeleteMessage",
                                        "sqs:ReceiveMessage",
                                    }},
                                    { "Resource", new []
                                    {
                                        myQueue1.AttrArn,
                                        myQueue2.AttrArn,
                                    }},
                                },
                            }},
                        },
                    },
                },
            });
        }
    }
}
