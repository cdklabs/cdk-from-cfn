use std::io;

use crate::{ir::CloudformationProgramIr, Error};

#[cfg(feature = "csharp")]
mod csharp;
#[cfg(feature = "csharp")]
#[doc(inline)]
pub use csharp::*;

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

#[cfg(feature = "python")]
mod python;
#[cfg(feature = "python")]
#[doc(inline)]
pub use python::*;

pub trait Synthesizer {
    fn synthesize(
        &self,
        ir: CloudformationProgramIr,
        into: &mut dyn io::Write,
        stack_name: &str,
    ) -> Result<(), Error>;
}

impl CloudformationProgramIr {
    #[inline(always)]
    pub fn synthesize(
        self,
        using: &dyn Synthesizer,
        into: &mut impl io::Write,
        stack_name: &str,
    ) -> Result<(), Error> {
        using.synthesize(self, into, stack_name)
    }
}
