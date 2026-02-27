package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.iam.*;
import software.amazon.awscdk.services.lambda.*;

class CustomResourceStack extends Stack {
    public CustomResourceStack(final Construct scope, final String id) {
        super(scope, id, null);
    }

    public CustomResourceStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        CfnRole lambdaRole = CfnRole.Builder.create(this, "LambdaRole")
                .assumeRolePolicyDocument(Map.of("Version", "2012-10-17",
                "Statement", Arrays.asList(
                        Map.of("Effect", "Allow",
                        "Principal", Map.of("Service", "lambda.amazonaws.com"),
                        "Action", "sts:AssumeRole"))))
                .build();

        CfnFunction backingLambda = CfnFunction.Builder.create(this, "BackingLambda")
                .runtime("python3.9")
                .handler("index.handler")
                .role(lambdaRole.getAttrArn())
                .code(CfnFunction.CodeProperty.builder()
                        .zipFile("""
                        def handler(event, context):
                          return {'Status': 'SUCCESS', 'Data': {'Endpoint': 'test-endpoint'}}
                        """)
                        .build())
                .build();

        CfnCustomResource cfnCustomResource = CfnCustomResource.Builder.create(this, "CfnCustomResource")
                .serviceToken(backingLambda.getAttrArn())
                .build();

        cfnCustomResource.addPropertyOverride("Region", "us-west-2");

        CfnCustomResource myCustomResource = CfnCustomResource.Builder.create(this, "MyCustomResource")
                .serviceToken(backingLambda.getAttrArn())
                .build();

        myCustomResource.addOverride("Type", "Custom::DatabaseSetup");
        myCustomResource.addPropertyOverride("DatabaseName", "mydb");
        myCustomResource.addPropertyOverride("TableCount", 5);
        myCustomResource.addPropertyOverride("EnableLogging", "true");
        myCustomResource.addPropertyOverride("Tags", Arrays.asList(
                "prod",
                "critical"));
        myCustomResource.addDependency(backingLambda);
        myCustomResource.applyRemovalPolicy(RemovalPolicy.RETAIN);

        CfnFunction consumerLambda = CfnFunction.Builder.create(this, "ConsumerLambda")
                .runtime("python3.9")
                .handler("index.handler")
                .role(lambdaRole.getAttrArn())
                .code(CfnFunction.CodeProperty.builder()
                        .zipFile("""
                        def handler(event, context):
                          pass
                        """)
                        .build())
                .environment(CfnFunction.EnvironmentProperty.builder()
                        .variables(Map.of("DB_ENDPOINT", myCustomResource.getAtt("Endpoint").toString(),
                        "CFN_RESULT", cfnCustomResource.getAtt("Result").toString()))
                        .build())
                .build();

    }
}
