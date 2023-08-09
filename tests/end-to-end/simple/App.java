package com.acme.test.simple;

import software.constructs.Construct;

import java.util.*;
import java.util.stream.Collectors;
import software.amazon.awscdk.*;
import software.amazon.awscdk.App;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.services.s3.*;
import software.amazon.awscdk.services.sqs.*;

public class NoctApp {
  public static void main(final String[] args) {
    App app = new App();
    StackProps props = StackProps.builder()
      .description("An example stack that uses many of the syntax elements permitted in a" + 
        "CloudFormation template, but does not attempt to represent a realistic stack.")
      .build();
    new SimpleStack(app, "MyProjectStack", props);
    app.synth();
  }
}

interface SimpleStackProps extends StackProps {
}

class SimpleStack extends Stack {
  private CfnOutput bucketArn, queueArn, isLarge;

  public CfnOutput getBucketArn() {
    return this.bucketArn;
  }
  public CfnOutput getQueueArn() {
    return this.queueArn;
  }
  public CfnOutput getIsLarge() {
    return this.isLarge;
  }
  public SimpleStack(final Construct scope, final String id) {
    super(scope, id, null);
  }
  public SimpleStack(final Construct scope, final String id, final StackProps props) {
    super(scope, id, props);
    // Start Mapping section
    final Mapping<Boolean> booleans = new Mapping<>(this, "Booleans");
    booleans.put("True", "true", true);
    booleans.put("False", "false", false);
    final CfnMapping booleansCfnMapping = booleans.get();

    final Mapping<List<String>> lists = new Mapping<>(this, "Lists");
    lists.put("Candidates", "Empty", new GenericList<String>());
    lists.put("Candidates", "Singleton", new GenericList<String>()
        .extend("One"));
    lists.put("Candidates", "Pair", new GenericList<String>()
        .extend("One")
        .extend("Two"));
    final CfnMapping listsCfnMapping = lists.get();

    final Mapping<Integer> numbers = new Mapping<>(this, "Numbers");
    numbers.put("Prime", "Eleven", 11);
    numbers.put("Prime", "Thirteen", 13);
    numbers.put("Prime", "Seventeen", 17);
    final CfnMapping numbersCfnMapping = numbers.get();

    final Mapping<String> strings = new Mapping<>(this, "Strings");
    strings.put("Foos", "Foo1", "Foo1");
    strings.put("Foos", "Foo2", "Foo2");
    strings.put("Bars", "Bar", "Bar");
    final CfnMapping stringsCfnMapping = strings.get();

    final Mapping<Object> table = new Mapping<>(this, "Table");
    table.put("Values", "Boolean", true);
    table.put("Values", "Float", 3.14);
    table.put("Values", "List", new GenericList<String>()
        .extend("1")
        .extend("2")
        .extend("3"));
    table.put("Values", "Number", 42);
    table.put("Values", "String", "Baz");
    final CfnMapping tableCfnMapping = table.get();

    final String bucketNamePrefix = CfnParameter.Builder.create(this, "BucketNamePrefix")
      .type("String")
      .description("The prefix for the bucket name")
      .defaultValue("bucket")
      .build()
      .getValueAsString();
    final String logDestinationBucketName = CfnParameter.Builder.create(this, "LogDestinationBucketName")
      .type("AWS::SSM::Parameter::Value<String>")
      .defaultValue("/logging/bucket/name")
      .build()
      .getValueAsString();
    CfnCondition isUs = CfnCondition.Builder.create(this, "IsUs").expression(Fn.conditionEquals(Fn.select(0, get(Fn.split("-", this.getRegion()))), "us")).build();
    CfnCondition isUsEast1 = CfnCondition.Builder.create(this, "IsUsEast1").expression(Fn.conditionEquals(this.getRegion(), "us-east-1")).build();
    CfnCondition isLargeRegion = CfnCondition.Builder.create(this, "IsLargeRegion").expression(isUsEast1).build();

    CfnQueue queue = CfnQueue.Builder.create(this, "Queue")
        .delaySeconds(42.1337)
        .fifoQueue(false)
        .kmsMasterKeyId("Shared.KmsKeyArn")
        .queueName(Fn.join("-", new GenericList<String>()
          .extend(this.getStackName())
          .extend(Fn.findInMap("Strings", "Bars", "Bar"))
          .extend(Fn.select(1,get(Fn.getAzs(String.valueOf(this.getRegion())))))))
        .redrivePolicy(null)
        .visibilityTimeout(Integer.valueOf(Fn.select(1,get(new GenericList<Integer>()
          .extend(60)
          .extend(120)
          .extend(240)))))
      .build();


    CfnBucket bucket = CfnBucket.Builder.create(this, "Bucket")
        .accessControl("private")
        .bucketName(Fn.sub(String.valueOf(bucketNamePrefix), new GenericMap<String, String>()
          .extend("-", this.getStackName())))
        .loggingConfiguration(CfnBucket.LoggingConfigurationProperty.builder()
          .destinationBucketName(logDestinationBucketName)
          .build())
        .websiteConfiguration(CfnBucket.WebsiteConfigurationProperty.builder()
          .indexDocument("index.html")
          .errorDocument("error.html")
          .redirectAllRequestsTo(CfnBucket.RedirectAllRequestsToProperty.builder()
          .hostName("example.com")
          .protocol("https")
          .build())
          .build())
        .tags(new GenericList<CfnTag>()
          .extend(new GenericMap<String, Object>()
          .extend("FancyTag",Fn.conditionIf("IsUsEast1", Fn.base64(String.valueOf(Fn.findInMap("Table", "Values", "String"))), Fn.base64(String.valueOf("8CiMvAo="))))
          .getTags()))
      .build();

    bucket.addMetadata("CostCenter", 1337);

    bucket.addDependency(queue);

    bucket.applyRemovalPolicy(RemovalPolicy.RETAIN);

    bucketArn = CfnOutput.Builder.create(this, "BucketArn")
      .value(String.valueOf(Fn.getAtt("Bucket", "Arn")))
      .description("The ARN of the bucket in this template!")
      .exportName("ExportName")
      .condition(isUsEast1)  .build();
    queueArn = CfnOutput.Builder.create(this, "QueueArn")
      .value(String.valueOf("Queue"))
      .description("The ARN of the SQS Queue")  .build();
    isLarge = CfnOutput.Builder.create(this, "IsLarge")
      .value(String.valueOf(Fn.conditionIf("IsLargeRegion", true, false)))
      .description("Whether this is a large region or not")  .build();
  }

  public static <T> List<String> get(final List<T> input) {
    return input.stream().map(String::valueOf).collect(Collectors.toList());
  }
}
class GenericList<T> extends LinkedList<T> {
  public GenericList<T> extend(final T object) {
    this.addLast(object);
    return this;
  }

  public GenericList<T> extend(final List<T> collection) {
    this.addAll(collection);
    return this;
  }
}

class GenericMap<T, S> extends HashMap<T, S> {
  public GenericMap<T, S> extend(final T key, final S value) {
    this.put(key, value);
    return this;
  }

  public List<CfnTag> getTags() {
    final List<CfnTag> tags = new LinkedList<>();
    for (Map.Entry<T, S> entry : this.entrySet()) {
      tags.add(
          CfnTag.builder()
              .key(String.valueOf(entry.getKey()))
              .value(String.valueOf(entry.getValue()))
              .build());
    }
    return tags;
  }
}

class Mapping<T> {
  private final String name;
  private final Construct scope;
  private final Map<String, Map<String, T>> inner = new TreeMap<>();

  public Mapping(Construct scope, String name) {
    this.name = name;
    this.scope = scope;
  }

  public Mapping<T> put(String primaryKey, String secondaryKey, T value) {
    final Map<String, T> map = inner.getOrDefault(primaryKey, new TreeMap<>());
    map.put(secondaryKey, value);
    inner.put(primaryKey, map);
    return this;
  }

  public CfnMapping get() {
    return CfnMapping.Builder.create(this.scope, this.name).mapping(this.inner).build();
  }
}

