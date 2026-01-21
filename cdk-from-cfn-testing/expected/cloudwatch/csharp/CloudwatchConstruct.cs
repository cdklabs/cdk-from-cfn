using Amazon.CDK;
using Amazon.CDK.AWS.CloudWatch;
using Constructs;
using System.Collections.Generic;

namespace CloudwatchConstruct
{
    public class CloudwatchConstructProps
    {
        /// <summary>
        /// Environment used for this deployment.
        /// </summary>
        public string EnvironmentName { get; set; }

    }

    public class CloudwatchConstruct : Construct
    {
        public CloudwatchConstruct(Construct scope, string id, CloudwatchConstructProps props = null) : base(scope, id)
        {
            // Applying default props
            props ??= new CloudwatchConstructProps();
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
                Threshold = 0.005,
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
