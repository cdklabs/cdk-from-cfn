package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.s3.*;

class BucketConstruct extends Construct {
    public BucketConstruct(final Construct scope, final String id) {
        super(scope, id);


        CfnBucket bucket = CfnBucket.Builder.create(this, "Bucket")
                .build();

    }
}
