import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { Construct } from 'constructs';

export interface Ec2ConstructProps {
}

export class Ec2Construct extends Construct {
  public constructor(scope: Construct, id: string, props: Ec2ConstructProps = {}) {
    super(scope, id);

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
