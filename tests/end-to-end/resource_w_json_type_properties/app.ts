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

    if (myQueue1 == null) { throw new Error(`A combination of conditions caused 'myQueue1' to be undefined. Fixit.`); }
    if (myQueue2 == null) { throw new Error(`A combination of conditions caused 'myQueue2' to be undefined. Fixit.`); }
    const myRdMessageQueueGroup = new iam.CfnGroup(this, 'MyRDMessageQueueGroup', {
      policies: [
        {
          policyName: 'MyQueueGroupPolicy',
          policyDocument: {
            statement: [
              {
                effect: 'Allow',
                action: [
                  'sqs:DeleteMessage',
                  'sqs:ReceiveMessage',
                ],
                resource: [
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
