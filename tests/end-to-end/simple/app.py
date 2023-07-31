from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_sqs as sqs
from constructs import Construct
import Buffer as _buffer

"""
  An example stack that uses many of the syntax elements permitted in a
  CloudFormation template, but does not attempt to represent a realistic stack.
"""
class SimpleStack(Stack):
  """
    The ARN of the bucket in this template!
  """
  global bucket_arn
  """
    The ARN of the SQS Queue
  """
  global queue_arn
  """
    Whether this is a large region or not
  """
  global is_large

  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Mappings
    booleans = {
      'True': {
        'true': True,
      },
      'False': {
        'false': False,
      },
    }
    lists = {
      'Candidates': {
        'Empty': [],
        'Singleton': ['One'],
        'Pair': ['One','Two'],
      },
    }
    numbers = {
      'Prime': {
        'Eleven': 11,
        'Thirteen': 13,
        'Seventeen': 17,
      },
    }
    strings = {
      'Foos': {
        'Foo1': 'Foo1',
        'Foo2': 'Foo2',
      },
      'Bars': {
        'Bar': 'Bar',
      },
    }
    table = {
      'Values': {
        'Boolean': True,
        'Float': 3.14,
        'List': ['1','2','3'],
        'Number': 42,
        'String': 'Baz',
      },
    }

    # Conditions
    is_us = cdk.Fn.select(0, self.region.split('-')) == 'us'
    is_us_east1 = self.region == 'us-east-1'
    is_large_region = is_us_east1

    # Resources
    queue = sqs.CfnQueue(self, 'Queue',
          delay_seconds = 42.1337,
          fifo_queue = False,
          kms_master_key_id = cdk.Fn.importValue('Shared.KmsKeyArn'),
          queue_name = [
            self.stackName,
            strings['Bars']['Bar'],
            cdk.Fn.select(1, cdk.Fn.getAzs(self.region)),
          ].join('-'),
          redrive_policy = None,
          visibility_timeout = 120,
        )

    if (queue is None): raise Exception("A combination of conditions caused 'queue' to be None. Fixit.")
    bucket = s3.CfnBucket(self, 'Bucket',
          access_control = 'private',
          bucket_name = '{props.bucketNamePrefix}-{self.stackName}-bucket',
          logging_configuration = {
            'destinationBucketName': props.logDestinationBucketName,
          },
          website_configuration = {
            'indexDocument': 'index.html',
            'errorDocument': 'error.html',
            'redirectAllRequestsTo': {
              'hostName': 'example.com',
              'protocol': 'https',
            },
          },
          tags = [
            {
              'key': 'FancyTag',
              'value': cdk.Fn.base64(table['Values']['String']) if is_us_east1 else _buffer.from('8CiMvAo=', 'base64').toString('binary'),
            },
          ],
        ) if is_us_east1 else None
    if (bucket is not None):
      bucket.cfnOptions.metadata = {
        CostCenter: 1337,
      }
      bucket.cfnOptions.deletionPolicy = cdk.CfnDeletionPolicy.RETAIN
      bucket.addDependency(queue)

    # Outputs
    self.bucket_arn = bucket.attrarn if is_us_east1 else None
    if (is_us_east1):
      cdk.CfnOutput(self, 'BucketArn', 
        description = 'The ARN of the bucket in this template!',
        export_name = 'ExportName',
        value = self.bucket_arn,
      )

    self.queue_arn = queue.ref
    self.is_large = True if is_large_region else False


