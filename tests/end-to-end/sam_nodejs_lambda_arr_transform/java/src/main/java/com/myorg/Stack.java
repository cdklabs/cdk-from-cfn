package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.sam.*;

class SAMNodeJSLambda extends Stack {
    public SAMNodeJSLambda(final Construct scope, final String id) {
        super(scope, id, null);
    }

    public SAMNodeJSLambda(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        this.addTransform("AWS::Serverless-2016-10-31");

        CfnFunction myFunction = CfnFunction.Builder.create(this, "MyFunction")
                .runtime("nodejs18.x")
                .handler("index.handler")
                .inlineCode("""
                exports.handler = async (event) => {
                  console.log(event);
                }
                """)
                .build();

    }
}
