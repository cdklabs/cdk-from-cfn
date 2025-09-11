import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import { Buffer } from 'buffer';

export interface SimpleStackProps extends cdk.StackProps {
  /**
   * The prefix for the bucket name
   * @default 'bucket'
   */
  readonly bucketNamePrefix?: string;
  /**
   * @default '/logging/bucket/name'
   */
  readonly logDestinationBucketName?: string;
}

/**
 * An example stack that uses many of the syntax elements permitted in a
 * CloudFormation template, but does not attempt to represent a realistic stack.
 */
export class SimpleStack extends cdk.Stack {
  /**
   * The ARN of the bucket in this template!
   */
  public readonly bucketArn?;
  /**
   * The ARN of the SQS Queue
   */
  public readonly queueArn;
  /**
   * Whether this is a large region or not
   */
  public readonly isLarge;

  public constructor(scope: cdk.App, id: string, props: SimpleStackProps = {}) {
    super(scope, id, props);

    // Applying default props
    props = {
      ...props,
      bucketNamePrefix: props.bucketNamePrefix ?? 'bucket',
      logDestinationBucketName: new cdk.CfnParameter(this, 'LogDestinationBucketName', {
        type: 'AWS::SSM::Parameter::Value<String>',
        default: props.logDestinationBucketName?.toString() ?? '/logging/bucket/name',
      }).valueAsString,
    };

    // Mappings
    const booleans: Record<string, Record<string, boolean>> = {
      'True': {
        'true': true,
      },
      'False': {
        'false': false,
      },
    };
    const lists: Record<string, Record<string, readonly string[]>> = {
      'Candidates': {
        'Empty': [],
        'Singleton': ['One'],
        'Pair': ['One','Two'],
      },
    };
    const numbers: Record<string, Record<string, number>> = {
      'Prime': {
        'Eleven': 11,
        'Thirteen': 13,
        'Seventeen': 17,
      },
    };
    const strings: Record<string, Record<string, string>> = {
      'Foos': {
        'Foo1': 'Foo1',
        'Foo2': 'Foo2',
      },
      'Bars': {
        'Bar': 'Bar',
      },
    };
    const table: Record<string, Record<string, any>> = {
      'Values': {
        'Boolean': true,
        'Float': 3.14,
        'List': ['1','2','3'],
        'Number': 42,
        'String': 'Baz',
      },
    };

    // Conditions
    const isUs = cdk.Fn.select(0, this.region.split('-')) === 'us';
    const isUsEast1 = this.region === 'us-east-1';
    const isLargeRegion = isUsEast1;

    // Resources
    const queue = new sqs.CfnQueue(this, 'Queue', {
      delaySeconds: 42,
      sqsManagedSseEnabled: false,
      kmsMasterKeyId: cdk.Fn.importValue('Shared-KmsKeyArn'),
      queueName: [
        this.stackName,
        strings['Bars']['Bar'],
        cdk.Fn.select(1, cdk.Fn.getAzs(this.region)),
      ].join('-'),
      redrivePolicy: undefined,
      visibilityTimeout: 120,
    });
    queue.cfnOptions.deletionPolicy = cdk.CfnDeletionPolicy.RETAIN_EXCEPT_ON_CREATE;

    const bucket = isUsEast1
      ? new s3.CfnBucket(this, 'Bucket', {
          accessControl: 'Private',
          bucketName: `${props.bucketNamePrefix!}-${this.region}-bucket`,
          loggingConfiguration: {
            destinationBucketName: props.logDestinationBucketName!,
          },
          websiteConfiguration: {
            redirectAllRequestsTo: {
              hostName: 'example.com',
              protocol: 'https',
            },
          },
          tags: [
            {
              key: 'FancyTag',
              value: isUsEast1 ? cdk.Fn.base64(table['Values']['String']) : Buffer.from('8CiMvAo=', 'base64').toString('binary'),
            },
          ],
        })
      : undefined;
    if (bucket != null) {
      bucket.cfnOptions.metadata = {
        CostCenter: 1337,
      };
      bucket.cfnOptions.deletionPolicy = cdk.CfnDeletionPolicy.DELETE;
      bucket.addDependency(queue);
    }

    // Outputs
    this.bucketArn = isUsEast1
      ? bucket?.attrArn
      : undefined;
    if (isUsEast1) {
      new cdk.CfnOutput(this, 'CfnOutputBucketArn', {
        key: 'BucketArn',
        description: 'The ARN of the bucket in this template!',
        exportName: 'ExportName',
        value: this.bucketArn!.toString(),
      });
    }
    this.queueArn = queue.ref;
    new cdk.CfnOutput(this, 'CfnOutputQueueArn', {
      key: 'QueueArn',
      description: 'The ARN of the SQS Queue',
      value: this.queueArn!.toString(),
    });
    this.isLarge = isLargeRegion ? true : false;
    new cdk.CfnOutput(this, 'CfnOutputIsLarge', {
      key: 'IsLarge',
      description: 'Whether this is a large region or not',
      value: this.isLarge!.toString(),
    });
  }
}
