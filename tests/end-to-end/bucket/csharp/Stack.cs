using Amazon.CDK;
using Amazon.CDK.AWS.S3;
using Constructs;
using System.Collections.Generic;

namespace BucketStack
{
    public class BucketStackProps : StackProps
    {
    }

    public class BucketStack : Stack
    {
        public BucketStack(Construct scope, string id, BucketStackProps props = null) : base(scope, id, props)
        {

            // Resources
            var bucket = new CfnBucket(this, "Bucket", new CfnBucketProps
            {
            });
        }
    }
}
