import * as cdk from 'aws-cdk-lib';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as s3 from 'aws-cdk-lib/aws-s3';
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
        'true': true
      },
      'False': {
        'false': false
      }
    };
    const lists: Record<string, Record<string, readonly string[]>> = {
      'Candidates': {
        'Empty': [],
        'Singleton': ['One'],
        'Pair': ['One','Two']
      }
    };
    const numbers: Record<string, Record<string, number>> = {
      'Prime': {
        'Eleven': 11,
        'Thirteen': 13,
        'Seventeen': 17
      }
    };
    const strings: Record<string, Record<string, string>> = {
      'Foos': {
        'Foo1': 'Foo1',
        'Foo2': 'Foo2'
      },
      'Bars': {
        'Bar': 'Bar'
      }
    };
    const table: Record<string, Record<string, any>> = {
      'Values': {
        'Boolean': true,
        'Float': 3.14,
        'List': ['1','2','3'],
        'Number': 42,
        'String': 'Baz'
      }
    };

    // Conditions
    const isUsEast1 = this.region === 'us-east-1';

    // Resources
    const queue = new sqs.CfnQueue(this, 'Queue', {
      queueName: [this.stackName, strings['Bars']['Bar'], cdk.Fn.select(1, cdk.Fn.getAzs(this.region))].join('-'),
    });
    let bucket;
    if (isUsEast1) {
if (queue === undefined) { throw new Error(`A combination of conditions caused 'queue' to be undefined. Fixit.`); }
    bucket = new s3.CfnBucket(this, 'Bucket', {
      bucketName: `${props.bucketNamePrefix}-${this.stackName}-bucket`,
    });
    bucket.addOverride('Metadata', {
CostCenter: 1337
});
bucket.addOverride('DeletionPolicy', 'Retain');
bucket.addOverride('DependsOn', [
'Queue'
]);
}

    // Outputs
    if (isUsEast1) {
    new cdk.CfnOutput(this, 'BucketArn', {
      value: bucket.attrArn
    });
}
  }
}
