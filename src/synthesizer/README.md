# `cdk_from_cfn::synthesizer`

This module contains the synthesizers for the various supported output
languages. They transform the Intermediate Representation (IR) produced by the
`cdk_from_cfn::ir` module into AWS CDK applications in a particular language.

Each target language is exposed as a specific Cargo feature (`typescript`,
`golang`, ...), so that users can build `cdk_from_cfn` binaries tailored down to
their specific use-cases, reducing compilation time and binary size. Languages
considered "stable" are however enabled by default, while "experimental" targets
are opt-in.

The `Synthesizer` API is very simple, receiving a CloudFormation Template IR
object, and a `Writer` to which the generated code should be written. The
`cdk_from_cfn::code` module provides assistance for generating code, in
particular for maintaining correct indentation levels.
