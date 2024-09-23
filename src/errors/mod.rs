// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use thiserror::Error;

#[derive(Debug, Error)]
pub enum Error {
    #[error("{message}")]
    ImportInstructionError { message: String },
    #[error("{message}")]
    ResourceTranslationError { message: String },
    #[error("{message}")]
    SubParseError { message: String },
    #[error("{message}")]
    ResourceInstructionError { message: String },
    #[error("{message}")]
    ResourceTypeError { message: String },
    #[error(transparent)]
    YamlParseError {
        #[from]
        err: serde_yaml::Error,
    },
    #[error("{language} is not a supported language")]
    UnsupportedLanguageError { language: String },
    #[error(transparent)]
    IOError {
        #[from]
        err: std::io::Error,
    },
    #[error("{message}")]
    TypeReferenceError { message: String },
    #[error("{message}")]
    PrimitiveError { message: String },
}

#[cfg(test)]
mod tests;
