from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_events as events
import aws_cdk.aws_groundstation as groundstation
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_sns as sns
from constructs import Construct

"""
  Ground Station S3 Data Delivery stack for JPSS1
"""
class GroundStationConstruct(Construct):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id)

    # Applying default props
    props = {
      'groundStationS3DataDeliveryBucketName': kwargs.get('groundStationS3DataDeliveryBucketName', 'aws-groundstation-s3dd-your-bucket'),
      'notificationEmail': kwargs.get('notificationEmail', 'someone@somewhere.com'),
      'satelliteName': kwargs.get('satelliteName', 'JPSS1'),
      'softwareS3Bucket': kwargs.get('softwareS3Bucket', 'your-software-bucket'),
      'sshCidrBlock': kwargs.get('sshCidrBlock', '15.16.17.18/32'),
      'sshKeyName': cdk.CfnParameter(self, 'sshKeyName', 
        type = 'AWS::EC2::KeyPair::KeyName',
        default = str(kwargs.get('sshKeyName', '')),
        description = 'Name of the ssh key used to access ec2 hosts. Set this up ahead of time.',
      ),
      'vpcId': cdk.CfnParameter(self, 'vpcId', 
        type = 'AWS::EC2::VPC::Id',
        default = str(kwargs.get('vpcId', '')),
        description = 'VPC to launch instances in.',
      ),
      'subnetId': cdk.CfnParameter(self, 'subnetId', 
        type = 'AWS::EC2::Subnet::Id',
        default = str(kwargs.get('subnetId', '')),
        description = 'Subnet to launch instances in',
      ),
    }

    # Transforms
    Stack.of(self).add_transform('AWS::Serverless-2016-10-31')

    # Mappings
    amiMap = {
      'eu-north-1': {
        'ami': 'ami-0abb1aa57ecf6a060',
      },
      'eu-west-1': {
        'ami': 'ami-082af980f9f5514f8',
      },
      'me-south-1': {
        'ami': 'ami-0687a5f8dac57444e',
      },
      'us-east-1': {
        'ami': 'ami-03c7d01cf4dedc891',
      },
      'us-east-2': {
        'ami': 'ami-06d5c50c30a35fb88',
      },
      'us-west-2': {
        'ami': 'ami-0ac64ad8517166fb1',
      },
      'ap-southeast-2': {
        'ami': 'ami-0074f30ddebf60493',
      },
      'af-south-1': {
        'ami': 'ami-0764fb4fffa117039',
      },
      'ap-northeast-2': {
        'ami': 'ami-03db74b70e1da9c56',
      },
      'ap-southeast-1': {
        'ami': 'ami-0b3a4110c36b9a5f0',
      },
      'eu-central-1': {
        'ami': 'ami-0adbcf08fdd664fed',
      },
      'sa-east-1': {
        'ami': 'ami-0c5cdf1548242305d',
      },
    }

    # Resources
    groundStationS3DataDeliveryBucket = s3.CfnBucket(self, 'GroundStationS3DataDeliveryBucket',
          bucket_name = props['groundStationS3DataDeliveryBucketName'],
        )
    groundStationS3DataDeliveryBucket.cfn_options.deletion_policy = cdk.CfnDeletionPolicy.RETAIN

    groundStationS3DataDeliveryRole = iam.CfnRole(self, 'GroundStationS3DataDeliveryRole',
          assume_role_policy_document = {
            'Statement': [
              {
                'Action': [
                  'sts:AssumeRole',
                ],
                'Effect': 'Allow',
                'Principal': {
                  'Service': [
                    'groundstation.amazonaws.com',
                  ],
                },
                'Condition': {
                  'StringEquals': {
                    'aws:SourceAccount': Stack.of(self).account,
                  },
                  'ArnLike': {
                    'aws:SourceArn': f"""arn:aws:groundstation:{Stack.of(self).region}:{Stack.of(self).account}:config/s3-recording/*""",
                  },
                },
              },
            ],
          },
        )

    instanceEip = ec2.CfnEIP(self, 'InstanceEIP',
          domain = 'vpc',
        )

    instanceRole = iam.CfnRole(self, 'InstanceRole',
          assume_role_policy_document = {
            'Version': '2012-10-17',
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
          managed_policy_arns = [
            'arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy',
            'arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM',
          ],
        )

    instanceSecurityGroup = ec2.CfnSecurityGroup(self, 'InstanceSecurityGroup',
          group_description = 'AWS Ground Station receiver instance security group.',
          vpc_id = props['vpcId'],
          security_group_ingress = [
            {
              'ipProtocol': 'tcp',
              'fromPort': 22,
              'toPort': 22,
              'cidrIp': props['sshCidrBlock'],
              'description': 'Inbound SSH access',
            },
          ],
        )

    snppJpssDownlinkDemodDecodeAntennaConfig = groundstation.CfnConfig(self, 'SnppJpssDownlinkDemodDecodeAntennaConfig',
          name = 'JPSS1 Downlink Demod Decode Antenna Config',
          config_data = {
            'antennaDownlinkDemodDecodeConfig': {
              'spectrumConfig': {
                'centerFrequency': {
                  'value': 7812,
                  'units': 'MHz',
                },
                'polarization': 'RIGHT_HAND',
                'bandwidth': {
                  'value': 30,
                  'units': 'MHz',
                },
              },
              'demodulationConfig': {
                'unvalidatedJson': '{ \"type\":\"QPSK\", \"qpsk\":{ \"carrierFrequencyRecovery\":{ \"centerFrequency\":{ \"value\":7812, \"units\":\"MHz\" }, \"range\":{ \"value\":250, \"units\":\"kHz\" } }, \"symbolTimingRecovery\":{ \"symbolRate\":{ \"value\":15, \"units\":\"Msps\" }, \"range\":{ \"value\":0.75, \"units\":\"ksps\" }, \"matchedFilter\":{ \"type\":\"ROOT_RAISED_COSINE\", \"rolloffFactor\":0.5 } } } }',
              },
              'decodeConfig': {
                'unvalidatedJson': '{ \"edges\":[ { \"from\":\"I-Ingress\", \"to\":\"IQ-Recombiner\" }, { \"from\":\"Q-Ingress\", \"to\":\"IQ-Recombiner\" }, { \"from\":\"IQ-Recombiner\", \"to\":\"CcsdsViterbiDecoder\" }, { \"from\":\"CcsdsViterbiDecoder\", \"to\":\"NrzmDecoder\" }, { \"from\":\"NrzmDecoder\", \"to\":\"UncodedFramesEgress\" } ], \"nodeConfigs\":{ \"I-Ingress\":{ \"type\":\"CODED_SYMBOLS_INGRESS\", \"codedSymbolsIngress\":{ \"source\":\"I\" } }, \"Q-Ingress\":{ \"type\":\"CODED_SYMBOLS_INGRESS\", \"codedSymbolsIngress\":{ \"source\":\"Q\" } }, \"IQ-Recombiner\":{ \"type\":\"IQ_RECOMBINER\" }, \"CcsdsViterbiDecoder\":{ \"type\":\"CCSDS_171_133_VITERBI_DECODER\", \"ccsds171133ViterbiDecoder\":{ \"codeRate\":\"ONE_HALF\" } }, \"NrzmDecoder\":{ \"type\":\"NRZ_M_DECODER\" }, \"UncodedFramesEgress\":{ \"type\":\"UNCODED_FRAMES_EGRESS\" } } }',
              },
            },
          },
        )

    trackingConfig = groundstation.CfnConfig(self, 'TrackingConfig',
          name = 'JPSS1 Tracking Config',
          config_data = {
            'trackingConfig': {
              'autotrack': 'PREFERRED',
            },
          },
        )

    snsTopic = sns.CfnTopic(self, 'snsTopic',
          display_name = '-'.join([
            'GS-S3-Data-Delivery',
            props['satelliteName'],
          ]),
          subscription = [
            {
              'endpoint': props['notificationEmail'],
              'protocol': 'email',
            },
          ],
        )

    generalInstanceProfile = iam.CfnInstanceProfile(self, 'GeneralInstanceProfile',
          roles = [
            instanceRole.ref,
          ],
        )
    generalInstanceProfile.add_dependency(instanceRole)

    groundStationS3DataDeliveryIamPolicy = iam.CfnPolicy(self, 'GroundStationS3DataDeliveryIamPolicy',
          policy_document = {
            'Version': '2012-10-17',
            'Statement': [
              {
                'Action': [
                  's3:GetBucketLocation',
                ],
                'Effect': 'Allow',
                'Resource': [
                  ''.join([
                    'arn:aws:s3:::',
                    props['groundStationS3DataDeliveryBucketName'],
                  ]),
                ],
              },
              {
                'Action': [
                  's3:PutObject',
                ],
                'Effect': 'Allow',
                'Resource': [
                  ''.join([
                    'arn:aws:s3:::',
                    props['groundStationS3DataDeliveryBucketName'],
                    '/*',
                  ]),
                ],
              },
            ],
          },
          policy_name = 'GroundStationS3DataDeliveryPolicy',
          roles = [
            groundStationS3DataDeliveryRole.ref,
          ],
        )

    instanceRoleEc2Policy = iam.CfnManagedPolicy(self, 'InstanceRoleEC2Policy',
          policy_document = {
            'Version': '2012-10-17',
            'Statement': [
              {
                'Action': [
                  'ec2:DescribeTags',
                ],
                'Effect': 'Allow',
                'Resource': '*',
              },
            ],
          },
          roles = [
            instanceRole.ref,
          ],
        )

    instanceRoleS3Policy = iam.CfnManagedPolicy(self, 'InstanceRoleS3Policy',
          policy_document = {
            'Version': '2012-10-17',
            'Statement': [
              {
                'Action': [
                  's3:PutObject',
                  's3:GetObject',
                ],
                'Effect': 'Allow',
                'Resource': ''.join([
                  'arn:aws:s3:::',
                  props['softwareS3Bucket'],
                  '/*',
                ]),
              },
              {
                'Action': [
                  's3:GetObject',
                ],
                'Effect': 'Allow',
                'Resource': ''.join([
                  'arn:aws:s3:::',
                  'space-solutions-',
                  'eu-west-1',
                  '/*',
                ]),
              },
              {
                'Action': [
                  's3:PutObject',
                  's3:GetObject',
                ],
                'Effect': 'Allow',
                'Resource': ''.join([
                  'arn:aws:s3:::',
                  groundStationS3DataDeliveryBucket.ref,
                  '/*',
                ]),
              },
              {
                'Action': [
                  's3:ListBucket',
                ],
                'Effect': 'Allow',
                'Resource': ''.join([
                  'arn:aws:s3:::',
                  props['softwareS3Bucket'],
                ]),
              },
              {
                'Action': [
                  's3:ListBucket',
                ],
                'Effect': 'Allow',
                'Resource': ''.join([
                  'arn:aws:s3:::',
                  'space-solutions-',
                  'eu-west-1',
                  '/*',
                ]),
              },
              {
                'Action': [
                  's3:ListBucket',
                ],
                'Effect': 'Allow',
                'Resource': ''.join([
                  'arn:aws:s3:::',
                  groundStationS3DataDeliveryBucket.ref,
                ]),
              },
            ],
          },
          roles = [
            instanceRole.ref,
          ],
        )

    instanceRoleSnsPolicy = iam.CfnManagedPolicy(self, 'InstanceRoleSNSPolicy',
          policy_document = {
            'Version': '2012-10-17',
            'Statement': [
              {
                'Action': [
                  'sns:Publish',
                ],
                'Effect': 'Allow',
                'Resource': snsTopic.ref,
              },
            ],
          },
          roles = [
            instanceRole.ref,
          ],
        )

    receiverInstanceNetworkInterfacePublic = ec2.CfnNetworkInterface(self, 'ReceiverInstanceNetworkInterfacePublic',
          description = 'Public network interface for troubleshooting',
          group_set = [
            instanceSecurityGroup.ref,
          ],
          subnet_id = props['subnetId'],
        )

    instanceEipAsscociation = ec2.CfnEIPAssociation(self, 'InstanceEIPAsscociation',
          allocation_id = instanceEip.attr_allocation_id,
          network_interface_id = receiverInstanceNetworkInterfacePublic.ref,
        )

    receiverInstance = ec2.CfnInstance(self, 'ReceiverInstance',
          disable_api_termination = False,
          iam_instance_profile = generalInstanceProfile.ref,
          image_id = amiMap[Stack.of(self).region]['ami'],
          instance_type = 'c5.4xlarge',
          key_name = props['sshKeyName'],
          monitoring = True,
          network_interfaces = [
            {
              'networkInterfaceId': receiverInstanceNetworkInterfacePublic.ref,
              'deviceIndex': 0,
              'deleteOnTermination': False,
            },
          ],
          block_device_mappings = [
            {
              'deviceName': '/dev/xvda',
              'ebs': {
                'volumeType': 'gp2',
                'volumeSize': 100,
              },
            },
          ],
          tags = [
            {
              'key': 'Name',
              'value': '-'.join([
                'Receiver',
                Stack.of(self).stack_name,
              ]),
            },
          ],
          user_data = cdk.Fn.base64(f"""#!/bin/bash

          exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
          echo `date +'%F %R:%S'` "INFO: Logging Setup" >&2

          echo "Setting instance hostname"
          export INSTANCE=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
          export HOSTNAME=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE" "Name=key,Values=Name" --region={Stack.of(self).region} --output=text |cut -f5)
          echo $HOSTNAME > /etc/hostname
          hostname $HOSTNAME

          echo "Installing RT-STPS pre-reqs"
          yum update -y && yum install -y wget java python3

          GROUND_STATION_DIR="/opt/aws/groundstation"
          GROUND_STATION_BIN_DIR="$GROUND_STATION_DIR/bin"
          PROCESS_SCRIPT="$GROUND_STATION_BIN_DIR/rt-stps-process.sh"

          echo "Creating $GROUND_STATION_BIN_DIR"
          mkdir -p "$GROUND_STATION_BIN_DIR"

          echo "Getting Assets from S3"
          aws s3 cp --region {Stack.of(self).region} "s3://{props['softwareS3Bucket']}/software/RT-STPS/rt-stps-process.sh" "$PROCESS_SCRIPT"
          chmod +x "$PROCESS_SCRIPT"
          chown ec2-user:ec2-user "$PROCESS_SCRIPT"

          echo "Adding call to $PROCESS_SCRIPT into /etc/rc.local"
          echo "TIMESTR=\$(date '+%Y%m%d-%H%M')" >> /etc/rc.local
          echo "$PROCESS_SCRIPT {props['satelliteName']} {props['softwareS3Bucket']} {props['groundStationS3DataDeliveryBucketName']} 2>&1 | tee $GROUND_STATION_BIN_DIR/data-capture_\$TIMESTR.log" >> /etc/rc.local
          chmod +x /etc/rc.d/rc.local

          echo "Creating /opt/aws/groundstation/bin/getSNSTopic.sh"
          echo "export SNS_TOPIC={snsTopic.ref}" > /opt/aws/groundstation/bin/getSNSTopic.sh
          chmod +x /opt/aws/groundstation/bin/getSNSTopic.sh

          echo "Sending completion SNS notification"
          export MESSAGE="GroundStation setup is complete for Satellite: {props['satelliteName']}.  The RT-STPS processor EC2 instance is all setup and ready to go! It will be automatically started after data from a satellite pass has been deposited in your S3 bucket.  Data will be processed using RT-STPS, then copied to the following S3 Bucket: {props['groundStationS3DataDeliveryBucketName']}.  A summary of the contact will be emailed to {props['notificationEmail']}. The EC2 instance will now be stopped."
          aws sns publish --topic-arn {snsTopic.ref} --message "$MESSAGE" --region {Stack.of(self).region}

          echo "Shutting down the EC2 instance"
          shutdown -h now

          exit 0
          """),
        )
    receiverInstance.add_dependency(instanceSecurityGroup)
    receiverInstance.add_dependency(generalInstanceProfile)

    s3RecordingConfig = groundstation.CfnConfig(self, 'S3RecordingConfig',
          name = 'JPSS1 Recording Config',
          config_data = {
            's3RecordingConfig': {
              'bucketArn': ''.join([
                'arn:aws:s3:::',
                props['groundStationS3DataDeliveryBucketName'],
              ]),
              'roleArn': groundStationS3DataDeliveryRole.attr_arn,
              'prefix': 'data/JPSS1/{year}/{month}/{day}',
            },
          },
        )
    s3RecordingConfig.add_dependency(groundStationS3DataDeliveryBucket)
    s3RecordingConfig.add_dependency(groundStationS3DataDeliveryIamPolicy)

    groundStationS3ddLambdaRolePolicy = iam.CfnManagedPolicy(self, 'GroundStationS3ddLambdaRolePolicy',
          policy_document = {
            'Version': '2012-10-17',
            'Statement': [
              {
                'Effect': 'Allow',
                'Action': [
                  'ec2:StartInstances',
                  'ec2:StopInstances',
                  'ec2:CreateTags',
                ],
                'Resource': [
                  f"""arn:aws:ec2:{Stack.of(self).region}:{Stack.of(self).account}:instance/{receiverInstance.ref}""",
                ],
              },
              {
                'Effect': 'Allow',
                'Action': [
                  'ec2:DescribeInstanceStatus',
                  'ec2:DescribeNetworkInterfaces',
                ],
                'Resource': [
                  '*',
                ],
              },
              {
                'Effect': 'Allow',
                'Action': [
                  'sns:Publish',
                ],
                'Resource': snsTopic.ref,
              },
              {
                'Effect': 'Allow',
                'Action': [
                  's3:PutObject',
                  's3:PutObjectAcl',
                  's3:GetObject',
                  's3:DeleteObjectVersion',
                  's3:DeleteObject',
                ],
                'Resource': [
                  ''.join([
                    'arn:aws:s3:::',
                    props['groundStationS3DataDeliveryBucketName'],
                    '/*',
                  ]),
                ],
              },
              {
                'Effect': 'Allow',
                'Action': [
                  's3:ListBucket',
                ],
                'Resource': [
                  ''.join([
                    'arn:aws:s3:::',
                    props['groundStationS3DataDeliveryBucketName'],
                  ]),
                ],
              },
            ],
          },
        )

    snppJpssDemodDecodeMissionProfile = groundstation.CfnMissionProfile(self, 'SnppJpssDemodDecodeMissionProfile',
          name = '43013 JPSS1 Demod Decode to S3',
          contact_pre_pass_duration_seconds = 120,
          contact_post_pass_duration_seconds = 120,
          minimum_viable_contact_duration_seconds = 180,
          tracking_config_arn = trackingConfig.ref,
          dataflow_edges = [
            {
              'source': '/'.join([
                snppJpssDownlinkDemodDecodeAntennaConfig.ref,
                'UncodedFramesEgress',
              ]),
              'destination': s3RecordingConfig.ref,
            },
          ],
        )

    groundStationS3ddLambdaRole = iam.CfnRole(self, 'GroundStationS3ddLambdaRole',
          path = '/',
          managed_policy_arns = [
            'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
            groundStationS3ddLambdaRolePolicy.ref,
          ],
          assume_role_policy_document = {
            'Version': '2012-10-17',
            'Statement': [
              {
                'Effect': 'Allow',
                'Principal': {
                  'Service': 'lambda.amazonaws.com',
                },
                'Action': [
                  'sts:AssumeRole',
                ],
              },
            ],
          },
        )

    lambdaFunctionStartRtstps = aws_lambda.CfnFunction(self, 'LambdaFunctionStartRtstps',
          environment = {
            'variables': {
              'RtstpsInstance': receiverInstance.ref,
            },
          },
          handler = 'index.handle_cloudwatch_event',
          runtime = 'python3.9',
          memory_size = 512,
          timeout = 300,
          role = groundStationS3ddLambdaRole.attr_arn,
          code = {
            's3Bucket': props['softwareS3Bucket'],
            's3Key': 'software/RT-STPS/lambda.zip',
          },
        )

    s3ContactCompleteEventRule = events.CfnRule(self, 'S3ContactCompleteEventRule',
          description = 'Triggered when all files have been uploaded for a Ground Station S3 data delivery contact',
          event_pattern = {
            'source': [
              'aws.groundstation',
            ],
            'detail-type': [
              'Ground Station S3 Upload Complete',
            ],
          },
          state = 'ENABLED',
          targets = [
            {
              'arn': lambdaFunctionStartRtstps.attr_arn,
              'id': 'LambdaFunctionStartRtstps',
            },
          ],
        )

    permissionForGroundStationCloudWatchEventsToInvokeLambda = aws_lambda.CfnPermission(self, 'PermissionForGroundStationCloudWatchEventsToInvokeLambda',
          function_name = lambdaFunctionStartRtstps.ref,
          action = 'lambda:InvokeFunction',
          principal = 'events.amazonaws.com',
          source_arn = s3ContactCompleteEventRule.attr_arn,
        )

    # Outputs
    self.sns_topic_arn = snsTopic.ref
    cdk.CfnOutput(self, 'CfnOutputSnsTopicArn', 
      key = 'SnsTopicArn',
      export_name = f"""{Stack.of(self).stack_name}-SnsTopicArn""",
      value = str(self.sns_topic_arn),
    )



