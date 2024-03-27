package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.iam.*;

class StackSetStack extends Stack {
    public StackSetStack(final Construct scope, final String id) {
        super(scope, id, null);
    }

    public StackSetStack(final Construct scope, final String id, final StackProps props) {
        this(scope, id, props, null, null, null);
    }

    public StackSetStack(final Construct scope, final String id, final StackProps props,
            String moduleName,
            String roleName,
            String rolePath) {
        super(scope, id, props);

        moduleName = Optional.ofNullable(moduleName).isPresent() ? moduleName
                : "lambda_function";
        roleName = Optional.ofNullable(roleName).isPresent() ? roleName
                : "";
        rolePath = Optional.ofNullable(rolePath).isPresent() ? rolePath
                : "";
        Boolean useRoleName = !(roleName.equals(""));
        Boolean useRolePath = !(rolePath.equals(""));

        CfnRole stackSetResourceRole = CfnRole.Builder.create(this, "StackSetResourceRole")
                .roleName(useRoleName ? roleName
                        : null)
                .path(useRolePath ? rolePath
                        : "/")
                .assumeRolePolicyDocument(Map.of("Version", "2012-10-17",
                "Statement", Arrays.asList(
                        Map.of("Effect", "Allow",
                        "Principal", Map.of("Service", "lambda.amazonaws.com"),
                        "Action", "sts:AssumeRole"))))
                .policies(Arrays.asList(
                        CfnRole.PolicyProperty.builder()
                                .policyName("IAMPassRolePermissions")
                                .policyDocument(Map.of("Version", "2012-10-17",
                                "Statement", Arrays.asList(
                                        Map.of("Effect", "Allow",
                                        "Action", "iam:PassRole",
                                        "Resource", "*"))))
                                .build(),
                        CfnRole.PolicyProperty.builder()
                                .policyName("CloudFormationPermissions")
                                .policyDocument(Map.of("Version", "2012-10-17",
                                "Statement", Arrays.asList(
                                        Map.of("Effect", "Allow",
                                        "Action", "cloudformation:*",
                                        "Resource", "*"))))
                                .build(),
                        CfnRole.PolicyProperty.builder()
                                .policyName("LambdaPermissions")
                                .policyDocument(Map.of("Version", "2012-10-17",
                                "Statement", Arrays.asList(
                                        Map.of("Effect", "Allow",
                                        "Action", "logs:CreateLogGroup",
                                        "Resource", Arrays.asList(
                                                "arn:aws:logs:" + this.getRegion() + ":" + this.getAccount() + ":*")),
                                        Map.of("Effect", "Allow",
                                        "Action", Arrays.asList(
                                                "logs:CreateLogStream",
                                                "logs:PutLogEvents"),
                                        "Resource", Arrays.asList(
                                                "arn:aws:logs:" + this.getRegion() + ":" + this.getAccount() + ":log-group:/aws/lambda/*")))))
                                .build(),
                        CfnRole.PolicyProperty.builder()
                                .policyName("S3Permissions")
                                .policyDocument(Map.of("Version", "2012-10-17",
                                "Statement", Arrays.asList(
                                        Map.of("Effect", "Allow",
                                        "Action", Arrays.asList(
                                                "s3:Get*",
                                                "s3:List*"),
                                        "Resource", "*"))))
                                .build()))
                .build();

    }
}
