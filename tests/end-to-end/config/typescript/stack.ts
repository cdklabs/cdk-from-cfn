import * as cdk from 'aws-cdk-lib';
import * as config from 'aws-cdk-lib/aws-config';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as sns from 'aws-cdk-lib/aws-sns';

export interface ConfigStackProps extends cdk.StackProps {
  /**
   * @default 'false'
   */
  readonly ec2VolumeAutoEnableIo?: boolean;
  /**
   * @default 'CostCenter'
   */
  readonly ec2VolumeTagKey?: string;
}

/**
 * AWS CloudFormation Sample Template Config: This template demonstrates the usage of AWS Config resources.  **WARNING** You will be billed for the AWS resources used if you create a stack from this template.
 */
export class ConfigStack extends cdk.Stack {
  public readonly configRuleForVolumeTagsArn;
  public readonly configRuleForVolumeTagsConfigRuleId;
  public readonly configRuleForVolumeAutoEnableIoComplianceType;

  public constructor(scope: cdk.App, id: string, props: ConfigStackProps = {}) {
    super(scope, id, props);

    // Applying default props
    props = {
      ...props,
      ec2VolumeAutoEnableIo: props.ec2VolumeAutoEnableIo ?? false,
      ec2VolumeTagKey: props.ec2VolumeTagKey ?? 'CostCenter',
    };

    // Resources
    const configBucket = new s3.CfnBucket(this, 'ConfigBucket', {
    });

    const configTopic = new sns.CfnTopic(this, 'ConfigTopic', {
    });

    const ec2Volume = new ec2.CfnVolume(this, 'Ec2Volume', {
      autoEnableIo: props.ec2VolumeAutoEnableIo!,
      size: 5,
      availabilityZone: cdk.Fn.select(0, cdk.Fn.getAzs('')),
      tags: [
        {
          key: props.ec2VolumeTagKey!,
          value: 'Ec2VolumeTagValue',
        },
      ],
    });

    const lambdaExecutionRole = new iam.CfnRole(this, 'LambdaExecutionRole', {
      assumeRolePolicyDocument: {
        Version: '2012-10-17',
        Statement: [
          {
            Effect: 'Allow',
            Principal: {
              Service: [
                'lambda.amazonaws.com',
              ],
            },
            Action: [
              'sts:AssumeRole',
            ],
          },
        ],
      },
      policies: [
        {
          policyName: 'root',
          policyDocument: {
            Version: '2012-10-17',
            Statement: [
              {
                Effect: 'Allow',
                Action: [
                  'logs:*',
                  'config:PutEvaluations',
                  'ec2:DescribeVolumeAttribute',
                ],
                Resource: '*',
              },
            ],
          },
        },
      ],
    });

    const configRole = new iam.CfnRole(this, 'ConfigRole', {
      assumeRolePolicyDocument: {
        Version: '2012-10-17',
        Statement: [
          {
            Effect: 'Allow',
            Principal: {
              Service: [
                'config.amazonaws.com',
              ],
            },
            Action: [
              'sts:AssumeRole',
            ],
          },
        ],
      },
      managedPolicyArns: [
        'arn:aws:iam::aws:policy/service-role/AWS_ConfigRole',
      ],
      policies: [
        {
          policyName: 'root',
          policyDocument: {
            Version: '2012-10-17',
            Statement: [
              {
                Effect: 'Allow',
                Action: 's3:GetBucketAcl',
                Resource: [
                  'arn:aws:s3:::',
                  configBucket.ref,
                ].join(''),
              },
              {
                Effect: 'Allow',
                Action: 's3:PutObject',
                Resource: [
                  'arn:aws:s3:::',
                  configBucket.ref,
                  '/AWSLogs/',
                  this.account,
                  '/*',
                ].join(''),
                Condition: {
                  StringEquals: {
                    's3:x-amz-acl': 'bucket-owner-full-control',
                  },
                },
              },
              {
                Effect: 'Allow',
                Action: 'config:Put*',
                Resource: '*',
              },
            ],
          },
        },
      ],
    });

    const configTopicPolicy = new sns.CfnTopicPolicy(this, 'ConfigTopicPolicy', {
      policyDocument: {
        Id: 'ConfigTopicPolicy',
        Version: '2012-10-17',
        Statement: [
          {
            Effect: 'Allow',
            Principal: {
              Service: 'config.amazonaws.com',
            },
            Action: 'SNS:Publish',
            Resource: '*',
          },
        ],
      },
      topics: [
        configTopic.ref,
      ],
    });

    const deliveryChannel = new config.CfnDeliveryChannel(this, 'DeliveryChannel', {
      configSnapshotDeliveryProperties: {
        deliveryFrequency: 'Six_Hours',
      },
      s3BucketName: configBucket.ref,
      snsTopicArn: configTopic.ref,
    });

    const volumeAutoEnableIoComplianceCheck = new lambda.CfnFunction(this, 'VolumeAutoEnableIOComplianceCheck', {
      code: {
        zipFile: [
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
        ].join('\n'),
      },
      handler: 'index.handler',
      runtime: 'nodejs18.x',
      timeout: 30,
      role: lambdaExecutionRole.attrArn,
    });

    const configPermissionToCallLambda = new lambda.CfnPermission(this, 'ConfigPermissionToCallLambda', {
      functionName: volumeAutoEnableIoComplianceCheck.attrArn,
      action: 'lambda:InvokeFunction',
      principal: 'config.amazonaws.com',
    });

    const configRecorder = new config.CfnConfigurationRecorder(this, 'ConfigRecorder', {
      name: 'default',
      recordingGroup: {
        resourceTypes: [
          'AWS::EC2::Volume',
        ],
      },
      roleArn: configRole.attrArn,
    });

    const configRuleForVolumeAutoEnableIo = new config.CfnConfigRule(this, 'ConfigRuleForVolumeAutoEnableIO', {
      configRuleName: 'ConfigRuleForVolumeAutoEnableIO',
      scope: {
        complianceResourceId: ec2Volume.ref,
        complianceResourceTypes: [
          'AWS::EC2::Volume',
        ],
      },
      source: {
        owner: 'CUSTOM_LAMBDA',
        sourceDetails: [
          {
            eventSource: 'aws.config',
            messageType: 'ConfigurationItemChangeNotification',
          },
        ],
        sourceIdentifier: volumeAutoEnableIoComplianceCheck.attrArn,
      },
    });
    configRuleForVolumeAutoEnableIo.addDependency(configPermissionToCallLambda);
    configRuleForVolumeAutoEnableIo.addDependency(configRecorder);

    const configRuleForVolumeTags = new config.CfnConfigRule(this, 'ConfigRuleForVolumeTags', {
      inputParameters: {
        tag1Key: 'CostCenter',
      },
      scope: {
        complianceResourceTypes: [
          'AWS::EC2::Volume',
        ],
      },
      source: {
        owner: 'AWS',
        sourceIdentifier: 'REQUIRED_TAGS',
      },
    });
    configRuleForVolumeTags.addDependency(configRecorder);

    // Outputs
    this.configRuleForVolumeTagsArn = configRuleForVolumeTags.attrArn;
    new cdk.CfnOutput(this, 'CfnOutputConfigRuleForVolumeTagsArn', {
      key: 'ConfigRuleForVolumeTagsArn',
      value: this.configRuleForVolumeTagsArn!.toString(),
    });
    this.configRuleForVolumeTagsConfigRuleId = configRuleForVolumeTags.attrConfigRuleId;
    new cdk.CfnOutput(this, 'CfnOutputConfigRuleForVolumeTagsConfigRuleId', {
      key: 'ConfigRuleForVolumeTagsConfigRuleId',
      value: this.configRuleForVolumeTagsConfigRuleId!.toString(),
    });
    this.configRuleForVolumeAutoEnableIoComplianceType = configRuleForVolumeAutoEnableIo.attrComplianceType;
    new cdk.CfnOutput(this, 'CfnOutputConfigRuleForVolumeAutoEnableIOComplianceType', {
      key: 'ConfigRuleForVolumeAutoEnableIOComplianceType',
      value: this.configRuleForVolumeAutoEnableIoComplianceType!.toString(),
    });
  }
}
