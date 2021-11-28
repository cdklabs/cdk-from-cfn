# noctilucent
In a world where people want to use the full extent of the cdk, there **was** no product that would transform all your 
json into beautiful typescript...until now. 

Noctilucent will take your json and output the equivalent typescript.

## Progress on Intrinsic Functions

There are known unsupported features that require some thinking
about. These are those features:
- [x] Fn::FindInMap
- [x] Fn::Join
- [x] Fn::Sub
- [x] Ref
- [x] Fn::And
- [x] Fn::Equals
- [x] Fn::If
- [x] Fn::Not
- [x] Fn::Or
- [x] Fn::GetAtt
- [x] Fn::Base64 support
- [x] Fn::ImportValue support
- [x] Fn::Select support
- [ ] Fn::Cidr support
- [ ] Fn::GetAZs support
- [ ] Fn::Transform (do we even want it?)

## Remaining implementation fixes

- [x] Resource ordering based on dependencies
- [ ] Conditions are emitted in ts but not attached to resource conditions
- [ ] Emission of outputs / exports
- [ ] Adding depends-on, and ordering based on it too.
- [ ] Metadata emission for updates to asgs / lambda functions.
- [ ] ssm metadata references
- [ ] secretsmanager references
- [ ] Rules (is this a thing in CDK?)
- [ ] Metadata section
