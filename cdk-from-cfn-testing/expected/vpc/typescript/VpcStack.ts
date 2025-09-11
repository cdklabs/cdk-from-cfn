import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

export interface VpcStackProps extends cdk.StackProps {
}

export class VpcStack extends cdk.Stack {
  public constructor(scope: cdk.App, id: string, props: VpcStackProps = {}) {
    super(scope, id, props);

    // Resources
    const vpc = new ec2.CfnVPC(this, 'VPC', {
      cidrBlock: '10.42.0.0/16',
      enableDnsSupport: true,
      enableDnsHostnames: true,
      tags: [
        {
          key: 'cost-center',
          value: '1337',
        },
      ],
    });

    const subnet1 = new ec2.CfnSubnet(this, 'Subnet1', {
      availabilityZone: cdk.Fn.select(0, cdk.Fn.getAzs('')),
      cidrBlock: cdk.Fn.select(0, cdk.Fn.cidr(vpc.attrCidrBlock, 6, String(8))),
      vpcId: vpc.ref,
    });

    const subnet2 = new ec2.CfnSubnet(this, 'Subnet2', {
      availabilityZone: cdk.Fn.select(1, cdk.Fn.getAzs('')),
      cidrBlock: cdk.Fn.select(1, cdk.Fn.cidr(vpc.attrCidrBlock, 6, String(8))),
      vpcId: vpc.ref,
    });

    const subnet3 = new ec2.CfnSubnet(this, 'Subnet3', {
      availabilityZone: cdk.Fn.select(2, cdk.Fn.getAzs('')),
      cidrBlock: cdk.Fn.select(2, cdk.Fn.cidr(vpc.attrCidrBlock, 6, String(8))),
      vpcId: vpc.ref,
    });
  }
}
