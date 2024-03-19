import * as cdk from 'aws-cdk-lib';
import * as autoscaling from 'aws-cdk-lib/aws-autoscaling';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as efs from 'aws-cdk-lib/aws-efs';
import * as iam from 'aws-cdk-lib/aws-iam';

export interface EfsStackProps extends cdk.StackProps {
  /**
   * WebServer EC2 instance type
   * @default 't2.small'
   */
  readonly instanceType?: string;
  /**
   * Maximum size and initial desired capacity of Auto Scaling Group
   * @default '2'
   */
  readonly asgMaxSize?: string;
  /**
   * The IP address range that can be used to connect to the EC2 instances by using SSH
   * @default '0.0.0.0/0'
   */
  readonly sshLocation?: string;
  /**
   * The name to be used for the EFS volume
   * @default 'myEFSvolume'
   */
  readonly volumeName?: string;
  /**
   * The Linux mount point for the EFS volume
   * @default 'myEFSvolume'
   */
  readonly mountPoint?: string;
}

/**
 * This template creates an Amazon EFS file system and mount target and associates it with Amazon EC2 instances in an Auto Scaling group. **WARNING** This template creates Amazon EC2 instances and related resources. You will be billed for the AWS resources used if you create a stack from this template.
 */
export class EfsStack extends cdk.Stack {
  /**
   * Mount target ID
   */
  public readonly mountTargetId;
  /**
   * File system ID
   */
  public readonly fileSystemId;

  public constructor(scope: cdk.App, id: string, props: EfsStackProps = {}) {
    super(scope, id, props);

    // Applying default props
    props = {
      ...props,
      instanceType: props.instanceType ?? 't2.small',
      asgMaxSize: props.asgMaxSize ?? '2',
      sshLocation: props.sshLocation ?? '0.0.0.0/0',
      volumeName: props.volumeName ?? 'myEFSvolume',
      mountPoint: props.mountPoint ?? 'myEFSvolume',
    };

    // Mappings
    const awsInstanceType2Arch: Record<string, Record<string, string>> = {
      't1.micro': {
        'Arch': 'HVM64',
      },
      't2.nano': {
        'Arch': 'HVM64',
      },
      't2.micro': {
        'Arch': 'HVM64',
      },
      't2.small': {
        'Arch': 'HVM64',
      },
      't2.medium': {
        'Arch': 'HVM64',
      },
      't2.large': {
        'Arch': 'HVM64',
      },
      'm1.small': {
        'Arch': 'HVM64',
      },
      'm1.medium': {
        'Arch': 'HVM64',
      },
      'm1.large': {
        'Arch': 'HVM64',
      },
      'm1.xlarge': {
        'Arch': 'HVM64',
      },
      'm2.xlarge': {
        'Arch': 'HVM64',
      },
      'm2.2xlarge': {
        'Arch': 'HVM64',
      },
      'm2.4xlarge': {
        'Arch': 'HVM64',
      },
      'm3.medium': {
        'Arch': 'HVM64',
      },
      'm3.large': {
        'Arch': 'HVM64',
      },
      'm3.xlarge': {
        'Arch': 'HVM64',
      },
      'm3.2xlarge': {
        'Arch': 'HVM64',
      },
      'm4.large': {
        'Arch': 'HVM64',
      },
      'm4.xlarge': {
        'Arch': 'HVM64',
      },
      'm4.2xlarge': {
        'Arch': 'HVM64',
      },
      'm4.4xlarge': {
        'Arch': 'HVM64',
      },
      'm4.10xlarge': {
        'Arch': 'HVM64',
      },
      'c1.medium': {
        'Arch': 'HVM64',
      },
      'c1.xlarge': {
        'Arch': 'HVM64',
      },
      'c3.large': {
        'Arch': 'HVM64',
      },
      'c3.xlarge': {
        'Arch': 'HVM64',
      },
      'c3.2xlarge': {
        'Arch': 'HVM64',
      },
      'c3.4xlarge': {
        'Arch': 'HVM64',
      },
      'c3.8xlarge': {
        'Arch': 'HVM64',
      },
      'c4.large': {
        'Arch': 'HVM64',
      },
      'c4.xlarge': {
        'Arch': 'HVM64',
      },
      'c4.2xlarge': {
        'Arch': 'HVM64',
      },
      'c4.4xlarge': {
        'Arch': 'HVM64',
      },
      'c4.8xlarge': {
        'Arch': 'HVM64',
      },
      'g2.2xlarge': {
        'Arch': 'HVMG2',
      },
      'g2.8xlarge': {
        'Arch': 'HVMG2',
      },
      'r3.large': {
        'Arch': 'HVM64',
      },
      'r3.xlarge': {
        'Arch': 'HVM64',
      },
      'r3.2xlarge': {
        'Arch': 'HVM64',
      },
      'r3.4xlarge': {
        'Arch': 'HVM64',
      },
      'r3.8xlarge': {
        'Arch': 'HVM64',
      },
      'i2.xlarge': {
        'Arch': 'HVM64',
      },
      'i2.2xlarge': {
        'Arch': 'HVM64',
      },
      'i2.4xlarge': {
        'Arch': 'HVM64',
      },
      'i2.8xlarge': {
        'Arch': 'HVM64',
      },
      'd2.xlarge': {
        'Arch': 'HVM64',
      },
      'd2.2xlarge': {
        'Arch': 'HVM64',
      },
      'd2.4xlarge': {
        'Arch': 'HVM64',
      },
      'd2.8xlarge': {
        'Arch': 'HVM64',
      },
      'hi1.4xlarge': {
        'Arch': 'HVM64',
      },
      'hs1.8xlarge': {
        'Arch': 'HVM64',
      },
      'cr1.8xlarge': {
        'Arch': 'HVM64',
      },
      'cc2.8xlarge': {
        'Arch': 'HVM64',
      },
    };
    const awsRegionArch2Ami: Record<string, Record<string, string>> = {
      'us-east-1': {
        'HVM64': 'ami-0ff8a91507f77f867',
        'HVMG2': 'ami-0a584ac55a7631c0c',
      },
      'us-west-2': {
        'HVM64': 'ami-a0cfeed8',
        'HVMG2': 'ami-0e09505bc235aa82d',
      },
      'us-west-1': {
        'HVM64': 'ami-0bdb828fd58c52235',
        'HVMG2': 'ami-066ee5fd4a9ef77f1',
      },
      'eu-west-1': {
        'HVM64': 'ami-047bb4163c506cd98',
        'HVMG2': 'ami-0a7c483d527806435',
      },
      'eu-west-2': {
        'HVM64': 'ami-f976839e',
        'HVMG2': 'NOT_SUPPORTED',
      },
      'eu-west-3': {
        'HVM64': 'ami-0ebc281c20e89ba4b',
        'HVMG2': 'NOT_SUPPORTED',
      },
      'eu-central-1': {
        'HVM64': 'ami-0233214e13e500f77',
        'HVMG2': 'ami-06223d46a6d0661c7',
      },
      'ap-northeast-1': {
        'HVM64': 'ami-06cd52961ce9f0d85',
        'HVMG2': 'ami-053cdd503598e4a9d',
      },
      'ap-northeast-2': {
        'HVM64': 'ami-0a10b2721688ce9d2',
        'HVMG2': 'NOT_SUPPORTED',
      },
      'ap-northeast-3': {
        'HVM64': 'ami-0d98120a9fb693f07',
        'HVMG2': 'NOT_SUPPORTED',
      },
      'ap-southeast-1': {
        'HVM64': 'ami-08569b978cc4dfa10',
        'HVMG2': 'ami-0be9df32ae9f92309',
      },
      'ap-southeast-2': {
        'HVM64': 'ami-09b42976632b27e9b',
        'HVMG2': 'ami-0a9ce9fecc3d1daf8',
      },
      'ap-south-1': {
        'HVM64': 'ami-0912f71e06545ad88',
        'HVMG2': 'ami-097b15e89dbdcfcf4',
      },
      'us-east-2': {
        'HVM64': 'ami-0b59bfac6be064b78',
        'HVMG2': 'NOT_SUPPORTED',
      },
      'ca-central-1': {
        'HVM64': 'ami-0b18956f',
        'HVMG2': 'NOT_SUPPORTED',
      },
      'sa-east-1': {
        'HVM64': 'ami-07b14488da8ea02a0',
        'HVMG2': 'NOT_SUPPORTED',
      },
      'cn-north-1': {
        'HVM64': 'ami-0a4eaf6c4454eda75',
        'HVMG2': 'NOT_SUPPORTED',
      },
      'cn-northwest-1': {
        'HVM64': 'ami-6b6a7d09',
        'HVMG2': 'NOT_SUPPORTED',
      },
    };

    // Resources
    const cloudWatchPutMetricsRole = new iam.CfnRole(this, 'CloudWatchPutMetricsRole', {
      assumeRolePolicyDocument: {
        Statement: [
          {
            Effect: 'Allow',
            Principal: {
              Service: [
                'ec2.amazonaws.com',
              ],
            },
            Action: [
              'sts:AssumeRole',
            ],
          },
        ],
      },
      path: '/',
    });

    const fileSystem = new efs.CfnFileSystem(this, 'FileSystem', {
      performanceMode: 'generalPurpose',
      fileSystemTags: [
        {
          key: 'Name',
          value: props.volumeName!,
        },
      ],
    });

    const fileSystemNoProps = new efs.CfnFileSystem(this, 'FileSystemNoProps', {
    });

    const internetGateway = new ec2.CfnInternetGateway(this, 'InternetGateway', {
      tags: [
        {
          key: 'Application',
          value: this.stackName,
        },
        {
          key: 'Network',
          value: 'Public',
        },
      ],
    });

    const vpc = new ec2.CfnVPC(this, 'VPC', {
      enableDnsSupport: true,
      enableDnsHostnames: true,
      cidrBlock: '10.0.0.0/16',
      tags: [
        {
          key: 'Application',
          value: this.stackId,
        },
      ],
    });

    const cloudWatchPutMetricsInstanceProfile = new iam.CfnInstanceProfile(this, 'CloudWatchPutMetricsInstanceProfile', {
      path: '/',
      roles: [
        cloudWatchPutMetricsRole.ref,
      ],
    });

    const cloudWatchPutMetricsRolePolicy = new iam.CfnPolicy(this, 'CloudWatchPutMetricsRolePolicy', {
      policyName: 'CloudWatch_PutMetricData',
      policyDocument: {
        Version: '2012-10-17',
        Statement: [
          {
            Sid: 'CloudWatchPutMetricData',
            Effect: 'Allow',
            Action: [
              'cloudwatch:PutMetricData',
            ],
            Resource: [
              '*',
            ],
          },
        ],
      },
      roles: [
        cloudWatchPutMetricsRole.ref,
      ],
    });

    const gatewayToInternet = new ec2.CfnVPCGatewayAttachment(this, 'GatewayToInternet', {
      vpcId: vpc.ref,
      internetGatewayId: internetGateway.ref,
    });

    const instanceSecurityGroup = new ec2.CfnSecurityGroup(this, 'InstanceSecurityGroup', {
      vpcId: vpc.ref,
      groupDescription: 'Enable SSH access via port 22',
      securityGroupIngress: [
        {
          ipProtocol: 'tcp',
          fromPort: 22,
          toPort: 22,
          cidrIp: props.sshLocation!,
        },
        {
          ipProtocol: 'tcp',
          fromPort: 80,
          toPort: 80,
          cidrIp: '0.0.0.0/0',
        },
      ],
    });

    const mountTargetSecurityGroup = new ec2.CfnSecurityGroup(this, 'MountTargetSecurityGroup', {
      vpcId: vpc.ref,
      groupDescription: 'Security group for mount target',
      securityGroupIngress: [
        {
          ipProtocol: 'tcp',
          fromPort: 2049,
          toPort: 2049,
          cidrIp: '0.0.0.0/0',
        },
      ],
    });

    const routeTable = new ec2.CfnRouteTable(this, 'RouteTable', {
      vpcId: vpc.ref,
    });

    const subnet = new ec2.CfnSubnet(this, 'Subnet', {
      vpcId: vpc.ref,
      cidrBlock: '10.0.0.0/24',
      tags: [
        {
          key: 'Application',
          value: this.stackId,
        },
      ],
    });

    const internetGatewayRoute = new ec2.CfnRoute(this, 'InternetGatewayRoute', {
      destinationCidrBlock: '0.0.0.0/0',
      routeTableId: routeTable.ref,
      gatewayId: internetGateway.ref,
    });

    const launchConfiguration = new autoscaling.CfnLaunchConfiguration(this, 'LaunchConfiguration', {
      associatePublicIpAddress: true,
      imageId: 'ami-0ff8a91507f77f86',
      instanceType: props.instanceType!,
      securityGroups: [
        instanceSecurityGroup.ref,
      ],
      iamInstanceProfile: cloudWatchPutMetricsInstanceProfile.ref,
      userData: cdk.Fn.base64([
        '#!/bin/bash -xe\n',
        'yum install -y aws-cfn-bootstrap\n',
        '/opt/aws/bin/cfn-init -v ',
        '         --stack ',
        this.stackName,
        '         --resource LaunchConfiguration ',
        '         --configsets MountConfig ',
        '         --region ',
        this.region,
        '\n',
        'crontab /home/ec2-user/crontab\n',
        '/opt/aws/bin/cfn-signal -e $? ',
        '         --stack ',
        this.stackName,
        '         --resource AutoScalingGroup ',
        '         --region ',
        this.region,
        '\n',
      ].join('')),
    });
    launchConfiguration.cfnOptions.metadata = {
    };

    const mountTarget = new efs.CfnMountTarget(this, 'MountTarget', {
      fileSystemId: fileSystem.ref,
      subnetId: subnet.ref,
      securityGroups: [
        mountTargetSecurityGroup.ref,
      ],
    });

    const subnetRouteTableAssoc = new ec2.CfnSubnetRouteTableAssociation(this, 'SubnetRouteTableAssoc', {
      routeTableId: routeTable.ref,
      subnetId: subnet.ref,
    });

    const autoScalingGroup = new autoscaling.CfnAutoScalingGroup(this, 'AutoScalingGroup', {
      vpcZoneIdentifier: [
        subnet.ref,
      ],
      launchConfigurationName: launchConfiguration.ref,
      minSize: '1',
      maxSize: props.asgMaxSize!,
      desiredCapacity: props.asgMaxSize!,
      tags: [
        {
          key: 'Name',
          value: 'EFS FileSystem Mounted Instance',
          propagateAtLaunch: true,
        },
      ],
    });
    autoScalingGroup.addDependency(mountTarget);
    autoScalingGroup.addDependency(gatewayToInternet);

    // Outputs
    this.mountTargetId = mountTarget.ref;
    new cdk.CfnOutput(this, 'CfnOutputMountTargetID', {
      key: 'MountTargetID',
      description: 'Mount target ID',
      value: this.mountTargetId!.toString(),
    });
    this.fileSystemId = fileSystem.ref;
    new cdk.CfnOutput(this, 'CfnOutputFileSystemID', {
      key: 'FileSystemID',
      description: 'File system ID',
      value: this.fileSystemId!.toString(),
    });
  }
}
