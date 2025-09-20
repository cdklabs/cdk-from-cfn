// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use std::{error::Error, fmt};

use aws_sdk_cloudformation::error::DisplayErrorContext as CfnDisplayErrorContext;
pub use aws_sdk_cloudformation::error::SdkError as CfnSdkError;
use aws_sdk_s3::error::DisplayErrorContext as S3DisplayErrorContext;
pub use aws_sdk_s3::error::SdkError as S3SdkError;
use aws_smithy_runtime_api::client::{
    result::CreateUnhandledError,
    waiters::{error::WaiterError, FinalPoll},
};
use aws_smithy_types::error::metadata::ProvideErrorMetadata;

/// Extracts meaningful error information from CloudFormation SDK errors.
/// 
/// Converts AWS SDK errors into human-readable strings by extracting error codes
/// and messages from the error metadata. Falls back to full error display if
/// metadata is not available.
/// 
/// # Arguments
/// * `result` - Result from a CloudFormation SDK operation
/// 
/// # Returns
/// Result with extracted error message as String on failure
/// 
/// # Type Parameters
/// * `T` - Success type of the original result
/// * `E` - Error type that provides metadata and can be displayed
pub fn extract_error_metadata<T, E>(result: Result<T, CfnSdkError<E>>) -> Result<T, String>
where
    E: Error + Send + Sync + CreateUnhandledError + ProvideErrorMetadata + 'static,
{
    result.map_err(|e| {
        // Capture the full error display before consuming it
        let full_error = CfnDisplayErrorContext(&e).to_string();
        
        match e.into_service_error() {
            service_error => {
                let meta = service_error.meta();
                let code = meta.code().unwrap_or("Unknown");
                let message = meta.message().unwrap_or("No message");
                
                // If we don't have useful metadata, use the full error
                if code == "Unknown" && message == "No message" {
                    full_error
                } else {
                    format!("{}: {}", code, message)
                }
            }
        }
    })
}

/// Extracts meaningful error information from S3 SDK errors.
/// 
/// Converts AWS S3 SDK errors into human-readable strings by extracting error codes
/// and messages from the error metadata. Falls back to full error display if
/// metadata is not available.
/// 
/// # Arguments
/// * `result` - Result from an S3 SDK operation
/// 
/// # Returns
/// Result with extracted error message as String on failure
/// 
/// # Type Parameters
/// * `T` - Success type of the original result
/// * `E` - Error type that provides metadata and can be displayed
pub fn extract_s3_error_metadata<T, E>(result: Result<T, S3SdkError<E>>) -> Result<T, String>
where
    E: Error + Send + Sync + CreateUnhandledError + ProvideErrorMetadata + 'static,
{
    result.map_err(|e| {
        // Capture the full error display before consuming it
        let full_error = S3DisplayErrorContext(&e).to_string();
        
        match e.into_service_error() {
            service_error => {
                let meta = service_error.meta();
                let code = meta.code().unwrap_or("Unknown");
                let message = meta.message().unwrap_or("No message");
                
                // If we don't have useful metadata, use the full error
                if code == "Unknown" && message == "No message" {
                    full_error
                } else {
                    format!("{}: {}", code, message)
                }
            }
        }
    })
}

/// Extracts results from AWS SDK waiter operations with detailed error handling.
/// 
/// Processes waiter results and converts various failure modes into descriptive
/// error messages. Handles timeout scenarios, failure states, operation failures,
/// and construction errors with appropriate context.
/// 
/// # Arguments
/// * `result` - Result from an AWS SDK waiter operation
/// 
/// # Returns
/// Result with the final output or descriptive error message
/// 
/// # Type Parameters
/// * `T` - Success type that must be cloneable and debuggable
/// * `E` - Error type that provides metadata and can be displayed
pub fn extract_waiter_result<T: Clone + fmt::Debug, E>(
    result: Result<FinalPoll<T, CfnSdkError<E>>, WaiterError<T, E>>,
) -> Result<T, String>
where
    E: Error + Send + Sync + CreateUnhandledError + ProvideErrorMetadata + 'static,
{
    match result {
        Ok(final_poll) => match final_poll.into_result() {
            Ok(output) => Ok(output),
            Err(e) => {
                // For dispatch failures and other SDK errors, show the full error
                Err(format!("{:?}", e))
            }
        },
        Err(waiter_error) => match waiter_error {
            WaiterError::ExceededMaxWait(poll) => {
                Err(format!("ExceededMaxWait: Waiter exceeded maximum wait time. Time Elapsed: [{:?}] Max Wait Time: [{:?}] Poll Count: [{}]", poll.elapsed(), poll.max_wait(), poll.poll_count()))
            }
            WaiterError::FailureState(state) => {
                match state.into_final_poll().into_result() {
                    Ok(output) => Ok(output),
                    Err(e) => {
                        let code = e.code().unwrap_or("Unknown");
                        let message = e.message().unwrap_or("No message");
                        
                        if code == "Unknown" && message == "No message" {
                            Err(format!("{:?}", e))
                        } else {
                            Err(format!("{}: {}", code, message))
                        }
                    }
                }
            }
            WaiterError::OperationFailed(operation) => {
                let error = operation.into_error();
                // For dispatch failures, show the full error with debug formatting
                Err(format!("{:?}", error))
            }
            WaiterError::ConstructionFailure(error) => Err(format!("ConstructionFailure: Waiter construction failure: {:?}", error)),
            _ => Err("Unknown: Some unexpected error occurred while waiting for a result".to_string()),
        },
    }
}
