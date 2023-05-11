use std::error::Error;
use std::fmt;

#[derive(Debug)]
pub struct TransmuteError {
    details: String,
}

impl TransmuteError {
    #[inline(always)]
    pub(crate) fn new(msg: impl ToString) -> TransmuteError {
        TransmuteError {
            details: msg.to_string(),
        }
    }
}

impl From<serde_yaml::Error> for TransmuteError {
    #[inline]
    fn from(val: serde_yaml::Error) -> Self {
        TransmuteError::new(val)
    }
}

impl fmt::Display for TransmuteError {
    #[inline]
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "TransmuteError: {}", self.details)
    }
}

impl Error for TransmuteError {}

#[cfg(test)]
mod tests {
    use serde::de::Error;

    use super::*;

    #[test]
    fn test_transmute_error() {
        let error = TransmuteError::new("Test error message");

        assert_eq!(error.details, "Test error message");
        assert_eq!(error.to_string(), "TransmuteError: Test error message");
    }

    #[test]
    fn test_transmute_error_from() {
        let yaml_error = serde_yaml::Error::custom("YAML parsing error");
        let transmute_error: TransmuteError = yaml_error.into();

        assert_eq!(transmute_error.details, "YAML parsing error");
    }
}
