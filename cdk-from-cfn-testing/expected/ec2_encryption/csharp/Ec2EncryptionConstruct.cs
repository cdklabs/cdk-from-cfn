using Amazon.CDK;
using Amazon.CDK.AWS.EC2;
using Constructs;
using System.Collections.Generic;

namespace Ec2EncryptionConstruct
{
    public class Ec2EncryptionConstructProps
    {
        public string Environment { get; set; }

        public string DatabaseType { get; set; }

        public bool? UseEncryption { get; set; }

        public string EncryptedAmi { get; set; }

        public string UnencryptedAmi { get; set; }

        public string SubnetType { get; set; }

        public bool? EnableMonitoringParameter { get; set; }

    }

    public class Ec2EncryptionConstruct : Construct
    {
        public Ec2EncryptionConstruct(Construct scope, string id, Ec2EncryptionConstructProps props = null) : base(scope, id)
        {
            // Applying default props
            props ??= new Ec2EncryptionConstructProps();
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
                ["us-east-1"] = new Dictionary<string, string> {["AMI"] = "ami-0c02fb55956c7d316", },
                ["us-west-2"] = new Dictionary<string, string> {["AMI"] = "ami-008fe2fc65df48dac", },
                ["eu-west-1"] = new Dictionary<string, string> {["AMI"] = "ami-0c9c942bd7bf113a2", },
                ["ap-southeast-1"] = new Dictionary<string, string> {["AMI"] = "ami-0c802847a7dd848c0", },
                ["us-east-2"] = new Dictionary<string, string> {["AMI"] = "ami-0900fe555666598a2", },
            };

            // Conditions
            bool hasDatabase = props.DatabaseType == "mysql";
            bool isProduction = props.Environment == "prod";
            bool usePrivateSecurityGroup = props.SubnetType == "Private1" || props.SubnetType == "Private2";
            bool keyPairProd = !isProduction;
            bool useEncryption = isProduction && hasDatabase;

            // Resources
            var privateSecurityGroup = new CfnSecurityGroup(this, "PrivateSecurityGroup", new CfnSecurityGroupProps
            {
                GroupDescription = "Private security group",
            });
            var publicSecurityGroup = new CfnSecurityGroup(this, "PublicSecurityGroup", new CfnSecurityGroupProps
            {
                GroupDescription = "Public security group",
            });
            var myApp = new CfnInstance(this, "MyApp", new CfnInstanceProps
            {
                ImageId = regionToAmi[Stack.Of(this).Region]["AMI"],
                InstanceType = "t3.micro",
                Tags = new []
                {
                    new CfnTag
                    {
                        Key = "Name",
                        Value = Fn.Select(1, "My-EC2-Instance".Split('-')),
                    },
                },
                SecurityGroups = new []
                {
                    usePrivateSecurityGroup ? privateSecurityGroup.Ref : publicSecurityGroup.Ref,
                },
            });
        }
    }
}
