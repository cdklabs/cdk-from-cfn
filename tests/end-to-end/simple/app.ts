import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Buffer } from 'buffer';

// Interfaces
export interface NoctStackProps extends cdk.StackProps {
  readonly bucketNamePrefix: string;
}

// Default parameters
// {
//   bucketNamePrefix: "bucket",
// }

// Stack
export class NoctStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props: NoctStackProps) {
    super(scope, id, props);

    // Mappings

    // Conditions

    // Resources
    const bucket = new s3.CfnBucket(this, 'Bucket', {
      bucketName: `${props.bucketNamePrefix}-${this.stackName}-bucket`
    });
    bucket.addOverride('Metadata', {
CostCenter: 1337
});

    // Outputs
    new cdk.CfnOutput(this, 'BucketArn', {
      value: bucket.attrArn
    });
  }
}
