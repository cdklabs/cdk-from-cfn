import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import { Construct } from 'constructs';

export interface JsonPropsConstructProps {
}

export class JsonPropsConstruct extends Construct {
  public constructor(scope: Construct, id: string, props: JsonPropsConstructProps = {}) {
    super(scope, id);

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
