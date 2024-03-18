from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from constructs import Construct

class Ec2Stack(Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Resources
    testVpc = ec2.CfnVPC(self, 'TestVPC',
          cidr_block = '10.0.0.0/16',
        )

    sg1 = ec2.CfnSecurityGroup(self, 'SG1',
          group_description = 'SG2',
          vpc_id = testVpc.ref,
          security_group_egress = [
            {
              'ipProtocol': 'TCP',
              'fromPort': 10000,
              'toPort': 10000,
              'cidrIp': '10.0.0.0/16',
            },
          ],
        )


