import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { Buffer } from 'buffer';

export interface NoctStackProps extends cdk.StackProps {
}

export class NoctStack extends cdk.Stack {
  public constructor(scope: cdk.App, id: string, props: NoctStackProps = {}) {
    super(scope, id, props);

    // Resources
    const vpc = new ec2.CfnVPC(this, 'VPC', {
      cidrBlock: '10.42.0.0/16',
      enableDnsSupport: true,
      enableDnsHostnames: true,
      tags: [
        {
          key: 'cost-center',
          value: 1337,
        },
      ],
    });

    if (vpc == null) { throw new Error(`A combination of conditions caused 'vpc' to be undefined. Fixit.`); }
    const subnet1 = new ec2.CfnSubnet(this, 'Subnet1', {
      availabilityZone: cdk.Fn.select(0, cdk.Fn.getAzs('')),
      cidrBlock: cdk.Fn.select(0, cdk.Fn.cidr(vpc.attrCidrBlock, 6, String(8))),
      vpcId: vpc.ref,
    });

    if (vpc == null) { throw new Error(`A combination of conditions caused 'vpc' to be undefined. Fixit.`); }
    const subnet2 = new ec2.CfnSubnet(this, 'Subnet2', {
      availabilityZone: cdk.Fn.select(1, cdk.Fn.getAzs('')),
      cidrBlock: cdk.Fn.select(1, cdk.Fn.cidr(vpc.attrCidrBlock, 6, String(8))),
      vpcId: vpc.ref,
    });

    if (vpc == null) { throw new Error(`A combination of conditions caused 'vpc' to be undefined. Fixit.`); }
    const subnet3 = new ec2.CfnSubnet(this, 'Subnet3', {
      availabilityZone: cdk.Fn.select(2, cdk.Fn.getAzs('')),
      cidrBlock: cdk.Fn.select(2, cdk.Fn.cidr(vpc.attrCidrBlock, 6, String(8))),
      vpcId: vpc.ref,
    });
  }
}
