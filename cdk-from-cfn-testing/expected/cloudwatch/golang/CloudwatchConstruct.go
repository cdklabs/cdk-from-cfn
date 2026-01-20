package main

import (
	"fmt"

	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	cloudwatch "github.com/aws/aws-cdk-go/awscdk/v2/awscloudwatch"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type CloudwatchConstructProps struct {
	/// Environment used for this deployment.
	EnvironmentName *string
}

type CloudwatchConstruct struct {
	constructs.Construct
}

func NewCloudwatchConstruct(scope constructs.Construct, id string, props *CloudwatchConstructProps) *CloudwatchConstruct {
	construct := constructs.NewConstruct(scope, &id)

	cloud_watch.NewCfnAlarm(
		construct,
		jsii.String("MyApi5xxErrorsAlarm"),
		&cloud_watch.CfnAlarmProps{
			AlarmDescription: jsii.String("Example alarm"),
			Namespace: jsii.String("AWS/ApiGateway"),
			Dimensions: &[]interface{}{
				&DimensionProperty{
					Name: jsii.String("ApiName"),
					Value: jsii.String("MyApi"),
				},
			},
			MetricName: jsii.String("5XXError"),
			ComparisonOperator: jsii.String("GreaterThanThreshold"),
			Statistic: jsii.String("Average"),
			Threshold: jsii.Number(0.005),
			Period: jsii.Number(900),
			EvaluationPeriods: jsii.Number(1),
			TreatMissingData: jsii.String("notBreaching"),
			AlarmActions: &[]*string{
				cdk.Fn_ImportValue(jsii.String(fmt.Sprintf("%vAlarmsTopicArn", props.EnvironmentName))),
			},
		},
	)

	return &CloudwatchConstruct{
		Construct: construct,
	}
}

