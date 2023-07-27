import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';

export interface RoleStackProps extends cdk.StackProps {
}

export class RoleStack extends cdk.Stack {
  public constructor(scope: cdk.App, id: string, props: RoleStackProps = {}) {
    super(scope, id, props);

    // Resources
    const myRole = new iam.CfnRole(this, 'MyRole', {
      assumeRolePolicyDocument: {
        'Statement': [
          {
            'Action': [
              'sts:AssumeRole',
            ],
            'Condition': {
              'StringLike': {
                'kms:ViaService': `s3.us-east-1.amazonaws.com`,
              },
            },
            'Effect': 'Allow',
            'Principal': {
              'Service': [
                'lambda.amazonaws.com',
              ],
            },
          },
        ],
        'Version': '2012-10-17',
      },
    });
  }
}
