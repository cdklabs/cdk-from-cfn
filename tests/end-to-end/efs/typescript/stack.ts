import * as cdk from 'aws-cdk-lib';
import * as efs from 'aws-cdk-lib/aws-efs';

export interface EfsStackProps extends cdk.StackProps {
}

export class EfsStack extends cdk.Stack {
  public constructor(scope: cdk.App, id: string, props: EfsStackProps = {}) {
    super(scope, id, props);

    // Resources
    const fileSystem = new efs.CfnFileSystem(this, 'FileSystem', {
    });
  }
}
