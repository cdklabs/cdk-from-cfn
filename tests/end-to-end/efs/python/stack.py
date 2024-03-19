from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_efs as efs
from constructs import Construct

class EfsStack(Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Resources
    fileSystem = efs.CfnFileSystem(self, 'FileSystem',
        )


