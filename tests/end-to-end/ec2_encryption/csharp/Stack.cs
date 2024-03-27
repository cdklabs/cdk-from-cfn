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

        public string SubnetType { get; set; }

        public bool? EnableMonitoringParameter { get; set; }

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
            props.SubnetType ??= "Private1";
            props.EnableMonitoringParameter ??= false;

            // Mappings
            var regionToAmi = new Dictionary<string, Dictionary<string,string>> 
            {
                ["us-east-1"] = new Dictionary<string, string> {["AMI"] = "ami-12345678", },
                ["us-west-2"] = new Dictionary<string, string> {["AMI"] = "ami-87654321", },
            };

            // Conditions
            bool hasDatabase = props.DatabaseType == "mysql";
            bool isProduction = props.Environment == "prod";
            bool usePrivateSecurityGroup = props.SubnetType == "Private1" || props.SubnetType == "Private2";
            bool keyPairProd = !(isProduction);
            bool useEncryption = isProduction && hasDatabase;

            // Resources
            var privateSecurityGroup = new CfnSecurityGroup(this, "PrivateSecurityGroup", new CfnSecurityGroupProps
            {
                GroupDescription = "Private security group",
                VpcId = "vpc-xxxxxxxx",
            });
            var publicSecurityGroup = new CfnSecurityGroup(this, "PublicSecurityGroup", new CfnSecurityGroupProps
            {
                GroupDescription = "Public security group",
                VpcId = "vpc-xxxxxxxx",
            });
            var myApp = new CfnInstance(this, "MyApp", new CfnInstanceProps
            {
                ImageId = regionToAmi["us-east-1"]["AMI"],
                SecurityGroups = new []
                {
                    usePrivateSecurityGroup ? privateSecurityGroup.Ref : publicSecurityGroup.Ref,
                },
            });
        }
    }
}
