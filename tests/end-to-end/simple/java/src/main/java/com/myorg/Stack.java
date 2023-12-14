package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.s3.*;
import software.amazon.awscdk.services.sqs.*;

class SimpleStack extends Stack {
    private Optional<Object> bucketArn;

    private Object queueArn;

    private Object isLarge;

    public Optional<Object> getBucketArn() {
        return this.bucketArn;
    }

    public Object getQueueArn() {
        return this.queueArn;
    }

    public Object getIsLarge() {
        return this.isLarge;
    }

    public SimpleStack(final Construct scope, final String id) {
        super(scope, id, null);
    }

    public SimpleStack(final Construct scope, final String id, final StackProps props) {
        this(scope, id, props, null, null);
    }

    public SimpleStack(final Construct scope, final String id, final StackProps props,
            String bucketNamePrefix,
            String logDestinationBucketName) {
        super(scope, id, props);

        bucketNamePrefix = Optional.ofNullable(bucketNamePrefix).isPresent() ? bucketNamePrefix
                : "bucket";
        logDestinationBucketName = Optional.ofNullable(logDestinationBucketName).isPresent()
                ? logDestinationBucketName
                : CfnParameter.Builder.create(this, "LogDestinationBucketName")
                        .type("AWS::SSM::Parameter::Value<String>")
                        .defaultValue("/logging/bucket/name")
                        .build()
                        .getValueAsString();

        // Mappings
        final CfnMapping booleans = new CfnMapping(this, "booleans");
        booleans.setValue("True", "true", true);
        booleans.setValue("False", "false", false);

        final CfnMapping lists = new CfnMapping(this, "lists");
        lists.setValue("Candidates", "Empty", Arrays.asList(""));
        lists.setValue("Candidates", "Singleton", Arrays.asList("One"));
        lists.setValue("Candidates", "Pair", Arrays.asList("One", "Two"));

        final CfnMapping numbers = new CfnMapping(this, "numbers");
        numbers.setValue("Prime", "Eleven", 11);
        numbers.setValue("Prime", "Thirteen", 13);
        numbers.setValue("Prime", "Seventeen", 17);

        final CfnMapping strings = new CfnMapping(this, "strings");
        strings.setValue("Foos", "Foo1", "Foo1");
        strings.setValue("Foos", "Foo2", "Foo2");
        strings.setValue("Bars", "Bar", "Bar");

        final CfnMapping table = new CfnMapping(this, "table");
        table.setValue("Values", "Boolean", true);
        table.setValue("Values", "Float", 3.14);
        table.setValue("Values", "List", Arrays.asList("1", "2", "3"));
        table.setValue("Values", "Number", 42);
        table.setValue("Values", "String", "Baz");

        Boolean isUs = Fn.select(0, Arrays.asList(this.getRegion().split("-"))).equals("us");
        Boolean isUsEast1 = this.getRegion().equals("us-east-1");
        Boolean isLargeRegion = isUsEast1;

        CfnQueue queue = CfnQueue.Builder.create(this, "Queue")
                .delaySeconds(42)
                .sqsManagedSseEnabled(false)
                .kmsMasterKeyId(Fn.importValue("Shared-KmsKeyArn"))
                .queueName(String.join("-",
                        this.getStackName(),
                        strings.findInMap("Bars", "Bar"),
                        Fn.select(1, Fn.getAzs(this.getRegion()))))
                .redrivePolicy(null)
                .visibilityTimeout(120)
                .build();

        Optional<CfnBucket> bucket = isUsEast1 ? Optional.of(CfnBucket.Builder.create(this, "Bucket")
                .accessControl("Private")
                .bucketName(bucketNamePrefix + "-" + this.getRegion() + "-bucket")
                .loggingConfiguration(CfnBucket.LoggingConfigurationProperty.builder()
                        .destinationBucketName(logDestinationBucketName)
                        .build())
                .websiteConfiguration(CfnBucket.WebsiteConfigurationProperty.builder()
                        .redirectAllRequestsTo(CfnBucket.RedirectAllRequestsToProperty.builder()
                                .hostName("example.com")
                                .protocol("https")
                                .build())
                        .build())
                .tags(Arrays.asList(
                        CfnTag.builder()
                                .key("FancyTag")
                                .value(isUsEast1 ? Fn.base64(table.findInMap("Values", "String"))
                                        : new String(Base64.getDecoder().decode("8CiMvAo=")))
                                .build()))
                .build()) : Optional.empty();

        bucket.ifPresent(_bucket -> _bucket.addMetadata("CostCenter", 1337));
        bucket.ifPresent(_bucket -> _bucket.addDependency(queue));
        bucket.ifPresent(_bucket -> _bucket.applyRemovalPolicy(RemovalPolicy.DESTROY));

        this.bucketArn = isUsEast1 ? Optional.of(bucket.isPresent() ? bucket.get().getAttrArn()
                : Optional.empty()) : Optional.empty();
        this.bucketArn.ifPresent(_bucketArn -> CfnOutput.Builder.create(this, "CfnOutputBucketArn")
                .key("BucketArn")
                .value(_bucketArn.toString())
                .description("The ARN of the bucket in this template!")
                .exportName("ExportName")
                .build());

        this.queueArn = queue.getRef();
        CfnOutput.Builder.create(this, "CfnOutputQueueArn")
                .key("QueueArn")
                .value(this.queueArn.toString())
                .description("The ARN of the SQS Queue")
                .build();

        this.isLarge = isLargeRegion ? true
                : false;
        CfnOutput.Builder.create(this, "CfnOutputIsLarge")
                .key("IsLarge")
                .value(this.isLarge.toString())
                .description("Whether this is a large region or not")
                .build();

    }
}
