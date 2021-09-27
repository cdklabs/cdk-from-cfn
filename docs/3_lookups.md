# Noctilucent Lookup Tables

This document describes the breakdown of how to do lookup table resolution in Noctilucent.

## Where does this fit? 

See [1_overview.md](replace with ref to file) for information on where a Mapping resource in a CloudFormation template
will get transpiled to in the produced CDK.

## Example

All Mappings will be in a Lookup Table area that are just giant hashmaps.

If you have a large mappings like...

```
    "AardvarkFlowLogAccessRoleMappingProd": {
      "ARN": {
        "PrincipalArn": "118920060295:role/AardvarkFlowLogAccessRole",
        "ResourceArnPrefix": "915915706018:role/AardvarkLambdaReadOnly"
      },
      ...
    }
```

then this gets translated to

```
const AardvarkFlowLogAccessRoleMappingProd Map<String, Map<String, String>> {
   "ARN" : {
        "PrincipalArn": "118920060295:role/AardvarkFlowLogAccessRole",
        "ResourceArnPrefix": "915915706018:role/AardvarkLambdaReadOnly"
   }
}
```

and then all meta lookups into the table will be replaced with hashmap lookups.

## Synthesis

There are two parts that need to be solved here. The first is to convert the Mapping structure in CloudFormation to CDK
maps. The second problem is to expose the name of these maps so they can be used by conditions and resources that
are generated at a later point.

Each mapping consists of a name and a key-value pair, where the value is another map. This can be built use recursion.

### Building Maps

Let's start with some basic terminology. Using the below example:

```
"AardvarkFlowLogAccessRoleMappingProd": {
      ````"ARN": {
        "PrincipalArn": "118920060295:role/AardvarkFlowLogAccessRole",
        "ResourceArnPrefix": "915915706018:role/AardvarkLambdaReadOnly"
      },
},
...
```

we create the following terms:

* `AardvarkFlowLogAccessRoleMappingProd` as **OuterMappingName**
* `ARN` as **OuterMappingKey**
* ```
  {
  "PrincipalArn": "118920060295:role/AardvarkFlowLogAccessRole",
  "ResourceArnPrefix": "915915706018:role/AardvarkLambdaReadOnly"
  }
  ``` 
  as **InnerMapping** 

The basic flow looks something like:

1. Create tracker for all mappings, structure looks like: Map<String, Map<String, Map<String, String>>
2. Start tracking for new outer mapping with key set to OuterMappingName
   1. Add new key-value entry, where
      1. key name matches OuterMappingKey
      2. Value is a Map<String, String> that will represent the InnerMapping
   2. Iterate through entries in the InnerMapping add them to Map assigned as value of the OuterMappingKey
3. Repeat for next mapping

### Publish

After all maps are created the CDK will be generated as follows:

1. Iterate through entry-set of mappings
2. Declare const with name matching key
3. Set value of const to be a dump of the OuterMapping represented by its value


