package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.ec2.*;
import software.amazon.awscdk.services.efs.*;
import software.amazon.awscdk.services.iam.*;

class EfsConstruct extends Construct {
    private Object mountTargetId;

    private Object fileSystemId;

    public Object getMountTargetId() {
        return this.mountTargetId;
    }

    public Object getFileSystemId() {
        return this.fileSystemId;
    }

    public EfsConstruct(final Construct scope, final String id) {
        this(scope, id, null, null, null, null, null);
    }

    public EfsConstruct(final Construct scope, final String id,
            String instanceType,
            String asgMaxSize,
            String sshLocation,
            String volumeName,
            String mountPoint) {
        super(scope, id);

        instanceType = Optional.ofNullable(instanceType).isPresent() ? instanceType
                : "t2.small";
        asgMaxSize = Optional.ofNullable(asgMaxSize).isPresent() ? asgMaxSize
                : "2";
        sshLocation = Optional.ofNullable(sshLocation).isPresent() ? sshLocation
                : "0.0.0.0/0";
        volumeName = Optional.ofNullable(volumeName).isPresent() ? volumeName
                : "myEFSvolume";
        mountPoint = Optional.ofNullable(mountPoint).isPresent() ? mountPoint
                : "myEFSvolume";
        // Mappings
        final CfnMapping awsInstanceType2Arch = new CfnMapping(this, "awsInstanceType2Arch");
        awsInstanceType2Arch.setValue("t1.micro", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("t2.nano", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("t2.micro", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("t2.small", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("t2.medium", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("t2.large", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m1.small", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m1.medium", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m1.large", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m1.xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m2.xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m2.2xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m2.4xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m3.medium", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m3.large", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m3.xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m3.2xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m4.large", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m4.xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m4.2xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m4.4xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("m4.10xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("c1.medium", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("c1.xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("c3.large", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("c3.xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("c3.2xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("c3.4xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("c3.8xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("c4.large", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("c4.xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("c4.2xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("c4.4xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("c4.8xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("g2.2xlarge", "Arch", "HVMG2");
        awsInstanceType2Arch.setValue("g2.8xlarge", "Arch", "HVMG2");
        awsInstanceType2Arch.setValue("r3.large", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("r3.xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("r3.2xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("r3.4xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("r3.8xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("i2.xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("i2.2xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("i2.4xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("i2.8xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("d2.xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("d2.2xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("d2.4xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("d2.8xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("hi1.4xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("hs1.8xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("cr1.8xlarge", "Arch", "HVM64");
        awsInstanceType2Arch.setValue("cc2.8xlarge", "Arch", "HVM64");

        final CfnMapping awsRegionArch2Ami = new CfnMapping(this, "awsRegionArch2Ami");
        awsRegionArch2Ami.setValue("us-east-1", "HVM64", "ami-0ff8a91507f77f867");
        awsRegionArch2Ami.setValue("us-east-1", "HVMG2", "ami-0a584ac55a7631c0c");
        awsRegionArch2Ami.setValue("us-west-2", "HVM64", "ami-a0cfeed8");
        awsRegionArch2Ami.setValue("us-west-2", "HVMG2", "ami-0e09505bc235aa82d");
        awsRegionArch2Ami.setValue("us-west-1", "HVM64", "ami-0bdb828fd58c52235");
        awsRegionArch2Ami.setValue("us-west-1", "HVMG2", "ami-066ee5fd4a9ef77f1");
        awsRegionArch2Ami.setValue("eu-west-1", "HVM64", "ami-047bb4163c506cd98");
        awsRegionArch2Ami.setValue("eu-west-1", "HVMG2", "ami-0a7c483d527806435");
        awsRegionArch2Ami.setValue("eu-west-2", "HVM64", "ami-f976839e");
        awsRegionArch2Ami.setValue("eu-west-2", "HVMG2", "NOT_SUPPORTED");
        awsRegionArch2Ami.setValue("eu-west-3", "HVM64", "ami-0ebc281c20e89ba4b");
        awsRegionArch2Ami.setValue("eu-west-3", "HVMG2", "NOT_SUPPORTED");
        awsRegionArch2Ami.setValue("eu-central-1", "HVM64", "ami-0233214e13e500f77");
        awsRegionArch2Ami.setValue("eu-central-1", "HVMG2", "ami-06223d46a6d0661c7");
        awsRegionArch2Ami.setValue("ap-northeast-1", "HVM64", "ami-06cd52961ce9f0d85");
        awsRegionArch2Ami.setValue("ap-northeast-1", "HVMG2", "ami-053cdd503598e4a9d");
        awsRegionArch2Ami.setValue("ap-northeast-2", "HVM64", "ami-0a10b2721688ce9d2");
        awsRegionArch2Ami.setValue("ap-northeast-2", "HVMG2", "NOT_SUPPORTED");
        awsRegionArch2Ami.setValue("ap-northeast-3", "HVM64", "ami-0d98120a9fb693f07");
        awsRegionArch2Ami.setValue("ap-northeast-3", "HVMG2", "NOT_SUPPORTED");
        awsRegionArch2Ami.setValue("ap-southeast-1", "HVM64", "ami-08569b978cc4dfa10");
        awsRegionArch2Ami.setValue("ap-southeast-1", "HVMG2", "ami-0be9df32ae9f92309");
        awsRegionArch2Ami.setValue("ap-southeast-2", "HVM64", "ami-09b42976632b27e9b");
        awsRegionArch2Ami.setValue("ap-southeast-2", "HVMG2", "ami-0a9ce9fecc3d1daf8");
        awsRegionArch2Ami.setValue("ap-south-1", "HVM64", "ami-0912f71e06545ad88");
        awsRegionArch2Ami.setValue("ap-south-1", "HVMG2", "ami-097b15e89dbdcfcf4");
        awsRegionArch2Ami.setValue("us-east-2", "HVM64", "ami-0b59bfac6be064b78");
        awsRegionArch2Ami.setValue("us-east-2", "HVMG2", "NOT_SUPPORTED");
        awsRegionArch2Ami.setValue("ca-central-1", "HVM64", "ami-0b18956f");
        awsRegionArch2Ami.setValue("ca-central-1", "HVMG2", "NOT_SUPPORTED");
        awsRegionArch2Ami.setValue("sa-east-1", "HVM64", "ami-07b14488da8ea02a0");
        awsRegionArch2Ami.setValue("sa-east-1", "HVMG2", "NOT_SUPPORTED");
        awsRegionArch2Ami.setValue("cn-north-1", "HVM64", "ami-0a4eaf6c4454eda75");
        awsRegionArch2Ami.setValue("cn-north-1", "HVMG2", "NOT_SUPPORTED");
        awsRegionArch2Ami.setValue("cn-northwest-1", "HVM64", "ami-6b6a7d09");
        awsRegionArch2Ami.setValue("cn-northwest-1", "HVMG2", "NOT_SUPPORTED");


        CfnRole cloudWatchPutMetricsRole = CfnRole.Builder.create(this, "CloudWatchPutMetricsRole")
                .assumeRolePolicyDocument(Map.of("Statement", Arrays.asList(
                        Map.of("Effect", "Allow",
                        "Principal", Map.of("Service", Arrays.asList(
                                "ec2.amazonaws.com")),
                        "Action", Arrays.asList(
                                "sts:AssumeRole")))))
                .path("/")
                .build();

        CfnFileSystem fileSystem = CfnFileSystem.Builder.create(this, "FileSystem")
                .performanceMode("generalPurpose")
                .fileSystemTags(Arrays.asList(
                        CfnFileSystem.ElasticFileSystemTagProperty.builder()
                                .key("Name")
                                .value(volumeName)
                                .build()))
                .build();

        CfnInternetGateway internetGateway = CfnInternetGateway.Builder.create(this, "InternetGateway")
                .tags(Arrays.asList(
                        CfnTag.builder()
                                .key("Application")
                                .value(Stack.of(this).getStackName())
                                .build(),
                        CfnTag.builder()
                                .key("Network")
                                .value("Public")
                                .build()))
                .build();

        CfnVPC vpc = CfnVPC.Builder.create(this, "VPC")
                .enableDnsSupport(true)
                .enableDnsHostnames(true)
                .cidrBlock("10.0.0.0/16")
                .tags(Arrays.asList(
                        CfnTag.builder()
                                .key("Application")
                                .value(Stack.of(this).getStackId())
                                .build()))
                .build();

        CfnInstanceProfile cloudWatchPutMetricsInstanceProfile = CfnInstanceProfile.Builder.create(this, "CloudWatchPutMetricsInstanceProfile")
                .path("/")
                .roles(Arrays.asList(
                        cloudWatchPutMetricsRole.getRef()))
                .build();

        CfnPolicy cloudWatchPutMetricsRolePolicy = CfnPolicy.Builder.create(this, "CloudWatchPutMetricsRolePolicy")
                .policyName("CloudWatch_PutMetricData")
                .policyDocument(Map.of("Version", "2012-10-17",
                "Statement", Arrays.asList(
                        Map.of("Sid", "CloudWatchPutMetricData",
                        "Effect", "Allow",
                        "Action", Arrays.asList(
                                "cloudwatch:PutMetricData"),
                        "Resource", Arrays.asList(
                                "*")))))
                .roles(Arrays.asList(
                        cloudWatchPutMetricsRole.getRef()))
                .build();

        CfnVPCGatewayAttachment gatewayToInternet = CfnVPCGatewayAttachment.Builder.create(this, "GatewayToInternet")
                .vpcId(vpc.getRef())
                .internetGatewayId(internetGateway.getRef())
                .build();

        CfnSecurityGroup instanceSecurityGroup = CfnSecurityGroup.Builder.create(this, "InstanceSecurityGroup")
                .vpcId(vpc.getRef())
                .groupDescription("Enable SSH access via port 22")
                .securityGroupIngress(Arrays.asList(
                        CfnSecurityGroup.IngressProperty.builder()
                                .ipProtocol("tcp")
                                .fromPort(22)
                                .toPort(22)
                                .cidrIp(sshLocation)
                                .build(),
                        CfnSecurityGroup.IngressProperty.builder()
                                .ipProtocol("tcp")
                                .fromPort(80)
                                .toPort(80)
                                .cidrIp("0.0.0.0/0")
                                .build()))
                .build();

        CfnSecurityGroup mountTargetSecurityGroup = CfnSecurityGroup.Builder.create(this, "MountTargetSecurityGroup")
                .vpcId(vpc.getRef())
                .groupDescription("Security group for mount target")
                .securityGroupIngress(Arrays.asList(
                        CfnSecurityGroup.IngressProperty.builder()
                                .ipProtocol("tcp")
                                .fromPort(2049)
                                .toPort(2049)
                                .cidrIp("0.0.0.0/0")
                                .build()))
                .build();

        CfnRouteTable routeTable = CfnRouteTable.Builder.create(this, "RouteTable")
                .vpcId(vpc.getRef())
                .build();

        CfnSubnet subnet = CfnSubnet.Builder.create(this, "Subnet")
                .vpcId(vpc.getRef())
                .cidrBlock("10.0.0.0/24")
                .tags(Arrays.asList(
                        CfnTag.builder()
                                .key("Application")
                                .value(Stack.of(this).getStackId())
                                .build()))
                .build();

        CfnRoute internetGatewayRoute = CfnRoute.Builder.create(this, "InternetGatewayRoute")
                .destinationCidrBlock("0.0.0.0/0")
                .routeTableId(routeTable.getRef())
                .gatewayId(internetGateway.getRef())
                .build();

        CfnMountTarget mountTarget = CfnMountTarget.Builder.create(this, "MountTarget")
                .fileSystemId(fileSystem.getRef())
                .subnetId(subnet.getRef())
                .securityGroups(Arrays.asList(
                        mountTargetSecurityGroup.getRef()))
                .build();

        CfnSubnetRouteTableAssociation subnetRouteTableAssoc = CfnSubnetRouteTableAssociation.Builder.create(this, "SubnetRouteTableAssoc")
                .routeTableId(routeTable.getRef())
                .subnetId(subnet.getRef())
                .build();

        this.mountTargetId = mountTarget.getRef();
        CfnOutput.Builder.create(this, "CfnOutputMountTargetID")
                .key("MountTargetID")
                .value(this.mountTargetId.toString())
                .description("Mount target ID")
                .build();

        this.fileSystemId = fileSystem.getRef();
        CfnOutput.Builder.create(this, "CfnOutputFileSystemID")
                .key("FileSystemID")
                .value(this.fileSystemId.toString())
                .description("File system ID")
                .build();

    }
}
