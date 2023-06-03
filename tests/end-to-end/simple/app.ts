import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import { Buffer } from 'buffer';

export interface NoctStackProps extends cdk.StackProps {
  /**
   * The prefix for the bucket name
   * @default "bucket"
   */
  readonly bucketNamePrefix?: string;
}

/**
 * An example stack that uses many of the syntax elements permitted in a
 * CloudFormation template, but does not attempt to represent a realistic stack.
 */
export class NoctStack extends cdk.Stack {
  /**
   * The ARN of the bucket in this template!
   */
  public readonly bucketArn?;
  /**
   * The ARN of the SQS Queue
   */
  public readonly queueArn;

  public constructor(scope: cdk.App, id: string, props: NoctStackProps = {}) {
    super(scope, id, props);

    // Applying default props
    props = {
      ...props,
      bucketNamePrefix: props.bucketNamePrefix ?? "bucket",
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

    // Resources
    const queue = new sqs.CfnQueue(this, 'Queue', {
      delaySeconds: 42.1337,
      fifoQueue: false,
      kmsMasterKeyId: cdk.Fn.importValue('Shared.KmsKeyArn'),
      queueName: [
        this.stackName,
        strings['Bars']['Bar'],
        cdk.Fn.select(1, cdk.Fn.getAzs(this.region)),
      ].join('-'),
      redrivePolicy: undefined,
      visibilityTimeout: 120,
    });

    if (queue == null) { throw new Error(`A combination of conditions caused 'queue' to be undefined. Fixit.`); }
    const bucket = isUsEast1
      ? new s3.CfnBucket(this, 'Bucket', {
          accessControl: 'private',
          bucketName: `${props.bucketNamePrefix}-${this.stackName}-bucket`,
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
      bucket.cfnOptions.deletionPolicy = cdk.CfnDeletionPolicy.RETAIN;
      bucket.addDependency(queue);
    }

    // Outputs
    this.bucketArn = isUsEast1
      ? bucket?.attrArn
      : undefined;
    if (isUsEast1) {
      new cdk.CfnOutput(this, 'BucketArn', {
        description: 'The ARN of the bucket in this template!',
        exportName: 'ExportName',
        value: this.bucketArn,
      });
    }
    this.queueArn = queue.ref;
  }
}
