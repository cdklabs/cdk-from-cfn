package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.ecs.*;
import software.amazon.awscdk.services.iam.*;

class EcsConstruct extends Construct {
    public EcsConstruct(final Construct scope, final String id) {
        super(scope, id);


        CfnRole backendEcsTaskRole = CfnRole.Builder.create(this, "BackendECSTaskRole")
                .path("/")
                .assumeRolePolicyDocument(Map.of("Statement", Arrays.asList(
                        Map.of("Action", "sts:AssumeRole",
                        "Effect", "Allow",
                        "Principal", Map.of("Service", "ecs-tasks.amazonaws.com")))))
                .build();

        CfnRole ecsTaskExecutionRole = CfnRole.Builder.create(this, "ECSTaskExecutionRole")
                .path("/")
                .assumeRolePolicyDocument(Map.of("Statement", Arrays.asList(
                        Map.of("Action", "sts:AssumeRole",
                        "Effect", "Allow",
                        "Principal", Map.of("Service", "ecs-tasks.amazonaws.com")))))
                .managedPolicyArns(Arrays.asList(
                        "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
                        "arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess",
                        "arn:aws:iam::aws:policy/SecretsManagerReadWrite"))
                .build();

        CfnTaskDefinition backendServiceEcsTaskDefinition = CfnTaskDefinition.Builder.create(this, "BackendServiceECSTaskDefinition")
                .family("test")
                .requiresCompatibilities(Arrays.asList(
                        "FARGATE"))
                .memory("1024")
                .cpu("256")
                .networkMode("awsvpc")
                .executionRoleArn(ecsTaskExecutionRole.getAttrArn())
                .taskRoleArn(backendEcsTaskRole.getAttrArn())
                .containerDefinitions(Arrays.asList(
                        CfnTaskDefinition.ContainerDefinitionProperty.builder()
                                .name("main")
                                .image("nginx")
                                .logConfiguration(CfnTaskDefinition.LogConfigurationProperty.builder()
                                        .options(Map.of("awslogs-group", "/aws/ecs/test/main",
                                        "awslogs-region", "ap-northeast-1",
                                        "awslogs-stream-prefix", "ecs"))
                                        .logDriver("awslogs")
                                        .build())
                                .build()))
                .build();

    }
}
