using Amazon.CDK;
using Amazon.CDK.AWS.EC2;
using Constructs;
using System.Collections.Generic;

namespace Com.Acme.Test.Simple
{
    public class VpcStackProps : StackProps
    {
    }

    public class VpcStack : Stack
    {
        public VpcStack(Construct scope, string id, VpcStackProps props = null) : base(scope, id, props)
        {
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
