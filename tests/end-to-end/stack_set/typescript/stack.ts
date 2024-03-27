import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';

export interface StackSetStackProps extends cdk.StackProps {
  /**
   * @default 'lambda_function'
   */
  readonly moduleName?: string;
  /**
   * @default ''
   */
  readonly roleName?: string;
  /**
   * @default ''
   */
  readonly rolePath?: string;
}

/**
 * Deploy required components for StackSet custom resources in this region.  Lambda ARN is exported as StackSetCustomResource
 */
export class StackSetStack extends cdk.Stack {
  public constructor(scope: cdk.App, id: string, props: StackSetStackProps = {}) {
    super(scope, id, props);

    // Applying default props
    props = {
      ...props,
      moduleName: props.moduleName ?? 'lambda_function',
      roleName: props.roleName ?? '',
      rolePath: props.rolePath ?? '',
    };

    // Conditions
    const useRoleName = !(props.roleName! === '');
    const useRolePath = !(props.rolePath! === '');

    // Resources
    const stackSetResourceRole = new iam.CfnRole(this, 'StackSetResourceRole', {
      roleName: useRoleName ? props.roleName! : undefined,
      path: useRolePath ? props.rolePath! : '/',
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
      policies: [
        {
          policyName: 'IAMPassRolePermissions',
          policyDocument: {
            Version: '2012-10-17',
            Statement: [
              {
                Effect: 'Allow',
                Action: 'iam:PassRole',
                Resource: '*',
              },
            ],
          },
        },
        {
          policyName: 'CloudFormationPermissions',
          policyDocument: {
            Version: '2012-10-17',
            Statement: [
              {
                Effect: 'Allow',
                Action: 'cloudformation:*',
                Resource: '*',
              },
            ],
          },
        },
        {
          policyName: 'LambdaPermissions',
          policyDocument: {
            Version: '2012-10-17',
            Statement: [
              {
                Effect: 'Allow',
                Action: 'logs:CreateLogGroup',
                Resource: [
                  `arn:aws:logs:${this.region}:${this.account}:*`,
                ],
              },
              {
                Effect: 'Allow',
                Action: [
                  'logs:CreateLogStream',
                  'logs:PutLogEvents',
                ],
                Resource: [
                  `arn:aws:logs:${this.region}:${this.account}:log-group:/aws/lambda/*`,
                ],
              },
            ],
          },
        },
        {
          policyName: 'S3Permissions',
          policyDocument: {
            Version: '2012-10-17',
            Statement: [
              {
                Effect: 'Allow',
                Action: [
                  's3:Get*',
                  's3:List*',
                ],
                Resource: '*',
              },
            ],
          },
        },
      ],
    });
  }
}
