from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_cloudwatch as cloudwatch
from constructs import Construct

class CloudwatchStack(Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Applying default props
    props = {
      'environmentName': kwargs.get('environmentName', 'dev'),
      'alarmThreshold': cdk.CfnParameter(self, 'alarmThreshold', 
        type = 'Number',
        default = str(kwargs.get('alarmThreshold', '0.005')),
        no_echo = True,
      ).value_as_number,
    }

    # Resources
    myApi5xxErrorsAlarm = cloudwatch.CfnAlarm(self, 'MyApi5xxErrorsAlarm',
          alarm_description = 'Example alarm',
          namespace = 'AWS/ApiGateway',
          dimensions = [
            {
              'name': 'ApiName',
              'value': 'MyApi',
            },
          ],
          metric_name = '5XXError',
          comparison_operator = 'GreaterThanThreshold',
          statistic = 'Average',
          threshold = props['alarmThreshold'],
          period = 900,
          evaluation_periods = 1,
          treat_missing_data = 'notBreaching',
          alarm_actions = [
            cdk.Fn.import_value(f"""{props['environmentName']}AlarmsTopicArn"""),
          ],
        )


