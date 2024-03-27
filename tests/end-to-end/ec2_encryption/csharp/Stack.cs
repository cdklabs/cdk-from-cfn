using Amazon.CDK;
using Amazon.CDK.AWS.EC2;
using Constructs;
using System.Collections.Generic;

namespace Ec2EncryptionStack
{
    public class Ec2EncryptionStackProps : StackProps
    {
        public string Environment { get; set; }

        public string DatabaseType { get; set; }

        public bool? UseEncryption { get; set; }

        public string EncryptedAmi { get; set; }

        public string UnencryptedAmi { get; set; }

    }

    public class Ec2EncryptionStack : Stack
    {
        public Ec2EncryptionStack(Construct scope, string id, Ec2EncryptionStackProps props = null) : base(scope, id, props)
        {
            // Applying default props
            props ??= new Ec2EncryptionStackProps();
            props.Environment ??= "dev";
            props.DatabaseType ??= "postgresql";
            props.UseEncryption ??= false;
            props.EncryptedAmi ??= "ami-1234567890abcdef0";
            props.UnencryptedAmi ??= "ami-0987654321fedcba0";


            // Conditions
            bool hasDatabase = props.DatabaseType == "mysql";
            bool isProduction = props.Environment == "prod";
            bool useEncryption = isProduction && hasDatabase;

            // Resources
            var myApp = new CfnInstance(this, "MyApp", new CfnInstanceProps
            {
                ImageId = useEncryption ? props.EncryptedAmi : props.UnencryptedAmi,
            });
        }
    }
}
