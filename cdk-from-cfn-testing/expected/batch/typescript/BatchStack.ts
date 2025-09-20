import * as cdk from 'aws-cdk-lib';
import * as batch from 'aws-cdk-lib/aws-batch';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as iam from 'aws-cdk-lib/aws-iam';

export interface BatchStackProps extends cdk.StackProps {
}

/**
 * AWS CloudFormation Sample Template Managed Single Batch Job Queue: This template demonstrates the usage of simple Job Queue and EC2 style Compute Environment.  **WARNING** You will be billed for the AWS resources used if you create a stack from this template.
 */
export class BatchStack extends cdk.Stack {
  public readonly computeEnvironmentArn;
  public readonly jobQueueArn;
  public readonly jobDefinitionArn;

  public constructor(scope: cdk.App, id: string, props: BatchStackProps = {}) {
    super(scope, id, props);

    // Resources
    const batchServiceRole = new iam.CfnRole(this, 'BatchServiceRole', {
      assumeRolePolicyDocument: {
        Version: '2012-10-17',
        Statement: [
          {
            Effect: 'Allow',
            Principal: {
              Service: 'batch.amazonaws.com',
            },
            Action: 'sts:AssumeRole',
          },
        ],
      },
      managedPolicyArns: [
        'arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole',
      ],
    });

    const ecsInstanceRole = new iam.CfnRole(this, 'EcsInstanceRole', {
      assumeRolePolicyDocument: {
        Version: '2008-10-17',
        Statement: [
          {
            Sid: '',
            Effect: 'Allow',
            Principal: {
              Service: 'ec2.amazonaws.com',
            },
            Action: 'sts:AssumeRole',
          },
        ],
      },
      managedPolicyArns: [
        'arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role',
      ],
    });

    const internetGateway = new ec2.CfnInternetGateway(this, 'InternetGateway', {
    });

    const jobDefinition = new batch.CfnJobDefinition(this, 'JobDefinition', {
      type: 'container',
      containerProperties: {
        image: [
          '137112412989.dkr.ecr.',
          this.region,
          '.amazonaws.com/amazonlinux:latest',
        ].join(''),
        vcpus: 2,
        memory: 2000,
        command: [
          'echo',
          'Hello world',
        ],
      },
      retryStrategy: {
        attempts: 1,
      },
    });

    const vpc = new ec2.CfnVPC(this, 'VPC', {
      cidrBlock: '10.0.0.0/16',
    });

    const iamInstanceProfile = new iam.CfnInstanceProfile(this, 'IamInstanceProfile', {
      roles: [
        ecsInstanceRole.ref,
      ],
    });

    const routeTable = new ec2.CfnRouteTable(this, 'RouteTable', {
      vpcId: vpc.ref,
    });

    const securityGroup = new ec2.CfnSecurityGroup(this, 'SecurityGroup', {
      groupDescription: 'EC2 Security Group for instances launched in the VPC by Batch',
      vpcId: vpc.ref,
    });

    const subnet = new ec2.CfnSubnet(this, 'Subnet', {
      cidrBlock: '10.0.0.0/24',
      vpcId: vpc.ref,
      mapPublicIpOnLaunch: true,
    });

    const vpcGatewayAttachment = new ec2.CfnVPCGatewayAttachment(this, 'VPCGatewayAttachment', {
      vpcId: vpc.ref,
      internetGatewayId: internetGateway.ref,
    });

    const computeEnvironment = new batch.CfnComputeEnvironment(this, 'ComputeEnvironment', {
      type: 'MANAGED',
      computeResources: {
        type: 'EC2',
        minvCpus: 0,
        desiredvCpus: 0,
        maxvCpus: 64,
        instanceTypes: [
          'optimal',
        ],
        subnets: [
          subnet.ref,
        ],
        securityGroupIds: [
          securityGroup.ref,
        ],
        instanceRole: iamInstanceProfile.ref,
      },
      serviceRole: batchServiceRole.ref,
    });

    const route = new ec2.CfnRoute(this, 'Route', {
      routeTableId: routeTable.ref,
      destinationCidrBlock: '0.0.0.0/0',
      gatewayId: internetGateway.ref,
    });

    const subnetRouteTableAssociation = new ec2.CfnSubnetRouteTableAssociation(this, 'SubnetRouteTableAssociation', {
      routeTableId: routeTable.ref,
      subnetId: subnet.ref,
    });

    const jobQueue = new batch.CfnJobQueue(this, 'JobQueue', {
      priority: 1,
      computeEnvironmentOrder: [
        {
          order: 1,
          computeEnvironment: computeEnvironment.ref,
        },
      ],
    });

    // Outputs
    this.computeEnvironmentArn = computeEnvironment.ref;
    new cdk.CfnOutput(this, 'CfnOutputComputeEnvironmentArn', {
      key: 'ComputeEnvironmentArn',
      value: this.computeEnvironmentArn!.toString(),
    });
    this.jobQueueArn = jobQueue.ref;
    new cdk.CfnOutput(this, 'CfnOutputJobQueueArn', {
      key: 'JobQueueArn',
      value: this.jobQueueArn!.toString(),
    });
    this.jobDefinitionArn = jobDefinition.ref;
    new cdk.CfnOutput(this, 'CfnOutputJobDefinitionArn', {
      key: 'JobDefinitionArn',
      value: this.jobDefinitionArn!.toString(),
    });
  }
}
