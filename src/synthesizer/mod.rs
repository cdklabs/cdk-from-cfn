use std::io;

use crate::ir::CloudformationProgramIr;

pub mod typescript_synthesizer;

pub trait Synthesizer {
    fn synthesize(&self, ir: CloudformationProgramIr, into: &mut dyn io::Write) -> io::Result<()>;
}

impl CloudformationProgramIr {
    #[inline(always)]
    pub fn synthesize(self, using: &dyn Synthesizer, into: &mut dyn io::Write) -> io::Result<()> {
        using.synthesize(self, into)
    }
}
