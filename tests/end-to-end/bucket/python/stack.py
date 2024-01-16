from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_s3 as s3
from constructs import Construct

class BucketStack(Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Resources
    bucket = s3.CfnBucket(self, 'Bucket',
        )


