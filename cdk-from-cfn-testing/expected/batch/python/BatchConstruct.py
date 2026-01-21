from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_batch as batch
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam
from constructs import Construct

"""
  AWS CloudFormation Sample Template Managed Single Batch Job Queue: This template demonstrates the usage of simple Job Queue and EC2 style Compute Environment.  **WARNING** You will be billed for the AWS resources used if you create a stack from this template.
"""
class BatchConstruct(Construct):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id)

    # Resources
    batchServiceRole = iam.CfnRole(self, 'BatchServiceRole',
          assume_role_policy_document = {
            'Version': '2012-10-17',
            'Statement': [
              {
                'Effect': 'Allow',
                'Principal': {
                  'Service': 'batch.amazonaws.com',
                },
                'Action': 'sts:AssumeRole',
              },
            ],
          },
          managed_policy_arns = [
            'arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole',
          ],
        )

    ecsInstanceRole = iam.CfnRole(self, 'EcsInstanceRole',
          assume_role_policy_document = {
            'Version': '2008-10-17',
            'Statement': [
              {
                'Sid': '',
                'Effect': 'Allow',
                'Principal': {
                  'Service': 'ec2.amazonaws.com',
                },
                'Action': 'sts:AssumeRole',
              },
            ],
          },
          managed_policy_arns = [
            'arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role',
          ],
        )

    internetGateway = ec2.CfnInternetGateway(self, 'InternetGateway',
        )

    jobDefinition = batch.CfnJobDefinition(self, 'JobDefinition',
          type = 'container',
          container_properties = {
            'image': ''.join([
              '137112412989.dkr.ecr.',
              Stack.of(self).region,
              '.amazonaws.com/amazonlinux:latest',
            ]),
            'vcpus': 2,
            'memory': 2000,
            'command': [
              'echo',
              'Hello world',
            ],
          },
          retry_strategy = {
            'attempts': 1,
          },
        )

    vpc = ec2.CfnVPC(self, 'VPC',
          cidr_block = '10.0.0.0/16',
        )

    iamInstanceProfile = iam.CfnInstanceProfile(self, 'IamInstanceProfile',
          roles = [
            ecsInstanceRole.ref,
          ],
        )

    routeTable = ec2.CfnRouteTable(self, 'RouteTable',
          vpc_id = vpc.ref,
        )

    securityGroup = ec2.CfnSecurityGroup(self, 'SecurityGroup',
          group_description = 'EC2 Security Group for instances launched in the VPC by Batch',
          vpc_id = vpc.ref,
        )

    subnet = ec2.CfnSubnet(self, 'Subnet',
          cidr_block = '10.0.0.0/24',
          vpc_id = vpc.ref,
          map_public_ip_on_launch = True,
        )

    vpcGatewayAttachment = ec2.CfnVPCGatewayAttachment(self, 'VPCGatewayAttachment',
          vpc_id = vpc.ref,
          internet_gateway_id = internetGateway.ref,
        )

    computeEnvironment = batch.CfnComputeEnvironment(self, 'ComputeEnvironment',
          type = 'MANAGED',
          compute_resources = {
            'type': 'EC2',
            'minvCpus': 0,
            'desiredvCpus': 0,
            'maxvCpus': 64,
            'instanceTypes': [
              'optimal',
            ],
            'subnets': [
              subnet.ref,
            ],
            'securityGroupIds': [
              securityGroup.ref,
            ],
            'instanceRole': iamInstanceProfile.ref,
          },
          service_role = batchServiceRole.ref,
        )

    route = ec2.CfnRoute(self, 'Route',
          route_table_id = routeTable.ref,
          destination_cidr_block = '0.0.0.0/0',
          gateway_id = internetGateway.ref,
        )

    subnetRouteTableAssociation = ec2.CfnSubnetRouteTableAssociation(self, 'SubnetRouteTableAssociation',
          route_table_id = routeTable.ref,
          subnet_id = subnet.ref,
        )

    jobQueue = batch.CfnJobQueue(self, 'JobQueue',
          priority = 1,
          compute_environment_order = [
            {
              'order': 1,
              'computeEnvironment': computeEnvironment.ref,
            },
          ],
        )

    # Outputs
    self.compute_environment_arn = computeEnvironment.ref
    cdk.CfnOutput(self, 'CfnOutputComputeEnvironmentArn', 
      key = 'ComputeEnvironmentArn',
      value = str(self.compute_environment_arn),
    )

    self.job_queue_arn = jobQueue.ref
    cdk.CfnOutput(self, 'CfnOutputJobQueueArn', 
      key = 'JobQueueArn',
      value = str(self.job_queue_arn),
    )

    self.job_definition_arn = jobDefinition.ref
    cdk.CfnOutput(self, 'CfnOutputJobDefinitionArn', 
      key = 'JobDefinitionArn',
      value = str(self.job_definition_arn),
    )



