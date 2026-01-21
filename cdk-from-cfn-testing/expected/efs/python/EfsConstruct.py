from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_efs as efs
import aws_cdk.aws_iam as iam
from constructs import Construct

"""
  This template creates an Amazon EFS file system and mount target and associates it with Amazon EC2 instances in an Auto Scaling group. **WARNING** This template creates Amazon EC2 instances and related resources. You will be billed for the AWS resources used if you create a stack from this template.
"""
class EfsConstruct(Construct):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id)

    # Applying default props
    props = {
      'instanceType': kwargs.get('instanceType', 't2.small'),
      'asgMaxSize': kwargs.get('asgMaxSize', '2'),
      'sshLocation': kwargs.get('sshLocation', '0.0.0.0/0'),
      'volumeName': kwargs.get('volumeName', 'myEFSvolume'),
      'mountPoint': kwargs.get('mountPoint', 'myEFSvolume'),
    }

    # Mappings
    awsInstanceType2Arch = {
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
    }
    awsRegionArch2Ami = {
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
    }

    # Resources
    cloudWatchPutMetricsRole = iam.CfnRole(self, 'CloudWatchPutMetricsRole',
          assume_role_policy_document = {
            'Statement': [
              {
                'Effect': 'Allow',
                'Principal': {
                  'Service': [
                    'ec2.amazonaws.com',
                  ],
                },
                'Action': [
                  'sts:AssumeRole',
                ],
              },
            ],
          },
          path = '/',
        )

    fileSystem = efs.CfnFileSystem(self, 'FileSystem',
          performance_mode = 'generalPurpose',
          file_system_tags = [
            {
              'key': 'Name',
              'value': props['volumeName'],
            },
          ],
        )

    internetGateway = ec2.CfnInternetGateway(self, 'InternetGateway',
          tags = [
            {
              'key': 'Application',
              'value': Stack.of(self).stack_name,
            },
            {
              'key': 'Network',
              'value': 'Public',
            },
          ],
        )

    vpc = ec2.CfnVPC(self, 'VPC',
          enable_dns_support = True,
          enable_dns_hostnames = True,
          cidr_block = '10.0.0.0/16',
          tags = [
            {
              'key': 'Application',
              'value': Stack.of(self).stack_id,
            },
          ],
        )

    cloudWatchPutMetricsInstanceProfile = iam.CfnInstanceProfile(self, 'CloudWatchPutMetricsInstanceProfile',
          path = '/',
          roles = [
            cloudWatchPutMetricsRole.ref,
          ],
        )

    cloudWatchPutMetricsRolePolicy = iam.CfnPolicy(self, 'CloudWatchPutMetricsRolePolicy',
          policy_name = 'CloudWatch_PutMetricData',
          policy_document = {
            'Version': '2012-10-17',
            'Statement': [
              {
                'Sid': 'CloudWatchPutMetricData',
                'Effect': 'Allow',
                'Action': [
                  'cloudwatch:PutMetricData',
                ],
                'Resource': [
                  '*',
                ],
              },
            ],
          },
          roles = [
            cloudWatchPutMetricsRole.ref,
          ],
        )

    gatewayToInternet = ec2.CfnVPCGatewayAttachment(self, 'GatewayToInternet',
          vpc_id = vpc.ref,
          internet_gateway_id = internetGateway.ref,
        )

    instanceSecurityGroup = ec2.CfnSecurityGroup(self, 'InstanceSecurityGroup',
          vpc_id = vpc.ref,
          group_description = 'Enable SSH access via port 22',
          security_group_ingress = [
            {
              'ipProtocol': 'tcp',
              'fromPort': 22,
              'toPort': 22,
              'cidrIp': props['sshLocation'],
            },
            {
              'ipProtocol': 'tcp',
              'fromPort': 80,
              'toPort': 80,
              'cidrIp': '0.0.0.0/0',
            },
          ],
        )

    mountTargetSecurityGroup = ec2.CfnSecurityGroup(self, 'MountTargetSecurityGroup',
          vpc_id = vpc.ref,
          group_description = 'Security group for mount target',
          security_group_ingress = [
            {
              'ipProtocol': 'tcp',
              'fromPort': 2049,
              'toPort': 2049,
              'cidrIp': '0.0.0.0/0',
            },
          ],
        )

    routeTable = ec2.CfnRouteTable(self, 'RouteTable',
          vpc_id = vpc.ref,
        )

    subnet = ec2.CfnSubnet(self, 'Subnet',
          vpc_id = vpc.ref,
          cidr_block = '10.0.0.0/24',
          tags = [
            {
              'key': 'Application',
              'value': Stack.of(self).stack_id,
            },
          ],
        )

    internetGatewayRoute = ec2.CfnRoute(self, 'InternetGatewayRoute',
          destination_cidr_block = '0.0.0.0/0',
          route_table_id = routeTable.ref,
          gateway_id = internetGateway.ref,
        )

    mountTarget = efs.CfnMountTarget(self, 'MountTarget',
          file_system_id = fileSystem.ref,
          subnet_id = subnet.ref,
          security_groups = [
            mountTargetSecurityGroup.ref,
          ],
        )

    subnetRouteTableAssoc = ec2.CfnSubnetRouteTableAssociation(self, 'SubnetRouteTableAssoc',
          route_table_id = routeTable.ref,
          subnet_id = subnet.ref,
        )

    # Outputs
    """
      Mount target ID
    """
    self.mount_target_id = mountTarget.ref
    cdk.CfnOutput(self, 'CfnOutputMountTargetID', 
      key = 'MountTargetID',
      description = 'Mount target ID',
      value = str(self.mount_target_id),
    )

    """
      File system ID
    """
    self.file_system_id = fileSystem.ref
    cdk.CfnOutput(self, 'CfnOutputFileSystemID', 
      key = 'FileSystemID',
      description = 'File system ID',
      value = str(self.file_system_id),
    )



