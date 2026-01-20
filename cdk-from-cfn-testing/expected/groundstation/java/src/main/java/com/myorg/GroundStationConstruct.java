package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.ec2.*;
import software.amazon.awscdk.services.events.*;
import software.amazon.awscdk.services.groundstation.*;
import software.amazon.awscdk.services.iam.*;
import software.amazon.awscdk.services.lambda.*;
import software.amazon.awscdk.services.s3.*;
import software.amazon.awscdk.services.sns.*;

class GroundStationConstruct extends Construct {
    private Object snsTopicArn;

    public Object getSnsTopicArn() {
        return this.snsTopicArn;
    }

    public GroundStationConstruct(final Construct scope, final String id) {
        this(scope, id, null, null, null, null, null, null, null, null);
    }

    public GroundStationConstruct(final Construct scope, final String id,
            String groundStationS3DataDeliveryBucketName,
            String notificationEmail,
            String satelliteName,
            String softwareS3Bucket,
            String sshCidrBlock,
            String sshKeyName,
            String vpcId,
            String subnetId) {
        super(scope, id);

        groundStationS3DataDeliveryBucketName = Optional.ofNullable(groundStationS3DataDeliveryBucketName).isPresent() ? groundStationS3DataDeliveryBucketName
                : "aws-groundstation-s3dd-your-bucket";
        notificationEmail = Optional.ofNullable(notificationEmail).isPresent() ? notificationEmail
                : "someone@somewhere.com";
        satelliteName = Optional.ofNullable(satelliteName).isPresent() ? satelliteName
                : "JPSS1";
        softwareS3Bucket = Optional.ofNullable(softwareS3Bucket).isPresent() ? softwareS3Bucket
                : "your-software-bucket";
        sshCidrBlock = Optional.ofNullable(sshCidrBlock).isPresent() ? sshCidrBlock
                : "15.16.17.18/32";
        sshKeyName = Optional.ofNullable(sshKeyName).isPresent()
                ? sshKeyName
                : CfnParameter.Builder.create(this, "SshKeyName")
                        .type("AWS::EC2::KeyPair::KeyName")
                        .defaultValue("")
                        .build()
                        .getValueAsString();

        vpcId = Optional.ofNullable(vpcId).isPresent()
                ? vpcId
                : CfnParameter.Builder.create(this, "VpcId")
                        .type("AWS::EC2::VPC::Id")
                        .defaultValue("")
                        .build()
                        .getValueAsString();

        subnetId = Optional.ofNullable(subnetId).isPresent()
                ? subnetId
                : CfnParameter.Builder.create(this, "SubnetId")
                        .type("AWS::EC2::Subnet::Id")
                        .defaultValue("")
                        .build()
                        .getValueAsString();


        Stack.of(this).addTransform("AWS::Serverless-2016-10-31");
        // Mappings
        final CfnMapping amiMap = new CfnMapping(this, "amiMap");
        amiMap.setValue("eu-north-1", "ami", "ami-0abb1aa57ecf6a060");
        amiMap.setValue("eu-west-1", "ami", "ami-082af980f9f5514f8");
        amiMap.setValue("me-south-1", "ami", "ami-0687a5f8dac57444e");
        amiMap.setValue("us-east-1", "ami", "ami-03c7d01cf4dedc891");
        amiMap.setValue("us-east-2", "ami", "ami-06d5c50c30a35fb88");
        amiMap.setValue("us-west-2", "ami", "ami-0ac64ad8517166fb1");
        amiMap.setValue("ap-southeast-2", "ami", "ami-0074f30ddebf60493");
        amiMap.setValue("af-south-1", "ami", "ami-0764fb4fffa117039");
        amiMap.setValue("ap-northeast-2", "ami", "ami-03db74b70e1da9c56");
        amiMap.setValue("ap-southeast-1", "ami", "ami-0b3a4110c36b9a5f0");
        amiMap.setValue("eu-central-1", "ami", "ami-0adbcf08fdd664fed");
        amiMap.setValue("sa-east-1", "ami", "ami-0c5cdf1548242305d");


        CfnBucket groundStationS3DataDeliveryBucket = CfnBucket.Builder.create(this, "GroundStationS3DataDeliveryBucket")
                .bucketName(groundStationS3DataDeliveryBucketName)
                .build();

        groundStationS3DataDeliveryBucket.applyRemovalPolicy(RemovalPolicy.RETAIN);

        CfnRole groundStationS3DataDeliveryRole = CfnRole.Builder.create(this, "GroundStationS3DataDeliveryRole")
                .assumeRolePolicyDocument(Map.of("Statement", Arrays.asList(
                        Map.of("Action", Arrays.asList(
                                "sts:AssumeRole"),
                        "Effect", "Allow",
                        "Principal", Map.of("Service", Arrays.asList(
                                "groundstation.amazonaws.com")),
                        "Condition", Map.of("StringEquals", Map.of("aws:SourceAccount", Stack.of(this).getAccount()),
                        "ArnLike", Map.of("aws:SourceArn", "arn:aws:groundstation:" + Stack.of(this).getRegion() + ":" + Stack.of(this).getAccount() + ":config/s3-recording/*"))))))
                .build();

        CfnEIP instanceEip = CfnEIP.Builder.create(this, "InstanceEIP")
                .domain("vpc")
                .build();

        CfnRole instanceRole = CfnRole.Builder.create(this, "InstanceRole")
                .assumeRolePolicyDocument(Map.of("Version", "2012-10-17",
                "Statement", Arrays.asList(
                        Map.of("Effect", "Allow",
                        "Principal", Map.of("Service", Arrays.asList(
                                "ec2.amazonaws.com")),
                        "Action", Arrays.asList(
                                "sts:AssumeRole")))))
                .path("/")
                .managedPolicyArns(Arrays.asList(
                        "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy",
                        "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"))
                .build();

        CfnSecurityGroup instanceSecurityGroup = CfnSecurityGroup.Builder.create(this, "InstanceSecurityGroup")
                .groupDescription("AWS Ground Station receiver instance security group.")
                .vpcId(vpcId)
                .securityGroupIngress(Arrays.asList(
                        CfnSecurityGroup.IngressProperty.builder()
                                .ipProtocol("tcp")
                                .fromPort(22)
                                .toPort(22)
                                .cidrIp(sshCidrBlock)
                                .description("Inbound SSH access")
                                .build()))
                .build();

        CfnConfig snppJpssDownlinkDemodDecodeAntennaConfig = CfnConfig.Builder.create(this, "SnppJpssDownlinkDemodDecodeAntennaConfig")
                .name("JPSS1 Downlink Demod Decode Antenna Config")
                .configData(CfnConfig.ConfigDataProperty.builder()
                        .antennaDownlinkDemodDecodeConfig(CfnConfig.AntennaDownlinkDemodDecodeConfigProperty.builder()
                                .spectrumConfig(CfnConfig.SpectrumConfigProperty.builder()
                                        .centerFrequency(CfnConfig.FrequencyProperty.builder()
                                                .value(7812)
                                                .units("MHz")
                                                .build())
                                        .polarization("RIGHT_HAND")
                                        .bandwidth(CfnConfig.FrequencyBandwidthProperty.builder()
                                                .value(30)
                                                .units("MHz")
                                                .build())
                                        .build())
                                .demodulationConfig(CfnConfig.DemodulationConfigProperty.builder()
                                        .unvalidatedJson("{ "type":"QPSK", "qpsk":{ "carrierFrequencyRecovery":{ "centerFrequency":{ "value":7812, "units":"MHz" }, "range":{ "value":250, "units":"kHz" } }, "symbolTimingRecovery":{ "symbolRate":{ "value":15, "units":"Msps" }, "range":{ "value":0.75, "units":"ksps" }, "matchedFilter":{ "type":"ROOT_RAISED_COSINE", "rolloffFactor":0.5 } } } }")
                                        .build())
                                .decodeConfig(CfnConfig.DecodeConfigProperty.builder()
                                        .unvalidatedJson("{ "edges":[ { "from":"I-Ingress", "to":"IQ-Recombiner" }, { "from":"Q-Ingress", "to":"IQ-Recombiner" }, { "from":"IQ-Recombiner", "to":"CcsdsViterbiDecoder" }, { "from":"CcsdsViterbiDecoder", "to":"NrzmDecoder" }, { "from":"NrzmDecoder", "to":"UncodedFramesEgress" } ], "nodeConfigs":{ "I-Ingress":{ "type":"CODED_SYMBOLS_INGRESS", "codedSymbolsIngress":{ "source":"I" } }, "Q-Ingress":{ "type":"CODED_SYMBOLS_INGRESS", "codedSymbolsIngress":{ "source":"Q" } }, "IQ-Recombiner":{ "type":"IQ_RECOMBINER" }, "CcsdsViterbiDecoder":{ "type":"CCSDS_171_133_VITERBI_DECODER", "ccsds171133ViterbiDecoder":{ "codeRate":"ONE_HALF" } }, "NrzmDecoder":{ "type":"NRZ_M_DECODER" }, "UncodedFramesEgress":{ "type":"UNCODED_FRAMES_EGRESS" } } }")
                                        .build())
                                .build())
                        .build())
                .build();

        CfnConfig trackingConfig = CfnConfig.Builder.create(this, "TrackingConfig")
                .name("JPSS1 Tracking Config")
                .configData(CfnConfig.ConfigDataProperty.builder()
                        .trackingConfig(CfnConfig.TrackingConfigProperty.builder()
                                .autotrack("PREFERRED")
                                .build())
                        .build())
                .build();

        CfnTopic snsTopic = CfnTopic.Builder.create(this, "snsTopic")
                .displayName(String.join("-",
                        "GS-S3-Data-Delivery",
                        satelliteName))
                .subscription(Arrays.asList(
                        CfnTopic.SubscriptionProperty.builder()
                                .endpoint(notificationEmail)
                                .protocol("email")
                                .build()))
                .build();

        CfnInstanceProfile generalInstanceProfile = CfnInstanceProfile.Builder.create(this, "GeneralInstanceProfile")
                .roles(Arrays.asList(
                        instanceRole.getRef()))
                .build();

        generalInstanceProfile.addDependency(instanceRole);

        CfnPolicy groundStationS3DataDeliveryIamPolicy = CfnPolicy.Builder.create(this, "GroundStationS3DataDeliveryIamPolicy")
                .policyDocument(Map.of("Version", "2012-10-17",
                "Statement", Arrays.asList(
                        Map.of("Action", Arrays.asList(
                                "s3:GetBucketLocation"),
                        "Effect", "Allow",
                        "Resource", Arrays.asList(
                                String.join("",
                                        "arn:aws:s3:::",
                                        groundStationS3DataDeliveryBucketName))),
                        Map.of("Action", Arrays.asList(
                                "s3:PutObject"),
                        "Effect", "Allow",
                        "Resource", Arrays.asList(
                                String.join("",
                                        "arn:aws:s3:::",
                                        groundStationS3DataDeliveryBucketName,
                                        "/*"))))))
                .policyName("GroundStationS3DataDeliveryPolicy")
                .roles(Arrays.asList(
                        groundStationS3DataDeliveryRole.getRef()))
                .build();

        CfnManagedPolicy instanceRoleEc2Policy = CfnManagedPolicy.Builder.create(this, "InstanceRoleEC2Policy")
                .policyDocument(Map.of("Version", "2012-10-17",
                "Statement", Arrays.asList(
                        Map.of("Action", Arrays.asList(
                                "ec2:DescribeTags"),
                        "Effect", "Allow",
                        "Resource", "*"))))
                .roles(Arrays.asList(
                        instanceRole.getRef()))
                .build();

        CfnManagedPolicy instanceRoleS3Policy = CfnManagedPolicy.Builder.create(this, "InstanceRoleS3Policy")
                .policyDocument(Map.of("Version", "2012-10-17",
                "Statement", Arrays.asList(
                        Map.of("Action", Arrays.asList(
                                "s3:PutObject",
                                "s3:GetObject"),
                        "Effect", "Allow",
                        "Resource", String.join("",
                                "arn:aws:s3:::",
                                softwareS3Bucket,
                                "/*")),
                        Map.of("Action", Arrays.asList(
                                "s3:GetObject"),
                        "Effect", "Allow",
                        "Resource", String.join("",
                                "arn:aws:s3:::",
                                "space-solutions-",
                                "eu-west-1",
                                "/*")),
                        Map.of("Action", Arrays.asList(
                                "s3:PutObject",
                                "s3:GetObject"),
                        "Effect", "Allow",
                        "Resource", String.join("",
                                "arn:aws:s3:::",
                                groundStationS3DataDeliveryBucket.getRef(),
                                "/*")),
                        Map.of("Action", Arrays.asList(
                                "s3:ListBucket"),
                        "Effect", "Allow",
                        "Resource", String.join("",
                                "arn:aws:s3:::",
                                softwareS3Bucket)),
                        Map.of("Action", Arrays.asList(
                                "s3:ListBucket"),
                        "Effect", "Allow",
                        "Resource", String.join("",
                                "arn:aws:s3:::",
                                "space-solutions-",
                                "eu-west-1",
                                "/*")),
                        Map.of("Action", Arrays.asList(
                                "s3:ListBucket"),
                        "Effect", "Allow",
                        "Resource", String.join("",
                                "arn:aws:s3:::",
                                groundStationS3DataDeliveryBucket.getRef())))))
                .roles(Arrays.asList(
                        instanceRole.getRef()))
                .build();

        CfnManagedPolicy instanceRoleSnsPolicy = CfnManagedPolicy.Builder.create(this, "InstanceRoleSNSPolicy")
                .policyDocument(Map.of("Version", "2012-10-17",
                "Statement", Arrays.asList(
                        Map.of("Action", Arrays.asList(
                                "sns:Publish"),
                        "Effect", "Allow",
                        "Resource", snsTopic.getRef()))))
                .roles(Arrays.asList(
                        instanceRole.getRef()))
                .build();

        CfnNetworkInterface receiverInstanceNetworkInterfacePublic = CfnNetworkInterface.Builder.create(this, "ReceiverInstanceNetworkInterfacePublic")
                .description("Public network interface for troubleshooting")
                .groupSet(Arrays.asList(
                        instanceSecurityGroup.getRef()))
                .subnetId(subnetId)
                .build();

        CfnEIPAssociation instanceEipAsscociation = CfnEIPAssociation.Builder.create(this, "InstanceEIPAsscociation")
                .allocationId(instanceEip.getAttrAllocationId())
                .networkInterfaceId(receiverInstanceNetworkInterfacePublic.getRef())
                .build();

        CfnInstance receiverInstance = CfnInstance.Builder.create(this, "ReceiverInstance")
                .disableApiTermination(false)
                .iamInstanceProfile(generalInstanceProfile.getRef())
                .imageId(amiMap.findInMap(Stack.of(this).getRegion(), "ami"))
                .instanceType("c5.4xlarge")
                .keyName(sshKeyName)
                .monitoring(true)
                .networkInterfaces(Arrays.asList(
                        CfnInstance.NetworkInterfaceProperty.builder()
                                .networkInterfaceId(receiverInstanceNetworkInterfacePublic.getRef())
                                .deviceIndex(0)
                                .deleteOnTermination(false)
                                .build()))
                .blockDeviceMappings(Arrays.asList(
                        CfnInstance.BlockDeviceMappingProperty.builder()
                                .deviceName("/dev/xvda")
                                .ebs(CfnInstance.EbsProperty.builder()
                                        .volumeType("gp2")
                                        .volumeSize(100)
                                        .build())
                                .build()))
                .tags(Arrays.asList(
                        CfnTag.builder()
                                .key("Name")
                                .value(String.join("-",
                                        "Receiver",
                                        Stack.of(this).getStackName()))
                                .build()))
                .userData(Fn.base64("#!/bin/bash

                exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
                echo `date +'%F %R:%S'` "INFO: Logging Setup" >&2

                echo "Setting instance hostname"
                export INSTANCE=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
                export HOSTNAME=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE" "Name=key,Values=Name" --region=" + Stack.of(this).getRegion() + " --output=text |cut -f5)
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
                aws s3 cp --region " + Stack.of(this).getRegion() + " "s3://" + softwareS3Bucket + "/software/RT-STPS/rt-stps-process.sh" "$PROCESS_SCRIPT"
                chmod +x "$PROCESS_SCRIPT"
                chown ec2-user:ec2-user "$PROCESS_SCRIPT"

                echo "Adding call to $PROCESS_SCRIPT into /etc/rc.local"
                echo "TIMESTR=\$(date '+%Y%m%d-%H%M')" >> /etc/rc.local
                echo "$PROCESS_SCRIPT " + satelliteName + " " + softwareS3Bucket + " " + groundStationS3DataDeliveryBucketName + " 2>&1 | tee $GROUND_STATION_BIN_DIR/data-capture_\$TIMESTR.log" >> /etc/rc.local
                chmod +x /etc/rc.d/rc.local

                echo "Creating /opt/aws/groundstation/bin/getSNSTopic.sh"
                echo "export SNS_TOPIC=" + snsTopic.getRef() + "" > /opt/aws/groundstation/bin/getSNSTopic.sh
                chmod +x /opt/aws/groundstation/bin/getSNSTopic.sh

                echo "Sending completion SNS notification"
                export MESSAGE="GroundStation setup is complete for Satellite: " + satelliteName + ".  The RT-STPS processor EC2 instance is all setup and ready to go! It will be automatically started after data from a satellite pass has been deposited in your S3 bucket.  Data will be processed using RT-STPS, then copied to the following S3 Bucket: " + groundStationS3DataDeliveryBucketName + ".  A summary of the contact will be emailed to " + notificationEmail + ". The EC2 instance will now be stopped."
                aws sns publish --topic-arn " + snsTopic.getRef() + " --message "$MESSAGE" --region " + Stack.of(this).getRegion() + "

                echo "Shutting down the EC2 instance"
                shutdown -h now

                exit 0
                "))
                .build();

        receiverInstance.addDependency(instanceSecurityGroup);
        receiverInstance.addDependency(generalInstanceProfile);

        CfnConfig s3RecordingConfig = CfnConfig.Builder.create(this, "S3RecordingConfig")
                .name("JPSS1 Recording Config")
                .configData(CfnConfig.ConfigDataProperty.builder()
                        .s3RecordingConfig(CfnConfig.S3RecordingConfigProperty.builder()
                                .bucketArn(String.join("",
                                        "arn:aws:s3:::",
                                        groundStationS3DataDeliveryBucketName))
                                .roleArn(groundStationS3DataDeliveryRole.getAttrArn())
                                .prefix("data/JPSS1/{year}/{month}/{day}")
                                .build())
                        .build())
                .build();

        s3RecordingConfig.addDependency(groundStationS3DataDeliveryBucket);
        s3RecordingConfig.addDependency(groundStationS3DataDeliveryIamPolicy);

        CfnManagedPolicy groundStationS3ddLambdaRolePolicy = CfnManagedPolicy.Builder.create(this, "GroundStationS3ddLambdaRolePolicy")
                .policyDocument(Map.of("Version", "2012-10-17",
                "Statement", Arrays.asList(
                        Map.of("Effect", "Allow",
                        "Action", Arrays.asList(
                                "ec2:StartInstances",
                                "ec2:StopInstances",
                                "ec2:CreateTags"),
                        "Resource", Arrays.asList(
                                "arn:aws:ec2:" + Stack.of(this).getRegion() + ":" + Stack.of(this).getAccount() + ":instance/" + receiverInstance.getRef())),
                        Map.of("Effect", "Allow",
                        "Action", Arrays.asList(
                                "ec2:DescribeInstanceStatus",
                                "ec2:DescribeNetworkInterfaces"),
                        "Resource", Arrays.asList(
                                "*")),
                        Map.of("Effect", "Allow",
                        "Action", Arrays.asList(
                                "sns:Publish"),
                        "Resource", snsTopic.getRef()),
                        Map.of("Effect", "Allow",
                        "Action", Arrays.asList(
                                "s3:PutObject",
                                "s3:PutObjectAcl",
                                "s3:GetObject",
                                "s3:DeleteObjectVersion",
                                "s3:DeleteObject"),
                        "Resource", Arrays.asList(
                                String.join("",
                                        "arn:aws:s3:::",
                                        groundStationS3DataDeliveryBucketName,
                                        "/*"))),
                        Map.of("Effect", "Allow",
                        "Action", Arrays.asList(
                                "s3:ListBucket"),
                        "Resource", Arrays.asList(
                                String.join("",
                                        "arn:aws:s3:::",
                                        groundStationS3DataDeliveryBucketName))))))
                .build();

        CfnMissionProfile snppJpssDemodDecodeMissionProfile = CfnMissionProfile.Builder.create(this, "SnppJpssDemodDecodeMissionProfile")
                .name("43013 JPSS1 Demod Decode to S3")
                .contactPrePassDurationSeconds(120)
                .contactPostPassDurationSeconds(120)
                .minimumViableContactDurationSeconds(180)
                .trackingConfigArn(trackingConfig.getRef())
                .dataflowEdges(Arrays.asList(
                        CfnMissionProfile.DataflowEdgeProperty.builder()
                                .source(String.join("/",
                                        snppJpssDownlinkDemodDecodeAntennaConfig.getRef(),
                                        "UncodedFramesEgress"))
                                .destination(s3RecordingConfig.getRef())
                                .build()))
                .build();

        CfnRole groundStationS3ddLambdaRole = CfnRole.Builder.create(this, "GroundStationS3ddLambdaRole")
                .path("/")
                .managedPolicyArns(Arrays.asList(
                        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
                        groundStationS3ddLambdaRolePolicy.getRef()))
                .assumeRolePolicyDocument(Map.of("Version", "2012-10-17",
                "Statement", Arrays.asList(
                        Map.of("Effect", "Allow",
                        "Principal", Map.of("Service", "lambda.amazonaws.com"),
                        "Action", Arrays.asList(
                                "sts:AssumeRole")))))
                .build();

        CfnFunction lambdaFunctionStartRtstps = CfnFunction.Builder.create(this, "LambdaFunctionStartRtstps")
                .environment(CfnFunction.EnvironmentProperty.builder()
                        .variables(Map.of("RtstpsInstance", receiverInstance.getRef()))
                        .build())
                .handler("index.handle_cloudwatch_event")
                .runtime("python3.9")
                .memorySize(512)
                .timeout(300)
                .role(groundStationS3ddLambdaRole.getAttrArn())
                .code(CfnFunction.CodeProperty.builder()
                        .s3Bucket(softwareS3Bucket)
                        .s3Key("software/RT-STPS/lambda.zip")
                        .build())
                .build();

        CfnRule s3ContactCompleteEventRule = CfnRule.Builder.create(this, "S3ContactCompleteEventRule")
                .description("Triggered when all files have been uploaded for a Ground Station S3 data delivery contact")
                .eventPattern(Map.of("source", Arrays.asList(
                        "aws.groundstation"),
                "detail-type", Arrays.asList(
                        "Ground Station S3 Upload Complete")))
                .state("ENABLED")
                .targets(Arrays.asList(
                        CfnRule.TargetProperty.builder()
                                .arn(lambdaFunctionStartRtstps.getAttrArn())
                                .id("LambdaFunctionStartRtstps")
                                .build()))
                .build();

        CfnPermission permissionForGroundStationCloudWatchEventsToInvokeLambda = CfnPermission.Builder.create(this, "PermissionForGroundStationCloudWatchEventsToInvokeLambda")
                .functionName(lambdaFunctionStartRtstps.getRef())
                .action("lambda:InvokeFunction")
                .principal("events.amazonaws.com")
                .sourceArn(s3ContactCompleteEventRule.getAttrArn())
                .build();

        this.snsTopicArn = snsTopic.getRef();
        CfnOutput.Builder.create(this, "CfnOutputSnsTopicArn")
                .key("SnsTopicArn")
                .value(this.snsTopicArn.toString())
                .exportName(Stack.of(this).getStackName() + "-SnsTopicArn")
                .build();

    }
}
