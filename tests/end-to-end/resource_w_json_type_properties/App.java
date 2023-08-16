package com.acme.test.resource_w_json_type_properties;

import software.constructs.Construct;

import java.util.*;
import java.util.stream.Collectors;
import software.amazon.awscdk.*;
import software.amazon.awscdk.App;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.services.iam.*;
import software.amazon.awscdk.services.sqs.*;

public class NoctApp {
  public static void main(final String[] args) {
    App app = new App();
    StackProps props = StackProps.builder()
      .build();
    new JsonPropsStack(app, "MyProjectStack", props);
    app.synth();
  }
}

interface JsonPropsStackProps extends StackProps {
}

class JsonPropsStack extends Stack {
  public JsonPropsStack(final Construct scope, final String id) {
    super(scope, id, null);
  }
  public JsonPropsStack(final Construct scope, final String id, final StackProps props) {
    super(scope, id, props);
    // Start Mapping section

    CfnQueue myQueue1 = CfnQueue.Builder.create(this, "MyQueue1")
      .build();


    CfnQueue myQueue2 = CfnQueue.Builder.create(this, "MyQueue2")
      .build();


    CfnGroup myRdMessageQueueGroup = CfnGroup.Builder.create(this, "MyRDMessageQueueGroup")
        .policies(new GenericList<CfnTag>()
          .extend(CfnGroup.PolicyProperty.builder()
          .policyName("MyQueueGroupPolicy")
          .policyDocument(new GenericMap<String, JsonNode jsonNode = objectMapper.readTree(jsonString);>()
          .extend(Statement, new GenericList<JsonNode jsonNode = objectMapper.readTree(jsonString);>()
          .extend(new GenericMap<String, JsonNode jsonNode = objectMapper.readTree(jsonString);>()
          .extend(Effect, "Allow")
          .extend(Action, new GenericList<JsonNode jsonNode = objectMapper.readTree(jsonString);>()
          .extend("sqs:DeleteMessage")
          .extend("sqs:ReceiveMessage"))
          .extend(Resource, new GenericList<JsonNode jsonNode = objectMapper.readTree(jsonString);>()
          .extend(Fn.getAtt("MyQueue1", "Arn"))
          .extend(Fn.getAtt("MyQueue2", "Arn"))))))
          .build()))
      .build();

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

