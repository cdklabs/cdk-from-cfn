use std::io;

use crate::ir::CloudformationProgramIr;

#[cfg(feature = "golang")]
mod golang;
#[cfg(feature = "golang")]
#[doc(inline)]
pub use golang::*;

#[cfg(feature = "java")]
mod java;
#[cfg(feature = "java")]
#[doc(inline)]
pub use java::*;

#[cfg(feature = "typescript")]
mod typescript;
#[cfg(feature = "typescript")]
#[doc(inline)]
pub use typescript::*;

pub trait Synthesizer {
    fn synthesize(&self, ir: CloudformationProgramIr, into: &mut dyn io::Write, stack_name: &str) -> io::Result<()>;
}

impl CloudformationProgramIr {
    #[inline(always)]
    pub fn synthesize(self, using: &dyn Synthesizer, into: &mut impl io::Write, stack_name: &str) -> io::Result<()> {
        using.synthesize(self, into, stack_name)
    }
}
