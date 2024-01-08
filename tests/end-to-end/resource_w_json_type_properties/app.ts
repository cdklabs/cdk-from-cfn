import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as sqs from 'aws-cdk-lib/aws-sqs';

export interface JsonPropsStackProps extends cdk.StackProps {
}

export class JsonPropsStack extends cdk.Stack {
  public constructor(scope: cdk.App, id: string, props: JsonPropsStackProps = {}) {
    super(scope, id, props);

    // Resources
    const myQueue1 = new sqs.CfnQueue(this, 'MyQueue1', {
    });

    const myQueue2 = new sqs.CfnQueue(this, 'MyQueue2', {
    });

    const myRdMessageQueueGroup = new iam.CfnGroup(this, 'MyRDMessageQueueGroup', {
      policies: [
        {
          policyName: 'MyQueueGroupPolicy',
          policyDocument: {
            Statement: [
              {
                Effect: 'Allow',
                Action: [
                  'sqs:DeleteMessage',
                  'sqs:ReceiveMessage',
                ],
                Resource: [
                  myQueue1.attrArn,
                  myQueue2.attrArn,
                ],
              },
            ],
          },
        },
      ],
    });
  }
}
