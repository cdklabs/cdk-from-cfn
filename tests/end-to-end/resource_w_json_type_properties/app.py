from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_iam as iam
import aws_cdk.aws_sqs as sqs
from constructs import Construct

class JsonPropsStack(Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Resources
    myQueue1 = sqs.CfnQueue(self, 'MyQueue1',
        )

    myQueue2 = sqs.CfnQueue(self, 'MyQueue2',
        )

    myRdMessageQueueGroup = iam.CfnGroup(self, 'MyRDMessageQueueGroup',
          policies = [
            {
              'policyName': 'MyQueueGroupPolicy',
              'policyDocument': {
                'statement': [
                  {
                    'effect': 'Allow',
                    'action': [
                      'sqs:DeleteMessage',
                      'sqs:ReceiveMessage',
                    ],
                    'resource': [
                      myQueue1.attrarn,
                      myQueue2.attrarn,
                    ],
                  },
                ],
              },
            },
          ],
        )


