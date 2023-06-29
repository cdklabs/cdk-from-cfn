package com.acme.test.vpc;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.*;
import software.amazon.awscdk.Fn.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;


import software.amazon.awscdk.services.ec2.*;

interface NoctStackProps extends StackProps {
}
class GenericSet<T> {
    private final Set<T> set = new HashSet<>();

    public GenericSet<T> add(final T object) {
        this.set.add(object);
        return this;
    }

    public Set<T> get() {
        return this.set;
    }
}

class GenericList<T> {
    private final List<T> list = new LinkedList<>();

    public GenericList<T> add(final T object) {
        this.list.add(object);
        return this;
    }
    public List<T> get() {
        return this.list;
    }
}

class GenericMap<T, S> {
    private final Map<T, S> map = new HashMap<>();

    public GenericMap<T, S> add(final T key, final S value) {
        this.map.put(key, value);
        return this;
    }

    public Map<T, S> get() {
        return this.map;
    }

    public List<CfnTag> getTags() {
        final List<CfnTag> tags = new LinkedList<>();
        for(Map.Entry<T,S> entry : this.map.entrySet()) {
            tags.add(CfnTag.builder().key(String.valueOf(entry.getKey())).value(String.valueOf(entry.getValue())).build());
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

public class NoctStack extends Stack {
	public NoctStack(final Construct scope, final String id) {
		super(scope, id, null);
	}
	public NoctStack(final Construct scope, final String id, final StackProps props) {
		super(scope, id, props);
		{ // Start Mapping section
		} // End Mapping section


		CfnVPC vpc = CfnVPC.Builder.create(this, "VPC")
			.cidrBlock("10.42.0.0/16").enableDnsSupport(true).enableDnsHostnames(true).tags().build();


		CfnSubnet subnet1 = CfnSubnet.Builder.create(this, "Subnet1")
			.availabilityZone().cidrBlock().vpcId().build();


		CfnSubnet subnet2 = CfnSubnet.Builder.create(this, "Subnet2")
			.availabilityZone().cidrBlock().vpcId().build();


		CfnSubnet subnet3 = CfnSubnet.Builder.create(this, "Subnet3")
			.availabilityZone().cidrBlock().vpcId().build();

	}
}
