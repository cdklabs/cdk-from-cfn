from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_iam as iam
import aws_cdk.aws_sqs as sqs
from constructs import Construct

class JsonPropsConstruct(Construct):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id)

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
                'Statement': [
                  {
                    'Effect': 'Allow',
                    'Action': [
                      'sqs:DeleteMessage',
                      'sqs:ReceiveMessage',
                    ],
                    'Resource': [
                      myQueue1.attr_arn,
                      myQueue2.attr_arn,
                    ],
                  },
                ],
              },
            },
          ],
        )


