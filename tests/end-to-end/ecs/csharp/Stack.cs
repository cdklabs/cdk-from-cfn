using Amazon.CDK;
using Amazon.CDK.AWS.ECS;
using Amazon.CDK.AWS.IAM;
using Constructs;
using System.Collections.Generic;

namespace EcsStack
{
    public class EcsStackProps : StackProps
    {
    }

    public class EcsStack : Stack
    {
        public EcsStack(Construct scope, string id, EcsStackProps props = null) : base(scope, id, props)
        {

            // Resources
            var backendEcsTaskRole = new CfnRole(this, "BackendECSTaskRole", new CfnRoleProps
            {
                Path = "/",
                AssumeRolePolicyDocument = new Dictionary<string, object>
                {
                    { "Statement", new []
                    {
                        new Dictionary<string, object>
                        {
                            { "Action", "sts:AssumeRole" },
                            { "Effect", "Allow" },
                            { "Principal", new Dictionary<string, object>
                            {
                                { "Service", "ecs-tasks.amazonaws.com" },
                            } },
                        },
                    } },
                },
            });
            var ecsTaskExecutionRole = new CfnRole(this, "ECSTaskExecutionRole", new CfnRoleProps
            {
                Path = "/",
                AssumeRolePolicyDocument = new Dictionary<string, object>
                {
                    { "Statement", new []
                    {
                        new Dictionary<string, object>
                        {
                            { "Action", "sts:AssumeRole" },
                            { "Effect", "Allow" },
                            { "Principal", new Dictionary<string, object>
                            {
                                { "Service", "ecs-tasks.amazonaws.com" },
                            } },
                        },
                    } },
                },
                ManagedPolicyArns = new []
                {
                    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
                    "arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess",
                    "arn:aws:iam::aws:policy/SecretsManagerReadWrite",
                },
            });
            var backendServiceEcsTaskDefinition = new CfnTaskDefinition(this, "BackendServiceECSTaskDefinition", new CfnTaskDefinitionProps
            {
                Family = "test",
                RequiresCompatibilities = new []
                {
                    "FARGATE",
                },
                Memory = "1024",
                Cpu = "256",
                NetworkMode = "awsvpc",
                ExecutionRoleArn = ecsTaskExecutionRole.AttrArn,
                TaskRoleArn = backendEcsTaskRole.AttrArn,
                ContainerDefinitions = new []
                {
                    new CfnTaskDefinition.ContainerDefinitionProperty
                    {
                        Name = "main",
                        Image = "nginx",
                        LogConfiguration = new CfnTaskDefinition.LogConfigurationProperty
                        {
                            Options = new Dictionary<string, string>
                            {
                                { "awslogs-group", "/aws/ecs/test/main" },
                                { "awslogs-region", "ap-northeast-1" },
                                { "awslogs-stream-prefix", "ecs" },
                            },
                            LogDriver = "awslogs",
                        },
                    },
                },
            });
        }
    }
}
