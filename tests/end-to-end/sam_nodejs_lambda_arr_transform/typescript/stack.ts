import * as cdk from 'aws-cdk-lib';
import * as sam from 'aws-cdk-lib/aws-sam';

export interface SAMNodeJSLambdaArrProps extends cdk.StackProps {
}

export class SAMNodeJSLambdaArr extends cdk.Stack {
  public constructor(scope: cdk.App, id: string, props: SAMNodeJSLambdaArrProps = {}) {
    super(scope, id, props);

    // Transforms
    this.addTransform('AWS::Serverless-2016-10-31');

    // Resources
    const myFunction = new sam.CfnFunction(this, 'MyFunction', {
      runtime: 'nodejs20.x',
      handler: 'index.handler',
      inlineCode: 'exports.handler = async (event) => {\n  console.log(event);\n}\n',
    });
  }
}
