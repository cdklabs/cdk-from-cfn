use thiserror::Error;

#[derive(Debug, Error)]
pub enum Error {
    #[error("{message}")]
    ImportInstructionError {
        message: String,
    },
    #[error("{message}")]
    ResourceTranslationError {
        message: String,
    },
    #[error("{message}")]
    SubParseError {
        message: String,
    },
    #[error("{message}")]
    ResourceInstructionError {
        message: String,
    },
    #[error("{message}")]
    ResourceTypeError {
        message: String,
    },
    #[error(transparent)]
    YamlParseError {
        #[from]
        err: serde_yaml::Error,
    },
}

#[cfg(test)]
mod tests;
