using Amazon.CDK;
using Amazon.CDK.AWS.EC2;
using Constructs;
using System.Collections.Generic;

namespace Ec2Construct
{
    public class Ec2ConstructProps
    {
    }

    public class Ec2Construct : Construct
    {
        public Ec2Construct(Construct scope, string id, Ec2ConstructProps props = null) : base(scope, id)
        {

            // Resources
            var testVpc = new CfnVPC(this, "TestVPC", new CfnVPCProps
            {
                CidrBlock = "10.0.0.0/16",
            });
            var sg1 = new CfnSecurityGroup(this, "SG1", new CfnSecurityGroupProps
            {
                GroupDescription = "SG2",
                VpcId = testVpc.Ref,
                SecurityGroupEgress = new []
                {
                    new CfnSecurityGroup.EgressProperty
                    {
                        IpProtocol = "TCP",
                        FromPort = 10000,
                        ToPort = 10000,
                        CidrIp = "10.0.0.0/16",
                    },
                },
            });
        }
    }
}
