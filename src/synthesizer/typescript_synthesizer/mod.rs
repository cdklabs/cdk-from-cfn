#![cfg_attr(coverage_nightly, feature(no_coverage))]

use crate::ir::conditions::ConditionIr;
use crate::ir::mappings::{MappingInstruction, OutputType};
use crate::ir::outputs::OutputInstruction;
use crate::ir::reference::{Origin, PseudoParameter, Reference};
use crate::ir::resources::{ResourceInstruction, ResourceIr};
use crate::ir::CloudformationProgramIr;
use crate::parser::lookup_table::MappingInnerValue;
use base64::Engine;
use indexmap::IndexMap;
use std::collections::HashMap;
use std::io;
use voca_rs::case::{camel_case, pascal_case};

use super::output::CodeSink;
use super::Synthesizer;

pub struct TypescriptSynthesizer {
    // TODO: Put options in here for different outputs in typescript
}

impl TypescriptSynthesizer {
    #[cfg_attr(coverage_nightly, no_coverage)]
    #[deprecated(note = "Prefer using the Synthesizer API instead")]
    pub fn output(ir: CloudformationProgramIr) -> String {
        let mut output = Vec::new();
        TypescriptSynthesizer {}
            .synthesize(ir, &mut output)
            .unwrap();
        String::from_utf8(output).unwrap()
    }
}

impl Synthesizer for TypescriptSynthesizer {
    fn synthesize(
        &self,
        ir: CloudformationProgramIr,
        output: &mut dyn io::Write,
    ) -> io::Result<()> {
        let mut output = CodeSink::typescript(output);

        for import in &ir.imports {
            output.write_text(&format!(
                "import * as {} from '{}';",
                import.name,
                import.path.join("/"),
            ))?;
        }
        // Static imports with base assumptions (e.g. using base 64)
        output.write_text("import { Buffer } from 'buffer';")?;
        output.blank_line()?;

        output.write_line("export interface NoctStackProps extends cdk.StackProps {")?;
        let default_props = {
            let output = &mut output.indented();
            let mut default_props: HashMap<&str, String> =
                HashMap::with_capacity(ir.constructor.inputs.len());
            for param in &ir.constructor.inputs {
                output.write_text("/**")?;
                if let Some(description) = &param.description {
                    output.write_with_prefix(" * ", description)?;
                }
                let question_mark_token = match &param.default_value {
                    None => "",
                    Some(value) => {
                        let value = match param.constructor_type.as_str() {
                            "String" => format!("{value:?}"),
                            _ => value.clone(),
                        };
                        output.write_line(&format!(" * @default {value}"))?;
                        default_props.insert(&param.name, value);
                        "?"
                    }
                };
                output.write_line(" */")?;
                output.write_line(&format!(
                    "readonly {}{question_mark_token}: {};",
                    pretty_name(&param.name),
                    pretty_name(&param.constructor_type),
                ))?;
            }
            default_props
        };
        output.write_line("}")?;
        output.blank_line()?;

        if let Some(description) = &ir.description {
            output.write_line("/**")?;
            output.write_with_prefix(" * ", description)?;
            output.write_line(" */")?;
        }
        output.write_line("export class NoctStack extends cdk.Stack {")?;
        {
            let output = &mut output.indented();

            if !ir.outputs.is_empty() {
                for op in &ir.outputs {
                    if let Some(description) = &op.description {
                        output.write_line("/**")?;
                        output.write_with_prefix(" * ", description)?;
                        output.write_line(" */")?;
                    }
                    // NOTE: the property type can be inferred by the compiler...
                    output.write_line(&format!(
                        "public readonly {name}{option};",
                        name = pretty_name(&op.name),
                        option = match &op.condition {
                            Some(_) => "?",
                            None => "",
                        }
                    ))?;
                }
                output.blank_line()?;
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

            output.write_line(&format!("public constructor(scope: cdk.App, id: string, props: NoctStackProps{default_empty}) {{"))?;
            {
                let mut output = output.indented();

                output.write_line("super(scope, id, props);")?;

                if !default_props.is_empty() {
                    output.blank_line()?;
                    output.write_line("// Applying default props")?;
                    output.write_line("props = {")?;
                    {
                        let output = &mut output.indented();
                        output.write_line("...props,")?;
                        for (name, value) in default_props {
                            output.write_line(&format!("{name}: props.{name} ?? {value},"))?;
                        }
                    }
                    output.write_line("};")?;
                }

                if !ir.mappings.is_empty() {
                    emit_mappings(&mut output, &ir.mappings)?;
                }

                if !ir.conditions.is_empty() {
                    output.blank_line()?;
                    output.write_line("// Conditions")?;

                    for cond in &ir.conditions {
                        let synthed = synthesize_condition_recursive(&cond.value);
                        output.write_line(&format!(
                            "const {} = {};",
                            pretty_name(&cond.name),
                            synthed
                        ))?;
                    }
                }

                output.blank_line()?;
                output.write_line("// Resources")?;

                let mut is_first_resource = true;
                for reference in &ir.resources {
                    if is_first_resource {
                        is_first_resource = false;
                    } else {
                        output.blank_line()?;
                    }
                    emit_resource(&mut output, reference)?;
                }

                if !ir.outputs.is_empty() {
                    output.blank_line()?;
                    output.write_line("// Outputs")?;

                    for op in &ir.outputs {
                        let var_name = pretty_name(&op.name);
                        let cond = op.condition.as_ref().map(|s| pretty_name(s));

                        if let Some(cond) = &cond {
                            output.write_line(&format!(
                                "this.{var_name} = {cond}",
                                cond = pretty_name(cond)
                            ))?;
                            let output = &mut output.indented();
                            output.write_raw("? ", true)?;
                            emit_resource_ir(&mut output.indented(), &op.value, false, Some(""))?;
                            output.write_line(": undefined;")?;
                        } else {
                            output.write_raw(&format!("this.{var_name} = "), true)?;
                            emit_resource_ir(&mut output, &op.value, false, Some(";"))?;
                        }

                        if let Some(export) = &op.export {
                            if let Some(cond) = cond {
                                output.write_line(&format!("if ({cond}) {{"))?;
                                emit_cfn_output(output.indented(), op, export, &var_name)?;
                                output.write_line("}")?;
                            } else {
                                emit_cfn_output(output.indented(), op, export, &var_name)?;
                            }
                        }
                    }
                }
            }
            output.write_line("}")?;
        }
        output.write_line("}")
    }
}

impl Reference {
    fn synthesize(&self) -> String {
        match &self.origin {
            Origin::Parameter => {
                format!("props.{}", camel_case(&self.name))
            }
            Origin::LogicalId { conditional } => format!(
                "{var}{chain}ref",
                var = camel_case(&self.name),
                chain = if *conditional { "?." } else { "." }
            ),
            Origin::Condition => camel_case(&self.name),
            Origin::PseudoParameter(x) => match x {
                PseudoParameter::Partition => String::from("this.partition"),
                PseudoParameter::Region => String::from("this.region"),
                PseudoParameter::StackId => String::from("this.stackId"),
                PseudoParameter::StackName => String::from("this.stackName"),
                PseudoParameter::URLSuffix => String::from("this.urlSuffix"),
                PseudoParameter::AccountId => String::from("this.account"),
                PseudoParameter::NotificationArns => String::from("this.notificationArns"),
            },
            Origin::GetAttribute {
                conditional,
                attribute,
            } => format!(
                "{var_name}{chain}attr{name}",
                var_name = camel_case(&self.name),
                chain = if *conditional { "?." } else { "." },
                name = pascal_case(attribute)
            ),
        }
    }
}

fn emit_cfn_output(
    mut output: CodeSink,
    op: &OutputInstruction,
    export: &ResourceIr,
    var_name: &str,
) -> io::Result<()> {
    output.write_line(&format!("new cdk.CfnOutput(this, '{}', {{", &op.name))?;

    let props = &mut output.indented();
    if let Some(description) = &op.description {
        props.write_line(&format!("description: '{}',", description.escape_debug()))?;
    }
    props.write_raw("exportName: ", true)?;
    emit_resource_ir(props, export, false, Some(","))?;
    props.write_line(&format!("value: this.{var_name},"))?;

    output.write_line("});")
}

fn emit_resource(output: &mut CodeSink, reference: &ResourceInstruction) -> io::Result<()> {
    let mut split_ref = reference.resource_type.split("::");
    let base_type = split_ref.next().unwrap();
    let service: String;
    let rtype: String;
    if base_type.starts_with("Custom") {
        service = String::from("CloudFormation").to_ascii_lowercase();
        rtype = String::from("CustomResource");
    } else {
        service = split_ref.next().unwrap().to_ascii_lowercase();
        rtype = String::from(split_ref.next().unwrap());
    }

    let var_name = pretty_name(&reference.name);

    let maybe_undefined = if let Some(cond) = &reference.condition {
        append_references(output, reference)?;

        output.write_line(&format!(
            "const {var_name} = {cond}",
            cond = pretty_name(cond)
        ))?;

        let mut output = output.indented();

        output.write_line(&format!(
            "? new {service}.Cfn{rtype}(this, '{}', {{",
            reference.name.escape_debug(),
        ))?;

        let mid_output = &mut output.indented();
        emit_resource_props(mid_output.indented(), &reference.properties)?;
        mid_output.write_line("})")?;

        output.write_line(": undefined;")?;

        true
    } else {
        append_references(output, reference)?;
        output.write_line(&format!(
            "const {var_name} = new {service}.Cfn{rtype}(this, '{}', {{",
            reference.name.escape_debug()
        ))?;

        emit_resource_props(output.indented(), &reference.properties)?;

        output.write_line("});")?;

        false
    };

    if maybe_undefined {
        output.write_line(&format!("if ({var_name} != null) {{"))?;
        emit_resource_attributes(&mut output.indented(), reference, &var_name)?;
        output.write_line("}")?;
    } else {
        emit_resource_attributes(output, reference, &var_name)?;
    }

    Ok(())
}

fn emit_resource_attributes(
    output: &mut CodeSink,
    reference: &ResourceInstruction,
    var_name: &str,
) -> io::Result<()> {
    if let Some(metadata) = &reference.metadata {
        output.write_line(&format!("{var_name}.cfnOptions.metadata = {{"))?;

        emit_resource_metadata(output.indented(), metadata)?;

        output.write_line("};")?;
    }

    if let Some(update_policy) = &reference.update_policy {
        output.write_line(&format!("{var_name}.cfnOptions.updatePolicy = "))?;
        emit_resource_ir(output, update_policy, false, Some(";"))?;
    }

    if let Some(deletion_policy) = &reference.deletion_policy {
        output.write_line(&format!(
            "{var_name}.cfnOptions.deletionPolicy = cdk.CfnDeletionPolicy.{deletion_policy};"
        ))?;
    }

    if !reference.dependencies.is_empty() {
        for dependency in &reference.dependencies {
            output.write_line(&format!(
                "{var_name}.addDependency({});",
                pretty_name(dependency)
            ))?;
        }
    }

    Ok(())
}

fn emit_resource_metadata(mut output: CodeSink, metadata: &ResourceIr) -> io::Result<()> {
    match metadata {
        ResourceIr::Object(_, entries) => {
            for (name, value) in entries {
                output.write_raw(&format!("{name}: "), true)?;
                emit_resource_ir(&mut output, value, false, Some(","))?;
            }
            Ok(())
        }
        unsupported => output.write_line(&format!("/* {unsupported:?} */")),
    }
}

fn emit_resource_props<S>(
    mut output: CodeSink,
    props: &IndexMap<String, ResourceIr, S>,
) -> io::Result<()> {
    for (name, prop) in props {
        output.write(&format!("{}: ", pretty_name(name)))?;
        emit_resource_ir(&mut output, prop, false, Some(","))?;
    }
    Ok(())
}

fn emit_resource_ir(
    output: &mut CodeSink,
    value: &ResourceIr,
    lead_indent: bool,
    trailer: Option<&str>,
) -> io::Result<()> {
    match value {
        // Literal values
        ResourceIr::Null => output.write_raw("undefined", lead_indent)?,
        ResourceIr::Bool(bool) => output.write_raw(&bool.to_string(), lead_indent)?,
        ResourceIr::Double(float) => output.write_raw(&format!("{float}"), lead_indent)?,
        ResourceIr::Number(int) => output.write_raw(&int.to_string(), lead_indent)?,
        ResourceIr::String(str) => {
            output.write_raw(&format!("'{}'", str.escape_debug()), lead_indent)?
        }

        // Collection values
        ResourceIr::Array(_, array) => {
            output.write_raw_line("[", lead_indent)?;
            let items = &mut output.indented();
            for item in array {
                emit_resource_ir(items, item, true, Some(","))?;
            }
            output.write("]")?
        }
        ResourceIr::Object(_, entries) => {
            output.write_raw_line("{", lead_indent)?;
            let items = &mut output.indented();
            for (name, value) in entries {
                items.write(&format!("{key}: ", key = pretty_name(name)))?;
                emit_resource_ir(items, value, false, Some(","))?;
            }
            output.write("}")?;
        }

        // Intrinsics
        ResourceIr::Base64(base64) => match base64.as_ref() {
            ResourceIr::String(b64) => {
                match base64::engine::general_purpose::STANDARD.decode(b64) {
                    Ok(plain) => match String::from_utf8(plain) {
                        Ok(plain) => {
                            output.write_raw(&format!("'{}'", plain.escape_debug()), lead_indent)?
                        }
                        Err(_) => output.write_raw(
                            &format!(
                                "Buffer.from('{}', 'base64').toString('binary')",
                                b64.escape_debug()
                            ),
                            lead_indent,
                        )?,
                    },
                    Err(cause) => {
                        return Err(io::Error::new(
                            io::ErrorKind::Other,
                            format!("invalid base64: {b64:?} -- {cause}"),
                        ))
                    }
                }
            }
            other => {
                output.write_raw("cdk.Fn.base64(", lead_indent)?;
                emit_resource_ir(output, other, false, None)?;
                output.write_raw(")", false)?
            }
        },
        ResourceIr::Cidr(ip_range, count, mask) => {
            output.write_raw("cdk.Fn.cidr(", lead_indent)?;
            emit_resource_ir(output, ip_range, false, None)?;
            output.write_raw(", ", false)?;
            emit_resource_ir(output, count, false, None)?;
            output.write_raw(", String(", false)?;
            emit_resource_ir(output, mask, false, None)?;
            output.write_raw("))", false)?;
        }
        ResourceIr::GetAZs(region) => {
            output.write_raw("cdk.Fn.getAzs(", lead_indent)?;
            emit_resource_ir(output, region, false, None)?;
            output.write_raw(")", false)?;
        }
        ResourceIr::If(cond_name, if_true, if_false) => {
            output.write_raw(&format!("{} ? ", pretty_name(cond_name)), lead_indent)?;
            emit_resource_ir(output, if_true, false, None)?;
            output.write_raw(" : ", false)?;
            emit_resource_ir(output, if_false, false, None)?;
        }
        ResourceIr::ImportValue(name) => output.write_raw(
            &format!("cdk.Fn.importValue('{}')", name.escape_debug()),
            lead_indent,
        )?,
        ResourceIr::Join(sep, list) => {
            output.write_raw_line("[", lead_indent)?;
            let items = &mut output.indented();
            for item in list {
                emit_resource_ir(items, item, true, Some(","))?;
            }
            output.write_raw(&format!("].join('{sep}')", sep = sep.escape_debug()), true)?
        }
        ResourceIr::Map(name, tlk, slk) => {
            output.write_raw(&format!("{}[", pretty_name(name)), lead_indent)?;
            emit_resource_ir(output, tlk, false, None)?;
            output.write_raw("][", false)?;
            emit_resource_ir(output, slk, false, None)?;
            output.write_raw("]", false)?
        }
        ResourceIr::Select(idx, list) => match list.as_ref() {
            ResourceIr::Array(_, array) => {
                if *idx <= array.len() {
                    emit_resource_ir(output, &array[*idx], lead_indent, None)?
                } else {
                    output.write_raw("undefined", lead_indent)?
                }
            }
            other => {
                output.write_raw("cdk.Fn.select(", lead_indent)?;
                output.write_raw(&idx.to_string(), false)?;
                output.write_raw(", ", false)?;
                emit_resource_ir(output, other, false, None)?;
                output.write_raw(")", false)?
            }
        },
        ResourceIr::Split(sep, str) => match str.as_ref() {
            ResourceIr::String(str) => {
                output.write_raw(&format!("'{str}'", str = str.escape_debug(),), lead_indent)?;
                output.write_raw(&format!(".split('{sep}')", sep = sep.escape_debug()), false)?
            }
            other => {
                output.write_raw(
                    &format!("cdk.Fn.split('{sep}', ", sep = sep.escape_debug()),
                    lead_indent,
                )?;
                emit_resource_ir(output, other, false, None)?;
                output.write_raw(")", false)?
            }
        },
        ResourceIr::Sub(parts) => {
            output.write_raw("`", lead_indent)?;
            for part in parts {
                match part {
                    ResourceIr::String(lit) => output.write_raw(lit, false)?,
                    other => {
                        output.write_raw("${", false)?;
                        emit_resource_ir(output, other, false, None)?;
                        output.write_raw("}", false)?;
                    }
                }
            }
            output.write_raw("`", false)?
        }

        // References
        ResourceIr::Ref(reference) => output.write_raw(&reference.synthesize(), lead_indent)?,
    }

    if let Some(trailer) = trailer {
        output.write_raw_line(trailer, false)
    } else {
        Ok(())
    }
}

fn emit_mappings(output: &mut CodeSink, mappings: &[MappingInstruction]) -> io::Result<()> {
    output.blank_line()?;
    output.write_line("// Mappings")?;

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

        output.write_line(&format!(
            "const {var}: Record<string, Record<string, {item_type}>> = {{",
            var = pretty_name(&mapping.name)
        ))?;
        emit_mapping_instruction(output.indented(), mapping)?;
        output.write_line("};")?;
    }

    Ok(())
}

fn synthesize_condition_recursive(val: &ConditionIr) -> String {
    match val {
        ConditionIr::And(x) => {
            let a: Vec<String> = x.iter().map(synthesize_condition_recursive).collect();

            let inner = a.join(" && ");
            format!("({inner})")
        }
        ConditionIr::Equals(a, b) => {
            format!(
                "{} === {}",
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

            let inner = a.join(" || ");
            format!("({inner})")
        }
        ConditionIr::Str(x) => {
            format!("'{x}'")
        }
        ConditionIr::Ref(x) => x.synthesize(),
        ConditionIr::Map(named_resource, l1, l2) => {
            let name = match named_resource.as_ref() {
                ConditionIr::Str(x) => pretty_name(x),
                &_ => synthesize_condition_recursive(named_resource.as_ref()),
            };

            format!(
                "{}[{}][{}]",
                name,
                synthesize_condition_recursive(l1.as_ref()),
                synthesize_condition_recursive(l2.as_ref())
            )
        }
    }
}

fn emit_mapping_instruction(
    mut output: CodeSink,
    mapping_instruction: &MappingInstruction,
) -> io::Result<()> {
    for (name, inner_mapping) in &mapping_instruction.map {
        output.write_line(&format!("'{key}': {{", key = name.escape_debug()))?;
        emit_inner_mapping(output.indented(), inner_mapping)?;
        output.write_line("},")?;
    }
    Ok(())
}

fn emit_inner_mapping(
    mut output: CodeSink,
    inner_mapping: &IndexMap<String, MappingInnerValue>,
) -> io::Result<()> {
    for (name, value) in inner_mapping {
        output.write_line(&format!("'{key}': {value},", key = name.escape_debug()))?;
    }
    Ok(())
}

fn append_references(output: &mut CodeSink, reference: &ResourceInstruction) -> io::Result<()> {
    if !reference.referrers.is_empty() {
        for dep in &reference.referrers {
            output.write_line(&format!("if ({dep} == null) {{ throw new Error(`A combination of conditions caused '{dep}' to be undefined. Fixit.`); }}", dep=pretty_name(dep)))?;
        }
    }
    Ok(())
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

#[cfg(test)]
mod tests;
