package config

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	config "github.com/aws/aws-cdk-go/awscdk/v2/awsconfig"
	ec2 "github.com/aws/aws-cdk-go/awscdk/v2/awsec2"
	iam "github.com/aws/aws-cdk-go/awscdk/v2/awsiam"
	lambda "github.com/aws/aws-cdk-go/awscdk/v2/awslambda"
	s3 "github.com/aws/aws-cdk-go/awscdk/v2/awss3"
	sns "github.com/aws/aws-cdk-go/awscdk/v2/awssns"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type ConfigStackProps struct {
	cdk.StackProps
	Ec2VolumeAutoEnableIo interface{/* Boolean */}
	Ec2VolumeTagKey *string
}

/// AWS CloudFormation Sample Template Config: This template demonstrates the usage of AWS Config resources.  **WARNING** You will be billed for the AWS resources used if you create a stack from this template.
type ConfigStack struct {
	cdk.Stack
	ConfigRuleForVolumeTagsArn interface{} // TODO: fix to appropriate type
	ConfigRuleForVolumeTagsConfigRuleId interface{} // TODO: fix to appropriate type
	ConfigRuleForVolumeAutoEnableIoComplianceType interface{} // TODO: fix to appropriate type
}

func NewConfigStack(scope constructs.Construct, id string, props ConfigStackProps) *ConfigStack {
	stack := cdk.NewStack(scope, &id, &props.StackProps)

	configBucket := s3.NewCfnBucket(
		stack,
		jsii.String("ConfigBucket"),
		&s3.CfnBucketProps{
		},
	)

	configTopic := sns.NewCfnTopic(
		stack,
		jsii.String("ConfigTopic"),
		&sns.CfnTopicProps{
		},
	)

	ec2Volume := ec2.NewCfnVolume(
		stack,
		jsii.String("Ec2Volume"),
		&ec2.CfnVolumeProps{
			AutoEnableIo: props.Ec2VolumeAutoEnableIo,
			Size: jsii.Number(5),
			AvailabilityZone: cdk.Fn_Select(jsii.Number(0), cdk.Fn_GetAzs(jsii.String(""))),
			Tags: &[]*cdk.CfnTag{
				&cdk.CfnTag{
					Key: props.Ec2VolumeTagKey,
					Value: jsii.String("Ec2VolumeTagValue"),
				},
			},
		},
	)

	lambdaExecutionRole := iam.NewCfnRole(
		stack,
		jsii.String("LambdaExecutionRole"),
		&iam.CfnRoleProps{
			AssumeRolePolicyDocument: map[string]interface{} {
				"Version": jsii.String("2012-10-17"),
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Effect": jsii.String("Allow"),
						"Principal": map[string]interface{} {
							"Service": &[]interface{}{
								jsii.String("lambda.amazonaws.com"),
							},
						},
						"Action": &[]interface{}{
							jsii.String("sts:AssumeRole"),
						},
					},
				},
			},
			Policies: &[]*Policy /* FIXME */{
				&Policy/* FIXME */{
					PolicyName: jsii.String("root"),
					PolicyDocument: map[string]interface{} {
						"Version": jsii.String("2012-10-17"),
						"Statement": &[]interface{}{
							map[string]interface{} {
								"Effect": jsii.String("Allow"),
								"Action": &[]interface{}{
									jsii.String("logs:*"),
									jsii.String("config:PutEvaluations"),
									jsii.String("ec2:DescribeVolumeAttribute"),
								},
								"Resource": jsii.String("*"),
							},
						},
					},
				},
			},
		},
	)

	configRole := iam.NewCfnRole(
		stack,
		jsii.String("ConfigRole"),
		&iam.CfnRoleProps{
			AssumeRolePolicyDocument: map[string]interface{} {
				"Version": jsii.String("2012-10-17"),
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Effect": jsii.String("Allow"),
						"Principal": map[string]interface{} {
							"Service": &[]interface{}{
								jsii.String("config.amazonaws.com"),
							},
						},
						"Action": &[]interface{}{
							jsii.String("sts:AssumeRole"),
						},
					},
				},
			},
			ManagedPolicyArns: &[]*string{
				jsii.String("arn:aws:iam::aws:policy/service-role/AWSConfigRole"),
			},
			Policies: &[]*Policy /* FIXME */{
				&Policy/* FIXME */{
					PolicyName: jsii.String("root"),
					PolicyDocument: map[string]interface{} {
						"Version": jsii.String("2012-10-17"),
						"Statement": &[]interface{}{
							map[string]interface{} {
								"Effect": jsii.String("Allow"),
								"Action": jsii.String("s3:GetBucketAcl"),
								"Resource": cdk.Fn_Join(jsii.String(""), &[]*string{
									jsii.String("arn:aws:s3:::"),
									configBucket.Ref(),
								}),
							},
							map[string]interface{} {
								"Effect": jsii.String("Allow"),
								"Action": jsii.String("s3:PutObject"),
								"Resource": cdk.Fn_Join(jsii.String(""), &[]*string{
									jsii.String("arn:aws:s3:::"),
									configBucket.Ref(),
									jsii.String("/AWSLogs/"),
									stack.Account(),
									jsii.String("/*"),
								}),
								"Condition": map[string]interface{} {
									"StringEquals": map[string]interface{} {
										"S3XAmzAcl": jsii.String("bucket-owner-full-control"),
									},
								},
							},
							map[string]interface{} {
								"Effect": jsii.String("Allow"),
								"Action": jsii.String("config:Put*"),
								"Resource": jsii.String("*"),
							},
						},
					},
				},
			},
		},
	)

	sns.NewCfnTopicPolicy(
		stack,
		jsii.String("ConfigTopicPolicy"),
		&sns.CfnTopicPolicyProps{
			PolicyDocument: map[string]interface{} {
				"Id": jsii.String("ConfigTopicPolicy"),
				"Version": jsii.String("2012-10-17"),
				"Statement": &[]interface{}{
					map[string]interface{} {
						"Effect": jsii.String("Allow"),
						"Principal": map[string]interface{} {
							"Service": jsii.String("config.amazonaws.com"),
						},
						"Action": jsii.String("SNS:Publish"),
						"Resource": jsii.String("*"),
					},
				},
			},
			Topics: &[]*string{
				configTopic.Ref(),
			},
		},
	)

	config.NewCfnDeliveryChannel(
		stack,
		jsii.String("DeliveryChannel"),
		&config.CfnDeliveryChannelProps{
			ConfigSnapshotDeliveryProperties: &ConfigSnapshotDeliveryProperties/* FIXME */{
				DeliveryFrequency: jsii.String("Six_Hours"),
			},
			S3BucketName: configBucket.Ref(),
			SnsTopicArn: configTopic.Ref(),
		},
	)

	volumeAutoEnableIoComplianceCheck := lambda.NewCfnFunction(
		stack,
		jsii.String("VolumeAutoEnableIOComplianceCheck"),
		&lambda.CfnFunctionProps{
			Code: &Code/* FIXME */{
				ZipFile: cdk.Fn_Join(jsii.String("\n"), &[]*string{
					jsii.String("var aws  = require('aws-sdk');"),
					jsii.String("var config = new aws.ConfigService();"),
					jsii.String("var ec2 = new aws.EC2();"),
					jsii.String("exports.handler = function(event, context) {"),
					jsii.String("    compliance = evaluateCompliance(event, function(compliance, event) {"),
					jsii.String("        var configurationItem = JSON.parse(event.invokingEvent).configurationItem;"),
					jsii.String("        var putEvaluationsRequest = {"),
					jsii.String("            Evaluations: [{"),
					jsii.String("                ComplianceResourceType: configurationItem.resourceType,"),
					jsii.String("                ComplianceResourceId: configurationItem.resourceId,"),
					jsii.String("                ComplianceType: compliance,"),
					jsii.String("                OrderingTimestamp: configurationItem.configurationItemCaptureTime"),
					jsii.String("            }],"),
					jsii.String("            ResultToken: event.resultToken"),
					jsii.String("        };"),
					jsii.String("        config.putEvaluations(putEvaluationsRequest, function(err, data) {"),
					jsii.String("            if (err) context.fail(err);"),
					jsii.String("            else context.succeed(data);"),
					jsii.String("        });"),
					jsii.String("    });"),
					jsii.String("};"),
					jsii.String("function evaluateCompliance(event, doReturn) {"),
					jsii.String("    var configurationItem = JSON.parse(event.invokingEvent).configurationItem;"),
					jsii.String("    var status = configurationItem.configurationItemStatus;"),
					jsii.String("    if (configurationItem.resourceType !== 'AWS::EC2::Volume' || event.eventLeftScope || (status !== 'OK' && status !== 'ResourceDiscovered'))"),
					jsii.String("        doReturn('NOT_APPLICABLE', event);"),
					jsii.String("    else ec2.describeVolumeAttribute({VolumeId: configurationItem.resourceId, Attribute: 'autoEnableIO'}, function(err, data) {"),
					jsii.String("        if (err) context.fail(err);"),
					jsii.String("        else if (data.AutoEnableIO.Value) doReturn('COMPLIANT', event);"),
					jsii.String("        else doReturn('NON_COMPLIANT', event);"),
					jsii.String("    });"),
					jsii.String("}"),
				}),
			},
			Handler: jsii.String("index.handler"),
			Runtime: jsii.String("nodejs"),
			Timeout: jsii.Number(30),
			Role: lambdaExecutionRole.AttrArn(),
		},
	)

	configPermissionToCallLambda := lambda.NewCfnPermission(
		stack,
		jsii.String("ConfigPermissionToCallLambda"),
		&lambda.CfnPermissionProps{
			FunctionName: volumeAutoEnableIoComplianceCheck.AttrArn(),
			Action: jsii.String("lambda:InvokeFunction"),
			Principal: jsii.String("config.amazonaws.com"),
		},
	)

	configRecorder := config.NewCfnConfigurationRecorder(
		stack,
		jsii.String("ConfigRecorder"),
		&config.CfnConfigurationRecorderProps{
			Name: jsii.String("default"),
			RecordingGroup: &RecordingGroup/* FIXME */{
				ResourceTypes: &[]*string{
					jsii.String("AWS::EC2::Volume"),
				},
			},
			RoleArn: configRole.AttrArn(),
		},
	)

	configRuleForVolumeAutoEnableIo := config.NewCfnConfigRule(
		stack,
		jsii.String("ConfigRuleForVolumeAutoEnableIO"),
		&config.CfnConfigRuleProps{
			ConfigRuleName: jsii.String("ConfigRuleForVolumeAutoEnableIO"),
			Scope: &Scope/* FIXME */{
				ComplianceResourceId: ec2Volume.Ref(),
				ComplianceResourceTypes: &[]*string{
					jsii.String("AWS::EC2::Volume"),
				},
			},
			Source: &Source/* FIXME */{
				Owner: jsii.String("CUSTOM_LAMBDA"),
				SourceDetails: &[]*SourceDetail /* FIXME */{
					&SourceDetail/* FIXME */{
						EventSource: jsii.String("aws.config"),
						MessageType: jsii.String("ConfigurationItemChangeNotification"),
					},
				},
				SourceIdentifier: volumeAutoEnableIoComplianceCheck.AttrArn(),
			},
		},
	)

	configRuleForVolumeTags := config.NewCfnConfigRule(
		stack,
		jsii.String("ConfigRuleForVolumeTags"),
		&config.CfnConfigRuleProps{
			InputParameters: map[string]interface{} {
				"Tag1Key": jsii.String("CostCenter"),
			},
			Scope: &Scope/* FIXME */{
				ComplianceResourceTypes: &[]*string{
					jsii.String("AWS::EC2::Volume"),
				},
			},
			Source: &Source/* FIXME */{
				Owner: jsii.String("AWS"),
				SourceIdentifier: jsii.String("REQUIRED_TAGS"),
			},
		},
	)

	return &ConfigStack{
		Stack: stack,
		ConfigRuleForVolumeTagsArn: configRuleForVolumeTags.AttrArn(),
		ConfigRuleForVolumeTagsConfigRuleId: configRuleForVolumeTags.AttrConfigRuleId(),
		ConfigRuleForVolumeAutoEnableIoComplianceType: configRuleForVolumeAutoEnableIo.AttrComplianceType(),
	}
}

func main() {
	defer jsii.Close()

	app := cdk.NewApp(nil)

	NewConfigStack(app, "Config", ConfigStackProps{
		cdk.StackProps{
			Env: env(),
		},
		Ec2VolumeAutoEnableIo: "false",
		Ec2VolumeTagKey: "CostCenter",
	})

	app.Synth(nil)
}

// env determines the AWS environment (account+region) in which our stack is to
// be deployed. For more information see: https://docs.aws.amazon.com/cdk/latest/guide/environments.html
func env() *cdk.Environment {
	// If unspecified, this stack will be "environment-agnostic".
	// Account/Region-dependent features and context lookups will not work, but a
	// single synthesized template can be deployed anywhere.
	//---------------------------------------------------------------------------
	return nil

	// Uncomment if you know exactly what account and region you want to deploy
	// the stack to. This is the recommendation for production stacks.
	//---------------------------------------------------------------------------
	// return &cdk.Environment{
	//  Account: jsii.String("123456789012"),
	//  Region:  jsii.String("us-east-1"),
	// }

	// Uncomment to specialize this stack for the AWS Account and Region that are
	// implied by the current CLI configuration. This is recommended for dev
	// stacks.
	//---------------------------------------------------------------------------
	// return &cdk.Environment{
	//  Account: jsii.String(os.Getenv("CDK_DEFAULT_ACCOUNT")),
	//  Region:  jsii.String(os.Getenv("CDK_DEFAULT_REGION")),
	// }
}
