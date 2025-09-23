import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

export interface Ec2StackProps extends cdk.StackProps {
}

export class Ec2Stack extends cdk.Stack {
  public constructor(scope: cdk.App, id: string, props: Ec2StackProps = {}) {
    super(scope, id, props);

    // Resources
    const testVpc = new ec2.CfnVPC(this, 'TestVPC', {
      cidrBlock: '10.0.0.0/16',
    });

    const sg1 = new ec2.CfnSecurityGroup(this, 'SG1', {
      groupDescription: 'SG2',
      vpcId: testVpc.ref,
      securityGroupEgress: [
        {
          ipProtocol: 'TCP',
          fromPort: 10000,
          toPort: 10000,
          cidrIp: '10.0.0.0/16',
        },
      ],
    });
  }
}
