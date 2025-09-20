import * as cdk from 'aws-cdk-lib';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as iam from 'aws-cdk-lib/aws-iam';

export interface EcsStackProps extends cdk.StackProps {
}

export class EcsStack extends cdk.Stack {
  public constructor(scope: cdk.App, id: string, props: EcsStackProps = {}) {
    super(scope, id, props);

    // Resources
    const backendEcsTaskRole = new iam.CfnRole(this, 'BackendECSTaskRole', {
      path: '/',
      assumeRolePolicyDocument: {
        Statement: [
          {
            Action: 'sts:AssumeRole',
            Effect: 'Allow',
            Principal: {
              Service: 'ecs-tasks.amazonaws.com',
            },
          },
        ],
      },
    });

    const ecsTaskExecutionRole = new iam.CfnRole(this, 'ECSTaskExecutionRole', {
      path: '/',
      assumeRolePolicyDocument: {
        Statement: [
          {
            Action: 'sts:AssumeRole',
            Effect: 'Allow',
            Principal: {
              Service: 'ecs-tasks.amazonaws.com',
            },
          },
        ],
      },
      managedPolicyArns: [
        'arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy',
        'arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess',
        'arn:aws:iam::aws:policy/SecretsManagerReadWrite',
      ],
    });

    const backendServiceEcsTaskDefinition = new ecs.CfnTaskDefinition(this, 'BackendServiceECSTaskDefinition', {
      family: 'test',
      requiresCompatibilities: [
        'FARGATE',
      ],
      memory: '1024',
      cpu: '256',
      networkMode: 'awsvpc',
      executionRoleArn: ecsTaskExecutionRole.attrArn,
      taskRoleArn: backendEcsTaskRole.attrArn,
      containerDefinitions: [
        {
          name: 'main',
          image: 'nginx',
          logConfiguration: {
            options: {
              'awslogs-group': '/aws/ecs/test/main',
              'awslogs-region': 'ap-northeast-1',
              'awslogs-stream-prefix': 'ecs',
            },
            logDriver: 'awslogs',
          },
        },
      ],
    });
  }
}
