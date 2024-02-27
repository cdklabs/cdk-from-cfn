package main

import (
	"fmt"

	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	cloudwatch "github.com/aws/aws-cdk-go/awscdk/v2/awscloudwatch"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type CloudwatchStackProps struct {
	cdk.StackProps
	/// Environment used for this deployment.
	EnvironmentName *string
}

type CloudwatchStack struct {
	cdk.Stack
}

func NewCloudwatchStack(scope constructs.Construct, id string, props *CloudwatchStackProps) *CloudwatchStack {
	var sprops cdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := cdk.NewStack(scope, &id, &sprops)

	cloud_watch.NewCfnAlarm(
		stack,
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
			Threshold: jsii.Number(0),
			Period: jsii.Number(900),
			EvaluationPeriods: jsii.Number(1),
			TreatMissingData: jsii.String("notBreaching"),
			AlarmActions: &[]*string{
				cdk.Fn_ImportValue(jsii.String(fmt.Sprintf("%vAlarmsTopicArn", props.EnvironmentName))),
			},
		},
	)

	return &CloudwatchStack{
		Stack: stack,
	}
}

