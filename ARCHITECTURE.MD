# cdk-from-cfn Architecture Overview

This document provides a high level overview of the key components in the cdk-from-cfn project and their responsibilities

## Processing Flow

The easiest way to understand the purpose behind the core components of `cdk-from-cfj`, is to look at the high-level processing flow 
of transforming a Cloudformation Template into a CDK Application:
```
CloudFormation Template
           ↓ (Parser)
Cloudformation Parse Tree
           ↓ (IR)
Cloudformation Program Ir
           ↓ (Synthesizer)
Generated CDK Code
```

Put simply, the idea behind the cdk-from-cfn processing flow is to transform a 
CFN template into an IR, and then use that IR plus a language synthesizer to generate a CDK Application.

To do so, the parser reads the text from the provided Cloudformation template and generates a simple, un-validated, data structure
called the `CloudformationParseTree` which is essentially a 1:1 in memory representation of the provided template

However the `CloudformationParseTree` is not sufficient for application synthesis and needs to be enriched with additional 
information and validated against the schema for correctness. This is the purpose of the `IR` which generates a `CloudformationProgramIr`.

A language specific synthesizer can then read the IR and use it to generate CDK stack code. 

In rust code this flow would look like:
```rust
// 1. Parse CloudFormation template
let cfn_tree: CloudformationParseTree = serde_yaml::from_str(template)?;

// 2. Convert to IR
let ir = CloudformationProgramIr::from(cfn_tree, schema)?;

// 3. Synthesize to target language
let synthesizer = TypeScript {};
ir.synthesize(synthesizer, output, stack_name)?;
```

## Core Components Overview

### Parser

Responsible for de-serializing the Cloudformation template into a `CloudformationParseTree` data structure. The parser's sole responsibility is creating a 1:1 representation of the template structure, without performing any validation or enhancement.

Key responsibilities:
- Reads YAML/JSON Cloudformation templates
- Creates corresponding Rust data structures
- Parses all template sections (Resources, Parameters, Conditions, etc.)
- Handles Cloudformation intrinsic functions (Fn::Join, Ref, etc.)

```rust
// CloudFormation Template
{
  "Resources": {
    "MyBucket": {
      "Type": "AWS::S3::Bucket",
      "Properties": {
        "BucketName": {
          "Fn::Join": ["-", ["mybucket", {"Ref": "AWS::Region"}]]
        }
      }
    }
  }
}

// Parse Tree - Just maps the structure directly
CloudformationParseTree {
    resources: {
        "MyBucket" => ResourceAttributes {
            resource_type: "AWS::S3::Bucket",
            properties: {
                "BucketName" => ResourceValue::IntrinsicFunction(
                    Fn::Join {
                        sep: "-",
                        list: ["mybucket", Ref("AWS::Region")]
                    }
                )
            }
        }
    }
}
```

### IR (Intermediate Representation)

Responsible for converting the raw ParseTree into a validated and enriched `CloudformationProgramIr` data structure. The IR's main purpose is to add necessary CDK-specific information and validate resources against the CDK schema before code generation.

Key responsibilities:
- Validates resources and properties against CDK schema
- Resolves references and tracks dependencies between resources
- Enhances references with type and origin information
- Orders resources based on dependencies
- Adds necessary CDK imports and type information

```rust
// IR - Adds understanding and validation
CloudformationProgramIr {
    resources: [
        ResourceInstruction {
            name: "MyBucket",
            resource_type: ResourceType::AWS { 
                service: "S3", 
                type_name: "Bucket" 
            },
            properties: {
                "bucketName": ResourceIr::Join(
                    "-",
                    [
                        ResourceIr::String("mybucket"),
                        ResourceIr::Ref(Reference {
                            origin: Origin::PseudoParameter(Region),
                            name: "AWS::Region"
                        })
                    ]
                )
            },
            // Additional validated information:
            references: ["AWS::Region"],  // Tracks dependencies
            condition: None,
            deletion_policy: None
        }
    ]
}
```

### Synthesizer

Responsible for converting the validated IR into CDK code in a specific target language. The synthesizer's main purpose is to generate idiomatic code that properly represents the CloudFormation resources as CDK constructs.

Key responsibilities:
- Converts IR constructs to language-specific CDK code
- Manages imports and module dependencies
- Handles language-specific code patterns (builders, properties, etc.)
- Generates properly formatted and structured code
- Implements string interpolation and type conversion for each language
