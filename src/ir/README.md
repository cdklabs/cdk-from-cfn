# `cdk_from_cfn::ir`

This module contains the Intermediate Representation (IR) `cdk_from_cfn` uses in
order to facilitate translating CloudFormation templates into AWS CDK
applications. The IR data structures are obtained by transforming Parse Trees
produced by the `cdk_from_cfn::parser` module.

The conversion is informed by a copy of the [AWS CloudFormation Resource
Specification][cfnspec] document, which provides information about properties
accepted (and attributes returned) by the various supported CloudFormation
Resource Types.

The IR is composed of various kinds of "instructions" (which can also be
thought about as declarations), which will compose the final AWS CDK
application:

- `ImportInstruction` convey information about modules that need importing in
  order to bring the necessary AWS CDK constructs in-scope;
- `ResourceInstruction` models a single CloudFormation Resource construct
  instanciation, listing the provided properties and their associated values;
- `OutputInstruction` represents properties exposed by the generated AWS CDK
  Stack class, optionally bound to a CloudFormation Output object;
- etc...

The IR is topologically sorted so that `cdk_from_cfn::synthesizer` can process
instructions in the order they are provided, resulting in a program with
correctly ordered declarations (while CloudFormation templates allow resources
to be declared in an arbitrary order, AWS CDK applications naturally require
variables to be declared before they can be referenced).

[cfnspec]: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-resource-specification.html
