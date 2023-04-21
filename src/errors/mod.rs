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

impl fmt::Display for TransmuteError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "TransmuteError: {}", self.details)
    }
}

impl Error for TransmuteError {}
