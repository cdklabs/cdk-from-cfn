import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';

export interface BucketConstructProps {
}

export class BucketConstruct extends Construct {
  public constructor(scope: Construct, id: string, props: BucketConstructProps = {}) {
    super(scope, id);

    // Resources
    const bucket = new s3.CfnBucket(this, 'Bucket', {
    });
  }
}
