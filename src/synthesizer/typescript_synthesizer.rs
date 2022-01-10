use crate::ir::conditions::ConditionIr;
use crate::ir::mappings::MappingInstruction;
use crate::ir::resources::ResourceIr;
use crate::ir::CloudformationProgramIr;
use crate::parser::lookup_table::MappingInnerValue;
use crate::specification::Complexity;
use std::collections::HashMap;
use voca_rs::case::camel_case;

pub struct TypescriptSynthesizer {
    // TODO: Put options in here for different outputs in typescript
}

impl TypescriptSynthesizer {
    pub fn output(ir: CloudformationProgramIr) {
        for import in ir.imports {
            println!(
                "import * as {} from '{}';",
                import.name,
                import.path.join("/")
            )
        }
        // Static imports with base assumptions (e.g. using base 64)
        println!("import {{Buffer}} from 'buffer';");

        println!("export interface NoctStackProps extends cdk.StackProps {{");
        for param in ir.constructor.inputs {
            println!(
                "\treadonly {}: {}",
                camel_case(&param.name),
                camel_case(&param.constructor_type)
            )
        }
        println!("}}");
        println!("export class NoctStack extends cdk.Stack {{");
        println!("\tconstructor(scope: cdk.App, id: string, props: NoctStackProps){{");
        println!("\t\tsuper(scope, id, props);");
        for mapping in ir.mappings.iter() {
            let record_type = match mapping.find_first_type() {
                MappingInnerValue::String(_) => "Record<string, Record<string, string>>",
                MappingInnerValue::List(_) => "Record<string, Record<string, Array<string>>>",
            };
            println!(
                "const {}: {} = {}",
                camel_case(&mapping.name),
                record_type,
                synthesize_mapping_instruction(mapping)
            );
        }

        for cond in ir.conditions {
            let synthed = synthesize_condition_recursive(&cond.value);
            println!("const {} = {};", camel_case(&cond.name), synthed)
        }

        for reference in ir.resources.iter() {
            let mut split_ref = reference.resource_type.split("::");
            split_ref.next();
            let service = split_ref.next().unwrap().to_ascii_lowercase();
            let rtype = split_ref.next().unwrap();

            if let Some(x) = &reference.condition {
                println!("if ({}){{", camel_case(x));
            }

            println!(
                "let {} = new {}.Cfn{}(this, '{}', {{",
                camel_case(&reference.name),
                service,
                rtype,
                reference.name
            );

            for (name, prop) in reference.properties.iter() {
                match to_string_ir(prop) {
                    None => {}
                    Some(x) => {
                        println!("\t{}:{},", camel_case(name), x);
                    }
                }
            }
            println!("}});");

            if let Some(metadata) = &reference.metadata {
                println!("{}.addOverride('Metadata', ", camel_case(&reference.name));
                match to_string_ir(metadata) {
                    None => panic!("This should never fail"),
                    Some(x) => {
                        println!("{}", x);
                    }
                };

                println!(");");
            }
            if let Some(update_policy) = &reference.update_policy {
                println!(
                    "{}.addOverride('UpdatePolicy', ",
                    camel_case(&reference.name)
                );
                match to_string_ir(update_policy) {
                    None => panic!("This should never fail"),
                    Some(x) => {
                        println!("{}", x);
                    }
                };
                println!(");");
            }

            if let Some(_x) = &reference.condition {
                println!("}}")
            }
        }

        for output in ir.outputs {
            println!("new cdk.CfnOutput(this, '{}', {{", output.name);

            let export_str = output.export.and_then(|x| to_string_ir(&x));
            if let Some(export) = export_str {
                println!("\texportName: {},", export);
            }
            match to_string_ir(&output.value) {
                None => {
                    panic!("Can't happen")
                }
                Some(x) => {
                    println!("\tvalue: {}", x);
                }
            }

            println!("}});");
        }

        println!("\t}}");
        println!("}}");
    }
}

pub fn to_string_ir(resource_value: &ResourceIr) -> Option<String> {
    match resource_value {
        ResourceIr::Null => Option::None,
        ResourceIr::Bool(b) => Option::Some(b.to_string()),
        ResourceIr::Number(n) => Option::Some(n.to_string()),
        ResourceIr::String(s) => Option::Some(format!("\'{}\'", s)),
        ResourceIr::Array(_, arr) => {
            let mut v = Vec::new();
            for a in arr {
                match to_string_ir(a) {
                    None => {}
                    Some(s) => v.push(s),
                }
            }

            Option::Some(format!("[{}]", v.join(",\n")))
        }
        ResourceIr::Object(complexity, o) => {
            // We are transforming to typescript-json which will not have quotes.
            let mut v = Vec::new();
            for (s, rv) in o {
                match to_string_ir(rv) {
                    None => {}
                    Some(r) => {
                        // If a type is complex, all it's properties will be camel-case in cdk-ts.
                        // simple types, even nested json, will have all characters preserved.
                        let s = match complexity {
                            Complexity::Simple(_) => s.to_string(),
                            Complexity::Complex(_) => camel_case(s),
                        };
                        if s.chars().all(char::is_alphanumeric) {
                            v.push(format!("{}: {}", s, r));
                        } else {
                            v.push(format!("\"{}\": {}", s, r));
                        }
                    }
                }
            }

            Option::Some(format!("{{{}}}", v.join(",\n")))
        }
        ResourceIr::Sub(arr) => {
            // Sub has two ways of being built: Either resolution via a bunch of objects
            // or everything is in the first sub element, and that's it.
            // just resolve the objects.
            let mut r = Vec::new();
            for i in arr.iter() {
                match i {
                    ResourceIr::String(s) => r.push(s.to_string()),
                    &_ => r.push(format!("${{ {} }}", to_string_ir(i).unwrap())),
                };
            }
            Option::Some(format!("`{}`", r.join("")))
        }
        ResourceIr::Map(mapper, first, second) => {
            let a: &ResourceIr = mapper.as_ref();
            let mapper_str = match a {
                ResourceIr::String(x) => camel_case(x),
                &_ => to_string_ir(mapper).unwrap(),
            };
            let first_str = to_string_ir(first).unwrap();
            let second_str = to_string_ir(second).unwrap();

            Option::Some(format!("{}[{}][{}]", mapper_str, first_str, second_str))
        }
        ResourceIr::If(bool_expr, true_expr, false_expr) => {
            let bool_expr = camel_case(bool_expr);
            let true_expr = match to_string_ir(true_expr) {
                None => String::from("{}"),
                Some(x) => x,
            };

            let false_expr = match to_string_ir(false_expr) {
                None => String::from("{}"),
                Some(x) => x,
            };

            Option::Some(format!("({})?{}:{}", bool_expr, true_expr, false_expr))
        }
        ResourceIr::Join(sep, join_obj) => {
            let mut strs = Vec::new();
            for rv in join_obj.iter() {
                match to_string_ir(rv) {
                    None => {}
                    Some(x_str) => strs.push(x_str),
                }
            }

            Option::Some(format!("{}.join(\"{}\")", strs.join(","), sep))
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

            let inner = a.join(" || ");
            format!("({})", inner)
        }
        ConditionIr::Str(x) => {
            format!("\"{}\"", x)
        }
        ConditionIr::Ref(x) => x.synthesize(),
        ConditionIr::Map(named_resource, l1, l2) => {
            let name = match named_resource.as_ref() {
                ConditionIr::Str(x) => camel_case(x),
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
            "\t\"{}\": {}",
            outer_mapping_key,
            synthesize_inner_mapping(inner_mapping)
        ));
    }

    let outer = outer_records.join(",\n");
    mapping_parse_tree_ts.push_str(&outer);
    mapping_parse_tree_ts.push_str("\n};\n");
    mapping_parse_tree_ts
}

fn synthesize_inner_mapping(inner_mapping: &HashMap<String, MappingInnerValue>) -> String {
    let mut inner_mapping_ts_str = String::from("{\n");
    let mut inner_mapping_entries = Vec::new();
    for (inner_mapping_key, inner_mapping_value) in inner_mapping {
        inner_mapping_entries.push(format!(
            "\t\t\"{}\": {}",
            inner_mapping_key, inner_mapping_value
        ));
    }
    inner_mapping_ts_str.push_str(&inner_mapping_entries.join(",\n"));
    inner_mapping_ts_str.push_str("\n\t}");
    inner_mapping_ts_str
}
