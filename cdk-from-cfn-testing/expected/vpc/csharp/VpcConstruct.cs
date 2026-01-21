using Amazon.CDK;
using Amazon.CDK.AWS.EC2;
using Constructs;
using System.Collections.Generic;

namespace VpcConstruct
{
    public class VpcConstructProps
    {
    }

    public class VpcConstruct : Construct
    {
        public VpcConstruct(Construct scope, string id, VpcConstructProps props = null) : base(scope, id)
        {

            // Resources
            var vpc = new CfnVPC(this, "VPC", new CfnVPCProps
            {
                CidrBlock = "10.42.0.0/16",
                EnableDnsSupport = true,
                EnableDnsHostnames = true,
                Tags = new []
                {
                    new CfnTag
                    {
                        Key = "cost-center",
                        Value = "1337",
                    },
                },
            });
            var subnet1 = new CfnSubnet(this, "Subnet1", new CfnSubnetProps
            {
                AvailabilityZone = Fn.Select(0, Fn.GetAzs("")),
                CidrBlock = Fn.Select(0, Fn.Cidr(vpc.AttrCidrBlock, 6, "8")),
                VpcId = vpc.Ref,
            });
            var subnet2 = new CfnSubnet(this, "Subnet2", new CfnSubnetProps
            {
                AvailabilityZone = Fn.Select(1, Fn.GetAzs("")),
                CidrBlock = Fn.Select(1, Fn.Cidr(vpc.AttrCidrBlock, 6, "8")),
                VpcId = vpc.Ref,
            });
            var subnet3 = new CfnSubnet(this, "Subnet3", new CfnSubnetProps
            {
                AvailabilityZone = Fn.Select(2, Fn.GetAzs("")),
                CidrBlock = Fn.Select(2, Fn.Cidr(vpc.AttrCidrBlock, 6, "8")),
                VpcId = vpc.Ref,
            });
        }
    }
}
