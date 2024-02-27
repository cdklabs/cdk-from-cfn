using Amazon.CDK;
using Amazon.CDK.AWS.CloudWatch;
using Constructs;
using System.Collections.Generic;

namespace CloudwatchStack
{
    public class CloudwatchStackProps : StackProps
    {
        /// <summary>
        /// Environment used for this deployment.
        /// </summary>
        public string EnvironmentName { get; set; }

    }

    public class CloudwatchStack : Stack
    {
        public CloudwatchStack(Construct scope, string id, CloudwatchStackProps props = null) : base(scope, id, props)
        {
            // Applying default props
            props ??= new CloudwatchStackProps();
            props.EnvironmentName ??= "dev";


            // Resources
            var myApi5xxErrorsAlarm = new CfnAlarm(this, "MyApi5xxErrorsAlarm", new CfnAlarmProps
            {
                AlarmDescription = "Example alarm",
                Namespace = "AWS/ApiGateway",
                Dimensions = new []
                {
                    new CfnAlarm.DimensionProperty
                    {
                        Name = "ApiName",
                        Value = "MyApi",
                    },
                },
                MetricName = "5XXError",
                ComparisonOperator = "GreaterThanThreshold",
                Statistic = "Average",
                Threshold = 0,
                Period = 900,
                EvaluationPeriods = 1,
                TreatMissingData = "notBreaching",
                AlarmActions = new []
                {
                    Fn.ImportValue($"{props.EnvironmentName}AlarmsTopicArn"),
                },
            });
        }
    }
}
