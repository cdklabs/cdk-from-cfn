import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as events from 'aws-cdk-lib/aws-events';
import * as groundstation from 'aws-cdk-lib/aws-groundstation';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as sns from 'aws-cdk-lib/aws-sns';

export interface GroundStationStackProps extends cdk.StackProps {
  /**
   * This bucket will be created. Data will be delivered to this S3 bucket. Name must start with "aws-groundstation-"
   * @default 'aws-groundstation-s3dd-your-bucket'
   */
  readonly groundStationS3DataDeliveryBucketName?: string;
  /**
   * Email address to receive contact updates
   * @default 'someone@somewhere.com'
   */
  readonly notificationEmail?: string;
  /**
   * Used for data processing task
   * @default 'JPSS1'
   */
  readonly satelliteName?: string;
  /**
   * RT-STPS Software
   * @default 'your-software-bucket'
   */
  readonly softwareS3Bucket?: string;
  /**
   * The CIDR Block that the security group will allow ssh access to an instance. The CIDR Block has the form x.x.x.x/x.
   * @default '15.16.17.18/32'
   */
  readonly sshCidrBlock?: string;
  /**
   * Name of the ssh key used to access ec2 hosts. Set this up ahead of time.
   * @default ''
   */
  readonly sshKeyName?: string;
  /**
   * VPC to launch instances in.
   * @default ''
   */
  readonly vpcId?: string;
  /**
   * Subnet to launch instances in
   * @default ''
   */
  readonly subnetId?: string;
}

/**
 * Ground Station S3 Data Delivery stack for JPSS1
 */
export class GroundStationStack extends cdk.Stack {
  public readonly snsTopicArn;

  public constructor(scope: cdk.App, id: string, props: GroundStationStackProps = {}) {
    super(scope, id, props);

    // Applying default props
    props = {
      ...props,
      groundStationS3DataDeliveryBucketName: props.groundStationS3DataDeliveryBucketName ?? 'aws-groundstation-s3dd-your-bucket',
      notificationEmail: props.notificationEmail ?? 'someone@somewhere.com',
      satelliteName: props.satelliteName ?? 'JPSS1',
      softwareS3Bucket: props.softwareS3Bucket ?? 'your-software-bucket',
      sshCidrBlock: props.sshCidrBlock ?? '15.16.17.18/32',
      sshKeyName: new cdk.CfnParameter(this, 'SshKeyName', {
        type: 'AWS::EC2::KeyPair::KeyName',
        default: props.sshKeyName?.toString() ?? '',
        description: 'Name of the ssh key used to access ec2 hosts. Set this up ahead of time.',
      }).valueAsString,
      vpcId: new cdk.CfnParameter(this, 'VpcId', {
        type: 'AWS::EC2::VPC::Id',
        default: props.vpcId?.toString() ?? '',
        description: 'VPC to launch instances in.',
      }).valueAsString,
      subnetId: new cdk.CfnParameter(this, 'SubnetId', {
        type: 'AWS::EC2::Subnet::Id',
        default: props.subnetId?.toString() ?? '',
        description: 'Subnet to launch instances in',
      }).valueAsString,
    };

    // Transforms
    this.addTransform('AWS::Serverless-2016-10-31');

    // Mappings
    const amiMap: Record<string, Record<string, string>> = {
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
    };

    // Resources
    const groundStationS3DataDeliveryBucket = new s3.CfnBucket(this, 'GroundStationS3DataDeliveryBucket', {
      bucketName: props.groundStationS3DataDeliveryBucketName!,
    });
    groundStationS3DataDeliveryBucket.cfnOptions.deletionPolicy = cdk.CfnDeletionPolicy.RETAIN;

    const groundStationS3DataDeliveryRole = new iam.CfnRole(this, 'GroundStationS3DataDeliveryRole', {
      assumeRolePolicyDocument: {
        Statement: [
          {
            Action: [
              'sts:AssumeRole',
            ],
            Effect: 'Allow',
            Principal: {
              Service: [
                'groundstation.amazonaws.com',
              ],
            },
            Condition: {
              StringEquals: {
                'aws:SourceAccount': this.account,
              },
              ArnLike: {
                'aws:SourceArn': `arn:aws:groundstation:${this.region}:${this.account}:config/s3-recording/*`,
              },
            },
          },
        ],
      },
    });

    const instanceEip = new ec2.CfnEIP(this, 'InstanceEIP', {
      domain: 'vpc',
    });

    const instanceRole = new iam.CfnRole(this, 'InstanceRole', {
      assumeRolePolicyDocument: {
        Version: '2012-10-17',
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
      managedPolicyArns: [
        'arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy',
        'arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM',
      ],
    });

    const instanceSecurityGroup = new ec2.CfnSecurityGroup(this, 'InstanceSecurityGroup', {
      groupDescription: 'AWS Ground Station receiver instance security group.',
      vpcId: props.vpcId!,
      securityGroupIngress: [
        {
          ipProtocol: 'tcp',
          fromPort: 22,
          toPort: 22,
          cidrIp: props.sshCidrBlock!,
          description: 'Inbound SSH access',
        },
      ],
    });

    const snppJpssDownlinkDemodDecodeAntennaConfig = new groundstation.CfnConfig(this, 'SnppJpssDownlinkDemodDecodeAntennaConfig', {
      name: 'JPSS1 Downlink Demod Decode Antenna Config',
      configData: {
        antennaDownlinkDemodDecodeConfig: {
          spectrumConfig: {
            centerFrequency: {
              value: 7812,
              units: 'MHz',
            },
            polarization: 'RIGHT_HAND',
            bandwidth: {
              value: 30,
              units: 'MHz',
            },
          },
          demodulationConfig: {
            unvalidatedJson: '{ \"type\":\"QPSK\", \"qpsk\":{ \"carrierFrequencyRecovery\":{ \"centerFrequency\":{ \"value\":7812, \"units\":\"MHz\" }, \"range\":{ \"value\":250, \"units\":\"kHz\" } }, \"symbolTimingRecovery\":{ \"symbolRate\":{ \"value\":15, \"units\":\"Msps\" }, \"range\":{ \"value\":0.75, \"units\":\"ksps\" }, \"matchedFilter\":{ \"type\":\"ROOT_RAISED_COSINE\", \"rolloffFactor\":0.5 } } } }',
          },
          decodeConfig: {
            unvalidatedJson: '{ \"edges\":[ { \"from\":\"I-Ingress\", \"to\":\"IQ-Recombiner\" }, { \"from\":\"Q-Ingress\", \"to\":\"IQ-Recombiner\" }, { \"from\":\"IQ-Recombiner\", \"to\":\"CcsdsViterbiDecoder\" }, { \"from\":\"CcsdsViterbiDecoder\", \"to\":\"NrzmDecoder\" }, { \"from\":\"NrzmDecoder\", \"to\":\"UncodedFramesEgress\" } ], \"nodeConfigs\":{ \"I-Ingress\":{ \"type\":\"CODED_SYMBOLS_INGRESS\", \"codedSymbolsIngress\":{ \"source\":\"I\" } }, \"Q-Ingress\":{ \"type\":\"CODED_SYMBOLS_INGRESS\", \"codedSymbolsIngress\":{ \"source\":\"Q\" } }, \"IQ-Recombiner\":{ \"type\":\"IQ_RECOMBINER\" }, \"CcsdsViterbiDecoder\":{ \"type\":\"CCSDS_171_133_VITERBI_DECODER\", \"ccsds171133ViterbiDecoder\":{ \"codeRate\":\"ONE_HALF\" } }, \"NrzmDecoder\":{ \"type\":\"NRZ_M_DECODER\" }, \"UncodedFramesEgress\":{ \"type\":\"UNCODED_FRAMES_EGRESS\" } } }',
          },
        },
      },
    });

    const trackingConfig = new groundstation.CfnConfig(this, 'TrackingConfig', {
      name: 'JPSS1 Tracking Config',
      configData: {
        trackingConfig: {
          autotrack: 'PREFERRED',
        },
      },
    });

    const snsTopic = new sns.CfnTopic(this, 'snsTopic', {
      displayName: [
        'GS-S3-Data-Delivery',
        props.satelliteName!,
      ].join('-'),
      subscription: [
        {
          endpoint: props.notificationEmail!,
          protocol: 'email',
        },
      ],
    });

    const generalInstanceProfile = new iam.CfnInstanceProfile(this, 'GeneralInstanceProfile', {
      roles: [
        instanceRole.ref,
      ],
    });
    generalInstanceProfile.addDependency(instanceRole);

    const groundStationS3DataDeliveryIamPolicy = new iam.CfnPolicy(this, 'GroundStationS3DataDeliveryIamPolicy', {
      policyDocument: {
        Version: '2012-10-17',
        Statement: [
          {
            Action: [
              's3:GetBucketLocation',
            ],
            Effect: 'Allow',
            Resource: [
              [
                'arn:aws:s3:::',
                props.groundStationS3DataDeliveryBucketName!,
              ].join(''),
            ],
          },
          {
            Action: [
              's3:PutObject',
            ],
            Effect: 'Allow',
            Resource: [
              [
                'arn:aws:s3:::',
                props.groundStationS3DataDeliveryBucketName!,
                '/*',
              ].join(''),
            ],
          },
        ],
      },
      policyName: 'GroundStationS3DataDeliveryPolicy',
      roles: [
        groundStationS3DataDeliveryRole.ref,
      ],
    });

    const instanceRoleEc2Policy = new iam.CfnManagedPolicy(this, 'InstanceRoleEC2Policy', {
      policyDocument: {
        Version: '2012-10-17',
        Statement: [
          {
            Action: [
              'ec2:DescribeTags',
            ],
            Effect: 'Allow',
            Resource: '*',
          },
        ],
      },
      roles: [
        instanceRole.ref,
      ],
    });

    const instanceRoleS3Policy = new iam.CfnManagedPolicy(this, 'InstanceRoleS3Policy', {
      policyDocument: {
        Version: '2012-10-17',
        Statement: [
          {
            Action: [
              's3:PutObject',
              's3:GetObject',
            ],
            Effect: 'Allow',
            Resource: [
              'arn:aws:s3:::',
              props.softwareS3Bucket!,
              '/*',
            ].join(''),
          },
          {
            Action: [
              's3:GetObject',
            ],
            Effect: 'Allow',
            Resource: [
              'arn:aws:s3:::',
              'space-solutions-',
              'eu-west-1',
              '/*',
            ].join(''),
          },
          {
            Action: [
              's3:PutObject',
              's3:GetObject',
            ],
            Effect: 'Allow',
            Resource: [
              'arn:aws:s3:::',
              groundStationS3DataDeliveryBucket.ref,
              '/*',
            ].join(''),
          },
          {
            Action: [
              's3:ListBucket',
            ],
            Effect: 'Allow',
            Resource: [
              'arn:aws:s3:::',
              props.softwareS3Bucket!,
            ].join(''),
          },
          {
            Action: [
              's3:ListBucket',
            ],
            Effect: 'Allow',
            Resource: [
              'arn:aws:s3:::',
              'space-solutions-',
              'eu-west-1',
              '/*',
            ].join(''),
          },
          {
            Action: [
              's3:ListBucket',
            ],
            Effect: 'Allow',
            Resource: [
              'arn:aws:s3:::',
              groundStationS3DataDeliveryBucket.ref,
            ].join(''),
          },
        ],
      },
      roles: [
        instanceRole.ref,
      ],
    });

    const instanceRoleSnsPolicy = new iam.CfnManagedPolicy(this, 'InstanceRoleSNSPolicy', {
      policyDocument: {
        Version: '2012-10-17',
        Statement: [
          {
            Action: [
              'sns:Publish',
            ],
            Effect: 'Allow',
            Resource: snsTopic.ref,
          },
        ],
      },
      roles: [
        instanceRole.ref,
      ],
    });

    const receiverInstanceNetworkInterfacePublic = new ec2.CfnNetworkInterface(this, 'ReceiverInstanceNetworkInterfacePublic', {
      description: 'Public network interface for troubleshooting',
      groupSet: [
        instanceSecurityGroup.ref,
      ],
      subnetId: props.subnetId!,
    });

    const instanceEipAsscociation = new ec2.CfnEIPAssociation(this, 'InstanceEIPAsscociation', {
      allocationId: instanceEip.attrAllocationId,
      networkInterfaceId: receiverInstanceNetworkInterfacePublic.ref,
    });

    const receiverInstance = new ec2.CfnInstance(this, 'ReceiverInstance', {
      disableApiTermination: false,
      iamInstanceProfile: generalInstanceProfile.ref,
      imageId: amiMap[this.region]['ami'],
      instanceType: 'c5.4xlarge',
      keyName: props.sshKeyName!,
      monitoring: true,
      networkInterfaces: [
        {
          networkInterfaceId: receiverInstanceNetworkInterfacePublic.ref,
          deviceIndex: 0,
          deleteOnTermination: false,
        },
      ],
      blockDeviceMappings: [
        {
          deviceName: '/dev/xvda',
          ebs: {
            volumeType: 'gp2',
            volumeSize: 100,
          },
        },
      ],
      tags: [
        {
          key: 'Name',
          value: [
            'Receiver',
            this.stackName,
          ].join('-'),
        },
      ],
      userData: cdk.Fn.base64(`#!/bin/bash

      exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
      echo `date +'%F %R:%S'` "INFO: Logging Setup" >&2

      echo "Setting instance hostname"
      export INSTANCE=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
      export HOSTNAME=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE" "Name=key,Values=Name" --region=${this.region} --output=text |cut -f5)
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
      aws s3 cp --region ${this.region} "s3://${props.softwareS3Bucket!}/software/RT-STPS/rt-stps-process.sh" "$PROCESS_SCRIPT"
      chmod +x "$PROCESS_SCRIPT"
      chown ec2-user:ec2-user "$PROCESS_SCRIPT"

      echo "Adding call to $PROCESS_SCRIPT into /etc/rc.local"
      echo "TIMESTR=\$(date '+%Y%m%d-%H%M')" >> /etc/rc.local
      echo "$PROCESS_SCRIPT ${props.satelliteName!} ${props.softwareS3Bucket!} ${props.groundStationS3DataDeliveryBucketName!} 2>&1 | tee $GROUND_STATION_BIN_DIR/data-capture_\$TIMESTR.log" >> /etc/rc.local
      chmod +x /etc/rc.d/rc.local

      echo "Creating /opt/aws/groundstation/bin/getSNSTopic.sh"
      echo "export SNS_TOPIC=${snsTopic.ref}" > /opt/aws/groundstation/bin/getSNSTopic.sh
      chmod +x /opt/aws/groundstation/bin/getSNSTopic.sh

      echo "Sending completion SNS notification"
      export MESSAGE="GroundStation setup is complete for Satellite: ${props.satelliteName!}.  The RT-STPS processor EC2 instance is all setup and ready to go! It will be automatically started after data from a satellite pass has been deposited in your S3 bucket.  Data will be processed using RT-STPS, then copied to the following S3 Bucket: ${props.groundStationS3DataDeliveryBucketName!}.  A summary of the contact will be emailed to ${props.notificationEmail!}. The EC2 instance will now be stopped."
      aws sns publish --topic-arn ${snsTopic.ref} --message "$MESSAGE" --region ${this.region}

      echo "Shutting down the EC2 instance"
      shutdown -h now

      exit 0
      `),
    });
    receiverInstance.addDependency(instanceSecurityGroup);
    receiverInstance.addDependency(generalInstanceProfile);

    const s3RecordingConfig = new groundstation.CfnConfig(this, 'S3RecordingConfig', {
      name: 'JPSS1 Recording Config',
      configData: {
        s3RecordingConfig: {
          bucketArn: [
            'arn:aws:s3:::',
            props.groundStationS3DataDeliveryBucketName!,
          ].join(''),
          roleArn: groundStationS3DataDeliveryRole.attrArn,
          prefix: 'data/JPSS1/{year}/{month}/{day}',
        },
      },
    });
    s3RecordingConfig.addDependency(groundStationS3DataDeliveryBucket);
    s3RecordingConfig.addDependency(groundStationS3DataDeliveryIamPolicy);

    const groundStationS3ddLambdaRolePolicy = new iam.CfnManagedPolicy(this, 'GroundStationS3ddLambdaRolePolicy', {
      policyDocument: {
        Version: '2012-10-17',
        Statement: [
          {
            Effect: 'Allow',
            Action: [
              'ec2:StartInstances',
              'ec2:StopInstances',
              'ec2:CreateTags',
            ],
            Resource: [
              `arn:aws:ec2:${this.region}:${this.account}:instance/${receiverInstance.ref}`,
            ],
          },
          {
            Effect: 'Allow',
            Action: [
              'ec2:DescribeInstanceStatus',
              'ec2:DescribeNetworkInterfaces',
            ],
            Resource: [
              '*',
            ],
          },
          {
            Effect: 'Allow',
            Action: [
              'sns:Publish',
            ],
            Resource: snsTopic.ref,
          },
          {
            Effect: 'Allow',
            Action: [
              's3:PutObject',
              's3:PutObjectAcl',
              's3:GetObject',
              's3:DeleteObjectVersion',
              's3:DeleteObject',
            ],
            Resource: [
              [
                'arn:aws:s3:::',
                props.groundStationS3DataDeliveryBucketName!,
                '/*',
              ].join(''),
            ],
          },
          {
            Effect: 'Allow',
            Action: [
              's3:ListBucket',
            ],
            Resource: [
              [
                'arn:aws:s3:::',
                props.groundStationS3DataDeliveryBucketName!,
              ].join(''),
            ],
          },
        ],
      },
    });

    const snppJpssDemodDecodeMissionProfile = new groundstation.CfnMissionProfile(this, 'SnppJpssDemodDecodeMissionProfile', {
      name: '43013 JPSS1 Demod Decode to S3',
      contactPrePassDurationSeconds: 120,
      contactPostPassDurationSeconds: 120,
      minimumViableContactDurationSeconds: 180,
      trackingConfigArn: trackingConfig.ref,
      dataflowEdges: [
        {
          source: [
            snppJpssDownlinkDemodDecodeAntennaConfig.ref,
            'UncodedFramesEgress',
          ].join('/'),
          destination: s3RecordingConfig.ref,
        },
      ],
    });

    const groundStationS3ddLambdaRole = new iam.CfnRole(this, 'GroundStationS3ddLambdaRole', {
      path: '/',
      managedPolicyArns: [
        'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
        groundStationS3ddLambdaRolePolicy.ref,
      ],
      assumeRolePolicyDocument: {
        Version: '2012-10-17',
        Statement: [
          {
            Effect: 'Allow',
            Principal: {
              Service: 'lambda.amazonaws.com',
            },
            Action: [
              'sts:AssumeRole',
            ],
          },
        ],
      },
    });

    const lambdaFunctionStartRtstps = new lambda.CfnFunction(this, 'LambdaFunctionStartRtstps', {
      environment: {
        variables: {
          RtstpsInstance: receiverInstance.ref,
        },
      },
      handler: 'index.handle_cloudwatch_event',
      runtime: 'python3.9',
      memorySize: 512,
      timeout: 300,
      role: groundStationS3ddLambdaRole.attrArn,
      code: {
        s3Bucket: props.softwareS3Bucket!,
        s3Key: 'software/RT-STPS/lambda.zip',
      },
    });

    const s3ContactCompleteEventRule = new events.CfnRule(this, 'S3ContactCompleteEventRule', {
      description: 'Triggered when all files have been uploaded for a Ground Station S3 data delivery contact',
      eventPattern: {
        source: [
          'aws.groundstation',
        ],
        'detail-type': [
          'Ground Station S3 Upload Complete',
        ],
      },
      state: 'ENABLED',
      targets: [
        {
          arn: lambdaFunctionStartRtstps.attrArn,
          id: 'LambdaFunctionStartRtstps',
        },
      ],
    });

    const permissionForGroundStationCloudWatchEventsToInvokeLambda = new lambda.CfnPermission(this, 'PermissionForGroundStationCloudWatchEventsToInvokeLambda', {
      functionName: lambdaFunctionStartRtstps.ref,
      action: 'lambda:InvokeFunction',
      principal: 'events.amazonaws.com',
      sourceArn: s3ContactCompleteEventRule.attrArn,
    });

    // Outputs
    this.snsTopicArn = snsTopic.ref;
    new cdk.CfnOutput(this, 'CfnOutputSnsTopicArn', {
      key: 'SnsTopicArn',
      exportName: `${this.stackName}-SnsTopicArn`,
      value: this.snsTopicArn!.toString(),
    });
  }
}
