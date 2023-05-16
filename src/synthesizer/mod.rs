use std::io;

use crate::ir::CloudformationProgramIr;

pub mod golang;
mod output;
pub mod typescript;

pub trait Synthesizer {
    fn synthesize(&self, ir: CloudformationProgramIr, into: &mut dyn io::Write) -> io::Result<()>;
}

impl CloudformationProgramIr {
    #[inline(always)]
    pub fn synthesize(self, using: &dyn Synthesizer, into: &mut impl io::Write) -> io::Result<()> {
        using.synthesize(self, into)
    }
}
