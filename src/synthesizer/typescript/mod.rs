// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use std::borrow::Cow;
use std::io;
use std::rc::Rc;

use indexmap::IndexMap;
use voca_rs::case::{camel_case, pascal_case};

use crate::cdk::TypeReference;
use crate::code::{CodeBuffer, IndentOptions};
use crate::ir::conditions::ConditionIr;
use crate::ir::constructor::ConstructorParameter;
use crate::ir::importer::ImportInstruction;
use crate::ir::mappings::{MappingInstruction, OutputType};
use crate::ir::outputs::OutputInstruction;
use crate::ir::reference::{Origin, PseudoParameter, Reference};
use crate::ir::resources::{ResourceInstruction, ResourceIr};
use crate::ir::CloudformationProgramIr;
use crate::parser::lookup_table::MappingInnerValue;
use crate::util::Hasher;
use crate::Error;

use super::{StackType, Synthesizer};

impl StackType {
    fn base_class(&self) -> &'static str {
        match self {
            StackType::Stack => "cdk.Stack",
            StackType::Construct => "Construct",
        }
    }

    fn scope_type(&self) -> &'static str {
        match self {
            StackType::Stack => "cdk.App",
            StackType::Construct => "Construct",
        }
    }

    fn props_extends(&self) -> &'static str {
        match self {
            StackType::Stack => " extends cdk.StackProps",
            StackType::Construct => "",
        }
    }

    fn super_call(&self) -> &'static str {
        match self {
            StackType::Stack => "super(scope, id, props);",
            StackType::Construct => "super(scope, id);",
        }
    }

    fn needs_construct_import(&self) -> bool {
        matches!(self, StackType::Construct)
    }

    fn add_transform_call(&self, transform: &str) -> String {
        match self {
            StackType::Stack => format!("this.addTransform('{transform}');"),
            StackType::Construct => format!("cdk.Stack.of(this).addTransform('{transform}');"),
        }
    }
}

const INDENT: Cow<'static, str> = Cow::Borrowed("  ");

pub struct Typescript {}

impl Synthesizer for Typescript {
    fn synthesize(
        &self,
        ir: CloudformationProgramIr,
        output: &mut dyn io::Write,
        stack_name: &str,
        stack_type: StackType,
    ) -> Result<(), Error> {
        let code = CodeBuffer::default();

        let imports = code.section(true);
        for import in &ir.imports {
            imports.line(import.to_typescript()?)
        }

        if stack_type.needs_construct_import() {
            imports.line("import { Construct } from 'constructs';");
        }

        let context = &mut TypescriptContext::with_imports(imports, stack_type);

        let iface_props = code.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(
                format!(
                    "export interface {stack_name}Props{} {{",
                    stack_type.props_extends()
                )
                .into(),
            ),
            trailing: Some("}".into()),
            trailing_newline: true,
        });
        for param in &ir.constructor.inputs {
            let comment = iface_props.tsdoc();
            if let Some(description) = &param.description {
                comment.line(description.to_owned());
            }
            let question_mark_token = match &param.default_value {
                None => "",
                Some(value) => {
                    let value = match param.constructor_type.as_str() {
                        "Number" => value.clone(),
                        _ => format!("'{}'", value.escape_debug()),
                    };
                    comment.line(format!("@default {value}"));
                    "?"
                }
            };
            let constructor_type = match param.constructor_type.as_str() {
                "List<Number>" => "number[]",
                t if t.contains("List") => "string[]",
                "Boolean" => "boolean",
                "Number" => "number",
                _ => "string",
            };
            iface_props.line(format!(
                "readonly {}{question_mark_token}: {};",
                pretty_name(&param.name),
                constructor_type,
            ));
        }
        code.newline();

        if let Some(description) = &ir.description {
            let comment = code.tsdoc();
            comment.line(description.to_owned());
        }
        let class = code.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(
                format!(
                    "export class {stack_name} extends {} {{",
                    stack_type.base_class()
                )
                .into(),
            ),
            trailing: Some("}".into()),
            trailing_newline: true,
        });
        if !ir.outputs.is_empty() {
            for op in &ir.outputs {
                if let Some(description) = &op.description {
                    let comment = class.tsdoc();
                    comment.line(description.to_owned());
                }
                // NOTE: the property type can be inferred by the compiler...
                class.line(format!(
                    "public readonly {name}{option};",
                    name = pretty_name(&op.name),
                    option = match &op.condition {
                        Some(_) => "?",
                        None => "",
                    }
                ));
            }
            class.newline();
        }

        let default_empty = if ir
            .constructor
            .inputs
            .iter()
            .all(|param| param.default_value.is_some())
        {
            " = {}"
        } else {
            ""
        };

        let  ctor = class.indent_with_options(IndentOptions{
            indent: INDENT,
            leading: Some(format!("public constructor(scope: {}, id: string, props: {stack_name}Props{default_empty}) {{", stack_type.scope_type()).into()),
            trailing: Some("}".into()),
            trailing_newline: true,
        });
        ctor.line(stack_type.super_call());

        let have_default_or_special_type_params = &ir
            .constructor
            .inputs
            .iter()
            .filter(|p| p.constructor_type.contains("AWS::") || p.default_value.is_some())
            .collect::<Vec<&ConstructorParameter>>();
        if !have_default_or_special_type_params.is_empty() {
            ctor.newline();
            ctor.line("// Applying default props");
            let obj = ctor.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some("props = {".into()),
                trailing: Some("};".into()),
                trailing_newline: true,
            });
            obj.line("...props,");
            for param in have_default_or_special_type_params {
                let name = &param.name;
                // example: AWS::EC2::Image::Id, List<AWS::EC2::VPC::Id>, AWS::SSM::Parameter::Value<List<String>>
                if param.constructor_type.contains("AWS::")
                    || param.no_echo.as_ref().is_some_and(|x| x == "true")
                {
                    let value_as = match &param.constructor_type {
                        t if t.contains("List") => "valueAsList",
                        _ => "valueAsString",
                    };
                    let cfn_param = obj.indent_with_options(IndentOptions {
                        indent: INDENT,
                        leading: Some(
                            format!(
                                "{name}: new cdk.CfnParameter(this, '{}', {{",
                                pascal_case(&param.name)
                            )
                            .into(),
                        ),
                        trailing: Some(format!("}}).{value_as},").into()),
                        trailing_newline: true,
                    });
                    cfn_param.line(format!("type: '{}',", param.constructor_type));
                    let to_string = match &param.constructor_type {
                        t if t.contains("List") => "join(',')",
                        _ => "toString()",
                    };
                    if let Some(v) = &param.default_value {
                        cfn_param.line(format!(
                            "default: props.{name}?.{to_string} ?? '{}',",
                            v.escape_debug()
                        ));
                    } else {
                        cfn_param.line(format!("default: props.{name}.{to_string},"));
                    };
                    if let Some(v) = &param.description {
                        cfn_param.line(format!("description: '{v}',"));
                    };
                    if let Some(v) = &param.no_echo {
                        cfn_param.line(format!("noEcho: {v},"));
                    }
                } else {
                    let value = match &param.default_value {
                        None => "".to_owned(),
                        Some(value) => {
                            let value = match param.constructor_type.as_str() {
                                "String" => format!("'{}'", value.escape_debug()),
                                "List<Number>" => format!("[{value}]"),
                                "CommaDelimitedList" => format!(
                                    "[{}]",
                                    value
                                        .split(',')
                                        .map(|v| format!("'{}'", v.escape_debug()))
                                        .collect::<Vec<String>>()
                                        .join(",")
                                ),
                                _ => value.clone(),
                            };
                            value
                        }
                    };

                    obj.line(format!("{name}: props.{name} ?? {value},"));
                };
            }
        }

        if !ir.transforms.is_empty() {
            ctor.newline();
            ctor.line("// Transforms");

            for transform in &ir.transforms {
                ctor.line(stack_type.add_transform_call(transform));
            }
        }

        emit_mappings(&ctor, &ir.mappings);

        if !ir.conditions.is_empty() {
            ctor.newline();
            ctor.line("// Conditions");

            for cond in &ir.conditions {
                let synthed = synthesize_condition_recursive(&cond.value, stack_type);
                ctor.line(format!("const {} = {};", pretty_name(&cond.name), synthed));
            }
        }

        ctor.newline();
        ctor.line("// Resources");

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
            ctor.line("// Outputs");

            for op in &ir.outputs {
                let var_name = pretty_name(&op.name);
                let cond = op.condition.as_ref().map(|s| pretty_name(s));

                if let Some(cond) = &cond {
                    ctor.line(format!(
                        "this.{var_name} = {cond}",
                        cond = pretty_name(cond)
                    ));
                    ctor.text(format!("{INDENT}? "));
                    let indented = ctor.indent(INDENT);
                    emit_resource_ir(context, &indented, &op.value, Some("\n"));
                    ctor.line(format!("{INDENT}: undefined;"));
                } else {
                    ctor.text(format!("this.{var_name} = "));
                    emit_resource_ir(context, &ctor, &op.value, Some(";\n"));
                }

                if let Some(cond) = cond {
                    let indented = ctor.indent_with_options(IndentOptions {
                        indent: INDENT,
                        leading: Some(format!("if ({cond}) {{").into()),
                        trailing: Some("}".into()),
                        trailing_newline: true,
                    });
                    emit_cfn_output(context, &indented, op, &var_name);
                } else {
                    emit_cfn_output(context, &ctor, op, &var_name);
                }
            }
        }

        Ok(code.write(output)?)
    }
}

impl ImportInstruction {
    fn to_typescript(&self) -> Result<String, Error> {
        let mut parts: Vec<String> = vec!["aws-cdk-lib".to_string()];
        match self.organization.as_str() {
            "AWS" => {
                if let Some(service) = &self.service {
                    parts.push(format!("aws-{}", service.to_lowercase()))
                }
            }
            "Alexa" => parts.push(format!(
                "alexa-{}",
                self.service.as_ref().unwrap().to_lowercase()
            )),
            org => {
                return Err(Error::ImportInstructionError {
                    message: format!("Expected organization to be AWS or Alexa. Found {org}"),
                })
            }
        }

        Ok(format!(
            "import * as {} from '{}';",
            self.service
                .as_ref()
                .unwrap_or(&"cdk".to_string())
                .to_lowercase(),
            parts.join("/")
        ))
    }
}

struct TypescriptContext {
    imports: Rc<CodeBuffer>,
    imports_buffer: bool,
    stack_type: StackType,
}
impl TypescriptContext {
    const fn with_imports(imports: Rc<CodeBuffer>, stack_type: StackType) -> Self {
        Self {
            imports,
            imports_buffer: false,
            stack_type,
        }
    }

    fn import_buffer(&mut self) {
        if self.imports_buffer {
            return;
        }
        self.imports.line("import { Buffer } from 'buffer';");
        self.imports_buffer = true;
    }
}

impl Reference {
    fn to_typescript(&self, stack_type: StackType) -> Cow<'static, str> {
        match &self.origin {
            Origin::CfnParameter | Origin::Parameter => {
                format!("props.{}!", camel_case(&self.name)).into()
            }
            Origin::LogicalId { conditional } => format!(
                "{var}{chain}ref",
                var = camel_case(&self.name),
                chain = if *conditional { "?." } else { "." }
            )
            .into(),
            Origin::Condition => camel_case(&self.name).into(),
            Origin::PseudoParameter(x) => {
                let prefix = if stack_type == StackType::Construct {
                    "cdk.Stack.of(this)."
                } else {
                    "this."
                };
                match x {
                    PseudoParameter::Partition => format!("{}partition", prefix).into(),
                    PseudoParameter::Region => format!("{}region", prefix).into(),
                    PseudoParameter::StackId => format!("{}stackId", prefix).into(),
                    PseudoParameter::StackName => format!("{}stackName", prefix).into(),
                    PseudoParameter::URLSuffix => format!("{}urlSuffix", prefix).into(),
                    PseudoParameter::AccountId => format!("{}account", prefix).into(),
                    PseudoParameter::NotificationArns => {
                        format!("{}notificationArns", prefix).into()
                    }
                }
            }
            Origin::GetAttribute {
                conditional,
                attribute,
            } => format!(
                "{var_name}{chain}attr{name}",
                var_name = camel_case(&self.name),
                chain = if *conditional { "?." } else { "." },
                name = pascal_case(&attribute.replace('.', ""))
            )
            .into(),
        }
    }
}

fn emit_cfn_output(
    context: &mut TypescriptContext,
    output: &CodeBuffer,
    op: &OutputInstruction,
    var_name: &str,
) {
    let output = output.indent_with_options(IndentOptions {
        indent: INDENT,
        leading: Some(format!("new cdk.CfnOutput(this, 'CfnOutput{}', {{", &op.name).into()),
        trailing: Some("});".into()),
        trailing_newline: true,
    });

    output.line(format!("key: '{}',", &op.name));
    if let Some(description) = &op.description {
        output.line(format!("description: '{}',", description.escape_debug()));
    }
    if let Some(export) = &op.export {
        output.text("exportName: ");
        emit_resource_ir(context, &output, export, Some(",\n"));
    }
    output.line(format!("value: this.{var_name}!.toString(),"));
}

fn emit_resource(
    context: &mut TypescriptContext,
    output: &CodeBuffer,
    reference: &ResourceInstruction,
) {
    let var_name = pretty_name(&reference.name);
    let service = reference.resource_type.service().to_lowercase();

    let maybe_undefined = if let Some(cond) = &reference.condition {
        output.line(format!(
            "const {var_name} = {cond}",
            cond = pretty_name(cond)
        ));

        let output = output.indent(INDENT);

        output.line(format!(
            "? new {service}.Cfn{rtype}(this, '{}', {{",
            reference.name.escape_debug(),
            rtype = reference.resource_type.type_name(),
        ));

        let mid_output = output.indent(INDENT);
        emit_resource_props(context, mid_output.indent(INDENT), &reference.properties);
        mid_output.line("})");

        output.line(": undefined;");

        true
    } else {
        output.line(format!(
            "const {var_name} = new {service}.Cfn{rtype}(this, '{}', {{",
            reference.name.escape_debug(),
            rtype = reference.resource_type.type_name(),
        ));

        emit_resource_props(context, output.indent(INDENT), &reference.properties);

        output.line("});");

        false
    };

    if maybe_undefined {
        output.line(format!("if ({var_name} != null) {{"));
        let indented = output.indent(INDENT);
        emit_resource_attributes(context, &indented, reference, &var_name);
        output.line("}");
    } else {
        emit_resource_attributes(context, output, reference, &var_name);
    }
}

fn emit_resource_attributes(
    context: &mut TypescriptContext,
    output: &CodeBuffer,
    reference: &ResourceInstruction,
    var_name: &str,
) {
    if let Some(metadata) = &reference.metadata {
        let md = output.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(format!("{var_name}.cfnOptions.metadata = {{").into()),
            trailing: Some("};".into()),
            trailing_newline: true,
        });
        emit_resource_metadata(context, md, metadata);
    }

    if let Some(update_policy) = &reference.update_policy {
        output.text(format!("{var_name}.cfnOptions.updatePolicy = "));
        emit_resource_ir(context, output, update_policy, Some(";"));
    }

    if let Some(deletion_policy) = &reference.deletion_policy {
        output.line(format!(
            "{var_name}.cfnOptions.deletionPolicy = cdk.CfnDeletionPolicy.{deletion_policy};"
        ));
    }

    if !reference.dependencies.is_empty() {
        for dependency in &reference.dependencies {
            output.line(format!(
                "{var_name}.addDependency({});",
                pretty_name(dependency)
            ));
        }
    }
}

fn emit_resource_metadata(
    context: &mut TypescriptContext,
    output: Rc<CodeBuffer>,
    metadata: &ResourceIr,
) {
    match metadata {
        ResourceIr::Object(_, entries) => {
            for (name, value) in entries {
                output.text(format!("{name}: "));
                emit_resource_ir(context, &output, value, Some(",\n"));
            }
        }
        unsupported => output.line(format!("/* {unsupported:?} */")),
    }
}

fn emit_resource_props(
    context: &mut TypescriptContext,
    output: Rc<CodeBuffer>,
    props: &IndexMap<String, ResourceIr, Hasher>,
) {
    for (name, prop) in props {
        output.text(format!("{}: ", pretty_name(name)));
        emit_resource_ir(context, &output, prop, Some(",\n"));
    }
}

fn emit_resource_ir(
    context: &mut TypescriptContext,
    output: &CodeBuffer,
    value: &ResourceIr,
    trailer: Option<&str>,
) {
    match value {
        // Literal values
        ResourceIr::Null => output.text("undefined"),
        ResourceIr::Bool(bool) => output.text(bool.to_string()),
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
                        if name.chars().all(|c| c.is_alphanumeric())
                            && name.chars().next().unwrap().is_alphabetic()
                        {
                            obj.text(format!("{name}: "));
                        } else {
                            obj.text(format!("'{name}': "));
                        }
                    }
                    _ => {
                        obj.text(format!("{key}: ", key = pretty_name(name)));
                    }
                }
                emit_resource_ir(context, &obj, value, Some(",\n"));
            }
        }

        // Intrinsics
        ResourceIr::Base64(base64) => match base64.as_ref() {
            ResourceIr::String(b64) => {
                context.import_buffer();
                output.text(format!(
                    "Buffer.from('{}', 'base64').toString('binary')",
                    b64.escape_debug()
                ))
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
            output.text(", String(");
            emit_resource_ir(context, output, mask, None);
            output.text("))")
        }
        ResourceIr::GetAZs(region) => {
            output.text("cdk.Fn.getAzs(");
            emit_resource_ir(context, output, region, None);
            output.text(")")
        }
        ResourceIr::If(cond_name, if_true, if_false) => {
            output.text(format!("{} ? ", pretty_name(cond_name)));
            emit_resource_ir(context, output, if_true, None);
            output.text(" : ");
            emit_resource_ir(context, output, if_false, None)
        }
        ResourceIr::ImportValue(import) => {
            output.text("cdk.Fn.importValue(");
            emit_resource_ir(context, output, import, None);
            output.text(")");
        }
        ResourceIr::Join(sep, list) => {
            let items = output.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some("[".into()),
                trailing: Some(format!("].join('{sep}')", sep = sep.escape_debug()).into()),
                trailing_newline: false,
            });
            for item in list {
                emit_resource_ir(context, &items, item, Some(",\n"));
            }
        }
        ResourceIr::Map(name, tlk, slk) => {
            output.text(format!("{}[", pretty_name(name)));
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
                    output.text("undefined")
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
            output.text("`");
            for part in parts {
                match part {
                    ResourceIr::String(lit) => output.text(lit.clone()),
                    other => {
                        output.text("${");
                        emit_resource_ir(context, output, other, None);
                        output.text("}");
                    }
                }
            }
            output.text("`")
        }

        // References
        ResourceIr::Ref(reference) => output.text(reference.to_typescript(context.stack_type)),
    }

    if let Some(trailer) = trailer {
        output.text(trailer.to_owned())
    }
}

fn emit_mappings(output: &CodeBuffer, mappings: &[MappingInstruction]) {
    if mappings.is_empty() {
        return;
    }

    output.newline();
    output.line("// Mappings");

    for mapping in mappings {
        let item_type = match mapping.output_type() {
            OutputType::Consistent(inner_type) => match inner_type {
                MappingInnerValue::Number(_) | MappingInnerValue::Float(_) => "number",
                MappingInnerValue::Bool(_) => "boolean",
                MappingInnerValue::String(_) => "string",
                MappingInnerValue::List(_) => "readonly string[]",
            },
            OutputType::Complex => "any",
        };

        let output = output.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(
                format!(
                    "const {var}: Record<string, Record<string, {item_type}>> = {{",
                    var = pretty_name(&mapping.name)
                )
                .into(),
            ),
            trailing: Some("};".into()),
            trailing_newline: true,
        });

        emit_mapping_instruction(output, mapping);
    }
}

fn synthesize_condition_recursive(val: &ConditionIr, stack_type: StackType) -> String {
    match val {
        ConditionIr::And(x) => {
            let a: Vec<String> = x
                .iter()
                .map(|v| synthesize_condition_recursive(v, stack_type))
                .collect();

            let inner = a.join(" && ");
            format!("({inner})")
        }
        ConditionIr::Equals(a, b) => {
            format!(
                "{} === {}",
                synthesize_condition_recursive(a.as_ref(), stack_type),
                synthesize_condition_recursive(b.as_ref(), stack_type)
            )
        }
        ConditionIr::Not(x) => {
            if x.is_simple() {
                format!(
                    "!{}",
                    synthesize_condition_recursive(x.as_ref(), stack_type)
                )
            } else {
                format!(
                    "!({})",
                    synthesize_condition_recursive(x.as_ref(), stack_type)
                )
            }
        }
        ConditionIr::Or(x) => {
            let a: Vec<String> = x
                .iter()
                .map(|v| synthesize_condition_recursive(v, stack_type))
                .collect();

            let inner = a.join(" || ");
            format!("({inner})")
        }
        ConditionIr::Str(x) => {
            format!("'{x}'")
        }
        ConditionIr::Condition(x) => pretty_name(x),
        ConditionIr::Ref(x) => x.to_typescript(stack_type).into(),
        ConditionIr::Map(named_resource, l1, l2) => {
            format!(
                "{}[{}][{}]",
                pretty_name(named_resource),
                synthesize_condition_recursive(l1.as_ref(), stack_type),
                synthesize_condition_recursive(l2.as_ref(), stack_type)
            )
        }
        ConditionIr::Split(sep, l1) => {
            let str = synthesize_condition_recursive(l1.as_ref(), stack_type);
            format!(
                "{str}.split('{sep}')",
                str = str.escape_debug(),
                sep = sep.escape_debug()
            )
        }
        ConditionIr::Select(index, l1) => {
            let str = synthesize_condition_recursive(l1.as_ref(), stack_type);
            format!("cdk.Fn.select({index}, {str})")
        }
    }
}

fn emit_mapping_instruction(output: Rc<CodeBuffer>, mapping_instruction: &MappingInstruction) {
    for (name, inner_mapping) in &mapping_instruction.map {
        let output = output.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(format!("'{key}': {{", key = name.escape_debug()).into()),
            trailing: Some("},".into()),
            trailing_newline: true,
        });
        emit_inner_mapping(output, inner_mapping);
    }
}

fn emit_inner_mapping(
    output: Rc<CodeBuffer>,
    inner_mapping: &IndexMap<String, MappingInnerValue, Hasher>,
) {
    for (name, value) in inner_mapping {
        output.line(format!("'{key}': {value},", key = name.escape_debug()));
    }
}

struct SuffixFix {
    suffix: &'static str,
    fix: &'static str,
}

/// If you have stumbled across this lunacy, I still don't fully understand it myself.
///
/// CDK folks decided to prettify a few names, e.g. ProviderARNs -> providerArns.
/// This list is hand-maintained, but always refer to the original source:
///
static SUFFIX_FIXES: &[SuffixFix] = &[
    SuffixFix {
        suffix: "ARNs",
        fix: "Arns",
    },
    SuffixFix {
        suffix: "MBs",
        fix: "MBs",
    },
    SuffixFix {
        suffix: "AZs",
        fix: "AZs",
    },
];

fn pretty_name(name: &str) -> String {
    // hardcoded consts that always need love.
    if name == "VPCs" {
        return "vpcs".to_string();
    }
    if name == "GetObject" {
        return "objectAccess".to_string();
    }
    if name == "Equals" {
        return "equalTo".to_string();
    }

    let mut end_str = name.to_string();
    for hay in SUFFIX_FIXES {
        if end_str.ends_with(hay.suffix) {
            end_str = end_str[0..end_str.len() - hay.suffix.len()].to_string();
            end_str.push_str(hay.fix);
            break;
        }
    }

    camel_case(&end_str)
}

trait TypescriptCodeBuffer {
    fn tsdoc(&self) -> Rc<CodeBuffer>;
}

impl TypescriptCodeBuffer for CodeBuffer {
    #[inline]
    fn tsdoc(&self) -> Rc<CodeBuffer> {
        self.indent_with_options(IndentOptions {
            indent: " * ".into(),
            leading: Some("/**".into()),
            trailing: Some(" */".into()),
            trailing_newline: true,
        })
    }
}

#[cfg(test)]
mod tests;
