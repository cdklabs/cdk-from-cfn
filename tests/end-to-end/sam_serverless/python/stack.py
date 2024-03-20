from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_sam as sam
from constructs import Construct

class SamServerlessStack(Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Transforms
    Stack.add_transform(self, 'AWS::Serverless-2016-10-31')

    # Resources
    clientFunction = sam.CfnFunction(self, 'ClientFunction',
          function_name = 'pricing-client',
          handler = 'client_lambda.lambda_handler',
          memory_size = 512,
          timeout = 300,
          code_uri = './pricing-client/',
          permissions_boundary = f"""arn:aws:iam::{self.account}:policy/GithubActionsIamResourcePermissionsBoundary""",
          runtime = 'python3.11',
          events = {
            'ApiEvent': {
              'type': 'Api',
              'properties': {
                'path': '/path',
                'method': 'get',
              },
            },
          },
        )


