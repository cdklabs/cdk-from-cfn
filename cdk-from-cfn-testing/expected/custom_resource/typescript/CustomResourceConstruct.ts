import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';

export interface CustomResourceConstructProps {
}

/**
 * Test Custom Resource conversion
 */
export class CustomResourceConstruct extends Construct {
  public constructor(scope: Construct, id: string, props: CustomResourceConstructProps = {}) {
    super(scope, id);

    // Resources
    const lambdaRole = new iam.CfnRole(this, 'LambdaRole', {
      assumeRolePolicyDocument: {
        Version: '2012-10-17',
        Statement: [
          {
            Effect: 'Allow',
            Principal: {
              Service: 'lambda.amazonaws.com',
            },
            Action: 'sts:AssumeRole',
          },
        ],
      },
    });

    const backingLambda = new lambda.CfnFunction(this, 'BackingLambda', {
      runtime: 'python3.9',
      handler: 'index.handler',
      role: lambdaRole.attrArn,
      code: {
        zipFile: 'def handler(event, context):\n  return {\'Status\': \'SUCCESS\', \'Data\': {\'Endpoint\': \'test-endpoint\'}}\n',
      },
    });

    const cfnCustomResource = new cdk.CfnCustomResource(this, 'CfnCustomResource', {
      serviceToken: backingLambda.attrArn,
    });
    cfnCustomResource.addPropertyOverride('Region', 'us-west-2');

    const myCustomResource = new cdk.CfnCustomResource(this, 'MyCustomResource', {
      serviceToken: backingLambda.attrArn,
    });
    myCustomResource.addOverride('Type', 'Custom::DatabaseSetup');
    myCustomResource.addPropertyOverride('DatabaseName', 'mydb');
    myCustomResource.addPropertyOverride('TableCount', 5);
    myCustomResource.addPropertyOverride('EnableLogging', 'true');
    myCustomResource.addPropertyOverride('Tags', [
      'prod',
      'critical',
    ]);
    myCustomResource.cfnOptions.deletionPolicy = cdk.CfnDeletionPolicy.RETAIN;
    myCustomResource.addDependency(backingLambda);

    const consumerLambda = new lambda.CfnFunction(this, 'ConsumerLambda', {
      runtime: 'python3.9',
      handler: 'index.handler',
      role: lambdaRole.attrArn,
      code: {
        zipFile: 'def handler(event, context):\n  pass\n',
      },
      environment: {
        variables: {
          'DB_ENDPOINT': myCustomResource.getAtt('Endpoint').toString(),
          'CFN_RESULT': cfnCustomResource.getAtt('Result').toString(),
        },
      },
    });
  }
}
