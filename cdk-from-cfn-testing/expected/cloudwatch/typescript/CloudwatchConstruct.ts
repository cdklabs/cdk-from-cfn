import * as cdk from 'aws-cdk-lib';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import { Construct } from 'constructs';

export interface CloudwatchConstructProps {
  /**
   * Environment used for this deployment.
   * @default 'dev'
   */
  readonly environmentName?: string;
}

export class CloudwatchConstruct extends Construct {
  public constructor(scope: Construct, id: string, props: CloudwatchConstructProps = {}) {
    super(scope, id);

    // Applying default props
    props = {
      ...props,
      environmentName: props.environmentName ?? 'dev',
    };

    // Resources
    const myApi5xxErrorsAlarm = new cloudwatch.CfnAlarm(this, 'MyApi5xxErrorsAlarm', {
      alarmDescription: 'Example alarm',
      namespace: 'AWS/ApiGateway',
      dimensions: [
        {
          name: 'ApiName',
          value: 'MyApi',
        },
      ],
      metricName: '5XXError',
      comparisonOperator: 'GreaterThanThreshold',
      statistic: 'Average',
      threshold: 0.005,
      period: 900,
      evaluationPeriods: 1,
      treatMissingData: 'notBreaching',
      alarmActions: [
        cdk.Fn.importValue(`${props.environmentName!}AlarmsTopicArn`),
      ],
    });
  }
}
