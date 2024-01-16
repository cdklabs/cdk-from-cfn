End-to-end tests: Use a more advanced mechanism to compare CloudFormation templates

The end-to-end tests currently use `git diff` to compare input and output CloudFormation templates. This is not sophisticated enough, because files of two templates may look different, even when the CloudFormation templates are equivalent. 

A couple options to implement a more advance mechanism here:
1. Do JSON object comparison. We should also consider automatically resolving differences where the JSON is different, but the CloudFormation templates are equivalent.
2. Create a CloudFormation stack from the original template, then do a `cdk diff` with the new stack. This will have challenges with handling credentials if we want to do it in a pipeline or in GitHub actions.

