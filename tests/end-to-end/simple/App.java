package com.acme.test.simple;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.*;
import software.amazon.awscdk.Fn.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;


import software.amazon.awscdk.services.s3.*;
import software.amazon.awscdk.services.sqs.*;

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
		final Mapping<Boolean> booleans = new Mapping<Boolean>(this, "Booleans");
		booleans.put("True", "true", true));
		booleans.put("False", "false", false);
		final CfnMapping booleansCfnMapping = booleans.get();

		final Mapping<List<String>> lists = new Mapping<List<String>>(this, "Lists");
		lists.put("Candidates", "Empty", List.of(
		));lists.put("Candidates", "Singleton", List.of(
			"One",
		));lists.put("Candidates", "Pair", List.of(
			"One",
			"Two",
		));final CfnMapping listsCfnMapping = lists.get();

		final Mapping<Integer> numbers = new Mapping<Integer>(this, "Numbers");
		numbers.put("Prime", "Eleven", 11);
		numbers.put("Prime", "Thirteen", 13);
		numbers.put("Prime", "Seventeen", 17);
		final CfnMapping numbersCfnMapping = numbers.get();

		final Mapping<String> strings = new Mapping<String>(this, "Strings");
		strings.put("Foos", "Foo1", "Foo1");
		strings.put("Foos", "Foo2", "Foo2");
		strings.put("Bars", "Bar", "Bar");
		final CfnMapping stringsCfnMapping = strings.get();

		final Mapping<Boolean> table = new Mapping<Boolean>(this, "Table");
		table.put("Values", "Boolean", true));
		table.put("Values", "Float", 3.14);
		table.put("Values", "List", List.of(
			"1",
			"2",
			"3",
		));table.put("Values", "Number", 42);
		table.put("Values", "String", "Baz");
		final CfnMapping tableCfnMapping = table.get();

		} // End Mapping section


		CfnQueue queue = CfnQueue.Builder.create(this, "Queue")
			.delaySeconds("42.1337").fifoQueue(false).kmsMasterKeyId("Shared.KmsKeyArn").queueName().redrivePolicy(null).visibilityTimeout().build();


		CfnBucket bucket = CfnBucket.Builder.create(this, "Bucket")
			.accessControl("private").bucketName().tags().build();

		Fn.conditionEquals(Fn.select(0, Fn.split("-"), Fn.ref(/* TODO */))), "us")Fn.conditionEquals(Fn.ref(/* TODO */), "us-east-1")""IsUsEast1""CfnOutput.Builder.create(this, "BucketArn")
			.value()
			.export(""ExportName"")
			.description("The ARN of the bucket in this template!")
			.condition("IsUsEast1")
		.build();
		CfnOutput.Builder.create(this, "QueueArn")
			.value()
			.description("The ARN of the SQS Queue")
		.build();
		CfnOutput.Builder.create(this, "IsLarge")
			.value()
			.description("Whether this is a large region or not")
		.build();
	}
}
