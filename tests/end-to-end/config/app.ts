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
        version: '2012-10-17',
        statement: [
          {
            effect: 'Allow',
            principal: {
              service: [
                'lambda.amazonaws.com',
              ],
            },
            action: [
              'sts:AssumeRole',
            ],
          },
        ],
      },
      policies: [
        {
          policyName: 'root',
          policyDocument: {
            version: '2012-10-17',
            statement: [
              {
                effect: 'Allow',
                action: [
                  'logs:*',
                  'config:PutEvaluations',
                  'ec2:DescribeVolumeAttribute',
                ],
                resource: '*',
              },
            ],
          },
        },
      ],
    });

    if (configBucket == null) { throw new Error(`A combination of conditions caused 'configBucket' to be undefined. Fixit.`); }
    const configRole = new iam.CfnRole(this, 'ConfigRole', {
      assumeRolePolicyDocument: {
        version: '2012-10-17',
        statement: [
          {
            effect: 'Allow',
            principal: {
              service: [
                'config.amazonaws.com',
              ],
            },
            action: [
              'sts:AssumeRole',
            ],
          },
        ],
      },
      managedPolicyArns: [
        'arn:aws:iam::aws:policy/service-role/AWSConfigRole',
      ],
      policies: [
        {
          policyName: 'root',
          policyDocument: {
            version: '2012-10-17',
            statement: [
              {
                effect: 'Allow',
                action: 's3:GetBucketAcl',
                resource: [
                  'arn:aws:s3:::',
                  configBucket.ref,
                ].join(''),
              },
              {
                effect: 'Allow',
                action: 's3:PutObject',
                resource: [
                  'arn:aws:s3:::',
                  configBucket.ref,
                  '/AWSLogs/',
                  this.account,
                  '/*',
                ].join(''),
                condition: {
                  stringEquals: {
                    s3XAmzAcl: 'bucket-owner-full-control',
                  },
                },
              },
              {
                effect: 'Allow',
                action: 'config:Put*',
                resource: '*',
              },
            ],
          },
        },
      ],
    });

    if (configTopic == null) { throw new Error(`A combination of conditions caused 'configTopic' to be undefined. Fixit.`); }
    const configTopicPolicy = new sns.CfnTopicPolicy(this, 'ConfigTopicPolicy', {
      policyDocument: {
        id: 'ConfigTopicPolicy',
        version: '2012-10-17',
        statement: [
          {
            effect: 'Allow',
            principal: {
              service: 'config.amazonaws.com',
            },
            action: 'SNS:Publish',
            resource: '*',
          },
        ],
      },
      topics: [
        configTopic.ref,
      ],
    });

    if (configBucket == null) { throw new Error(`A combination of conditions caused 'configBucket' to be undefined. Fixit.`); }
    if (configTopic == null) { throw new Error(`A combination of conditions caused 'configTopic' to be undefined. Fixit.`); }
    const deliveryChannel = new config.CfnDeliveryChannel(this, 'DeliveryChannel', {
      configSnapshotDeliveryProperties: {
        deliveryFrequency: 'Six_Hours',
      },
      s3BucketName: configBucket.ref,
      snsTopicArn: configTopic.ref,
    });

    if (lambdaExecutionRole == null) { throw new Error(`A combination of conditions caused 'lambdaExecutionRole' to be undefined. Fixit.`); }
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
      runtime: 'nodejs',
      timeout: 30,
      role: lambdaExecutionRole.attrArn,
    });

    if (volumeAutoEnableIoComplianceCheck == null) { throw new Error(`A combination of conditions caused 'volumeAutoEnableIoComplianceCheck' to be undefined. Fixit.`); }
    const configPermissionToCallLambda = new lambda.CfnPermission(this, 'ConfigPermissionToCallLambda', {
      functionName: volumeAutoEnableIoComplianceCheck.attrArn,
      action: 'lambda:InvokeFunction',
      principal: 'config.amazonaws.com',
    });

    if (configRole == null) { throw new Error(`A combination of conditions caused 'configRole' to be undefined. Fixit.`); }
    const configRecorder = new config.CfnConfigurationRecorder(this, 'ConfigRecorder', {
      name: 'default',
      recordingGroup: {
        resourceTypes: [
          'AWS::EC2::Volume',
        ],
      },
      roleArn: configRole.attrArn,
    });

    if (configPermissionToCallLambda == null) { throw new Error(`A combination of conditions caused 'configPermissionToCallLambda' to be undefined. Fixit.`); }
    if (configRecorder == null) { throw new Error(`A combination of conditions caused 'configRecorder' to be undefined. Fixit.`); }
    if (ec2Volume == null) { throw new Error(`A combination of conditions caused 'ec2Volume' to be undefined. Fixit.`); }
    if (volumeAutoEnableIoComplianceCheck == null) { throw new Error(`A combination of conditions caused 'volumeAutoEnableIoComplianceCheck' to be undefined. Fixit.`); }
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

    if (configRecorder == null) { throw new Error(`A combination of conditions caused 'configRecorder' to be undefined. Fixit.`); }
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
    this.configRuleForVolumeTagsConfigRuleId = configRuleForVolumeTags.attrConfigRuleId;
    this.configRuleForVolumeAutoEnableIoComplianceType = configRuleForVolumeAutoEnableIo.attrComplianceType;
  }
}
