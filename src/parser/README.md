# `cdk_from_cfn::parser`

This module is responsible for parsing AWS CloudFormation YAML (and JSON)
templates to a very immediate rust representation of it. The parsing logic is
implemented using the [`serde` crate][serde] (a part of it is derived, while
some special cases are hand-coded, typically to accommodate for specific
CloudFormation syntax allowances). Naturally, the
[`serde_yaml` crate][serde_yaml] produces the YAML/JSON specific parser
front-end.

The [Template anatomy][cfn-template-anatomy] page in the CloudFormation user
guide describes the elements and schema of the various components of a
CloudFormation template document. It is worth noting however that CloudFormation
is relatively lenient in how it parses and validates templates:

- it is often legal to pass a single, scalar value in a place where an array is
  expected, and CloudFormation usually interprets this as synonymous to a single
  valued array containing that value;
- CloudFormation is able to transparently convert data between types as is
  necessary, as long as the conversion is straight-forward (e.g: the string
  `'1337'` can trivially be converted to the integer `1337`, and vice-versa);

This leniency explains most of the complexity and hand-written parts of the
parser module, which is otherwise a straight-forward translation of the schema
described by the [Template anatomy][cfn-template-anatomy] documentation.

[serde]: https://docs.rs/serde/latest/serde/
[serde_yaml]: https://docs.rs/serde_yaml/latest/serde_yaml/
[cfn-template-anatomy]: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html
