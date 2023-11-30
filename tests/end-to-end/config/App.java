package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.config.*;
import software.amazon.awscdk.services.ec2.*;
import software.amazon.awscdk.services.iam.*;
import software.amazon.awscdk.services.lambda.*;
import software.amazon.awscdk.services.s3.*;
import software.amazon.awscdk.services.sns.*;

class ConfigStack extends Stack {
    private Object configRuleForVolumeTagsArn;

    private Object configRuleForVolumeTagsConfigRuleId;

    private Object configRuleForVolumeAutoEnableIoComplianceType;

    public Object getConfigRuleForVolumeTagsArn() {
        return this.configRuleForVolumeTagsArn;
    }

    public Object getConfigRuleForVolumeTagsConfigRuleId() {
        return this.configRuleForVolumeTagsConfigRuleId;
    }

    public Object getConfigRuleForVolumeAutoEnableIoComplianceType() {
        return this.configRuleForVolumeAutoEnableIoComplianceType;
    }

    public ConfigStack(final Construct scope, final String id) {
        super(scope, id, null);
    }

    public ConfigStack(final Construct scope, final String id, final StackProps props) {
        this(scope, id, props, null, null);
    }

    public ConfigStack(final Construct scope, final String id, final StackProps props,
            Boolean ec2VolumeAutoEnableIo,
            String ec2VolumeTagKey) {
        super(scope, id, props);

        ec2VolumeAutoEnableIo = Optional.ofNullable(ec2VolumeAutoEnableIo).isPresent() ? ec2VolumeAutoEnableIo
                : false;
        ec2VolumeTagKey = Optional.ofNullable(ec2VolumeTagKey).isPresent() ? ec2VolumeTagKey
                : "CostCenter";

        CfnBucket configBucket = CfnBucket.Builder.create(this, "ConfigBucket")
                .build();

        CfnTopic configTopic = CfnTopic.Builder.create(this, "ConfigTopic")
                .build();

        CfnVolume ec2Volume = CfnVolume.Builder.create(this, "Ec2Volume")
                .autoEnableIo(ec2VolumeAutoEnableIo)
                .size(5)
                .availabilityZone(Fn.select(0, Fn.getAzs("")))
                .tags(Arrays.asList(
                        CfnTag.builder()
                                .key(ec2VolumeTagKey)
                                .value("Ec2VolumeTagValue")
                                .build()))
                .build();

        CfnRole lambdaExecutionRole = CfnRole.Builder.create(this, "LambdaExecutionRole")
                .assumeRolePolicyDocument(Map.of("Version", "2012-10-17",
                "Statement", Arrays.asList(
                        Map.of("Effect", "Allow",
                        "Principal", Map.of("Service", Arrays.asList(
                                "lambda.amazonaws.com")),
                        "Action", Arrays.asList(
                                "sts:AssumeRole")))))
                .policies(Arrays.asList(
                        CfnRole.PolicyProperty.builder()
                                .policyName("root")
                                .policyDocument(Map.of("Version", "2012-10-17",
                                "Statement", Arrays.asList(
                                        Map.of("Effect", "Allow",
                                        "Action", Arrays.asList(
                                                "logs:*",
                                                "config:PutEvaluations",
                                                "ec2:DescribeVolumeAttribute"),
                                        "Resource", "*"))))
                                .build()))
                .build();

        CfnRole configRole = CfnRole.Builder.create(this, "ConfigRole")
                .assumeRolePolicyDocument(Map.of("Version", "2012-10-17",
                "Statement", Arrays.asList(
                        Map.of("Effect", "Allow",
                        "Principal", Map.of("Service", Arrays.asList(
                                "config.amazonaws.com")),
                        "Action", Arrays.asList(
                                "sts:AssumeRole")))))
                .managedPolicyArns(Arrays.asList(
                        "arn:aws:iam::aws:policy/service-role/AWSConfigRole"))
                .policies(Arrays.asList(
                        CfnRole.PolicyProperty.builder()
                                .policyName("root")
                                .policyDocument(Map.of("Version", "2012-10-17",
                                "Statement", Arrays.asList(
                                        Map.of("Effect", "Allow",
                                        "Action", "s3:GetBucketAcl",
                                        "Resource", String.join("",
                                                "arn:aws:s3:::",
                                                configBucket.getRef())),
                                        Map.of("Effect", "Allow",
                                        "Action", "s3:PutObject",
                                        "Resource", String.join("",
                                                "arn:aws:s3:::",
                                                configBucket.getRef(),
                                                "/AWSLogs/",
                                                this.getAccount(),
                                                "/*"),
                                        "Condition", Map.of("StringEquals", Map.of("s3:x-amz-acl", "bucket-owner-full-control"))),
                                        Map.of("Effect", "Allow",
                                        "Action", "config:Put*",
                                        "Resource", "*"))))
                                .build()))
                .build();

        CfnTopicPolicy configTopicPolicy = CfnTopicPolicy.Builder.create(this, "ConfigTopicPolicy")
                .policyDocument(Map.of("Id", "ConfigTopicPolicy",
                "Version", "2012-10-17",
                "Statement", Arrays.asList(
                        Map.of("Effect", "Allow",
                        "Principal", Map.of("Service", "config.amazonaws.com"),
                        "Action", "SNS:Publish",
                        "Resource", "*"))))
                .topics(Arrays.asList(
                        configTopic.getRef()))
                .build();

        CfnDeliveryChannel deliveryChannel = CfnDeliveryChannel.Builder.create(this, "DeliveryChannel")
                .configSnapshotDeliveryProperties(CfnDeliveryChannel.ConfigSnapshotDeliveryPropertiesProperty.builder()
                        .deliveryFrequency("Six_Hours")
                        .build())
                .s3BucketName(configBucket.getRef())
                .snsTopicArn(configTopic.getRef())
                .build();

        CfnFunction volumeAutoEnableIoComplianceCheck = CfnFunction.Builder.create(this, "VolumeAutoEnableIOComplianceCheck")
                .code(CfnFunction.CodeProperty.builder()
                        .zipFile(String.join("\n",
                                "var aws  = require('aws-sdk');",
                                "var config = new aws.ConfigService();",
                                "var ec2 = new aws.EC2();",
                                "exports.handler = function(event, context) {",
                                "    compliance = evaluateCompliance(event, function(compliance, event) {",
                                "        var configurationItem = JSON.parse(event.invokingEvent).configurationItem;",
                                "        var putEvaluationsRequest = {",
                                "            Evaluations: [{",
                                "                ComplianceResourceType: configurationItem.resourceType,",
                                "                ComplianceResourceId: configurationItem.resourceId,",
                                "                ComplianceType: compliance,",
                                "                OrderingTimestamp: configurationItem.configurationItemCaptureTime",
                                "            }],",
                                "            ResultToken: event.resultToken",
                                "        };",
                                "        config.putEvaluations(putEvaluationsRequest, function(err, data) {",
                                "            if (err) context.fail(err);",
                                "            else context.succeed(data);",
                                "        });",
                                "    });",
                                "};",
                                "function evaluateCompliance(event, doReturn) {",
                                "    var configurationItem = JSON.parse(event.invokingEvent).configurationItem;",
                                "    var status = configurationItem.configurationItemStatus;",
                                "    if (configurationItem.resourceType !== 'AWS::EC2::Volume' || event.eventLeftScope || (status !== 'OK' && status !== 'ResourceDiscovered'))",
                                "        doReturn('NOT_APPLICABLE', event);",
                                "    else ec2.describeVolumeAttribute({VolumeId: configurationItem.resourceId, Attribute: 'autoEnableIO'}, function(err, data) {",
                                "        if (err) context.fail(err);",
                                "        else if (data.AutoEnableIO.Value) doReturn('COMPLIANT', event);",
                                "        else doReturn('NON_COMPLIANT', event);",
                                "    });",
                                "}"))
                        .build())
                .handler("index.handler")
                .runtime("nodejs")
                .timeout(30)
                .role(lambdaExecutionRole.getAttrArn())
                .build();

        CfnPermission configPermissionToCallLambda = CfnPermission.Builder.create(this, "ConfigPermissionToCallLambda")
                .functionName(volumeAutoEnableIoComplianceCheck.getAttrArn())
                .action("lambda:InvokeFunction")
                .principal("config.amazonaws.com")
                .build();

        CfnConfigurationRecorder configRecorder = CfnConfigurationRecorder.Builder.create(this, "ConfigRecorder")
                .name("default")
                .recordingGroup(CfnConfigurationRecorder.RecordingGroupProperty.builder()
                        .resourceTypes(Arrays.asList(
                                "AWS::EC2::Volume"))
                        .build())
                .roleArn(configRole.getAttrArn())
                .build();

        CfnConfigRule configRuleForVolumeAutoEnableIo = CfnConfigRule.Builder.create(this, "ConfigRuleForVolumeAutoEnableIO")
                .configRuleName("ConfigRuleForVolumeAutoEnableIO")
                .scope(CfnConfigRule.ScopeProperty.builder()
                        .complianceResourceId(ec2Volume.getRef())
                        .complianceResourceTypes(Arrays.asList(
                                "AWS::EC2::Volume"))
                        .build())
                .source(CfnConfigRule.SourceProperty.builder()
                        .owner("CUSTOM_LAMBDA")
                        .sourceDetails(Arrays.asList(
                                CfnConfigRule.SourceDetailProperty.builder()
                                        .eventSource("aws.config")
                                        .messageType("ConfigurationItemChangeNotification")
                                        .build()))
                        .sourceIdentifier(volumeAutoEnableIoComplianceCheck.getAttrArn())
                        .build())
                .build();

        configRuleForVolumeAutoEnableIo.addDependency(configPermissionToCallLambda);
        configRuleForVolumeAutoEnableIo.addDependency(configRecorder);

        CfnConfigRule configRuleForVolumeTags = CfnConfigRule.Builder.create(this, "ConfigRuleForVolumeTags")
                .inputParameters(Map.of("tag1Key", "CostCenter"))
                .scope(CfnConfigRule.ScopeProperty.builder()
                        .complianceResourceTypes(Arrays.asList(
                                "AWS::EC2::Volume"))
                        .build())
                .source(CfnConfigRule.SourceProperty.builder()
                        .owner("AWS")
                        .sourceIdentifier("REQUIRED_TAGS")
                        .build())
                .build();

        configRuleForVolumeTags.addDependency(configRecorder);

        this.configRuleForVolumeTagsArn = configRuleForVolumeTags.getAttrArn();
        CfnOutput.Builder.create(this, "CfnOutputConfigRuleForVolumeTagsArn")
                .key("ConfigRuleForVolumeTagsArn")
                .value(this.configRuleForVolumeTagsArn.toString())
                .build();

        this.configRuleForVolumeTagsConfigRuleId = configRuleForVolumeTags.getAttrConfigRuleId();
        CfnOutput.Builder.create(this, "CfnOutputConfigRuleForVolumeTagsConfigRuleId")
                .key("ConfigRuleForVolumeTagsConfigRuleId")
                .value(this.configRuleForVolumeTagsConfigRuleId.toString())
                .build();

        this.configRuleForVolumeAutoEnableIoComplianceType = configRuleForVolumeAutoEnableIo.getAttrComplianceType();
        CfnOutput.Builder.create(this, "CfnOutputConfigRuleForVolumeAutoEnableIOComplianceType")
                .key("ConfigRuleForVolumeAutoEnableIOComplianceType")
                .value(this.configRuleForVolumeAutoEnableIoComplianceType.toString())
                .build();

    }
}
