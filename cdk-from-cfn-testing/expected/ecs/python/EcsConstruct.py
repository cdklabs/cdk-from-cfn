from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_iam as iam
from constructs import Construct

class EcsConstruct(Construct):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id)

    # Resources
    backendEcsTaskRole = iam.CfnRole(self, 'BackendECSTaskRole',
          path = '/',
          assume_role_policy_document = {
            'Statement': [
              {
                'Action': 'sts:AssumeRole',
                'Effect': 'Allow',
                'Principal': {
                  'Service': 'ecs-tasks.amazonaws.com',
                },
              },
            ],
          },
        )

    ecsTaskExecutionRole = iam.CfnRole(self, 'ECSTaskExecutionRole',
          path = '/',
          assume_role_policy_document = {
            'Statement': [
              {
                'Action': 'sts:AssumeRole',
                'Effect': 'Allow',
                'Principal': {
                  'Service': 'ecs-tasks.amazonaws.com',
                },
              },
            ],
          },
          managed_policy_arns = [
            'arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy',
            'arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess',
            'arn:aws:iam::aws:policy/SecretsManagerReadWrite',
          ],
        )

    backendServiceEcsTaskDefinition = ecs.CfnTaskDefinition(self, 'BackendServiceECSTaskDefinition',
          family = 'test',
          requires_compatibilities = [
            'FARGATE',
          ],
          memory = '1024',
          cpu = '256',
          network_mode = 'awsvpc',
          execution_role_arn = ecsTaskExecutionRole.attr_arn,
          task_role_arn = backendEcsTaskRole.attr_arn,
          container_definitions = [
            {
              'name': 'main',
              'image': 'nginx',
              'logConfiguration': {
                'options': {
                  'awslogs-group': '/aws/ecs/test/main',
                  'awslogs-region': 'ap-northeast-1',
                  'awslogs-stream-prefix': 'ecs',
                },
                'logDriver': 'awslogs',
              },
            },
          ],
        )


