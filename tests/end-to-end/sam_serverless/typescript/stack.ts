import * as cdk from 'aws-cdk-lib';
import * as sam from 'aws-cdk-lib/aws-sam';

export interface SamServerlessStackProps extends cdk.StackProps {
}

export class SamServerlessStack extends cdk.Stack {
  public constructor(scope: cdk.App, id: string, props: SamServerlessStackProps = {}) {
    super(scope, id, props);

    // Transforms
    this.addTransform('AWS::Serverless-2016-10-31');

    // Resources
    const clientFunction = new sam.CfnFunction(this, 'ClientFunction', {
      functionName: 'pricing-client',
      handler: 'client_lambda.lambda_handler',
      memorySize: 512,
      timeout: 300,
      codeUri: './pricing-client/',
      permissionsBoundary: `arn:aws:iam::${this.account}:policy/GithubActionsIamResourcePermissionsBoundary`,
      runtime: 'python3.11',
      events: {
        ApiEvent: {
          type: 'Api',
          properties: {
            path: '/path',
            method: 'get',
          },
        },
      },
    });
  }
}
