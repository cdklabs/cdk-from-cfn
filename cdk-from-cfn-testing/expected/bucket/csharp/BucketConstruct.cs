using Amazon.CDK;
using Amazon.CDK.AWS.S3;
using Constructs;
using System.Collections.Generic;

namespace BucketConstruct
{
    public class BucketConstructProps
    {
    }

    public class BucketConstruct : Construct
    {
        public BucketConstruct(Construct scope, string id, BucketConstructProps props = null) : base(scope, id)
        {

            // Resources
            var bucket = new CfnBucket(this, "Bucket", new CfnBucketProps
            {
            });
        }
    }
}
