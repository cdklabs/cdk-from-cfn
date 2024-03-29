import * as cdk from 'aws-cdk-lib';
import * as sam from 'aws-cdk-lib/aws-sam';

export interface SAMNodeJSLambdaProps extends cdk.StackProps {
}

export class SAMNodeJSLambda extends cdk.Stack {
  public constructor(scope: cdk.App, id: string, props: SAMNodeJSLambdaProps = {}) {
    super(scope, id, props);

    // Transforms
    this.addTransform('AWS::Serverless-2016-10-31');

    // Resources
    const myFunction = new sam.CfnFunction(this, 'MyFunction', {
      runtime: 'nodejs18.x',
      handler: 'index.handler',
      inlineCode: 'exports.handler = async (event) => {\n  console.log(event);\n}\n',
    });
  }
}
