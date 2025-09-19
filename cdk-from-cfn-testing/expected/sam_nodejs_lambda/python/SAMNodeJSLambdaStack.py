from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_sam as sam
from constructs import Construct

class SAMNodeJSLambdaStack(Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Transforms
    Stack.add_transform(self, 'AWS::Serverless-2016-10-31')

    # Resources
    myFunction = sam.CfnFunction(self, 'MyFunction',
          runtime = 'nodejs20.x',
          handler = 'index.handler',
          inline_code = 'exports.handler = async (event) => {\n  console.log(event);\n}\n',
        )


