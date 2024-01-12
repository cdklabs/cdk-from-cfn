This directory contains a directory for each language supported by cdk-from-cfn. 

Each language-specific directory contains the minimum necessary boilerplate
files for running a CDK application in that language. During runtime execution
of the end-to-end tests, all files in a language's directory here are copied to
the temporary working directory for each test case.

See the main end-to-end test [README](../README.md) for more information.