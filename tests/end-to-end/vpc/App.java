package com.acme.test.vpc;

import software.constructs.Construct;

import java.util.*;
import java.util.stream.Collectors;
import software.amazon.awscdk.*;
import software.amazon.awscdk.App;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.services.ec2.*;

public class NoctApp {
  public static void main(final String[] args) {
    App app = new App();
    StackProps props = StackProps.builder()
      .build();
    new VpcStack(app, "MyProjectStack", props);
    app.synth();
  }
}

interface VpcStackProps extends StackProps {
}

class VpcStack extends Stack {
  public VpcStack(final Construct scope, final String id) {
    super(scope, id, null);
  }
  public VpcStack(final Construct scope, final String id, final StackProps props) {
    super(scope, id, props);
    // Start Mapping section

    CfnVPC vpc = CfnVPC.Builder.create(this, "VPC")
        .cidrBlock("10.42.0.0/16")
        .enableDnsSupport(true)
        .enableDnsHostnames(true)
        .tags(new GenericList<CfnTag>()
          .extend(new GenericMap<String, Object>()
          .extend("cost-center",1337)
          .getTags()))
      .build();


    CfnSubnet subnet1 = CfnSubnet.Builder.create(this, "Subnet1")
        .availabilityZone(Fn.select(0,get(Fn.getAzs(""))))
        .cidrBlock(Fn.select(0,get(Fn.cidr(String.valueOf(Fn.getAtt("VPC", "CidrBlock")), 6, String.valueOf(8)))))
        .vpcId("VPC")
      .build();


    CfnSubnet subnet2 = CfnSubnet.Builder.create(this, "Subnet2")
        .availabilityZone(Fn.select(1,get(Fn.getAzs(""))))
        .cidrBlock(Fn.select(1,get(Fn.cidr(String.valueOf(Fn.getAtt("VPC", "CidrBlock")), 6, String.valueOf(8)))))
        .vpcId("VPC")
      .build();


    CfnSubnet subnet3 = CfnSubnet.Builder.create(this, "Subnet3")
        .availabilityZone(Fn.select(2,get(Fn.getAzs(""))))
        .cidrBlock(Fn.select(2,get(Fn.cidr(String.valueOf(Fn.getAtt("VPC", "CidrBlock")), 6, String.valueOf(8)))))
        .vpcId("VPC")
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

