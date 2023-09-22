package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.services.iam.*;
import software.amazon.awscdk.services.sqs.*;

class JsonPropsStack extends Stack {
    public JsonPropsStack(final Construct scope, final String id) {
        super(scope, id, null);
    }

    public JsonPropsStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        CfnQueue myQueue1 = CfnQueue.Builder.create(this, "MyQueue1")
                .build();

        CfnQueue myQueue2 = CfnQueue.Builder.create(this, "MyQueue2")
                .build();

        CfnGroup myRdMessageQueueGroup = CfnGroup.Builder.create(this, "MyRDMessageQueueGroup")
                .policies(Arrays.asList(
                        CfnGroup.PolicyProperty.builder()
                                .policyName("MyQueueGroupPolicy")
                                .policyDocument(Map.of("Statement", Arrays.asList(
                                        Map.of("Effect", "Allow",
                                        "Action", Arrays.asList(
                                                "sqs:DeleteMessage",
                                                "sqs:ReceiveMessage"),
                                        "Resource", Arrays.asList(
                                                myQueue1.getAttrArn(),
                                                myQueue2.getAttrArn())))))
                                .build()))
                .build();

    }
}
