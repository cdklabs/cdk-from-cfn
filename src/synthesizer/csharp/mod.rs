use std::borrow::Cow;
use std::io;
use super::Synthesizer;
use crate::code::CodeBuffer;
use crate::ir::CloudformationProgramIr;

const INDENT: Cow<'static, str> = Cow::Borrowed("  ");
const STACK_NAME: Cow<'static, str> = Cow::Borrowed("NoctStack");

pub struct CSharp {
    package_name: String,
}

impl CSharp {
    pub fn new(package_name: impl Into<String>) -> Self {
        Self {
            package_name: package_name.into(),
        }
    }
}

impl Default for CSharp {
    fn default() -> Self {
        Self::new("com.acme.test.simple")
    }
}

impl Synthesizer for CSharp {
    fn synthesize(&self, ir: CloudformationProgramIr, into: &mut dyn io::Write) -> io::Result<()> {
        let code = CodeBuffer::default();
        code.line(if let Some(descr) = ir.description {
            descr
        } else {
            "".into()
        });
        code.write(into)
    }
}

#[cfg(test)]
mod tests {}
