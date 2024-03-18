package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.cloudwatch.*;

class CloudwatchStack extends Stack {
    public CloudwatchStack(final Construct scope, final String id) {
        super(scope, id, null);
    }

    public CloudwatchStack(final Construct scope, final String id, final StackProps props) {
        this(scope, id, props, null);
    }

    public CloudwatchStack(final Construct scope, final String id, final StackProps props,
            String environmentName) {
        super(scope, id, props);

        environmentName = Optional.ofNullable(environmentName).isPresent() ? environmentName
                : "dev";

        CfnAlarm myApi5xxErrorsAlarm = CfnAlarm.Builder.create(this, "MyApi5xxErrorsAlarm")
                .alarmDescription("Example alarm")
                .namespace("AWS/ApiGateway")
                .dimensions(Arrays.asList(
                        CfnAlarm.DimensionProperty.builder()
                                .name("ApiName")
                                .value("MyApi")
                                .build()))
                .metricName("5XXError")
                .comparisonOperator("GreaterThanThreshold")
                .statistic("Average")
                .threshold(0)
                .period(900)
                .evaluationPeriods(1)
                .treatMissingData("notBreaching")
                .alarmActions(Arrays.asList(
                        Fn.importValue(environmentName + "AlarmsTopicArn")))
                .build();

    }
}
