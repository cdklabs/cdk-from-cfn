from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_config as config
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_sns as sns
from constructs import Construct

"""
  AWS CloudFormation Sample Template Config: This template demonstrates the usage of AWS Config resources.  **WARNING** You will be billed for the AWS resources used if you create a stack from this template.
"""
class ConfigStack(Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Applying default props
    props = {
      'ec2VolumeAutoEnableIo': kwargs.get('ec2VolumeAutoEnableIo', False),
      'ec2VolumeTagKey': kwargs.get('ec2VolumeTagKey', 'CostCenter'),
    }

    # Resources
    configBucket = s3.CfnBucket(self, 'ConfigBucket',
        )

    configTopic = sns.CfnTopic(self, 'ConfigTopic',
        )

    ec2Volume = ec2.CfnVolume(self, 'Ec2Volume',
          auto_enable_io = props['ec2VolumeAutoEnableIo'],
          size = 5,
          availability_zone = cdk.Fn.select(0, cdk.Fn.get_azs('')),
          tags = [
            {
              'key': props['ec2VolumeTagKey'],
              'value': 'Ec2VolumeTagValue',
            },
          ],
        )

    lambdaExecutionRole = iam.CfnRole(self, 'LambdaExecutionRole',
          assume_role_policy_document = {
            'Version': '2012-10-17',
            'Statement': [
              {
                'Effect': 'Allow',
                'Principal': {
                  'Service': [
                    'lambda.amazonaws.com',
                  ],
                },
                'Action': [
                  'sts:AssumeRole',
                ],
              },
            ],
          },
          policies = [
            {
              'policyName': 'root',
              'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                  {
                    'Effect': 'Allow',
                    'Action': [
                      'logs:*',
                      'config:PutEvaluations',
                      'ec2:DescribeVolumeAttribute',
                    ],
                    'Resource': '*',
                  },
                ],
              },
            },
          ],
        )

    configRole = iam.CfnRole(self, 'ConfigRole',
          assume_role_policy_document = {
            'Version': '2012-10-17',
            'Statement': [
              {
                'Effect': 'Allow',
                'Principal': {
                  'Service': [
                    'config.amazonaws.com',
                  ],
                },
                'Action': [
                  'sts:AssumeRole',
                ],
              },
            ],
          },
          managed_policy_arns = [
            'arn:aws:iam::aws:policy/service-role/AWSConfigRole',
          ],
          policies = [
            {
              'policyName': 'root',
              'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                  {
                    'Effect': 'Allow',
                    'Action': 's3:GetBucketAcl',
                    'Resource': ''.join([
                      'arn:aws:s3:::',
                      configBucket.ref,
                    ]),
                  },
                  {
                    'Effect': 'Allow',
                    'Action': 's3:PutObject',
                    'Resource': ''.join([
                      'arn:aws:s3:::',
                      configBucket.ref,
                      '/AWSLogs/',
                      self.account,
                      '/*',
                    ]),
                    'Condition': {
                      'StringEquals': {
                        's3:x-amz-acl': 'bucket-owner-full-control',
                      },
                    },
                  },
                  {
                    'Effect': 'Allow',
                    'Action': 'config:Put*',
                    'Resource': '*',
                  },
                ],
              },
            },
          ],
        )

    configTopicPolicy = sns.CfnTopicPolicy(self, 'ConfigTopicPolicy',
          policy_document = {
            'Id': 'ConfigTopicPolicy',
            'Version': '2012-10-17',
            'Statement': [
              {
                'Effect': 'Allow',
                'Principal': {
                  'Service': 'config.amazonaws.com',
                },
                'Action': 'SNS:Publish',
                'Resource': '*',
              },
            ],
          },
          topics = [
            configTopic.ref,
          ],
        )

    deliveryChannel = config.CfnDeliveryChannel(self, 'DeliveryChannel',
          config_snapshot_delivery_properties = {
            'deliveryFrequency': 'Six_Hours',
          },
          s3_bucket_name = configBucket.ref,
          sns_topic_arn = configTopic.ref,
        )

    volumeAutoEnableIoComplianceCheck = aws_lambda.CfnFunction(self, 'VolumeAutoEnableIOComplianceCheck',
          code = {
            'zipFile': '\n'.join([
              'var aws  = require(\'aws-sdk\');',
              'var config = new aws.ConfigService();',
              'var ec2 = new aws.EC2();',
              'exports.handler = function(event, context) {',
              '    compliance = evaluateCompliance(event, function(compliance, event) {',
              '        var configurationItem = JSON.parse(event.invokingEvent).configurationItem;',
              '        var putEvaluationsRequest = {',
              '            Evaluations: [{',
              '                ComplianceResourceType: configurationItem.resourceType,',
              '                ComplianceResourceId: configurationItem.resourceId,',
              '                ComplianceType: compliance,',
              '                OrderingTimestamp: configurationItem.configurationItemCaptureTime',
              '            }],',
              '            ResultToken: event.resultToken',
              '        };',
              '        config.putEvaluations(putEvaluationsRequest, function(err, data) {',
              '            if (err) context.fail(err);',
              '            else context.succeed(data);',
              '        });',
              '    });',
              '};',
              'function evaluateCompliance(event, doReturn) {',
              '    var configurationItem = JSON.parse(event.invokingEvent).configurationItem;',
              '    var status = configurationItem.configurationItemStatus;',
              '    if (configurationItem.resourceType !== \'AWS::EC2::Volume\' || event.eventLeftScope || (status !== \'OK\' && status !== \'ResourceDiscovered\'))',
              '        doReturn(\'NOT_APPLICABLE\', event);',
              '    else ec2.describeVolumeAttribute({VolumeId: configurationItem.resourceId, Attribute: \'autoEnableIO\'}, function(err, data) {',
              '        if (err) context.fail(err);',
              '        else if (data.AutoEnableIO.Value) doReturn(\'COMPLIANT\', event);',
              '        else doReturn(\'NON_COMPLIANT\', event);',
              '    });',
              '}',
            ]),
          },
          handler = 'index.handler',
          runtime = 'nodejs',
          timeout = 30,
          role = lambdaExecutionRole.attr_arn,
        )

    configPermissionToCallLambda = aws_lambda.CfnPermission(self, 'ConfigPermissionToCallLambda',
          function_name = volumeAutoEnableIoComplianceCheck.attr_arn,
          action = 'lambda:InvokeFunction',
          principal = 'config.amazonaws.com',
        )

    configRecorder = config.CfnConfigurationRecorder(self, 'ConfigRecorder',
          name = 'default',
          recording_group = {
            'resourceTypes': [
              'AWS::EC2::Volume',
            ],
          },
          role_arn = configRole.attr_arn,
        )

    configRuleForVolumeAutoEnableIo = config.CfnConfigRule(self, 'ConfigRuleForVolumeAutoEnableIO',
          config_rule_name = 'ConfigRuleForVolumeAutoEnableIO',
          scope = {
            'complianceResourceId': ec2Volume.ref,
            'complianceResourceTypes': [
              'AWS::EC2::Volume',
            ],
          },
          source = {
            'owner': 'CUSTOM_LAMBDA',
            'sourceDetails': [
              {
                'eventSource': 'aws.config',
                'messageType': 'ConfigurationItemChangeNotification',
              },
            ],
            'sourceIdentifier': volumeAutoEnableIoComplianceCheck.attr_arn,
          },
        )
    configRuleForVolumeAutoEnableIo.add_dependency(configPermissionToCallLambda)
    configRuleForVolumeAutoEnableIo.add_dependency(configRecorder)

    configRuleForVolumeTags = config.CfnConfigRule(self, 'ConfigRuleForVolumeTags',
          input_parameters = {
            'tag1Key': 'CostCenter',
          },
          scope = {
            'complianceResourceTypes': [
              'AWS::EC2::Volume',
            ],
          },
          source = {
            'owner': 'AWS',
            'sourceIdentifier': 'REQUIRED_TAGS',
          },
        )
    configRuleForVolumeTags.add_dependency(configRecorder)

    # Outputs
    self.config_rule_for_volume_tags_arn = configRuleForVolumeTags.attr_arn
    cdk.CfnOutput(self, 'CfnOutputConfigRuleForVolumeTagsArn', 
      key = 'ConfigRuleForVolumeTagsArn',
      value = str(self.config_rule_for_volume_tags_arn),
    )

    self.config_rule_for_volume_tags_config_rule_id = configRuleForVolumeTags.attr_config_rule_id
    cdk.CfnOutput(self, 'CfnOutputConfigRuleForVolumeTagsConfigRuleId', 
      key = 'ConfigRuleForVolumeTagsConfigRuleId',
      value = str(self.config_rule_for_volume_tags_config_rule_id),
    )

    self.config_rule_for_volume_auto_enable_io_compliance_type = configRuleForVolumeAutoEnableIo.attr_compliance_type
    cdk.CfnOutput(self, 'CfnOutputConfigRuleForVolumeAutoEnableIOComplianceType', 
      key = 'ConfigRuleForVolumeAutoEnableIOComplianceType',
      value = str(self.config_rule_for_volume_auto_enable_io_compliance_type),
    )



