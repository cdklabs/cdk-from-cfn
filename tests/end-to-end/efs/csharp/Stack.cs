using Amazon.CDK;
using Amazon.CDK.AWS.EFS;
using Constructs;
using System.Collections.Generic;

namespace EfsStack
{
    public class EfsStackProps : StackProps
    {
    }

    public class EfsStack : Stack
    {
        public EfsStack(Construct scope, string id, EfsStackProps props = null) : base(scope, id, props)
        {

            // Resources
            var fileSystem = new CfnFileSystem(this, "FileSystem", new CfnFileSystemProps
            {
            });
        }
    }
}
