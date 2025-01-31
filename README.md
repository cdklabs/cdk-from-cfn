# cdk-from-cfn

`cdk-from-cfn` is a command-line tool that converts AWS CloudFormation templates into AWS CDK code. It supports multiple programming languages including TypeScript, Python, Java, Go, and C#.

## Installation

```console
$ cargo install cdk-from-cfn
```

## Usage

```console
$ cdk-from-cfn [INPUT] [OUTPUT] --language <LANGUAGE> --stack-name <STACK_NAME>
```

- `INPUT` is the input file path (STDIN by default).
- `OUTPUT` is the output file path; if not specified, output will be printed on your command line (STDOUT by default).

## Node.js Module Usage

cdk-from-cfn leverages WebAssembly (WASM) bindings to provide a cross-platform [npm](https://www.npmjs.com/package/cdk-from-cfn) module, which exposes apis to be used in Node.js projects. Simply take a dependency on `cdk-from-cfn` in your package.json and utilize it as you would a normal module. i.e.

```typescript
import * as cdk_from_cfn from 'cdk-from-cfn';

// get supported languages
cdk_from_cfn.supported_languages();

// transmute cfn template into cdk app
cdk_from_cfn.transmute(template, language, stackName)
```

## Language and Feature support

Name         | Enabled by default | Description
-------------|:------------------:|---------------------------------------------
`typescript` | :heavy_check_mark: | Enables support for TypeScript output
`golang`     | :heavy_check_mark: | Enables support for Go output
`java`       | :heavy_check_mark: | Enables support for Java output
`Python`     | :heavy_check_mark: | Enables support for Python output
`csharp`     | :heavy_check_mark: | Enables support for C# output

You can enable experimental languages (not enabled by default) by enabling the relevant feature:

```console
$ cargo build --release --features=<feature-name>
Finished release [optimized] target(s) in 0.17s
```

If you want to disable on-by-default languages, you can pass `--no-default-features`:

```console
$ cargo build --release --no-default-features --features=golang
Finished release [optimized] target(s) in 0.17s
```

### Implemented

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
- [x] Fn::GetAZs support
- [x] Adding depends-on, and ordering based on it too.
- [x] Deletion policy
- [x] Fn::Cidr support

### Remaining

There are known unsupported features. Working on them in priority order:

- [ ] Create policy
- [ ] ssm metadata references
- [ ] secretsmanager references
