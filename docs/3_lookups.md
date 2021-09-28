# Noctilucent Lookup Tables

This document describes the breakdown of how the Mappings section of a CloudFormation template is converted to CDK 
typescript in Noctilucent.

## Where does this fit? 

See [1_overview.md](./1_overview.md) for information on where a Mapping resource in a CloudFormation template
will get transpiled to in the produced CDK.

## Example

All Mappings will be in a Lookup Table area that are just giant hashmaps.

If you have a large mappings like...

```
    "LogAccessRoleMappingProd": {
      "ARN": {
        "PrincipalArn": "111111111111:role/LogAccessRole",
        "ResourceArnPrefix": "222233334444:role/LambdaReadOnly"
      },
      ...
    }
```

then this gets translated to

```
const LogAccessRoleMappingProd Map<String, Map<String, String>> {
   "ARN" : {
        "PrincipalArn": "111111111111:role/LogAccessRole",
        "ResourceArnPrefix": "222233334444:role/LambdaReadOnly"
   }
}
```

and then all meta lookups into the table will be replaced with hashmap lookups.

## High Level Overview

There are two parts that need to be solved here: Parsing and Synthesis. Parsing is responsible for converting the 
Mappings to an internal representation. Synthesis is responsible for translating the internal representation to 
CDK typescript that can be used in the rest of the CDK document.

### Parsing

Let's start with some basic terminology. Using the below example:

```
"LogAccessRoleMappingProd [1]": {
      "ARN [2]": {
        "PrincipalArn [3]": "111111111111:role/LogAccessRole [4]",
        "ResourceArnPrefix": "222233334444:role/LambdaReadOnly"
      }[5],
}[6],
...
```

we define the following terms:

1. `LogAccessRoleMappingProd` as **OuterMappingName**
2. `ARN` as **OuterMappingKey**
3. `PrincipalArn` as **InnerMappingKey**
4. `111111111111:role/LogAccessRole` as **InnerMappingValue**
5. 
```
{
  "PrincipalArn": "111111111111:role/LogAccessRole",
  "ResourceArnPrefix": "222233334444:role/LambdaReadOnly"
}
``` 
   as **InnerMapping**
```
"LogAccessRoleMappingProd": {
      "ARN": {
        "PrincipalArn": "111111111111:role/LogAccessRole",
        "ResourceArnPrefix": "222233334444:role/LambdaReadOnly"
      },
}
```
   as **OuterMapping**

The basic flow looks something like:

1. Create tracker for all mappings, structure looks like: Map<String, Map<String, Map<String, String|List<String>>>
2. Start tracking for new outer mapping with key set to OuterMappingName
   1. Build a map entry, where
      1. Key name matches OuterMappingKey
      2. Value is a Map<String, String|List<String>> that will represent the InnerMapping
         1. Iterate through entries in the InnerMapping add them to internal Map representation
3. Repeat for next mapping

### Synthesis

After all maps are created the CDK typescript mapping will be generated 

1. Iterate through entry-set of mappings
   1. Start mapping declaration as `const <name> = ` where name is the key (OuterMappingName) from the entry-set
   2. Construct value from entry-set value (OuterMapping) as
      1. Start value `new Map(`
      2. Iterate through entry-set of OuterMapping
         1. Start entry `[`
         2. Add key `\"<key>\"` where key is OuterMappingKey
         3. Start value `new Map(`
         4. Iterate through entry-set of InnerMapping
            1. Start entry `[`
            2. Add key `\"<key>\"` where key is InnerMappingKey
            3. Add value where value is either:
               1. `\"<value>\"` - simple string value, or
               2. `[\"<value1>\",\"<value2>\",...,\"<valueN>\"]` - List of strings
            4. End entry `]`
         5. End value `)`
         6. End entry `]`
      3. End value `)`

  


