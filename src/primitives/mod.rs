/**
 * Primitives are for things that can be outside the scope of parsing and IR and used heavily across both
 * Generally, attempt to keep this section to a minimu
 *
 */
use std::fmt;

/// WrapperF64 exists because compraisons and outputs into typescripts are annoying with the
/// default f64. Use this whenever referring to a floating point number in CFN standard.
#[derive(Debug, Clone, Copy)]
pub struct WrapperF64 {
    num: f64,
}

impl WrapperF64 {
    pub fn new(num: f64) -> WrapperF64 {
        WrapperF64 { num }
    }
}

impl PartialEq for WrapperF64 {
    fn eq(&self, other: &Self) -> bool {
        // It's equal if the diff is very small
        (self.num - other.num).abs() < 0.0000001
    }
}

impl fmt::Display for WrapperF64 {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.num)
    }
}

impl Eq for WrapperF64 {}

impl From<f64> for WrapperF64 {
    fn from(num: f64) -> Self {
        WrapperF64::new(num)
    }
}

impl From<u64> for WrapperF64 {
    fn from(num: u64) -> Self {
        WrapperF64::new(num as f64)
    }
}

impl From<i128> for WrapperF64 {
    fn from(num: i128) -> Self {
        WrapperF64::new(num as f64)
    }
}

impl From<u128> for WrapperF64 {
    fn from(num: u128) -> Self {
        WrapperF64::new(num as f64)
    }
}
