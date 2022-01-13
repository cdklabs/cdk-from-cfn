# noctilucent
In a world where people want to use the full extent of the cdk, there **was** no product that would transform all your 
json into beautiful typescript...until now. 

Noctilucent will take your json and output the equivalent typescript.

## Implemented

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
- [x] Resource ordering based on dependencies
- [x] Conditions are emitted in ts but not attached to resource conditions
- [x] Metadata emission for updates to asgs / lambda functions.
- [x] Emission of outputs / exports

## Remaining

There are known unsupported features. Working on them in priority order:

- [ ] Fn::GetAZs support
- [ ] Adding depends-on, and ordering based on it too.
- [ ] Fn::Cidr support
- [ ] ssm metadata references
- [ ] secretsmanager references
