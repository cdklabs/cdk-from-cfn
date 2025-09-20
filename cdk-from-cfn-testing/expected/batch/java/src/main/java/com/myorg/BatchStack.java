package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.batch.*;
import software.amazon.awscdk.services.ec2.*;
import software.amazon.awscdk.services.iam.*;

class BatchStack extends Stack {
    private Object computeEnvironmentArn;

    private Object jobQueueArn;

    private Object jobDefinitionArn;

    public Object getComputeEnvironmentArn() {
        return this.computeEnvironmentArn;
    }

    public Object getJobQueueArn() {
        return this.jobQueueArn;
    }

    public Object getJobDefinitionArn() {
        return this.jobDefinitionArn;
    }

    public BatchStack(final Construct scope, final String id) {
        super(scope, id, null);
    }

    public BatchStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        CfnRole batchServiceRole = CfnRole.Builder.create(this, "BatchServiceRole")
                .assumeRolePolicyDocument(Map.of("Version", "2012-10-17",
                "Statement", Arrays.asList(
                        Map.of("Effect", "Allow",
                        "Principal", Map.of("Service", "batch.amazonaws.com"),
                        "Action", "sts:AssumeRole"))))
                .managedPolicyArns(Arrays.asList(
                        "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"))
                .build();

        CfnRole ecsInstanceRole = CfnRole.Builder.create(this, "EcsInstanceRole")
                .assumeRolePolicyDocument(Map.of("Version", "2008-10-17",
                "Statement", Arrays.asList(
                        Map.of("Sid", "",
                        "Effect", "Allow",
                        "Principal", Map.of("Service", "ec2.amazonaws.com"),
                        "Action", "sts:AssumeRole"))))
                .managedPolicyArns(Arrays.asList(
                        "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"))
                .build();

        CfnInternetGateway internetGateway = CfnInternetGateway.Builder.create(this, "InternetGateway")
                .build();

        CfnJobDefinition jobDefinition = CfnJobDefinition.Builder.create(this, "JobDefinition")
                .type("container")
                .containerProperties(CfnJobDefinition.ContainerPropertiesProperty.builder()
                        .image(String.join("",
                                "137112412989.dkr.ecr.",
                                this.getRegion(),
                                ".amazonaws.com/amazonlinux:latest"))
                        .vcpus(2)
                        .memory(2000)
                        .command(Arrays.asList(
                                "echo",
                                "Hello world"))
                        .build())
                .retryStrategy(CfnJobDefinition.RetryStrategyProperty.builder()
                        .attempts(1)
                        .build())
                .build();

        CfnVPC vpc = CfnVPC.Builder.create(this, "VPC")
                .cidrBlock("10.0.0.0/16")
                .build();

        CfnInstanceProfile iamInstanceProfile = CfnInstanceProfile.Builder.create(this, "IamInstanceProfile")
                .roles(Arrays.asList(
                        ecsInstanceRole.getRef()))
                .build();

        CfnRouteTable routeTable = CfnRouteTable.Builder.create(this, "RouteTable")
                .vpcId(vpc.getRef())
                .build();

        CfnSecurityGroup securityGroup = CfnSecurityGroup.Builder.create(this, "SecurityGroup")
                .groupDescription("EC2 Security Group for instances launched in the VPC by Batch")
                .vpcId(vpc.getRef())
                .build();

        CfnSubnet subnet = CfnSubnet.Builder.create(this, "Subnet")
                .cidrBlock("10.0.0.0/24")
                .vpcId(vpc.getRef())
                .mapPublicIpOnLaunch(true)
                .build();

        CfnVPCGatewayAttachment vpcGatewayAttachment = CfnVPCGatewayAttachment.Builder.create(this, "VPCGatewayAttachment")
                .vpcId(vpc.getRef())
                .internetGatewayId(internetGateway.getRef())
                .build();

        CfnComputeEnvironment computeEnvironment = CfnComputeEnvironment.Builder.create(this, "ComputeEnvironment")
                .type("MANAGED")
                .computeResources(CfnComputeEnvironment.ComputeResourcesProperty.builder()
                        .type("EC2")
                        .minvCpus(0)
                        .desiredvCpus(0)
                        .maxvCpus(64)
                        .instanceTypes(Arrays.asList(
                                "optimal"))
                        .subnets(Arrays.asList(
                                subnet.getRef()))
                        .securityGroupIds(Arrays.asList(
                                securityGroup.getRef()))
                        .instanceRole(iamInstanceProfile.getRef())
                        .build())
                .serviceRole(batchServiceRole.getRef())
                .build();

        CfnRoute route = CfnRoute.Builder.create(this, "Route")
                .routeTableId(routeTable.getRef())
                .destinationCidrBlock("0.0.0.0/0")
                .gatewayId(internetGateway.getRef())
                .build();

        CfnSubnetRouteTableAssociation subnetRouteTableAssociation = CfnSubnetRouteTableAssociation.Builder.create(this, "SubnetRouteTableAssociation")
                .routeTableId(routeTable.getRef())
                .subnetId(subnet.getRef())
                .build();

        CfnJobQueue jobQueue = CfnJobQueue.Builder.create(this, "JobQueue")
                .priority(1)
                .computeEnvironmentOrder(Arrays.asList(
                        CfnJobQueue.ComputeEnvironmentOrderProperty.builder()
                                .order(1)
                                .computeEnvironment(computeEnvironment.getRef())
                                .build()))
                .build();

        this.computeEnvironmentArn = computeEnvironment.getRef();
        CfnOutput.Builder.create(this, "CfnOutputComputeEnvironmentArn")
                .key("ComputeEnvironmentArn")
                .value(this.computeEnvironmentArn.toString())
                .build();

        this.jobQueueArn = jobQueue.getRef();
        CfnOutput.Builder.create(this, "CfnOutputJobQueueArn")
                .key("JobQueueArn")
                .value(this.jobQueueArn.toString())
                .build();

        this.jobDefinitionArn = jobDefinition.getRef();
        CfnOutput.Builder.create(this, "CfnOutputJobDefinitionArn")
                .key("JobDefinitionArn")
                .value(this.jobDefinitionArn.toString())
                .build();

    }
}
