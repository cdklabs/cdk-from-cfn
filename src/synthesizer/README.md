# `noctilucent::synthesizer`

This module contains the synthesizers for the various supported output
languages. They transform the Intermediate Representation (IR) produced by the
`noctilucent::ir` module into AWS CDK applications in a particular language.

Each target language is exposed as a specific Cargo feature (`typescript`,
`golang`, ...), so that users can build `noctilucent` binaries tailored down to
their specific use-cases, reducing compilation time and binary size. Languages
considered "stable" are however enabled by default, while "experimental" targets
are opt-in.

The `Synthesizer` API is very simple, reciving a CloudFormation Template IR
object, and a `Writer` to which the generated code should be written. The
`noctilucent::code` module provides assistance for generating code, in
particular for maintaining correct indentation levels.
