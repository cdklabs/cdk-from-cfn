import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';

export interface BucketStackProps extends cdk.StackProps {
}

export class BucketStack extends cdk.Stack {
  public constructor(scope: cdk.App, id: string, props: BucketStackProps = {}) {
    super(scope, id, props);

    // Resources
    const bucket = new s3.CfnBucket(this, 'Bucket', {
    });
  }
}
