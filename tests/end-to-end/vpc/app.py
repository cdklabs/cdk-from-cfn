from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from constructs import Construct

class VpcStack(Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Resources
    vpc = ec2.CfnVPC(self, 'VPC',
          cidr_block = '10.42.0.0/16',
          enable_dns_support = True,
          enable_dns_hostnames = True,
          tags = [
            {
              'key': 'cost-center',
              'value': 1337,
            },
          ],
        )

    subnet1 = ec2.CfnSubnet(self, 'Subnet1',
          availability_zone = cdk.Fn.select(0, cdk.Fn.getAzs('')),
          cidr_block = cdk.Fn.select(0, cdk.Fn.cidr(vpc.attr_cidr_block, 6, str(8))),
          vpc_id = vpc.ref,
        )

    subnet2 = ec2.CfnSubnet(self, 'Subnet2',
          availability_zone = cdk.Fn.select(1, cdk.Fn.getAzs('')),
          cidr_block = cdk.Fn.select(1, cdk.Fn.cidr(vpc.attr_cidr_block, 6, str(8))),
          vpc_id = vpc.ref,
        )

    subnet3 = ec2.CfnSubnet(self, 'Subnet3',
          availability_zone = cdk.Fn.select(2, cdk.Fn.getAzs('')),
          cidr_block = cdk.Fn.select(2, cdk.Fn.cidr(vpc.attr_cidr_block, 6, str(8))),
          vpc_id = vpc.ref,
        )


