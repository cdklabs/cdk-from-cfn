from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as aws_lambda
from constructs import Construct

"""
  Test Custom Resource conversion
"""
class CustomResourceConstruct(Construct):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id)

    # Resources
    lambdaRole = iam.CfnRole(self, 'LambdaRole',
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
        )

    backingLambda = aws_lambda.CfnFunction(self, 'BackingLambda',
          runtime = 'python3.9',
          handler = 'index.handler',
          role = lambdaRole.attr_arn,
          code = {
            'zipFile': 'def handler(event, context):\n  return {\'Status\': \'SUCCESS\', \'Data\': {\'Endpoint\': \'test-endpoint\'}}\n',
          },
        )

    myCustomResource = cdk.CfnCustomResource(self, 'MyCustomResource',
      service_token = backingLambda.attr_arn,
      )
    myCustomResource.add_override('Type', 'Custom::DatabaseSetup')
    myCustomResource.add_property_override('DatabaseName', 'mydb')
    myCustomResource.add_property_override('TableCount', 5)
    myCustomResource.add_property_override('EnableLogging', 'true')
    myCustomResource.add_property_override('Tags', [
      'prod',
      'critical',
    ])
    myCustomResource.cfn_options.deletion_policy = cdk.CfnDeletionPolicy.RETAIN
    myCustomResource.add_dependency(backingLambda)

    consumerLambda = aws_lambda.CfnFunction(self, 'ConsumerLambda',
          runtime = 'python3.9',
          handler = 'index.handler',
          role = lambdaRole.attr_arn,
          code = {
            'zipFile': 'def handler(event, context):\n  pass\n',
          },
          environment = {
            'variables': {
              'DB_ENDPOINT': myCustomResource.get_att('Endpoint').to_string(),
            },
          },
        )


