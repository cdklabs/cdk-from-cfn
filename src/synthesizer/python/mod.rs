use crate::code::{CodeBuffer, IndentOptions};
use crate::ir::conditions::ConditionIr;
use crate::ir::mappings::{MappingInstruction, OutputType};
use crate::ir::outputs::OutputInstruction;
use crate::ir::reference::{Origin, PseudoParameter, Reference};
use crate::ir::resources::{ResourceInstruction, ResourceIr};
use crate::ir::CloudformationProgramIr;
use crate::parser::lookup_table::MappingInnerValue;
use indexmap::IndexMap;
use std::borrow::Cow;
use std::collections::HashMap;
use std::io;
use std::rc::Rc;
use voca_rs::case::{camel_case, pascal_case};

use super::Synthesizer;

const INDENT: Cow<'static, str> = Cow::Borrowed("  ");

pub struct Python {
    // TODO: Put options in here for different outputs in typescript
}

impl Python {
    #[cfg_attr(coverage_nightly, no_coverage)]
    #[deprecated(note = "Prefer using the Synthesizer API instead")]
    pub fn output(ir: CloudformationProgramIr) -> String {
        let mut output = Vec::new();
        Python {}.synthesize(ir, &mut output).unwrap();
        String::from_utf8(output).unwrap()
    }
}

impl Synthesizer for Python {
    fn synthesize(
        &self,
        ir: CloudformationProgramIr,
        output: &mut dyn io::Write,
    ) -> io::Result<()> {
        let code = CodeBuffer::default();

        // no judgement allowed lol, still trying to understand the synthesizer
        let imports = code.section(true);
        for import in &ir.imports {
            imports.line(format!("# TODO: {import:?}"));
        }

        code.write(output)
    }
}
