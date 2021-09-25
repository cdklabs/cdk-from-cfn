# Noctilucent Conditions

This document describes the breakdown of how to do conditions resolution in Noctilucent.

## v.beta

For Beta, Conditions will only support resolution of the following:

* Ref of Parameters
* 2 Intrinsics (AWS::Region / AWS::Partition)
* Fn::Equals
* Fn::Or
* Fn::And
* Condition: "NAME"
* Fn::Not
* String

This covers 100% of the use cases in the sample template, and which is one of the more heavy examples.

In order to achieve this resolution, we will need an internal representation for:
* Ref names
* Intrinsics

As they need to be replaced with variable names in code. 

## 2 Phase Conditions

In order to succeed in v.beta, Conditions must be supported. 

An example of this:

```
    "IsInCanadaOrVirginia": {
      "Fn::Or": [
        {
          "Fn::Equals": [
            "us-east-1",
            {
              "Ref": "AWS::Region"
            }
          ]
        },
        {
          "Fn::Equals": [
            "ca-central-1",
            {
              "Ref": "AWS::Region"
            }
          ]
        },
        {
          "Condition": "IsBeta"
        }
      ]
    },
    "IsBeta": {
      "Fn::Equals": [
        {
          "Ref": "Stage"
        },
        "BETA"
      ]
    },
```

This is a valid condition set, which **requires** the following ordering in typescript, in order to remain correct:

```
- const isBeta = ( props.stage == "BETA" );
- const isInCanadaOrVirginia = ( isBeta || ("us-east-1" == this.region) || ("ca-central-1" == this.region)
```

But the ordering of the conditions in json are in a map which is unordered. This means the two-phases:

1. Loop through and parse an internal representation of Conditions
2. dep-chain: Look through Condition blocks and add dependency chains, such as `IsCelluar -> IsBeta`
3. When outputting, reverse output by dependencies.

This will always ensure a correct program in typescript (if the json is correct).

## Synthesis

Due to the small language set, recursive resolution of conditions should work for all cases.

### Synthesis: Ref of parameters

A Ref Condition will have an internal representation of: `Ref(string)` (TODO: can the string be recursively resolved? 
E.g. "Ref": { If ... } , I don't think so, so for this version we will not recursively resolve).

It will synthesize as a name of a prop, since all parameters will be props.

So:

`{ "Ref" : "Stage" }` synthesizes as `props.stage`. 

While here, all parameter's first characters will be lowercased, while the rest kept the same to transform from pascal-case
to camel-case. This is a stylistic decision we may revert.

The string will look up if it's an intrinsic function.

**Intrinsic Function subcase**

Both intrinsics supported out the gate will be replaced with "this.<intrinsic>". Since the core.Stack in CDK supports
all intrinsics from the get-go, we will heavily rely on it for intrinsic replacement.

Specifically, in cdk, if you extend from a stack, you get:
* Region
* Partition
* StackId
* NotificationArns

as references, which are 4 very easy to find-replace for synthesis

### Synthesis: Intrinsics

Intrinsics can only be found in Ref and Sub functions. Look at these sections to understand usage.

### Synthesis: Fn::And / Fn::Or 

Both `and` and `or` are recursively resolved by other condition functions, such as equal, other ors/ands, ifs, refs, etc.

In typescript, parenthesis are respected to be resolved first, so to cleanly transpile these two functions, we will 
translate to the following:

*Or* : `( <condition_0> || <condition_1> ... || <condition_n> )` where n is the amount of conditions in the array's internal
representation. In reality, this is about 20, since that's all cloudformation supports.

*And*, follows the same pattern: `( <condition_0> && <condition_1> ... && <condition_n> )` .

By recursively resolving internal conditions, if you have something like:

```json
{
  "ShouldCreateResource": {
    "Fn::And": [
      {
        "Condition": "IsOtherCondition"
      },
      {
        "Fn::Or": [
          {
            "Fn::Equals": [
              "BETA",
              {
                "Ref": "Stage"
              }
            ]
          },
          {
            "Fn::Equals": [
              "GAMMA",
              {
                "Ref": "Stage"
              }
            ]
          },
          {
            "Fn::And": [
              {
                "Fn::Not": [
                  {
                    "Condition": "IsPersonalAccount"
                  }
                ]
              },
              {
                "Fn::Not": [
                  {
                    "Condition": "IsConstrained"
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
```
Then you start with the first outter `and` and do: 
1. Build `(` 
2. start resolving first condition
3. First condition is literally `Condition` which resolves by replacing with condition name `isRootCell`
4. exit back out to outer `and`, build " && ".
5. Second condition is or, start building: `(`
6. Inner part of Or is equals, start resolving equal's first condition: String. Emit string. `"BETA"`
7. Before second part of Equals, emit ` == `
8. Second part of Equals is `Ref`, emis `props.stage`
9. Exit Equals, enter next part of or: equals again.
10. Emit " || " from the `Fn::Or`
11. To skip some process, this turns out to be `"GAMMA" == props.stage`
12. ... and onward.

Just the part we built looks like `(isSomeOtherCondition && ("BETA" == props.stage || "GAMMA" == props.stage)...)` which is the correct form. 

Using the semantics of typescript, and using Inorder traversal on the tree of enums, we can build the correct output for *All conditions*.

### Synthesis: Fn::Equals

This follows roughly the same pattern of `Fn::And`, as it's recursively resolved.

The system will do the following:

1. Resolve and emit the left hand of the equals.
2. Output ` === `
3. Resolve and emit the right hand of the equals

### Synthesis: Fn::Not

Similar to `Fn::And` / `Fn::Equal`

1. Output `!(`
2. Resolve condition and emit.
3. Output `)`

### Synthesis: Condition: "NAME"

There is a second pass that orders the conditions in the correct ordering, so synthesis of this will not take that into account.

This simplifies the condition output to just be:

1. Output NAME

The ordering procedure outputs

`const NAME = ...` and so just referring to NAME will give the correct value.
