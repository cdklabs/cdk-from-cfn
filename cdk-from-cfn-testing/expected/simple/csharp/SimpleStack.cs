using Amazon.CDK;
using Amazon.CDK.AWS.S3;
using Amazon.CDK.AWS.SQS;
using Constructs;
using System.Collections.Generic;

namespace SimpleStack
{
    public class SimpleStackProps : StackProps
    {
        /// <summary>
        /// The prefix for the bucket name
        /// </summary>
        public string BucketNamePrefix { get; set; }

        public string LogDestinationBucketName { get; set; }

        /// <summary>
        /// A number parameter to test type generation
        /// </summary>
        public double? NumberParam { get; set; }

    }

    /// <summary>
    /// An example stack that uses many of the syntax elements permitted in a
    /// CloudFormation template, but does not attempt to represent a realistic stack.
    /// </summary>
    public class SimpleStack : Stack
    {
        /// <summary>
        /// The ARN of the bucket in this template!
        /// </summary>
        public object BucketArn { get; } 

        /// <summary>
        /// The ARN of the SQS Queue
        /// </summary>
        public object QueueArn { get; } 

        /// <summary>
        /// Whether this is a large region or not
        /// </summary>
        public object IsLarge { get; } 

        public SimpleStack(Construct scope, string id, SimpleStackProps props = null) : base(scope, id, props)
        {
            // Applying default props
            props ??= new SimpleStackProps();
            props.BucketNamePrefix ??= "bucket";
            props.LogDestinationBucketName = new CfnParameter(this, "LogDestinationBucketName", new CfnParameterProps
            {
                Type = "AWS::SSM::Parameter::Value<String>",
                Default = props.LogDestinationBucketName ?? "/logging/bucket/name",
            }).ValueAsString;
            props.NumberParam ??= 42;

            // Mappings
            var booleans = new Dictionary<string, Dictionary<string,bool>> 
            {
                ["True"] = new Dictionary<string, bool> {["true"] = true, },
                ["False"] = new Dictionary<string, bool> {["false"] = false, },
            };
            var lists = new Dictionary<string, Dictionary<string,string[]>> 
            {
                ["Candidates"] = new Dictionary<string, string[]> {["Empty"] = new string[] {}, ["Singleton"] = new string[] {"One", }, ["Pair"] = new string[] {"One", "Two", }, },
            };
            var numbers = new Dictionary<string, Dictionary<string,int>> 
            {
                ["Prime"] = new Dictionary<string, int> {["Eleven"] = 11, ["Thirteen"] = 13, ["Seventeen"] = 17, },
            };
            var strings = new Dictionary<string, Dictionary<string,string>> 
            {
                ["Foos"] = new Dictionary<string, string> {["Foo1"] = "Foo1", ["Foo2"] = "Foo2", },
                ["Bars"] = new Dictionary<string, string> {["Bar"] = "Bar", },
            };
            var table = new Dictionary<string, Dictionary<string,object>> 
            {
                ["Values"] = new Dictionary<string, object> {["Boolean"] = true, ["Float"] = 3.14, ["List"] = new string[] {"1", "2", "3", }, ["Number"] = 42, ["String"] = "Baz", },
            };

            // Conditions
            bool isUs = Fn.Select(0, Fn.Split("-", Region)) == "us";
            bool isUsEast1 = Region == "us-east-1";
            bool isLargeRegion = isUsEast1;

            // Resources
            var queue = new CfnQueue(this, "Queue", new CfnQueueProps
            {
                DelaySeconds = 42,
                SqsManagedSseEnabled = false,
                KmsMasterKeyId = Fn.ImportValue("Shared-KmsKeyArn"),
                QueueName = string.Join("-", new []
                {
                    StackName,
                    strings["Bars"]["Bar"],
                    Fn.Select(1, Fn.GetAzs(Region)),
                }),
                RedrivePolicy = null,
                VisibilityTimeout = 120,
            });
            var bucket = new CfnBucket(this, "Bucket", new CfnBucketProps
            {
                AccessControl = "Private",
                LoggingConfiguration = new CfnBucket.LoggingConfigurationProperty
                {
                    DestinationBucketName = props.LogDestinationBucketName,
                },
                WebsiteConfiguration = new CfnBucket.WebsiteConfigurationProperty
                {
                    RedirectAllRequestsTo = new CfnBucket.RedirectAllRequestsToProperty
                    {
                        HostName = "example.com",
                        Protocol = "https",
                    },
                },
                Tags = new []
                {
                    new CfnTag
                    {
                        Key = "FancyTag",
                        Value = isUsEast1 ? Fn.Base64(table["Values"]["String"] as string) : Fn.Base64("8CiMvAo=" as string),
                    },
                },
            });

            // Outputs
            BucketArn = isUsEast1
                ? bucket.AttrArn
                : null;
            if (isUsEast1) {
                new CfnOutput(this, "CfnOutputBucketArn", new CfnOutputProps {
                    Key = "BucketArn",
                    Description = "The ARN of the bucket in this template!",
                    ExportName = "ExportName",
                    Value = BucketArn as string,
                });
            }
            QueueArn = queue.Ref;
            IsLarge = isLargeRegion ? true : false;
        }
    }
}
