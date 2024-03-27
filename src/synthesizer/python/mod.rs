use crate::cdk::TypeReference;
use crate::code::{CodeBuffer, IndentOptions};
use crate::ir::conditions::ConditionIr;
use crate::ir::constructor::ConstructorParameter;
use crate::ir::importer::ImportInstruction;
use crate::ir::mappings::MappingInstruction;
use crate::ir::outputs::OutputInstruction;
use crate::ir::reference::{Origin, PseudoParameter, Reference};
use crate::ir::resources::{ResourceInstruction, ResourceIr};
use crate::ir::CloudformationProgramIr;
use crate::parser::lookup_table::MappingInnerValue;
use crate::Error;
use indexmap::IndexMap;
use std::borrow::Cow;
use std::io;
use std::rc::Rc;
use voca_rs::case::{camel_case, pascal_case, snake_case};
use voca_rs::Voca;

use super::Synthesizer;

const INDENT: Cow<'static, str> = Cow::Borrowed("  ");

// reserved python keywords as of 3.13 (https://docs.python.org/3/reference/lexical_analysis.html#keywords)
// if we happen to name a module with one of these keywords, we need to prepend 'aws_' to avoid a name conflict
const KEYWORDS: &[&str] = &[
    "False", "await", "else", "import", "pass", "None", "break", "except", "in", "raise", "True",
    "class", "finally", "is", "return", "and", "continue", "for", "lambda", "try", "as", "def",
    "from", "nonlocal", "while", "assert", "del", "global", "not", "with", "async", "elif", "if",
    "or", "yield",
];

pub struct Python {}

impl Synthesizer for Python {
    fn synthesize(
        &self,
        ir: CloudformationProgramIr,
        output: &mut dyn io::Write,
        stack_name: &str,
    ) -> Result<(), Error> {
        let code = CodeBuffer::default();

        let imports = code.section(true);
        imports.line("from aws_cdk import Stack");
        for import in &ir.imports {
            imports.line(import.to_python()?);
        }
        imports.line("from constructs import Construct");

        let context = &mut PythonContext::with_imports(imports);

        if let Some(description) = &ir.description {
            let comment = code.pydoc();
            comment.line(description.to_owned());
        }
        let class = code.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(format!("class {}(Stack):", stack_name).into()),
            trailing: Some("".into()),
            trailing_newline: true,
        });

        let ctor = class.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(
                "def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:"
                    .to_string()
                    .into(),
            ),
            trailing: Some("".into()),
            trailing_newline: true,
        });
        ctor.line("super().__init__(scope, construct_id, **kwargs)");

        let have_default_or_special_type_params = &ir
            .constructor
            .inputs
            .iter()
            .filter(|p| p.constructor_type.contains("AWS::") || p.default_value.is_some())
            .collect::<Vec<&ConstructorParameter>>();
        if !have_default_or_special_type_params.is_empty() {
            ctor.newline();
            // props are handled weirdly in python. Python doesn't have interfaces so we try and retrieve
            // the props from kwargs, and default to None or a default value if one is given.
            ctor.line("# Applying default props");
            let obj = ctor.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some("props = {".into()),
                trailing: Some("}".into()),
                trailing_newline: true,
            });
            for param in have_default_or_special_type_params {
                let name = &param.name;
                if param.constructor_type.contains("AWS::")
                    || param.no_echo.as_ref().is_some_and(|x| x == "true")
                {
                    let cfn_param = obj.indent_with_options(IndentOptions {
                        indent: INDENT,
                        leading: Some(
                            format!(
                                "'{name}': cdk.CfnParameter(self, '{}', ",
                                camel_case(&param.name)
                            )
                            .into(),
                        ),
                        trailing: Some("),".into()),
                        trailing_newline: true,
                    });
                    cfn_param.line(format!("type = '{}',", param.constructor_type));
                    if let Some(v) = &param.default_value {
                        cfn_param.line(format!(
                            "default = str(kwargs.get('{name}', '{}')),",
                            v.escape_debug()
                        ));
                    } else {
                        cfn_param.line(format!("default = str(kwargs.get('{name}')),"));
                    };
                    if let Some(v) = &param.description {
                        cfn_param.line(format!("description = '{}',", v));
                    };
                    if let Some(v) = &param.no_echo {
                        cfn_param.line(format!("no_echo = {},", v._pascal_case()));
                    };
                } else {
                    let value = match &param.default_value {
                        None => "".to_owned(),
                        Some(value) => {
                            let value = match param.constructor_type.as_str() {
                                "String" => format!("'{}'", value.escape_debug()),
                                "List<Number>" => format!("[{}]", value),
                                "CommaDelimitedList" => format!(
                                    "[{}]",
                                    value
                                        .split(',')
                                        .map(|v| format!("'{}'", v.escape_debug()))
                                        .collect::<Vec<String>>()
                                        .join(",")
                                ),
                                "Boolean" => pascal_case(value),
                                _ => value.clone(),
                            };
                            value
                        }
                    };

                    obj.line(format!("'{name}': kwargs.get('{name}', {value}),"));
                };
            }
        }

        if !ir.transforms.is_empty() {
            ctor.newline();
            ctor.line("# Transforms");

            for transform in &ir.transforms {
                ctor.line(format!("Stack.add_transform(self, '{transform}')"))
            }
        }

        emit_mappings(&ctor, &ir.mappings);

        if !ir.conditions.is_empty() {
            ctor.newline();
            ctor.line("# Conditions");

            for cond in &ir.conditions {
                let synthed = synthesize_condition_recursive(&cond.value);
                ctor.line(format!("{} = {}", snake_case(&cond.name), synthed));
            }
        }

        ctor.newline();
        ctor.line("# Resources");

        let mut is_first_resource = true;
        for reference in &ir.resources {
            if is_first_resource {
                is_first_resource = false;
            } else {
                ctor.newline();
            }
            emit_resource(context, &ctor, reference);
        }

        if !ir.outputs.is_empty() {
            ctor.newline();
            ctor.line("# Outputs");

            for op in &ir.outputs {
                let var_name = snake_case(&op.name);
                let cond = op.condition.as_ref().map(|s| snake_case(s));
                if let Some(description) = &op.description {
                    let comment = ctor.pydoc();
                    comment.line(description.to_owned());
                }
                if let Some(cond) = &cond {
                    ctor.text(format!("self.{var_name} = "));
                    emit_resource_ir(context, &ctor, &op.value, Some(""));
                    ctor.line(format!(" if {cond} else None"));
                } else {
                    ctor.text(format!("self.{var_name} = "));
                    emit_resource_ir(context, &ctor, &op.value, Some("\n"));
                }

                if let Some(cond) = cond {
                    let indented = ctor.indent_with_options(IndentOptions {
                        indent: INDENT,
                        leading: Some(format!("if ({cond}):").into()),
                        trailing: Some("".into()),
                        trailing_newline: true,
                    });
                    emit_cfn_output(context, &indented, op, &var_name);
                } else {
                    emit_cfn_output(context, &ctor, op, &var_name);
                }
                ctor.newline();
            }
        }

        Ok(code.write(output)?)
    }
}

fn emit_cfn_output(
    context: &mut PythonContext,
    output: &CodeBuffer,
    op: &OutputInstruction,
    var_name: &str,
) {
    let output = output.indent_with_options(IndentOptions {
        indent: INDENT,
        leading: Some(format!("cdk.CfnOutput(self, 'CfnOutput{}', ", &op.name).into()),
        trailing: Some(")".into()),
        trailing_newline: true,
    });

    output.line(format!("key = '{}',", &op.name));
    if let Some(description) = &op.description {
        output.line(format!("description = '{}',", description.escape_debug()));
    }
    if let Some(export) = &op.export {
        output.text("export_name = ");
        emit_resource_ir(context, &output, export, Some(",\n"));
    }
    output.line(format!("value = str(self.{var_name}),"));
}

impl ImportInstruction {
    fn to_python(&self) -> Result<String, Error> {
        let import = match self.organization.as_str() {
            "AWS" => match &self.service {
                Some(service) => {
                    let s = service.to_lowercase();
                    if KEYWORDS.contains(&s.as_str()) {
                        format!("import aws_cdk.aws_{s} as aws_{s}").to_string()
                    } else {
                        format!("import aws_cdk.aws_{s} as {s}").to_string()
                    }
                }
                None => "import aws_cdk as cdk".to_string(),
            },
            "Alexa" => {
                let s = self.service.as_ref().unwrap().to_lowercase();
                format!("import alexa_{s} as ask from {s}").to_string()
            }
            org => {
                return Err(Error::ImportInstructionError {
                    message: format!("Expected organization to be AWS or Alexa. Found {org}"),
                })
            }
        };
        Ok(import)
    }
}

struct PythonContext {
    imports: Rc<CodeBuffer>,
    imports_base64: bool,
}

impl PythonContext {
    const fn with_imports(imports: Rc<CodeBuffer>) -> Self {
        Self {
            imports,
            imports_base64: false,
        }
    }

    fn import_base64(&mut self) {
        if self.imports_base64 {
            return;
        }
        self.imports.line("import base64");
        self.imports_base64 = true;
    }
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
            leading: Some(format!("{var} = {{", var = camel_case(&mapping.name)).into()),
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
        match value {
            MappingInnerValue::Bool(_) => output.line(format!(
                "'{key}': {value},",
                key = name.escape_debug(),
                value = capitalize(&value.to_string())
            )),
            _ => output.line(format!("'{key}': {value},", key = name.escape_debug())),
        }
    }
}

fn synthesize_condition_recursive(val: &ConditionIr) -> String {
    match val {
        ConditionIr::And(x) => {
            let a: Vec<String> = x
                .iter()
                .map(synthesize_condition_recursive)
                .map(|condition| snake_case(&condition))
                .collect();

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
                format!("not {}", snake_case(&synthesize_condition_recursive(x.as_ref())))
            } else {
                format!("not ({})", snake_case(&synthesize_condition_recursive(x.as_ref())))
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
        ConditionIr::Condition(x) => snake_case(x),
        ConditionIr::Ref(x) => x.to_python().into(),
        ConditionIr::Map(named_resource, l1, l2) => {
            format!(
                "{}[{}][{}]",
                snake_case(named_resource),
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
            Origin::CfnParameter => {
                format!("props['{}'].value_as_string", camel_case(&self.name)).into()
            }
            Origin::Parameter => format!("props['{}']", camel_case(&self.name)).into(),
            Origin::LogicalId { conditional: _ } => {
                format!("{var}{chain}ref", var = camel_case(&self.name), chain = ".").into()
            }
            Origin::Condition => camel_case(&self.name).into(),
            Origin::PseudoParameter(x) => match x {
                PseudoParameter::Partition => "self.partition".into(),
                PseudoParameter::Region => "self.region".into(),
                PseudoParameter::StackId => "self.stack_id".into(),
                PseudoParameter::StackName => "self.stack_name".into(),
                PseudoParameter::URLSuffix => "self.url_suffix".into(),
                PseudoParameter::AccountId => "self.account".into(),
                PseudoParameter::NotificationArns => "self.notification_arns".into(),
            },
            Origin::GetAttribute {
                conditional: _,
                attribute,
            } => format!(
                "{var_name}{chain}attr_{name}",
                var_name = camel_case(&self.name),
                chain = ".",
                name = snake_case(attribute)
            )
            .into(),
        }
    }
}

fn emit_resource(
    context: &mut PythonContext,
    output: &CodeBuffer,
    reference: &ResourceInstruction,
) {
    let var_name = camel_case(&reference.name);
    // lambda is a reserved keyword in python. If we encounter it or another keyword, we prepend 'aws_'
    let mut service: String = reference.resource_type.service().to_lowercase();
    if KEYWORDS.contains(&service.as_str()) {
        service = format!("aws_{}", reference.resource_type.service().to_lowercase());
    }
    let maybe_undefined = if let Some(cond) = &reference.condition {
        output.line(format!(
            "{var_name} = {service}.Cfn{rtype}(self, '{}',",
            reference.name.escape_debug(),
            rtype = reference.resource_type.type_name()
        ));

        let output = output.indent(INDENT);

        let mid_output = output.indent(INDENT);
        emit_resource_props(context, mid_output.indent(INDENT), &reference.properties);
        mid_output.line(format!(") if {} else None", snake_case(cond)));

        true
    } else {
        output.line(format!(
            "{var_name} = {service}.Cfn{rtype}(self, '{}',",
            reference.name.escape_debug(),
            rtype = reference.resource_type.type_name()
        ));

        let output = output.indent(INDENT);

        let mid_output = output.indent(INDENT);
        emit_resource_props(context, mid_output.indent(INDENT), &reference.properties);
        mid_output.line(")");

        false
    };

    if maybe_undefined {
        output.line(format!("if ({var_name} is not None):"));
        let indented = output.indent(INDENT);
        emit_resource_attributes(context, &indented, reference, &var_name);
    } else {
        emit_resource_attributes(context, output, reference, &var_name);
    }
}

fn emit_resource_attributes(
    context: &mut PythonContext,
    output: &CodeBuffer,
    reference: &ResourceInstruction,
    var_name: &str,
) {
    if let Some(metadata) = &reference.metadata {
        let md = output.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(format!("{var_name}.cfn_options.metadata = {{").into()),
            trailing: Some("}".into()),
            trailing_newline: true,
        });
        emit_resource_metadata(context, md, metadata);
    }

    if let Some(update_policy) = &reference.update_policy {
        output.text(format!("{var_name}.cfn_options.update_policy = "));
        emit_resource_ir(context, output, update_policy, Some(""));
    }

    if let Some(deletion_policy) = &reference.deletion_policy {
        output.line(format!(
            "{var_name}.cfn_options.deletion_policy = cdk.CfnDeletionPolicy.{deletion_policy}"
        ));
    }

    if !reference.dependencies.is_empty() {
        for dependency in &reference.dependencies {
            output.line(format!(
                "{var_name}.add_dependency({})",
                camel_case(dependency)
            ));
        }
    }
}

fn emit_resource_metadata(
    context: &mut PythonContext,
    output: Rc<CodeBuffer>,
    metadata: &ResourceIr,
) {
    match metadata {
        ResourceIr::Object(_, entries) => {
            for (name, value) in entries {
                output.text(format!("'{name}': "));
                emit_resource_ir(context, &output, value, Some(",\n"));
            }
        }
        unsupported => output.line(format!("\"\"\" {unsupported:?} \"\"\"")),
    }
}

fn emit_resource_props<S>(
    context: &mut PythonContext,
    output: Rc<CodeBuffer>,
    props: &IndexMap<String, ResourceIr, S>,
) {
    for (name, prop) in props {
        output.text(format!("{} = ", snake_case(name)));
        emit_resource_ir(context, &output, prop, Some(",\n"));
    }
}

fn emit_resource_ir(
    context: &mut PythonContext,
    output: &CodeBuffer,
    value: &ResourceIr,
    trailer: Option<&str>,
) {
    match value {
        // Literal values
        ResourceIr::Null => output.text("None"),
        ResourceIr::Bool(bool) => output.text(capitalize(&bool.to_string())),
        ResourceIr::Double(float) => output.text(format!("{float}")),
        ResourceIr::Number(int) => output.text(int.to_string()),
        ResourceIr::String(str) => output.text(format!("'{}'", str.escape_debug())),

        // Collection values
        ResourceIr::Array(_, array) => {
            let arr = output.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some("[".into()),
                trailing: Some("]".into()),
                trailing_newline: false,
            });
            for item in array {
                emit_resource_ir(context, &arr, item, Some(",\n"));
            }
        }
        ResourceIr::Object(structure, entries) => {
            let obj = output.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some("{".into()),
                trailing: Some("}".into()),
                trailing_newline: false,
            });
            for (name, value) in entries {
                match structure {
                    TypeReference::Primitive(_) | TypeReference::Map(_) => {
                        obj.text(format!("'{name}': "));
                    }
                    _ => {
                        obj.text(format!("'{key}': ", key = camel_case(name)));
                    }
                }
                emit_resource_ir(context, &obj, value, Some(",\n"));
            }
        }

        // Intrinsics
        ResourceIr::Base64(base64) => match base64.as_ref() {
            ResourceIr::String(b64) => {
                context.import_base64();
                output.text(format!("base64.b64decode('{}')", b64.escape_debug()))
            }
            other => {
                output.text("cdk.Fn.base64(");
                emit_resource_ir(context, output, other, None);
                output.text(")")
            }
        },
        ResourceIr::Cidr(ip_range, count, mask) => {
            output.text("cdk.Fn.cidr(");
            emit_resource_ir(context, output, ip_range, None);
            output.text(", ");
            emit_resource_ir(context, output, count, None);
            output.text(", str(");
            emit_resource_ir(context, output, mask, None);
            output.text("))")
        }
        ResourceIr::GetAZs(region) => {
            output.text("cdk.Fn.get_azs(");
            emit_resource_ir(context, output, region, None);
            output.text(")")
        }
        ResourceIr::If(cond_name, if_true, if_false) => {
            emit_resource_ir(context, output, if_true, None);
            output.text(format!(" if {} else ", snake_case(cond_name)));
            emit_resource_ir(context, output, if_false, None)
        }
        ResourceIr::ImportValue(import) => {
            output.text("cdk.Fn.import_value(");
            emit_resource_ir(context, output, import, None);
            output.text(")");
        }
        ResourceIr::Join(sep, list) => {
            let items = output.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some(format!("'{sep}'.join([", sep = sep.escape_debug()).into()),
                trailing: Some("])".into()),
                trailing_newline: false,
            });
            for item in list {
                emit_resource_ir(context, &items, item, Some(",\n"));
            }
        }
        ResourceIr::Map(name, tlk, slk) => {
            output.text(format!("{}[", camel_case(name)));
            emit_resource_ir(context, output, tlk, None);
            output.text("][");
            emit_resource_ir(context, output, slk, None);
            output.text("]")
        }
        ResourceIr::Select(idx, list) => match list.as_ref() {
            ResourceIr::Array(_, array) => {
                if *idx <= array.len() {
                    emit_resource_ir(context, output, &array[*idx], None)
                } else {
                    output.text("None")
                }
            }
            other => {
                output.text("cdk.Fn.select(");
                output.text(idx.to_string());
                output.text(", ");
                emit_resource_ir(context, output, other, None);
                output.text(")")
            }
        },
        ResourceIr::Split(sep, str) => match str.as_ref() {
            ResourceIr::String(str) => {
                output.text(format!("'{str}'", str = str.escape_debug()));
                output.text(format!(".split('{sep}')", sep = sep.escape_debug()))
            }
            other => {
                output.text(format!("cdk.Fn.split('{sep}', ", sep = sep.escape_debug()));
                emit_resource_ir(context, output, other, None);
                output.text(")")
            }
        },
        ResourceIr::Sub(parts) => {
            output.text("f\"\"\"");
            for part in parts {
                match part {
                    ResourceIr::String(lit) => {
                        let escaped_lit = lit.replace('{', "{{").replace('}', "}}");
                        output.text(escaped_lit);
                    }
                    other => {
                        output.text("{");
                        emit_resource_ir(context, output, other, None);
                        output.text("}");
                    }
                }
            }
            output.text("\"\"\"")
        }

        // References
        ResourceIr::Ref(reference) => output.text(reference.to_python()),
    }
    if let Some(trailer) = trailer {
        output.text(trailer.to_owned())
    }
}

pub fn capitalize(s: &str) -> String {
    let mut c = s.chars();
    match c.next() {
        None => String::new(),
        Some(f) => f.to_uppercase().collect::<String>() + c.as_str(),
    }
}
