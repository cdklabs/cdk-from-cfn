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
        imports.line("from aws_cdk import Stack");
        for import in &ir.imports {
            imports.line(import.to_python());
        }
        imports.line("from constructs import Construct");

        let context = &mut PythonContext::with_imports(imports);

        if let Some(description) = &ir.description {
            let comment = code.pydoc();
            comment.line(description.to_owned());
        }
        let class = code.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some("class PythonStack(Stack):".into()),
            trailing: Some("".into()),
            trailing_newline: true,
        });
        if !ir.outputs.is_empty() {
            for op in &ir.outputs {
                if let Some(description) = &op.description {
                    let comment = class.pydoc();
                    comment.line(description.to_owned());
                }
                // NOTE: the property type can be inferred by the compiler...
                class.line(format!(
                    "global {name}",
                    name = pretty_name(&op.name)
                ));
            }
            class.newline();
        }
        
        let  ctor = class.indent_with_options(IndentOptions{
            indent: INDENT,
            leading: Some(format!("def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:").into()),
            trailing: Some("".into()),
            trailing_newline: true,
        });
        ctor.line("super().__init__(scope, construct_id, **kwargs)");
        
        emit_mappings(&ctor, &ir.mappings);
        
        if !ir.conditions.is_empty() {
            ctor.newline();
            ctor.line("# Conditions");

            for cond in &ir.conditions {
                let synthed = synthesize_condition_recursive(&cond.value);
                ctor.line(format!("{} = {}", camel_case(&cond.name), synthed));
            }
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

fn pretty_name(name: &str) -> String {
    let mut pretty = String::new();
    for (i, ch) in name.chars().enumerate() {
        if ch.is_uppercase() && i != 0 {
            pretty.push('_');
        }
        pretty.push(ch.to_lowercase().next().unwrap());
    }
    pretty
}

trait PythonCodeBuffer {
    fn pydoc(&self) -> Rc<CodeBuffer>;
}

impl PythonCodeBuffer for CodeBuffer {
    #[inline]
    fn pydoc(&self) -> Rc<CodeBuffer> {
        self.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some("\"\"\"".into()),
            trailing: Some("\"\"\"".into()),
            trailing_newline: true,
        })
    }
}

fn emit_mappings(output: &CodeBuffer, mappings: &[MappingInstruction]) {
    if mappings.is_empty() {
        return;
    }

    output.newline();
    output.line("# Mappings");

    for mapping in mappings {

        let output = output.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(
                format!(
                    "{var} = {{",
                    var = pretty_name(&mapping.name)
                )
                .into(),
            ),
            trailing: Some("}".into()),
            trailing_newline: true,
        });

        emit_mapping_instruction(output, mapping);
    }
}

fn emit_mapping_instruction(output: Rc<CodeBuffer>, mapping_instruction: &MappingInstruction) {
    for (name, inner_mapping) in &mapping_instruction.map {
        let output = output.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(format!("'{}': {{", name.escape_debug()).into()),
            trailing: Some("},".into()),
            trailing_newline: true,
        });
        emit_inner_mapping(output, inner_mapping);
    }
}

fn emit_inner_mapping(output: Rc<CodeBuffer>, inner_mapping: &IndexMap<String, MappingInnerValue>) {
    for (name, value) in inner_mapping {
        output.line(format!("'{key}': {value},", key = name.escape_debug()));
    }
}

fn synthesize_condition_recursive(val: &ConditionIr) -> String {
    match val {
        ConditionIr::And(x) => {
            let a: Vec<String> = x.iter().map(synthesize_condition_recursive).collect();

            let inner = a.join(" and ");
            format!("({inner})")
        }
        ConditionIr::Equals(a, b) => {
            format!(
                "{} == {}",
                synthesize_condition_recursive(a.as_ref()),
                synthesize_condition_recursive(b.as_ref())
            )
        }
        ConditionIr::Not(x) => {
            if x.is_simple() {
                format!("!{}", synthesize_condition_recursive(x.as_ref()))
            } else {
                format!("!({})", synthesize_condition_recursive(x.as_ref()))
            }
        }
        ConditionIr::Or(x) => {
            let a: Vec<String> = x.iter().map(synthesize_condition_recursive).collect();

            let inner = a.join(" or ");
            format!("({inner})")
        }
        ConditionIr::Str(x) => {
            format!("'{x}'")
        }
        ConditionIr::Condition(x) => pretty_name(x),
        ConditionIr::Ref(x) => x.to_python().into(),
        ConditionIr::Map(named_resource, l1, l2) => {
            format!(
                "{}[{}][{}]",
                pretty_name(named_resource),
                synthesize_condition_recursive(l1.as_ref()),
                synthesize_condition_recursive(l2.as_ref())
            )
        }
        ConditionIr::Split(sep, l1) => {
            let str = synthesize_condition_recursive(l1.as_ref());
            format!(
                "{str}.split('{sep}')",
                str = str.escape_debug(),
                sep = sep.escape_debug()
            )
        }
        ConditionIr::Select(index, l1) => {
            let str = synthesize_condition_recursive(l1.as_ref());
            format!("cdk.Fn.select({index}, {str})")
        }
    }
}

impl Reference {
    fn to_python(&self) -> Cow<'static, str> {
        match &self.origin {
            Origin::Parameter => format!("props.{}", camel_case(&self.name)).into(),
            Origin::LogicalId { conditional } => format!(
                "{var}{chain}ref",
                var = camel_case(&self.name),
                chain = if *conditional { "?." } else { "." }
            )
            .into(),
            Origin::Condition => camel_case(&self.name).into(),
            Origin::PseudoParameter(x) => match x {
                PseudoParameter::Partition => "self.partition".into(),
                PseudoParameter::Region => "self.region".into(),
                PseudoParameter::StackId => "self.stackId".into(),
                PseudoParameter::StackName => "self.stackName".into(),
                PseudoParameter::URLSuffix => "self.urlSuffix".into(),
                PseudoParameter::AccountId => "self.account".into(),
                PseudoParameter::NotificationArns => "self.notificationArns".into(),
            },
            Origin::GetAttribute {
                conditional,
                attribute,
            } => format!(
                "{var_name}{chain}attr{name}",
                var_name = camel_case(&self.name),
                chain = if *conditional { "?." } else { "." },
                name = camel_case(attribute)
            )
            .into(),
        }
    }
}