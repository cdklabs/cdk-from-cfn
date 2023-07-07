use crate::code::{CodeBuffer, IndentOptions};
use crate::ir::conditions::ConditionIr;
use crate::ir::importer::ImportInstruction;
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

        let imports = code.section(true);
        for import in &ir.imports {
            imports.line(import.to_python());
        }
        
        code.write(output)
    }
}

impl ImportInstruction {
    fn to_python(&self) -> String {
        let mut parts: Vec<String> = vec![match self.path[0].as_str() {
            "aws-cdk-lib" => "aws_cdk".to_string(),
            other => other.to_string(),
        }];

        // mapping all - in imports to _ is a bit hacky but it should always be fine
        parts.extend(self.path[1..].iter().map(|item| {
            item.chars()
                .map(|ch| if ch == '-' { '_' } else { ch })
                .filter(|ch| ch.is_alphanumeric() || *ch == '_')
                .collect::<String>()
        }));

        let module = parts.join(".");
        if !module.is_empty() {
            format!(
                "import {} as {}",
                module,
                self.name,
            )
        } else {
            "".to_string()
        }
    }
}

struct PythonContext {
    imports: Rc<CodeBuffer>,
    imports_buffer: bool,
}

impl PythonContext {
    const fn with_imports(imports: Rc<CodeBuffer>) -> Self {
        Self {
            imports,
            imports_buffer: false,
        }
    }

    fn import_buffer(&mut self) {
        if self.imports_buffer {
            return;
        }
        self.imports.line("import buffer as _buffer"); 
        self.imports_buffer = true;
    }
}