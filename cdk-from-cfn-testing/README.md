# cdk-from-cfn-testing

Testing infrastructure for `cdk-from-cfn`. This crate provides the core testing framework for validating CloudFormation to CDK code generation and synthesis.

## Directory Structure

- `cases/` - Test case definitions with CloudFormation templates
- `expected/` - Expected CDK stack outputs for each language
- `actual/` - Generated test outputs (created during test runs)
- `boilerplate/` - Language-specific build files and configurations
- `src/` - Testing infrastructure source code

## Test Types

### Synthesizer Tests
Validate that `cdk-from-cfn` generates the expected CDK stack code:
- Compare generated stack files against expected outputs
- Support for TypeScript, Python, Java, Go, and C#

### CDK Stack Synthesis Tests
End-to-end validation that generated CDK code can be synthesized:
- Generate CDK stack code from CloudFormation templates
- Create working directories with boilerplate files
- Run `cdk synth` to produce CloudFormation templates
- Compare synthesized templates with original inputs

## Key Components

### Core Testing
- **StackTestCase**: Main test case runner for comparing generated vs expected stack outputs
- **StackDiff**: Compares and reports differences between stack files
- **CdkAppTestCase**: Individual CDK application test execution
- **CdkAppTestGroup**: Manages groups of CDK app tests across languages

### Configuration & Organization
- **Scope**: Organizes tests by module, test name, and language
- **Language**: Language-specific processing and validation
- **Stack**: Stack configuration and metadata
- **EndToEndTestStack**: Configuration for deployment testing

### File System Operations
- **Files**: Test artifact I/O operations and cleanup
- **Paths**: Test directory and file path resolution
- **Zip**: Snapshot archive extraction and management

### Validation & Comparison
- **Templates**: CloudFormation template loading and validation
- **JSON**: JSON parsing and validation utilities
- **Template Diff**: Template comparison utilities

### Test Execution
- **Bootstrap**: App file generation and dependency installation
- **TestFilter**: Test filtering and skip list management
- **SkipSynthList**: Manages tests to skip for known issues

### Build Integration
- **Snapshot Management**: Automated zipping of test cases and expected outputs
- **Dependency Pre-installation**: Language-specific dependency caching
- **Shared Installations**: Optimized dependency sharing across tests

## Cargo Features

- `update-snapshots`: Update expected test outputs when tests pass
- `skip-clean`: Preserve test working directories for debugging
- `end-to-end`: Enable deployment testing with AWS CloudFormation
- `pre-install`: Pre-install language dependencies during build
- Language features: `typescript`, `python`, `java`, `golang`, `csharp`

## Build Process

During build, this crate:
1. Creates a zip archive of test snapshots at `$OUT_DIR/test/end-to-end-test-snapshots.zip`
2. Optionally pre-installs language dependencies (Go modules, Python venv, Maven deps, etc.)
3. Sets up shared installation directories for optimized test performance

This crate is not published to crates.io and is intended for internal use only.