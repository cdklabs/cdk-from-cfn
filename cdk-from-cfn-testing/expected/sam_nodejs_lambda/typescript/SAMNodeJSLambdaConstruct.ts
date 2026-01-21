import * as cdk from 'aws-cdk-lib';
import * as sam from 'aws-cdk-lib/aws-sam';
import { Construct } from 'constructs';

export interface SAMNodeJSLambdaConstructProps {
}

export class SAMNodeJSLambdaConstruct extends Construct {
  public constructor(scope: Construct, id: string, props: SAMNodeJSLambdaConstructProps = {}) {
    super(scope, id);

    // Transforms
    cdk.Stack.of(this).addTransform('AWS::Serverless-2016-10-31');

    // Resources
    const myFunction = new sam.CfnFunction(this, 'MyFunction', {
      runtime: 'nodejs20.x',
      handler: 'index.handler',
      inlineCode: 'exports.handler = async (event) => {\n  console.log(event);\n}\n',
    });
  }
}
