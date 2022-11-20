use crate::ir::conditions::ConditionIr;
use crate::ir::mappings::{MappingInstruction, OutputType};
use crate::ir::resources::ResourceIr;
use crate::ir::CloudformationProgramIr;
use crate::parser::lookup_table::MappingInnerValue;
use crate::specification::Structure;
use std::collections::HashMap;
use voca_rs::case::camel_case;

pub struct TypescriptSynthesizer {
    // TODO: Put options in here for different outputs in typescript
}

impl TypescriptSynthesizer {
    pub fn output(ir: CloudformationProgramIr) -> String {
        let output = &mut String::new();

        for import in ir.imports {
            append_with_newline(
                output,
                &format!(
                    "import * as {} from '{}';",
                    import.name,
                    import.path.join("/")
                ),
            );
        }
        // Static imports with base assumptions (e.g. using base 64)
        append_with_newline(output, "import {Buffer} from 'buffer';");
        append_with_newline(output, "\n// Interfaces");
        append_with_newline(
            output,
            "export interface NoctStackProps extends cdk.StackProps {",
        );

        for param in ir.constructor.inputs {
            append_with_newline(
                output,
                &format!(
                    "\treadonly {}: {};",
                    pretty_name(&param.name),
                    pretty_name(&param.constructor_type)
                ),
            );
        }

        append_with_newline(output, "}");
        append_with_newline(output, "\n// Stack");
        append_with_newline(output, "export class NoctStack extends cdk.Stack {");
        append_with_newline(
            output,
            "\tconstructor(scope: cdk.App, id: string, props: NoctStackProps) {",
        );
        append_with_newline(output, "\t\tsuper(scope, id, props);");
        append_with_newline(output, "\n\t\t// Mappings");

        for mapping in ir.mappings.iter() {
            let record_type = match mapping.output_type() {
                OutputType::Consistent(inner_type) => match inner_type {
                    MappingInnerValue::Number(_) | MappingInnerValue::Float(_) => {
                        "Record<string, Record<string, number>>"
                    }
                    MappingInnerValue::Bool(_) => "Record<string, Record<string, bool>>",
                    MappingInnerValue::String(_) => "Record<string, Record<string, string>>",
                    MappingInnerValue::List(_) => "Record<string, Record<string, Array<string>>>",
                },
                OutputType::Complex => "Record<string, Record<string, any>>",
            };

            append_with_newline(
                output,
                &format!(
                    "\t\tconst {}: {} = {};",
                    pretty_name(&mapping.name),
                    record_type,
                    synthesize_mapping_instruction(mapping),
                ),
            );
        }

        append_with_newline(output, "\n\t\t// Conditions");

        for cond in ir.conditions {
            let synthed = synthesize_condition_recursive(&cond.value);

            append_with_newline(
                output,
                &format!("\t\tconst {} = {};", pretty_name(&cond.name), synthed),
            );
        }

        append_with_newline(output, "\n\t\t// Resources");

        for reference in ir.resources.iter() {
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

            if let Some(x) = &reference.condition {
                append_with_newline(
                    output,
                    &format!("\t\tlet {};", pretty_name(&reference.name)),
                );
                append_with_newline(output, &format!("\t\tif ({}) {{", pretty_name(x)));
                append_with_newline(
                    output,
                    &format!(
                        "\t\t{} = new {}.Cfn{}(this, '{}', {{",
                        pretty_name(&reference.name),
                        service,
                        rtype,
                        reference.name,
                    ),
                );
            } else {
                append_with_newline(
                    output,
                    &format!(
                        "\t\tconst {} = new {}.Cfn{}(this, '{}', {{",
                        pretty_name(&reference.name),
                        service,
                        rtype,
                        reference.name,
                    ),
                );
            }

            for (i, (name, prop)) in reference.properties.iter().enumerate() {
                match to_string_ir(prop) {
                    None => {}
                    Some(x) => {
                        append_with_newline(
                            output,
                            &format!(
                                "{}: {}{}",
                                pretty_name(name),
                                x,
                                match i {
                                    // Remove trailing comma.
                                    x if x == reference.properties.len() - 1 => "",
                                    _ => ",",
                                }
                            ),
                        );
                    }
                }
            }

            append_with_newline(output, "\t\t});");

            if let Some(metadata) = &reference.metadata {
                append_with_newline(
                    output,
                    &format!("{}.addOverride('Metadata', ", pretty_name(&reference.name)),
                );

                match to_string_ir(metadata) {
                    None => panic!("This should never fail"),
                    Some(x) => {
                        append_with_newline(output, &x.to_string());
                    }
                };

                append_with_newline(output, ");");
            }

            if let Some(update_policy) = &reference.update_policy {
                append_with_newline(
                    output,
                    &format!(
                        "{}.addOverride('UpdatePolicy', ",
                        pretty_name(&reference.name),
                    ),
                );

                match to_string_ir(update_policy) {
                    None => panic!("This should never fail"),
                    Some(x) => {
                        append_with_newline(output, &x.to_string());
                    }
                };

                append_with_newline(output, ");");
            }

            if let Some(deletion_policy) = &reference.deletion_policy {
                append_with_newline(
                    output,
                    &format!(
                        "{}.addOverride('DeletionPolicy', '{}');",
                        pretty_name(&reference.name),
                        deletion_policy,
                    ),
                );
            }

            if !reference.dependencies.is_empty() {
                append_with_newline(
                    output,
                    &format!(
                        "{}.addOverride('DependsOn', [",
                        pretty_name(&reference.name)
                    ),
                );

                let x: Vec<String> = reference
                    .dependencies
                    .iter()
                    .map(|x| format!("'{}'", x))
                    .collect();

                append_with_newline(output, &x.join(",").to_string());
                append_with_newline(output, "]);");
            }

            if let Some(_x) = &reference.condition {
                append_with_newline(output, "}")
            }
        }

        append_with_newline(output, "\n\t\t// Outputs");

        for op in ir.outputs {
            append_with_newline(
                output,
                &format!("new cdk.CfnOutput(this, '{}', {{", op.name),
            );

            let export_str = op.export.and_then(|x| to_string_ir(&x));

            if let Some(export) = export_str {
                append_with_newline(output, &format!("\texportName: {},", export));
            }

            match to_string_ir(&op.value) {
                None => {
                    panic!("Can't happen")
                }
                Some(x) => {
                    append_with_newline(output, &format!("\tvalue: {}", x));
                }
            }

            append_with_newline(output, "});");
        }

        append_with_newline(output, "\t}");
        append_with_newline(
            output,
            "function assertDefined(name: string, x: any): asserts x is NonNullable<any> {
  if (x === undefined) {
    throw new Error(`A combination of conditions caused '${name}' to be undefined. Fixit.`);
  }
}",
        );
        append_with_newline(output, "}");

        output.to_string()
    }
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
            Option::Some(format!("'{}'", formatted_str))
        }
        ResourceIr::Array(_, arr) => {
            let mut v = Vec::new();
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
            let mut v = Vec::new();
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
                            v.push(format!("{}: {}", s, r));
                        } else {
                            v.push(format!("'{}': {}", s, r));
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
            let mut r = Vec::new();
            for i in arr.iter() {
                match i {
                    ResourceIr::String(s) => r.push(s.to_string()),
                    &_ => r.push(format!("${{{}}}", to_string_ir(i).unwrap())),
                };
            }
            Option::Some(format!("`{}`", r.join("")))
        }
        ResourceIr::Map(mapper, first, second) => {
            let a: &ResourceIr = mapper.as_ref();
            let mapper_str = match a {
                ResourceIr::String(x) => pretty_name(x),
                &_ => to_string_ir(mapper).unwrap(),
            };
            let first_str = to_string_ir(first).unwrap();
            let second_str = to_string_ir(second).unwrap();

            Option::Some(format!("{}[{}][{}]", mapper_str, first_str, second_str))
        }
        ResourceIr::If(bool_expr, true_expr, false_expr) => {
            let bool_expr = pretty_name(bool_expr);
            let true_expr = match to_string_ir(true_expr) {
                None => String::from("{}"),
                Some(x) => x,
            };
            let false_expr = match to_string_ir(false_expr) {
                // Convert to undefined to avoid type mismatch errors. This works for most cases but
                // not all, e.g., Type 'undefined' is not assignable to type 'IResolvable | PolicyProperty'.
                // As of now, the user should manually fix when still seeing type mismatch errors.
                None => String::from("undefined"),
                Some(x) => x,
            };

            Option::Some(format!("{} ? {} : {}", bool_expr, true_expr, false_expr))
        }
        ResourceIr::Join(sep, join_obj) => {
            let mut strs = Vec::new();
            for rv in join_obj.iter() {
                match to_string_ir(rv) {
                    None => {}
                    Some(x_str) => strs.push(x_str),
                }
            }

            Option::Some(format!("{}.join('{}')", strs.join(","), sep.escape_debug()))
        }
        ResourceIr::Ref(x) => Option::Some(x.synthesize()),
        ResourceIr::Base64(x) => {
            let str = to_string_ir(x.as_ref()).unwrap();
            Option::Some(format!("Buffer.from({}).toString('base64')", str))
        }
        ResourceIr::ImportValue(x) => {
            let str = to_string_ir(x.as_ref()).unwrap();
            Option::Some(format!("cdk.Fn.importValue({})", str))
        }
        ResourceIr::GetAZs(x) => {
            let str = to_string_ir(x.as_ref()).unwrap();
            // This means it's just a ""
            if str.len() == 2 {
                return Option::Some("cdk.Fn.getAzs()".to_string());
            }
            Option::Some(format!("cdk.Fn.getAzs({})", str))
        }
        ResourceIr::Select(index, obj) => {
            let str = to_string_ir(obj.as_ref()).unwrap();
            Option::Some(format!("{}[{}]", str, *index))
        }
    }
}

fn synthesize_condition_recursive(val: &ConditionIr) -> String {
    match val {
        ConditionIr::And(x) => {
            let a: Vec<String> = x.iter().map(synthesize_condition_recursive).collect();

            let inner = a.join(" && ");
            format!("({})", inner)
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
            format!("({})", inner)
        }
        ConditionIr::Str(x) => {
            format!("'{}'", x)
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

fn synthesize_mapping_instruction(mapping_instruction: &MappingInstruction) -> String {
    let mut mapping_parse_tree_ts = String::from("{\n");
    let mut outer_records = Vec::new();
    for (outer_mapping_key, inner_mapping) in mapping_instruction.map.iter() {
        outer_records.push(format!(
            "\t\t\t'{}': {}",
            outer_mapping_key,
            synthesize_inner_mapping(inner_mapping)
        ));
    }

    let outer = outer_records.join(",\n");
    mapping_parse_tree_ts.push_str(&outer);
    mapping_parse_tree_ts.push_str("\n\t\t}");
    mapping_parse_tree_ts
}

fn synthesize_inner_mapping(inner_mapping: &HashMap<String, MappingInnerValue>) -> String {
    let mut inner_mapping_ts_str = String::from("{\n");
    let mut inner_mapping_entries = Vec::new();
    for (inner_mapping_key, inner_mapping_value) in inner_mapping {
        inner_mapping_entries.push(format!(
            "\t\t\t\t'{}': {}",
            inner_mapping_key, inner_mapping_value
        ));
    }
    inner_mapping_ts_str.push_str(&inner_mapping_entries.join(",\n"));
    inner_mapping_ts_str.push_str("\n\t\t\t}");
    inner_mapping_ts_str
}

fn append_with_newline(result: &mut String, string: &str) {
    String::push_str(result, &format!("{}\n", string));
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

#[test]
fn pretty_name_fixes() {
    assert_eq!("vpc", pretty_name("VPC"));
    assert_eq!("objectAccess", pretty_name("GetObject"));
    assert_eq!("equalTo", pretty_name("Equals"));
    assert_eq!("providerArns", pretty_name("ProviderARNs"));
    assert_eq!("targetAZs", pretty_name("TargetAZs"));
    assert_eq!("diskSizeMBs", pretty_name("DiskSizeMBs"));
}
