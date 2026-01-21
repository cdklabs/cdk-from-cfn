package main

import (
	"fmt"

	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	ec2 "github.com/aws/aws-cdk-go/awscdk/v2/awsec2"
	events "github.com/aws/aws-cdk-go/awscdk/v2/awsevents"
	groundstation "github.com/aws/aws-cdk-go/awscdk/v2/awsgroundstation"
	iam "github.com/aws/aws-cdk-go/awscdk/v2/awsiam"
	lambda "github.com/aws/aws-cdk-go/awscdk/v2/awslambda"
	s3 "github.com/aws/aws-cdk-go/awscdk/v2/awss3"
	sns "github.com/aws/aws-cdk-go/awscdk/v2/awssns"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type GroundStationConstructProps struct {
	/// This bucket will be created. Data will be delivered to this S3 bucket. Name must start with "aws-groundstation-"
	GroundStationS3DataDeliveryBucketName *string
	/// Email address to receive contact updates
	NotificationEmail *string
	/// Used for data processing task
	SatelliteName *string
	/// RT-STPS Software
	SoftwareS3Bucket *string
	/// The CIDR Block that the security group will allow ssh access to an instance. The CIDR Block has the form x.x.x.x/x.
	SshCidrBlock *string
	/// Name of the ssh key used to access ec2 hosts. Set this up ahead of time.
	SshKeyName interface{/* AWS::EC2::KeyPair::KeyName */}
	/// VPC to launch instances in.
	VpcId interface{/* AWS::EC2::VPC::Id */}
	/// Subnet to launch instances in
	SubnetId interface{/* AWS::EC2::Subnet::Id */}
}

/// Ground Station S3 Data Delivery stack for JPSS1
type GroundStationConstruct struct {
	constructs.Construct
	SnsTopicArn interface{} // TODO: fix to appropriate type
}

func NewGroundStationConstruct(scope constructs.Construct, id string, props *GroundStationConstructProps) *GroundStationConstruct {
	amiMap := map[*string]map[*string]*string{
		jsii.String("eu-north-1"): map[*string]*string{
			jsii.String("ami"): jsii.String("ami-0abb1aa57ecf6a060"),
		},
		jsii.String("eu-west-1"): map[*string]*string{
			jsii.String("ami"): jsii.String("ami-082af980f9f5514f8"),
		},
		jsii.String("me-south-1"): map[*string]*string{
			jsii.String("ami"): jsii.String("ami-0687a5f8dac57444e"),
		},
		jsii.String("us-east-1"): map[*string]*string{
			jsii.String("ami"): jsii.String("ami-03c7d01cf4dedc891"),
		},
		jsii.String("us-east-2"): map[*string]*string{
			jsii.String("ami"): jsii.String("ami-06d5c50c30a35fb88"),
		},
		jsii.String("us-west-2"): map[*string]*string{
			jsii.String("ami"): jsii.String("ami-0ac64ad8517166fb1"),
		},
		jsii.String("ap-southeast-2"): map[*string]*string{
			jsii.String("ami"): jsii.String("ami-0074f30ddebf60493"),
		},
		jsii.String("af-south-1"): map[*string]*string{
			jsii.String("ami"): jsii.String("ami-0764fb4fffa117039"),
		},
		jsii.String("ap-northeast-2"): map[*string]*string{
			jsii.String("ami"): jsii.String("ami-03db74b70e1da9c56"),
		},
		jsii.String("ap-southeast-1"): map[*string]*string{
			jsii.String("ami"): jsii.String("ami-0b3a4110c36b9a5f0"),
		},
		jsii.String("eu-central-1"): map[*string]*string{
			jsii.String("ami"): jsii.String("ami-0adbcf08fdd664fed"),
		},
		jsii.String("sa-east-1"): map[*string]*string{
			jsii.String("ami"): jsii.String("ami-0c5cdf1548242305d"),
		},
	}

	construct := constructs.NewConstruct(scope, &id)

	cdk.Stack_Of(construct).AddTransform(jsii.String("AWS::Serverless-2016-10-31"))

	groundStationS3DataDeliveryBucket := s3.NewCfnBucket(
		construct,
		jsii.String("GroundStationS3DataDeliveryBucket"),
		&s3.CfnBucketProps{
			BucketName: props.GroundStationS3DataDeliveryBucketName,
		},
	)

	groundStationS3DataDeliveryRole := iam.NewCfnRole(
		construct,
		jsii.String("GroundStationS3DataDeliveryRole"),
		&iam.CfnRoleProps{
			AssumeRolePolicyDocument: map[string]interface{} {
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Action": &[]interface{}{
							jsii.String("sts:AssumeRole"),
						},
						"Effect": jsii.String("Allow"),
						"Principal": map[string]interface{} {
							"Service": &[]interface{}{
								jsii.String("groundstation.amazonaws.com"),
							},
						},
						"Condition": map[string]interface{} {
							"StringEquals": map[string]interface{} {
								"Aws:SourceAccount": cdk.Stack_Of(construct).Account(),
							},
							"ArnLike": map[string]interface{} {
								"Aws:SourceArn": jsii.String(fmt.Sprintf("arn:aws:groundstation:%v:%v:config/s3-recording/*", cdk.Stack_Of(construct).Region(), cdk.Stack_Of(construct).Account())),
							},
						},
					},
				},
			},
		},
	)

	instanceEip := ec2.NewCfnEIP(
		construct,
		jsii.String("InstanceEIP"),
		&ec2.CfnEIPProps{
			Domain: jsii.String("vpc"),
		},
	)

	instanceRole := iam.NewCfnRole(
		construct,
		jsii.String("InstanceRole"),
		&iam.CfnRoleProps{
			AssumeRolePolicyDocument: map[string]interface{} {
				"Version": jsii.String("2012-10-17"),
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Effect": jsii.String("Allow"),
						"Principal": map[string]interface{} {
							"Service": &[]interface{}{
								jsii.String("ec2.amazonaws.com"),
							},
						},
						"Action": &[]interface{}{
							jsii.String("sts:AssumeRole"),
						},
					},
				},
			},
			Path: jsii.String("/"),
			ManagedPolicyArns: &[]*string{
				jsii.String("arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"),
				jsii.String("arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"),
			},
		},
	)

	instanceSecurityGroup := ec2.NewCfnSecurityGroup(
		construct,
		jsii.String("InstanceSecurityGroup"),
		&ec2.CfnSecurityGroupProps{
			GroupDescription: jsii.String("AWS Ground Station receiver instance security group."),
			VpcId: props.VpcId,
			SecurityGroupIngress: &[]interface{}{
				&IngressProperty{
					IpProtocol: jsii.String("tcp"),
					FromPort: jsii.Number(22),
					ToPort: jsii.Number(22),
					CidrIp: props.SshCidrBlock,
					Description: jsii.String("Inbound SSH access"),
				},
			},
		},
	)

	snppJpssDownlinkDemodDecodeAntennaConfig := ground_station.NewCfnConfig(
		construct,
		jsii.String("SnppJpssDownlinkDemodDecodeAntennaConfig"),
		&ground_station.CfnConfigProps{
			Name: jsii.String("JPSS1 Downlink Demod Decode Antenna Config"),
			ConfigData: &ConfigDataProperty{
				AntennaDownlinkDemodDecodeConfig: &AntennaDownlinkDemodDecodeConfigProperty{
					SpectrumConfig: &SpectrumConfigProperty{
						CenterFrequency: &FrequencyProperty{
							Value: jsii.Number(7812),
							Units: jsii.String("MHz"),
						},
						Polarization: jsii.String("RIGHT_HAND"),
						Bandwidth: &FrequencyBandwidthProperty{
							Value: jsii.Number(30),
							Units: jsii.String("MHz"),
						},
					},
					DemodulationConfig: &DemodulationConfigProperty{
						UnvalidatedJson: jsii.String("{ \"type\":\"QPSK\", \"qpsk\":{ \"carrierFrequencyRecovery\":{ \"centerFrequency\":{ \"value\":7812, \"units\":\"MHz\" }, \"range\":{ \"value\":250, \"units\":\"kHz\" } }, \"symbolTimingRecovery\":{ \"symbolRate\":{ \"value\":15, \"units\":\"Msps\" }, \"range\":{ \"value\":0.75, \"units\":\"ksps\" }, \"matchedFilter\":{ \"type\":\"ROOT_RAISED_COSINE\", \"rolloffFactor\":0.5 } } } }"),
					},
					DecodeConfig: &DecodeConfigProperty{
						UnvalidatedJson: jsii.String("{ \"edges\":[ { \"from\":\"I-Ingress\", \"to\":\"IQ-Recombiner\" }, { \"from\":\"Q-Ingress\", \"to\":\"IQ-Recombiner\" }, { \"from\":\"IQ-Recombiner\", \"to\":\"CcsdsViterbiDecoder\" }, { \"from\":\"CcsdsViterbiDecoder\", \"to\":\"NrzmDecoder\" }, { \"from\":\"NrzmDecoder\", \"to\":\"UncodedFramesEgress\" } ], \"nodeConfigs\":{ \"I-Ingress\":{ \"type\":\"CODED_SYMBOLS_INGRESS\", \"codedSymbolsIngress\":{ \"source\":\"I\" } }, \"Q-Ingress\":{ \"type\":\"CODED_SYMBOLS_INGRESS\", \"codedSymbolsIngress\":{ \"source\":\"Q\" } }, \"IQ-Recombiner\":{ \"type\":\"IQ_RECOMBINER\" }, \"CcsdsViterbiDecoder\":{ \"type\":\"CCSDS_171_133_VITERBI_DECODER\", \"ccsds171133ViterbiDecoder\":{ \"codeRate\":\"ONE_HALF\" } }, \"NrzmDecoder\":{ \"type\":\"NRZ_M_DECODER\" }, \"UncodedFramesEgress\":{ \"type\":\"UNCODED_FRAMES_EGRESS\" } } }"),
					},
				},
			},
		},
	)

	trackingConfig := ground_station.NewCfnConfig(
		construct,
		jsii.String("TrackingConfig"),
		&ground_station.CfnConfigProps{
			Name: jsii.String("JPSS1 Tracking Config"),
			ConfigData: &ConfigDataProperty{
				TrackingConfig: &TrackingConfigProperty{
					Autotrack: jsii.String("PREFERRED"),
				},
			},
		},
	)

	snsTopic := sns.NewCfnTopic(
		construct,
		jsii.String("snsTopic"),
		&sns.CfnTopicProps{
			DisplayName: cdk.Fn_Join(jsii.String("-"), &[]*string{
				jsii.String("GS-S3-Data-Delivery"),
				props.SatelliteName,
			}),
			Subscription: &[]interface{}{
				&SubscriptionProperty{
					Endpoint: props.NotificationEmail,
					Protocol: jsii.String("email"),
				},
			},
		},
	)

	generalInstanceProfile := iam.NewCfnInstanceProfile(
		construct,
		jsii.String("GeneralInstanceProfile"),
		&iam.CfnInstanceProfileProps{
			Roles: &[]*string{
				instanceRole.Ref(),
			},
		},
	)

	groundStationS3DataDeliveryIamPolicy := iam.NewCfnPolicy(
		construct,
		jsii.String("GroundStationS3DataDeliveryIamPolicy"),
		&iam.CfnPolicyProps{
			PolicyDocument: map[string]interface{} {
				"Version": jsii.String("2012-10-17"),
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Action": &[]interface{}{
							jsii.String("s3:GetBucketLocation"),
						},
						"Effect": jsii.String("Allow"),
						"Resource": &[]interface{}{
							cdk.Fn_Join(jsii.String(""), &[]*string{
								jsii.String("arn:aws:s3:::"),
								props.GroundStationS3DataDeliveryBucketName,
							}),
						},
					},
					map[string]interface{} {
						"Action": &[]interface{}{
							jsii.String("s3:PutObject"),
						},
						"Effect": jsii.String("Allow"),
						"Resource": &[]interface{}{
							cdk.Fn_Join(jsii.String(""), &[]*string{
								jsii.String("arn:aws:s3:::"),
								props.GroundStationS3DataDeliveryBucketName,
								jsii.String("/*"),
							}),
						},
					},
				},
			},
			PolicyName: jsii.String("GroundStationS3DataDeliveryPolicy"),
			Roles: &[]*string{
				groundStationS3DataDeliveryRole.Ref(),
			},
		},
	)

	iam.NewCfnManagedPolicy(
		construct,
		jsii.String("InstanceRoleEC2Policy"),
		&iam.CfnManagedPolicyProps{
			PolicyDocument: map[string]interface{} {
				"Version": jsii.String("2012-10-17"),
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Action": &[]interface{}{
							jsii.String("ec2:DescribeTags"),
						},
						"Effect": jsii.String("Allow"),
						"Resource": jsii.String("*"),
					},
				},
			},
			Roles: &[]*string{
				instanceRole.Ref(),
			},
		},
	)

	iam.NewCfnManagedPolicy(
		construct,
		jsii.String("InstanceRoleS3Policy"),
		&iam.CfnManagedPolicyProps{
			PolicyDocument: map[string]interface{} {
				"Version": jsii.String("2012-10-17"),
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Action": &[]interface{}{
							jsii.String("s3:PutObject"),
							jsii.String("s3:GetObject"),
						},
						"Effect": jsii.String("Allow"),
						"Resource": cdk.Fn_Join(jsii.String(""), &[]*string{
							jsii.String("arn:aws:s3:::"),
							props.SoftwareS3Bucket,
							jsii.String("/*"),
						}),
					},
					map[string]interface{} {
						"Action": &[]interface{}{
							jsii.String("s3:GetObject"),
						},
						"Effect": jsii.String("Allow"),
						"Resource": cdk.Fn_Join(jsii.String(""), &[]*string{
							jsii.String("arn:aws:s3:::"),
							jsii.String("space-solutions-"),
							jsii.String("eu-west-1"),
							jsii.String("/*"),
						}),
					},
					map[string]interface{} {
						"Action": &[]interface{}{
							jsii.String("s3:PutObject"),
							jsii.String("s3:GetObject"),
						},
						"Effect": jsii.String("Allow"),
						"Resource": cdk.Fn_Join(jsii.String(""), &[]*string{
							jsii.String("arn:aws:s3:::"),
							groundStationS3DataDeliveryBucket.Ref(),
							jsii.String("/*"),
						}),
					},
					map[string]interface{} {
						"Action": &[]interface{}{
							jsii.String("s3:ListBucket"),
						},
						"Effect": jsii.String("Allow"),
						"Resource": cdk.Fn_Join(jsii.String(""), &[]*string{
							jsii.String("arn:aws:s3:::"),
							props.SoftwareS3Bucket,
						}),
					},
					map[string]interface{} {
						"Action": &[]interface{}{
							jsii.String("s3:ListBucket"),
						},
						"Effect": jsii.String("Allow"),
						"Resource": cdk.Fn_Join(jsii.String(""), &[]*string{
							jsii.String("arn:aws:s3:::"),
							jsii.String("space-solutions-"),
							jsii.String("eu-west-1"),
							jsii.String("/*"),
						}),
					},
					map[string]interface{} {
						"Action": &[]interface{}{
							jsii.String("s3:ListBucket"),
						},
						"Effect": jsii.String("Allow"),
						"Resource": cdk.Fn_Join(jsii.String(""), &[]*string{
							jsii.String("arn:aws:s3:::"),
							groundStationS3DataDeliveryBucket.Ref(),
						}),
					},
				},
			},
			Roles: &[]*string{
				instanceRole.Ref(),
			},
		},
	)

	iam.NewCfnManagedPolicy(
		construct,
		jsii.String("InstanceRoleSNSPolicy"),
		&iam.CfnManagedPolicyProps{
			PolicyDocument: map[string]interface{} {
				"Version": jsii.String("2012-10-17"),
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Action": &[]interface{}{
							jsii.String("sns:Publish"),
						},
						"Effect": jsii.String("Allow"),
						"Resource": snsTopic.Ref(),
					},
				},
			},
			Roles: &[]*string{
				instanceRole.Ref(),
			},
		},
	)

	receiverInstanceNetworkInterfacePublic := ec2.NewCfnNetworkInterface(
		construct,
		jsii.String("ReceiverInstanceNetworkInterfacePublic"),
		&ec2.CfnNetworkInterfaceProps{
			Description: jsii.String("Public network interface for troubleshooting"),
			GroupSet: &[]*string{
				instanceSecurityGroup.Ref(),
			},
			SubnetId: props.SubnetId,
		},
	)

	ec2.NewCfnEIPAssociation(
		construct,
		jsii.String("InstanceEIPAsscociation"),
		&ec2.CfnEIPAssociationProps{
			AllocationId: instanceEip.AttrAllocationId(),
			NetworkInterfaceId: receiverInstanceNetworkInterfacePublic.Ref(),
		},
	)

	receiverInstance := ec2.NewCfnInstance(
		construct,
		jsii.String("ReceiverInstance"),
		&ec2.CfnInstanceProps{
			DisableApiTermination: jsii.Bool(false),
			IamInstanceProfile: generalInstanceProfile.Ref(),
			ImageId: amiMap[cdk.Stack_Of(construct).Region()][jsii.String("ami")],
			InstanceType: jsii.String("c5.4xlarge"),
			KeyName: props.SshKeyName,
			Monitoring: jsii.Bool(true),
			NetworkInterfaces: &[]interface{}{
				&NetworkInterfaceProperty{
					NetworkInterfaceId: receiverInstanceNetworkInterfacePublic.Ref(),
					DeviceIndex: jsii.Number(0),
					DeleteOnTermination: jsii.Bool(false),
				},
			},
			BlockDeviceMappings: &[]interface{}{
				&BlockDeviceMappingProperty{
					DeviceName: jsii.String("/dev/xvda"),
					Ebs: &EbsProperty{
						VolumeType: jsii.String("gp2"),
						VolumeSize: jsii.Number(100),
					},
				},
			},
			Tags: &[]*cdk.CfnTag{
				&cdk.CfnTag{
					Key: jsii.String("Name"),
					Value: cdk.Fn_Join(jsii.String("-"), &[]*string{
						jsii.String("Receiver"),
						cdk.Stack_Of(construct).StackName(),
					}),
				},
			},
			UserData: cdk.Fn_Base64(jsii.String(fmt.Sprintf("#!/bin/bash\n\nexec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1\necho `date +'%F %R:%S'` \"INFO: Logging Setup\" >&2\n\necho \"Setting instance hostname\"\nexport INSTANCE=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)\nexport HOSTNAME=$(aws ec2 describe-tags --filters \"Name=resource-id,Values=$INSTANCE\" \"Name=key,Values=Name\" --region=%v --output=text |cut -f5)\necho $HOSTNAME > /etc/hostname\nhostname $HOSTNAME\n\necho \"Installing RT-STPS pre-reqs\"\nyum update -y && yum install -y wget java python3\n\nGROUND_STATION_DIR=\"/opt/aws/groundstation\"\nGROUND_STATION_BIN_DIR=\"$GROUND_STATION_DIR/bin\"\nPROCESS_SCRIPT=\"$GROUND_STATION_BIN_DIR/rt-stps-process.sh\"\n\necho \"Creating $GROUND_STATION_BIN_DIR\"\nmkdir -p \"$GROUND_STATION_BIN_DIR\"\n\necho \"Getting Assets from S3\"\naws s3 cp --region %v \"s3://%v/software/RT-STPS/rt-stps-process.sh\" \"$PROCESS_SCRIPT\"\nchmod +x \"$PROCESS_SCRIPT\"\nchown ec2-user:ec2-user \"$PROCESS_SCRIPT\"\n\necho \"Adding call to $PROCESS_SCRIPT into /etc/rc.local\"\necho \"TIMESTR=\\$(date '+%Y%m%d-%H%M')\" >> /etc/rc.local\necho \"$PROCESS_SCRIPT %v %v %v 2>&1 | tee $GROUND_STATION_BIN_DIR/data-capture_\\$TIMESTR.log\" >> /etc/rc.local\nchmod +x /etc/rc.d/rc.local\n\necho \"Creating /opt/aws/groundstation/bin/getSNSTopic.sh\"\necho \"export SNS_TOPIC=%v\" > /opt/aws/groundstation/bin/getSNSTopic.sh\nchmod +x /opt/aws/groundstation/bin/getSNSTopic.sh\n\necho \"Sending completion SNS notification\"\nexport MESSAGE=\"GroundStation setup is complete for Satellite: %v.  The RT-STPS processor EC2 instance is all setup and ready to go! It will be automatically started after data from a satellite pass has been deposited in your S3 bucket.  Data will be processed using RT-STPS, then copied to the following S3 Bucket: %v.  A summary of the contact will be emailed to %v. The EC2 instance will now be stopped.\"\naws sns publish --topic-arn %v --message \"$MESSAGE\" --region %v\n\necho \"Shutting down the EC2 instance\"\nshutdown -h now\n\nexit 0\n", cdk.Stack_Of(construct).Region(), cdk.Stack_Of(construct).Region(), props.SoftwareS3Bucket, props.SatelliteName, props.SoftwareS3Bucket, props.GroundStationS3DataDeliveryBucketName, snsTopic.Ref(), props.SatelliteName, props.GroundStationS3DataDeliveryBucketName, props.NotificationEmail, snsTopic.Ref(), cdk.Stack_Of(construct).Region()))),
		},
	)

	s3RecordingConfig := ground_station.NewCfnConfig(
		construct,
		jsii.String("S3RecordingConfig"),
		&ground_station.CfnConfigProps{
			Name: jsii.String("JPSS1 Recording Config"),
			ConfigData: &ConfigDataProperty{
				S3RecordingConfig: &S3RecordingConfigProperty{
					BucketArn: cdk.Fn_Join(jsii.String(""), &[]*string{
						jsii.String("arn:aws:s3:::"),
						props.GroundStationS3DataDeliveryBucketName,
					}),
					RoleArn: groundStationS3DataDeliveryRole.AttrArn(),
					Prefix: jsii.String("data/JPSS1/{year}/{month}/{day}"),
				},
			},
		},
	)

	groundStationS3ddLambdaRolePolicy := iam.NewCfnManagedPolicy(
		construct,
		jsii.String("GroundStationS3ddLambdaRolePolicy"),
		&iam.CfnManagedPolicyProps{
			PolicyDocument: map[string]interface{} {
				"Version": jsii.String("2012-10-17"),
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Effect": jsii.String("Allow"),
						"Action": &[]interface{}{
							jsii.String("ec2:StartInstances"),
							jsii.String("ec2:StopInstances"),
							jsii.String("ec2:CreateTags"),
						},
						"Resource": &[]interface{}{
							jsii.String(fmt.Sprintf("arn:aws:ec2:%v:%v:instance/%v", cdk.Stack_Of(construct).Region(), cdk.Stack_Of(construct).Account(), receiverInstance.Ref())),
						},
					},
					map[string]interface{} {
						"Effect": jsii.String("Allow"),
						"Action": &[]interface{}{
							jsii.String("ec2:DescribeInstanceStatus"),
							jsii.String("ec2:DescribeNetworkInterfaces"),
						},
						"Resource": &[]interface{}{
							jsii.String("*"),
						},
					},
					map[string]interface{} {
						"Effect": jsii.String("Allow"),
						"Action": &[]interface{}{
							jsii.String("sns:Publish"),
						},
						"Resource": snsTopic.Ref(),
					},
					map[string]interface{} {
						"Effect": jsii.String("Allow"),
						"Action": &[]interface{}{
							jsii.String("s3:PutObject"),
							jsii.String("s3:PutObjectAcl"),
							jsii.String("s3:GetObject"),
							jsii.String("s3:DeleteObjectVersion"),
							jsii.String("s3:DeleteObject"),
						},
						"Resource": &[]interface{}{
							cdk.Fn_Join(jsii.String(""), &[]*string{
								jsii.String("arn:aws:s3:::"),
								props.GroundStationS3DataDeliveryBucketName,
								jsii.String("/*"),
							}),
						},
					},
					map[string]interface{} {
						"Effect": jsii.String("Allow"),
						"Action": &[]interface{}{
							jsii.String("s3:ListBucket"),
						},
						"Resource": &[]interface{}{
							cdk.Fn_Join(jsii.String(""), &[]*string{
								jsii.String("arn:aws:s3:::"),
								props.GroundStationS3DataDeliveryBucketName,
							}),
						},
					},
				},
			},
		},
	)

	ground_station.NewCfnMissionProfile(
		construct,
		jsii.String("SnppJpssDemodDecodeMissionProfile"),
		&ground_station.CfnMissionProfileProps{
			Name: jsii.String("43013 JPSS1 Demod Decode to S3"),
			ContactPrePassDurationSeconds: jsii.Number(120),
			ContactPostPassDurationSeconds: jsii.Number(120),
			MinimumViableContactDurationSeconds: jsii.Number(180),
			TrackingConfigArn: trackingConfig.Ref(),
			DataflowEdges: &[]interface{}{
				&DataflowEdgeProperty{
					Source: cdk.Fn_Join(jsii.String("/"), &[]*string{
						snppJpssDownlinkDemodDecodeAntennaConfig.Ref(),
						jsii.String("UncodedFramesEgress"),
					}),
					Destination: s3RecordingConfig.Ref(),
				},
			},
		},
	)

	groundStationS3ddLambdaRole := iam.NewCfnRole(
		construct,
		jsii.String("GroundStationS3ddLambdaRole"),
		&iam.CfnRoleProps{
			Path: jsii.String("/"),
			ManagedPolicyArns: &[]*string{
				jsii.String("arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"),
				groundStationS3ddLambdaRolePolicy.Ref(),
			},
			AssumeRolePolicyDocument: map[string]interface{} {
				"Version": jsii.String("2012-10-17"),
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Effect": jsii.String("Allow"),
						"Principal": map[string]interface{} {
							"Service": jsii.String("lambda.amazonaws.com"),
						},
						"Action": &[]interface{}{
							jsii.String("sts:AssumeRole"),
						},
					},
				},
			},
		},
	)

	lambdaFunctionStartRtstps := lambda.NewCfnFunction(
		construct,
		jsii.String("LambdaFunctionStartRtstps"),
		&lambda.CfnFunctionProps{
			Environment: &EnvironmentProperty{
				Variables: map[string]interface{} {
					"RtstpsInstance": receiverInstance.Ref(),
				},
			},
			Handler: jsii.String("index.handle_cloudwatch_event"),
			Runtime: jsii.String("python3.9"),
			MemorySize: jsii.Number(512),
			Timeout: jsii.Number(300),
			Role: groundStationS3ddLambdaRole.AttrArn(),
			Code: &CodeProperty{
				S3Bucket: props.SoftwareS3Bucket,
				S3Key: jsii.String("software/RT-STPS/lambda.zip"),
			},
		},
	)

	s3ContactCompleteEventRule := events.NewCfnRule(
		construct,
		jsii.String("S3ContactCompleteEventRule"),
		&events.CfnRuleProps{
			Description: jsii.String("Triggered when all files have been uploaded for a Ground Station S3 data delivery contact"),
			EventPattern: map[string]interface{} {
				"Source": &[]interface{}{
					jsii.String("aws.groundstation"),
				},
				"DetailType": &[]interface{}{
					jsii.String("Ground Station S3 Upload Complete"),
				},
			},
			State: jsii.String("ENABLED"),
			Targets: &[]interface{}{
				&TargetProperty{
					Arn: lambdaFunctionStartRtstps.AttrArn(),
					Id: jsii.String("LambdaFunctionStartRtstps"),
				},
			},
		},
	)

	lambda.NewCfnPermission(
		construct,
		jsii.String("PermissionForGroundStationCloudWatchEventsToInvokeLambda"),
		&lambda.CfnPermissionProps{
			FunctionName: lambdaFunctionStartRtstps.Ref(),
			Action: jsii.String("lambda:InvokeFunction"),
			Principal: jsii.String("events.amazonaws.com"),
			SourceArn: s3ContactCompleteEventRule.AttrArn(),
		},
	)

	cdk.NewCfnOutput(construct, jsii.String("CfnOutputSnsTopicArn"), &cdk.CfnOutputProps{
		Key: jsii.String("SnsTopicArn"),
		ExportName: jsii.String(fmt.Sprintf("%v-SnsTopicArn", cdk.Stack_Of(construct).StackName())),
		Value: snsTopic.Ref(),
	})

	return &GroundStationConstruct{
		Construct: construct,
		SnsTopicArn: snsTopic.Ref(),
	}
}

