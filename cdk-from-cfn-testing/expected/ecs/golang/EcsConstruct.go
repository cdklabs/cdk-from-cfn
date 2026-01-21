package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	ecs "github.com/aws/aws-cdk-go/awscdk/v2/awsecs"
	iam "github.com/aws/aws-cdk-go/awscdk/v2/awsiam"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type EcsConstructProps struct {
}

type EcsConstruct struct {
	constructs.Construct
}

func NewEcsConstruct(scope constructs.Construct, id string, props *EcsConstructProps) *EcsConstruct {
	construct := constructs.NewConstruct(scope, &id)

	backendEcsTaskRole := iam.NewCfnRole(
		construct,
		jsii.String("BackendECSTaskRole"),
		&iam.CfnRoleProps{
			Path: jsii.String("/"),
			AssumeRolePolicyDocument: map[string]interface{} {
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Action": jsii.String("sts:AssumeRole"),
						"Effect": jsii.String("Allow"),
						"Principal": map[string]interface{} {
							"Service": jsii.String("ecs-tasks.amazonaws.com"),
						},
					},
				},
			},
		},
	)

	ecsTaskExecutionRole := iam.NewCfnRole(
		construct,
		jsii.String("ECSTaskExecutionRole"),
		&iam.CfnRoleProps{
			Path: jsii.String("/"),
			AssumeRolePolicyDocument: map[string]interface{} {
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Action": jsii.String("sts:AssumeRole"),
						"Effect": jsii.String("Allow"),
						"Principal": map[string]interface{} {
							"Service": jsii.String("ecs-tasks.amazonaws.com"),
						},
					},
				},
			},
			ManagedPolicyArns: &[]*string{
				jsii.String("arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"),
				jsii.String("arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess"),
				jsii.String("arn:aws:iam::aws:policy/SecretsManagerReadWrite"),
			},
		},
	)

	ecs.NewCfnTaskDefinition(
		construct,
		jsii.String("BackendServiceECSTaskDefinition"),
		&ecs.CfnTaskDefinitionProps{
			Family: jsii.String("test"),
			RequiresCompatibilities: &[]*string{
				jsii.String("FARGATE"),
			},
			Memory: jsii.String("1024"),
			Cpu: jsii.String("256"),
			NetworkMode: jsii.String("awsvpc"),
			ExecutionRoleArn: ecsTaskExecutionRole.AttrArn(),
			TaskRoleArn: backendEcsTaskRole.AttrArn(),
			ContainerDefinitions: &[]interface{}{
				&ContainerDefinitionProperty{
					Name: jsii.String("main"),
					Image: jsii.String("nginx"),
					LogConfiguration: &LogConfigurationProperty{
						Options: map[string]interface{} {
							"awslogs-group": jsii.String("/aws/ecs/test/main"),
							"awslogs-region": jsii.String("ap-northeast-1"),
							"awslogs-stream-prefix": jsii.String("ecs"),
						},
						LogDriver: jsii.String("awslogs"),
					},
				},
			},
		},
	)

	return &EcsConstruct{
		Construct: construct,
	}
}

