# CDK Stack Synthesis Tests

This directory contains the CDK stack synthesis tests for `cdk-from-cfn`. These tests validate the complete workflow from CloudFormation template to working CDK application.

For an overview of all testing types in this project, see the [Testing Overview](../cdk-from-cfn-testing/README.md).

- [CDK Stack Synthesis Tests](#cdk-stack-synthesis-tests)
  - [Usage](#usage)
    - [Command examples](#command-examples)
    - [Environment Variables](#environment-variables)
  - [Glossary](#glossary)
  - [What do the CDK Stack Synthesis tests do?](#what-do-the-cdk-stack-synthesis-tests-do)

  - [How to add a new test](#how-to-add-a-new-test)
  - [How to update a test](#how-to-update-a-test)
  - [Layout of this directory](#layout-of-this-directory)
  - [Workflow Design: What happens when you run the tests?](#workflow-design-what-happens-when-you-run-the-tests)
  - [Some detail about the snapshots](#some-detail-about-the-snapshots)

## Usage
To run the CDK stack synthesis tests, use these commands. **Note: Using `-- --nocapture` is recommended to see test progress and output in real-time.** For full details about how to
write new tests, update tests, and how the test workflow works, read the rest of
this document.

### Command examples
```sh
# run all CDK stack synthesis tests
cargo test --test cdk-stack-synth

# run one test case in all languages
cargo test --test cdk-stack-synth simple

# run one test case in one language
cargo test --test cdk-stack-synth simple::typescript

# run one test case in one language, and monitor its output (recommended)
cargo test --test cdk-stack-synth simple::typescript -- --nocapture

# skip specific tests by name pattern
cargo test --test cdk-stack-synth -- --skip simple
cargo test --test cdk-stack-synth -- --skip simple --skip batch

# run only typescript tests across all test cases
cargo test --test cdk-stack-synth typescript

# control test parallelism
cargo test --test cdk-stack-synth -- --test-threads=4
cargo test --test cdk-stack-synth -- --test-threads=1  # single-threaded

# preserve working directories for debugging (don't clean up after tests)
cargo test --test cdk-stack-synth --features skip-clean

# update test snapshots when tests pass (overwrites expected outputs)
cargo test --test cdk-stack-synth --features update-snapshots
```

### Features

| Feature | Description |
| ------- | ----------- |
| `update-snapshots` | Update all snapshot files and acceptable diff file. Overwrites expected outputs with actual test results. |
| `skip-clean` | Preserve working directories after test execution for debugging. Prevents cleanup of working directories. |
| `end-to-end` | Enable end-to-end testing with actual CloudFormation stack creation and deployment validation. |
| `pre-install` | Enable pre-installation of dependencies and shared resources for faster test execution. This is enabled by default but can be disabled if you do not have access to internet and are only running the ir synthesizer tests |

**Configured Skips:**
Some tests skip CDK synthesis in certain languages due to known issues. These are managed through the `SkipSynthList` in `cdk-from-cfn-testing/src/synth/skip.rs`:
```rust
// Example: simple test skips golang due to compilation issues
skip!(Language::GOLANG, Self::I626_GO_COMPILATION)
```
When tests are skipped, you'll see helpful output like:
```
⏭️  Skipping CDK synth for simple::golang: Go is an approximation at best. It does not compile (#626)
```
The issue numbers are clickable links to the GitHub repository for easy tracking.

**Debugging Failed Tests:**
To debug test failures, you can preserve the working directories where `cdk synth` was executed:
```bash
cargo test --test cdk-stack-synth --features skip-clean
```
This prevents cleanup of working directories, allowing you to inspect the generated CDK app files, examine `cdk synth` output, and debug issues manually.

**Updating Test Snapshots:**
When you make changes that affect test outputs, update the expected snapshots:
```bash
cargo test --test cdk-stack-synth --features update-snapshots
```
This overwrites the expected output files with the actual test results when tests pass, effectively updating the "golden" snapshots.

## Glossary

A few key terms that can be easily confused.

- **[CloudFormation
  template](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-whatis-concepts.html#cfn-concepts-templates)
  or CFN template**: refers to a file in JSON or YAML that defines a
  CloudFormation stack. Also, one of the outputs of `cdk synth`.
- **[CloudFormation
  stack](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-whatis-concepts.html#cfn-concepts-stacks)
  or CFN stack**: refers to a collection of live AWS resources that can be
  managed together using CloudFormation. Think of it as an "instance" of a CFN
  template.
- **[CDK
  stack](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Stack.html)**:
  A Stack Construct defined in code in a high-level programming language. When
  an instance of this construct is synthesized in a CDK app, it produces a
  CloudFormation template (among other things).
- **cdk-from-cfn**: This tool which takes CFN templates as input, and produces
  CDK stacks.
- **cdk-from-cfn synthesize**: The step in the workflow of `cdk-from-cfn` that
  code generates a CDK stack in a target programming language (ex. typescript).
- **cdk synth**: A CDK CLI command that synthesizes a CDK application,
  generating a cloud assembly including CFN templates.

To put all of these terms into one sentence: **cdk-from-cfn** **synthesizes**
**CDK stacks** you can run **cdk synth** on to produce **CFN templates** which
define **CFN stacks**. 

*Note: These definitions are sufficient for this documentation, but are not
all-encompassing.*

## Workflow Design: What happens when you run the tests?

The CDK stack synthesis tests follow this workflow for each test case and language combination:

1. **Execute cdk-from-cfn** - Run the built binary to generate CDK stack code from the CloudFormation template
2. **Compare generated code** - Check if the generated CDK stack matches the expected output in `cdk-from-cfn-testing/expected/` in the zip file created at build time
3. **Create working directory** - Set up a temporary directory in `cdk-from-cfn-testing/actual/` with the generated CDK code
4 **Generate app file** - Generate a generic app file for each test case in the working directory
4. **Copy boilerplate files** - Add language-specific build files (package.json, pom.xml, etc.) from the testing infrastructure
5. **Run cdk synth** - Execute CDK CLI to synthesize CloudFormation templates from the generated CDK code
6. **Compare templates** - Check if the synthesized template matches the original or acceptable differences in `Stack.diff`
7. **With end-to-end feature** - Deploy original template and create change sets to validate deployment equivalence

**Key behaviors:**
- Tests run in parallel for different test cases but serially for different languages of the same test case
- With `update-snapshots` feature: Updates expected outputs when tests pass
- With `skip-clean` feature: Preserves working directories for debugging
- Configured skips: Some language/test combinations are skipped due to known issues tracked in GitHub

**Test outcomes:**
- ✅ **Pass**: Generated code matches expected output and templates are equivalent
- ❌ **Fail**: Code generation differs, CDK synthesis fails, or templates have unacceptable differences

## How to add a new test

1. Create a folder under `cdk-from-cfn-testing/cases/`. The name of this folder will be
   the name of the new test. Example: `cdk-from-cfn-testing/cases/mytest/template.json`.

   *The name of the folder must be a valid Rust identifier.*
2. Save the CloudFormation template that will be the input for the test to a
   file at `cdk-from-cfn-testing/cases/mytest/template.json`. This template must be in
   JSON, not YAML format, because `cdk synth` creates CloudFormation templates
   in JSON. It's easier to compare these if they are in the same format.
3. If the template you want to test relies on referencing resources that must
   already exist, also add a template that creates those dependency resources at
   `cdk-from-cfn-testing/cases/mytest/dependency_stack_template.json`. If this file is present, the
   tests will create a CloudFormation stack with this template, before
   attempting to create a CloudFormation stack with the template called
   `template.json`.
4. Add your test case to the `TEST_DEFINITIONS` array in `cdk-from-cfn-macros/src/lib.rs`.

    The file contains a constant array that defines all test cases:
    ```rust
    const TEST_DEFINITIONS: &[(&str, &str)] = &[
        (BATCH, "BatchStack"),
        (BUCKET, "BucketStack"),
        (SIMPLE, "SimpleStack"),
        (VPC, "VpcStack"),
        // Add your new test case here
        (MYTEST, "MyStack"),
    ];
    ```

    Each entry is a tuple of `(test_name_constant, stack_name)` where:
    - `test_name_constant` references a string constant (e.g., `MYTEST: &str = "mytest"`)
    - `stack_name` is the CloudFormation stack name used for stack creation and synthesis testing
    - The test name must match your test case folder name and be a valid Rust identifier
5. Create snapshots for your test case: Use the `update-snapshots` feature to create a stack file in `cdk-from-cfn-testing/expected/mytest/lang` and to 
    potentially generate a `Stack.diff` file in `cdk-from-cfn-testing/cases/mytest`.

  
      All subsequent validations during this single test run will use the new stack file in `cdk-from-cfn-testing/expected/mytest/lang` rather than in the zip file created at build time. 
    
      Only use this when creating a new test or when creating a fix that updates the output in the stack files or you will receive false positive tests. 
    
        Note, this same flag can also be used when running `synthesizer` tests but `cdk synth` is not run*
        against the newly generated files in those tests so no `Stack.diff` file will be generated. 
        Subsequent test runs using `cargo test` or `cargo test --test cdk-stack-synth` may fail.

      Once the stack files are generated, in both `cdk-from-cfn-testing/expected/mytest/lang` and `cdk-from-cfn-testing/actual/cdk_stack_synth::mytest::lang` (formatted as such to match the testing output), an app file will be written to `cdk-from-cfn-testing/actual/cdk_stack_synth::mytest::lang` and then other boilerplate files will be copied from the testing infrastructure into that same folder.

      `cdk synth` is run on the generated app and a comparison is run between the original template and the resulting template in `cdk.out`

        Because there are multiple ways to express the same thing in CloudFormation stacks, the result of `cdk synth` may not be precisely the same as the original `template.json` file. The `Stack.diff` file accounts for that list of differences. Deployment equivalence is tested further on in the testing workflow.

      If any steps above fail, the template may be invalid or there may be a bug in the code for one or more target languages. If there is a bug, you may add an entry to `SkipSynthList` in `cdk-from-cfn-testing/src/synth/skip.rs`. Each entry requires an issue constant with a GitHub issue number.

6. Test deployment with the `end-to-end` feature

    ```bash
    cargo test --test cdk-stack-synth mytest --features end-to-end -- --nocapture
    ```

    This will use the Rust AWS SDK to create a CloudFormation stack from the
    test's input CloudFormation template. Your shell must have AWS
    credentials available to create the CloudFormation stack for your test.        

        The `--nocapture` flag here allows you to monitor the progress of your test as it is running. It tells `cargo` to not capture the output of the test, and print it to stdout right away. Normal `cargo test` behavior is to only print stdout of a test if it fails. Some of these tests are long running and may appear to be unresponsive if `--nocapture` isn't used.

    You will see a message indicating that the initial creation of the CloudFormation stack was successful. If deployment fails, update fix the issues with the template and iterate on your template until deployment is successful.

    Once the template is successfully deployed, for each target language that is not on the `SkipSynthList`, a change set will be created. If there are no changes, that test returns a success, if there are changes, it will fail with an error message describing those changes. This indicates that there is a bug in the code for that target language.

## How to update a test

In these steps, assume you are updating a test called "simple".

1. After making changes to any of the following, you may need to update the end
   to end tests.
    - Source code in `cdk-from-cfn/src`
    - A test's CloudFormation templates: `template.json` or `dependency_stack_template.json`
    - A test's CDK app writers or boilerplate files in the testing infrastructure
2. First, run the tests without any features to mimic CI/CD after your changes.
    ```sh
    cargo test --test cdk-stack-synth
    ```
    If you changed a test, something should fail here. If you made source code
    changes, and we have good test coverage, some test should probably fail as
    well. If it doesn't, add a new test!
3. If the input CloudFormation templates changed, make sure they are valid.
4. Run your test with the `update-snapshots` feature.
    ```sh
    cargo test --test cdk-stack-synth simple --features update-snapshots
    ```
5. If needed, iterate on failing tests until they succeed.

    For example:
    ```sh
    cargo test --test cdk-stack-synth simple::java -- --nocapture
    ```

6. Finally, review the files that have changed using git. Files that may change:
    - `cdk-from-cfn-testing/expected/simple/typescript/SimpleStack.ts`
        - Changes to this file indicate that `cdk-from-cfn` is now producing
          different CDK code than before. Is this expected? Did code generation
          logic change? Or, did the input `template.json` change?
    - `cdk-from-cfn-testing/cases/simple/Stack.diff`
        - Changes to this file mean that the difference between the original CFN
          template, and the CFN template generated by a CDK stack generated by
          cdk-from-cfn has changed. Run the test using the `end-to-end` feature
          to ensure the deployed resources and properties are still the same.
    - ... etc for all languages.

## Layout of this directory

Below is a subset of the files in this test suite, to demonstrate how the test cases are
organized for the CDK stack synthesis tests. 

```
cdk-from-cfn
├── tests/
│   ├── cdk-stack-synth.rs
│   └── README.md
└── cdk-from-cfn-testing/
    ├── cases/
    │   ├── simple/
    │   │   ├── template.json
    │   │   ├── dependency_stack_template.json
    │   │   └── Stack.diff
    │   └── vpc/
    │       └── template.json
    ├── expected/
    │   ├── simple/
    │   │   ├── csharp/
    │   │   │   └── SimpleStack.cs
    │   │   ├── golang/
    │   │   │   └── SimpleStack.go
    │   │   ├── java/
    │   │   │   └── SimpleStack.java
    │   │   ├── python/
    │   │   │   └── SimpleStack.py
    │   │   └── typescript/
    │   │       └── SimpleStack.ts
    │   └── vpc/
    ├── actual/
    │   ├── cdk_stack_synth::simple::typescript/
    │   │   ├── cdk.out/
    │   │   │   └── cdk-from-cfn-e2e-test-SimpleStack.template.json
    │   │   ├── app.ts
    │   │   ├── SimpleStack.ts
    │   │   ├── package.json
    │   │   └── tsconfig.json
    │   └── synthesizer::simple::typescript/
    │       └── SimpleStack.ts
    └── boilerplate/
        ├── typescript/
        │   ├── package.json
        │   └── tsconfig.json
        ├── python/
        │   └── requirements.txt
        ├── java/
        │   └── pom.xml
        ├── golang/
        │   └── go.mod
        └── csharp/
            └── CSharp.csproj
```

The `cdk-from-cfn/tests/cdk-stack-synth.rs` Rust module contains the source code for
the CDK stack synthesis tests.

The testing infrastructure contains boilerplate files for each language, which
are necessary to run a CDK app in that language. These include build files like
`package.json`, `pom.xml`, etc., and setup scripts that run language-specific
commands like `npm install` before executing `cdk synth`. These files are
copied into each test's working directory during test execution.

The `cdk-from-cfn-testing/cases/simple/` folder contains one test case. Each test case has its own folder
in `cdk-from-cfn-testing/cases/`. It has the input CloudFormation template, `template.json`, optionally a
CloudFormation template defining resources that the main one depends on,
`dependency_stack_template.json`, and optionally a `Stack.diff` files that records acceptable
differences between the input template and the generated template.

The `cdk-from-cfn-testing/expected/simple/` folder contains the expected output for each language.
The stack definition files (`SimpleStack.ts, SimpleStack.java`, etc.) are generated by `cdk-from-cfn`. 

Upon each test run, the `cdk-from-cfn-testing/actual/` is generated with a folder containing each test case. 
The naming of the folder matches the output shown when `cargo test` is run, for example:

    synthesizer::simple::python
    cdk_stack_synth::simple::typescript

`cdk-from-cfn-testing/cases/`, `cdk-from-cfn-testing/expected`, and `cdk-from-cfn-testing/actual` are shared by both synthesizer tests suites because
the test cases should be the same for each.


## Some detail about the snapshots

The snapshot files are zipped during build time to an archive at `$OUT_DIR/test/end-to-end-test-snapshots.zip`. This zip file is git-ignored. The snapshots zip is included in the end-to-end tests as part of the binary. This is to optimize runtime performance of the test, by avoiding loading and reading all of these files during runtime. As a developer working with this repo, you shouldn't have to do anything different because of this. The zip file is automatically regenerated whenever any relevant files change.
