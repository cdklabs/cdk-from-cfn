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
}

#[cfg(test)]
mod tests;
