from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_iam as iam
from constructs import Construct

"""
  Deploy required components for StackSet custom resources in this region.  Lambda ARN is exported as StackSetCustomResource
"""
class StackSetStack(Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Applying default props
    props = {
      'moduleName': kwargs.get('moduleName', 'lambda_function'),
      'roleName': kwargs.get('roleName', ''),
      'rolePath': kwargs.get('rolePath', ''),
    }

    # Conditions
    use_role_name = not (props['roleName'] == '')
    use_role_path = not (props['rolePath'] == '')

    # Resources
    stackSetResourceRole = iam.CfnRole(self, 'StackSetResourceRole',
          role_name = props['roleName'] if use_role_name else None,
          path = props['rolePath'] if use_role_path else '/',
          assume_role_policy_document = {
            'Version': '2012-10-17',
            'Statement': [
              {
                'Effect': 'Allow',
                'Principal': {
                  'Service': 'lambda.amazonaws.com',
                },
                'Action': 'sts:AssumeRole',
              },
            ],
          },
          policies = [
            {
              'policyName': 'IAMPassRolePermissions',
              'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                  {
                    'Effect': 'Allow',
                    'Action': 'iam:PassRole',
                    'Resource': '*',
                  },
                ],
              },
            },
            {
              'policyName': 'CloudFormationPermissions',
              'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                  {
                    'Effect': 'Allow',
                    'Action': 'cloudformation:*',
                    'Resource': '*',
                  },
                ],
              },
            },
            {
              'policyName': 'LambdaPermissions',
              'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                  {
                    'Effect': 'Allow',
                    'Action': 'logs:CreateLogGroup',
                    'Resource': [
                      f"""arn:aws:logs:{self.region}:{self.account}:*""",
                    ],
                  },
                  {
                    'Effect': 'Allow',
                    'Action': [
                      'logs:CreateLogStream',
                      'logs:PutLogEvents',
                    ],
                    'Resource': [
                      f"""arn:aws:logs:{self.region}:{self.account}:log-group:/aws/lambda/*""",
                    ],
                  },
                ],
              },
            },
            {
              'policyName': 'S3Permissions',
              'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                  {
                    'Effect': 'Allow',
                    'Action': [
                      's3:Get*',
                      's3:List*',
                    ],
                    'Resource': '*',
                  },
                ],
              },
            },
          ],
        )


