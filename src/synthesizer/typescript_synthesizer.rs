use crate::ir::conditions::ConditionIr;
use crate::ir::mappings::{MappingInstruction, OutputType};
use crate::ir::outputs::OutputInstruction;
use crate::ir::resources::{ResourceInstruction, ResourceIr};
use crate::ir::CloudformationProgramIr;
use crate::parser::lookup_table::MappingInnerValue;
use crate::specification::Structure;
use indexmap::IndexMap;
use std::collections::HashMap;
use std::io;
use voca_rs::case::camel_case;

use super::output::CodeSink;
use super::Synthesizer;

pub struct TypescriptSynthesizer {
    // TODO: Put options in here for different outputs in typescript
}

impl TypescriptSynthesizer {
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
                        let val = to_string_ir(&op.value)
                            .unwrap_or_else(|| format!("undefined as any /* {:?} */", &op.value));

                        let cond = op.condition.as_ref().map(|s| pretty_name(s));

                        if let Some(cond) = &cond {
                            output.write_line(&format!(
                                "this.{var_name} = {cond}",
                                cond = pretty_name(cond)
                            ))?;
                            let output = &mut output.indented();
                            output.write_line(&format!("? {val}"))?;
                            output.write_line(": undefined;")?;
                        } else {
                            output.write_line(&format!("this.{var_name} = {val};"))?;
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
    props.write_line(&format!(
        "exportName: {},",
        to_string_ir(export).unwrap_or_else(|| format!("undefined /* {export:?} */"))
    ))?;
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
        output.write_line(&format!("{var_name}.cfnOptions.updatePolicy ="))?;

        if let Some(code) = to_string_ir(update_policy) {
            output.write_text(&code)?;
        };

        output.write_line(";")?;
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
                output.write_line(&format!(
                    "{name}: {},",
                    to_string_ir(value)
                        .unwrap_or_else(|| format!("undefined as any /* {value:?} */"))
                ))?;
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
        output.write_line(&format!(
            "{prop}: {val},",
            prop = pretty_name(name),
            val = to_string_ir(prop).unwrap_or_else(|| format!("undefined as any /* {prop:?} */"))
        ))?;
    }
    Ok(())
}

// The indent generated by this method is not perfect. You have to copy the generated code to an IDE
// and use IDE to format.
pub fn to_string_ir(resource_value: &ResourceIr) -> Option<String> {
    match resource_value {
        ResourceIr::Null => Option::None,
        ResourceIr::Bool(b) => Option::Some(b.to_string()),
        ResourceIr::Number(n) => Option::Some(n.to_string()),
        ResourceIr::Double(d) => Option::Some(d.to_string()),
        ResourceIr::String(s) => {
            let formatted_str = s.replace("\\'", "'");
            let formatted_str = formatted_str.escape_debug();
            Option::Some(format!("'{formatted_str}'"))
        }
        ResourceIr::Array(_, arr) => {
            let mut v = Vec::with_capacity(arr.len());
            for a in arr {
                match to_string_ir(a) {
                    None => {}
                    Some(s) => v.push(s),
                }
            }

            Option::Some(format!("[\n{}\n]", v.join(",\n")))
        }
        ResourceIr::Object(complexity, o) => {
            // We are transforming to typescript-json which will not have quotes.
            let mut v = Vec::with_capacity(o.len());
            for (s, rv) in o {
                match to_string_ir(rv) {
                    None => {}
                    Some(r) => {
                        // If a type is composite, all it's properties will be camel-case in cdk-ts.
                        // simple types, even nested json, will have all characters preserved.
                        let s = match complexity {
                            Structure::Simple(_) => s.to_string(),
                            Structure::Composite(_) => pretty_name(s),
                        };
                        if s.chars().all(char::is_alphanumeric) && !s.starts_with(char::is_numeric)
                        {
                            v.push(format!("{s}: {r}"));
                        } else {
                            v.push(format!("'{s}': {r}"));
                        }
                    }
                }
            }

            Option::Some(format!("{{\n{}\n}}", v.join(",\n")))
        }
        ResourceIr::Sub(arr) => {
            // Sub has two ways of being built: Either resolution via a bunch of objects
            // or everything is in the first sub element, and that's it.
            // just resolve the objects.
            let mut r = Vec::with_capacity(arr.len());
            for i in arr.iter() {
                match i {
                    ResourceIr::String(s) => {
                        // Since we are changing the output strings to use ticks for typescript sugar syntax,
                        // we need to escape the ticks that already exist.
                        let _replaced = s.replace('`', "\\`");
                        let _replaced = s.replace('{', "\\{`");
                        let replaced = s.replace('}', "\\}`");
                        r.push(replaced.to_string())
                    }
                    &_ => r.push(format!("${{{}}}", to_string_ir(i).unwrap())),
                };
            }
            let full_text = r.join("");
            Option::Some(format!("`{full_text}`"))
        }
        ResourceIr::Map(mapper, first, second) => {
            let a: &ResourceIr = mapper.as_ref();
            let mapper_str = match a {
                ResourceIr::String(x) => pretty_name(x),
                &_ => to_string_ir(mapper).unwrap(),
            };
            let first_str = to_string_ir(first).unwrap();
            let second_str = to_string_ir(second).unwrap();

            Option::Some(format!("{mapper_str}[{first_str}][{second_str}]"))
        }
        ResourceIr::If(bool_expr, true_expr, false_expr) => {
            let bool_expr = pretty_name(bool_expr);
            let true_expr = match to_string_ir(true_expr) {
                None => String::from("undefined"),
                Some(x) => x,
            };
            let false_expr = match to_string_ir(false_expr) {
                // Convert to undefined to avoid type mismatch errors. This works for most cases but
                // not all, e.g., Type 'undefined' is not assignable to type 'IResolvable | PolicyProperty'.
                // As of now, the user should manually fix when still seeing type mismatch errors.
                None => String::from("undefined"),
                Some(x) => x,
            };

            Option::Some(format!("{bool_expr} ? {true_expr} : {false_expr}"))
        }
        ResourceIr::Join(sep, join_obj) => {
            let mut strs = Vec::with_capacity(join_obj.len());
            for rv in join_obj.iter() {
                match to_string_ir(rv) {
                    None => {}
                    Some(x_str) => strs.push(x_str),
                }
            }

            Option::Some(format!(
                "[{}].join('{}')",
                strs.join(", "),
                sep.escape_debug()
            ))
        }
        ResourceIr::Split(sep, ir) => Option::Some(format!(
            "cdk.Fn.split({sep:?}, {})",
            to_string_ir(ir).unwrap()
        )),
        ResourceIr::Ref(x) => Option::Some(x.synthesize()),
        ResourceIr::Base64(x) => {
            let str = to_string_ir(x.as_ref()).unwrap();
            Option::Some(format!("Buffer.from({str}).toString('base64')"))
        }
        ResourceIr::ImportValue(x) => {
            let str = to_string_ir(x.as_ref()).unwrap();
            Option::Some(format!("cdk.Fn.importValue({str})"))
        }
        ResourceIr::GetAZs(x) => {
            let str = to_string_ir(x.as_ref()).unwrap();
            // This means it's just a ""
            if str.len() == 2 {
                return Option::Some("cdk.Fn.getAzs()".to_string());
            }
            Option::Some(format!("cdk.Fn.getAzs({str})"))
        }
        ResourceIr::Select(index, obj) => {
            let str = to_string_ir(obj.as_ref()).unwrap();
            match obj as &ResourceIr {
                ResourceIr::GetAZs(_) => {
                    Option::Some(format!("cdk.Fn.select({}, {})", *index, str))
                }
                _ => Option::Some(format!("{}[{}]", str, *index)),
            }
        }
        ResourceIr::Cidr(ip_block, count, cidr_bits) => {
            let ip_block_str = to_string_ir(ip_block.as_ref()).unwrap();
            let count_str = to_string_ir(count.as_ref()).unwrap();
            let cidr_bits_str = to_string_ir(cidr_bits.as_ref()).unwrap();
            Option::Some(format!(
                "cdk.Fn.cidr({ip_block_str}, {count_str}, '{cidr_bits_str}')"
            ))
        }
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
        for dep in reference.referrers.iter() {
            output.write_line(&format!("if ({dep} === undefined) {{ throw new Error(`A combination of conditions caused '{dep}' to be undefined. Fixit.`); }}", dep=pretty_name(dep)))?;
        }
    }
    Ok(())
}

struct SuffixFix<'a> {
    suffix: &'a str,
    fix: &'a str,
}

/// If you have stumbled across this lunacy, I still don't fully understand it myself.
///
/// CDK folks decided to prettify a few names, e.g. ProviderARNs -> providerArns.
/// This list is hand-maintained, but always refer to the original source:
///
const SUFFIX_FIXES: &[SuffixFix] = &[
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
    for hay in SUFFIX_FIXES.iter() {
        if end_str.ends_with(hay.suffix) {
            let temp = end_str.strip_suffix(hay.suffix).unwrap();
            end_str = temp.to_string();
            end_str.push_str(hay.fix);
        }
    }

    camel_case(&end_str)
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn pretty_name_fixes() {
        assert_eq!("vpc", pretty_name("VPC"));
        assert_eq!("objectAccess", pretty_name("GetObject"));
        assert_eq!("equalTo", pretty_name("Equals"));
        assert_eq!("providerArns", pretty_name("ProviderARNs"));
        assert_eq!("targetAZs", pretty_name("TargetAZs"));
        assert_eq!("diskSizeMBs", pretty_name("DiskSizeMBs"));
    }
}
