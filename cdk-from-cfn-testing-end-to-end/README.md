# cdk-from-cfn-testing-end-to-end

End-to-end deployment testing for `cdk-from-cfn`. This crate provides AWS CloudFormation deployment validation to ensure that generated CDK code produces functionally equivalent infrastructure.

## Architecture Decision

This crate is intentionally kept separate from `cdk-from-cfn-testing` for several important reasons:

- **Dependency Size**: The AWS SDK dependencies (CloudFormation, S3, etc.) are substantial and would significantly increase build times and binary size for all users
- **Code Quality Assurance**: By keeping this as a separate crate, the code is always compiled and checked for errors/warnings, unlike feature-gated code within a single crate that gets ignored by the compiler when the feature is disabled
- **Dependency Isolation**: Heavy AWS SDK dependencies are only pulled in when explicitly needed for end-to-end testing
- **Optional Functionality**: End-to-end testing requires AWS credentials and is typically only run in CI/CD or by developers explicitly testing deployment equivalence
- **Build Performance**: Most development workflows (unit tests, code generation tests) don't need AWS integration and benefit from faster builds

## Testing Purpose

This crate validates deployment equivalence by:
1. **Deploying original CloudFormation templates** to AWS
2. **Creating change sets** from CDK-generated templates
3. **Verifying no differences** exist between original and generated infrastructure

## Key Components

### EndToEndTest
Main test orchestrator that manages the complete end-to-end testing workflow:
- Coordinates stack deployment and cleanup
- Manages test execution across multiple languages
- Handles AWS resource lifecycle

### EndToEndController
Core controller for AWS operations:
- **Stack Management**: Deploy, update, and delete CloudFormation stacks
- **Change Set Testing**: Create and analyze change sets for deployment equivalence
- **Dependency Handling**: Manage dependency stack deployment order

### AWS Integration
- **AwsClient**: AWS SDK client wrapper for CloudFormation and S3 operations
- **Stack Controllers**: Specialized controllers for different stack operations
  - `TestFixtureController`: Manages test stack lifecycle
  - `ChangeSetTestController`: Validates change sets for deployment differences
  - `BaseController`: Common AWS operations and error handling

## Workflow

1. **Setup**: Deploy original CloudFormation templates to AWS
2. **Generate**: Create CDK code from CloudFormation templates
3. **Synthesize**: Run `cdk synth` to produce new CloudFormation templates
4. **Validate**: Create change sets to compare original vs generated templates
5. **Verify**: Ensure no infrastructure changes would occur
6. **Cleanup**: Delete all test stacks and resources

## AWS Requirements

- **AWS Credentials**: Valid AWS credentials with CloudFormation permissions
- **Region Access**: Access to deploy resources in the specified AWS region
- **Permissions**: IAM permissions for:
  - CloudFormation stack operations (create, update, delete, describe)
  - Change set operations (create, describe, delete)
  - S3 operations (for large templates)
  - Resource-specific permissions for deployed infrastructure

## Cargo Features

- `default`: Enables all language features and end-to-end testing
- `end-to-end`: Enable end-to-end testing functionality (automatically enables `pre-install`)
- `skip-clean`: Preserve AWS resources for debugging
- Language features: `typescript`, `python`, `java`, `golang`, `csharp`

**Note**: The `pre-install` feature from `cdk-from-cfn-testing` is automatically enabled when using end-to-end testing to ensure language dependencies are cached for optimal performance.

## Usage

This crate is typically used through the main test suite:

```bash
# Run end-to-end tests for a specific test case
cargo test --test cdk-stack-synth simple --features end-to-end -- --nocapture

# Run all end-to-end tests
cargo test --features end-to-end -- --nocapture
```

## Error Handling

The crate provides detailed error reporting for:
- **AWS API Errors**: CloudFormation operation failures
- **Deployment Failures**: Stack creation/update issues
- **Change Set Differences**: Infrastructure drift detection
- **Timeout Issues**: Long-running operation handling

## Cost Considerations

End-to-end tests deploy real AWS resources, which may incur costs. The test suite:
- Uses minimal resource configurations where possible
- Implements automatic cleanup to minimize costs
- Supports the `skip-clean` feature for debugging (manual cleanup required)

This crate is not published to crates.io and is intended for internal use only.