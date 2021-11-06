use crate::ir::conditions::ConditionIr;
use crate::ir::mappings::MappingInstruction;
use crate::ir::reference::Origin;
use crate::ir::reference::PseudoParameter;
use crate::ir::CloudformationProgramIr;
use crate::parser::lookup_table::MappingInnerValue;
use crate::parser::resource::ResourceValue;
use crate::parser::sub::{sub_parse_tree, SubValue};
use crate::CloudformationParseTree;
use std::collections::HashMap;
use voca_rs::case::camel_case;


pub struct TypescriptSynthesizer {
    // TODO: Put options in here for different outputs in typescript
}

impl TypescriptSynthesizer {
    // TODO - remove parse_tree
    pub fn output(parse_tree: CloudformationParseTree, ir: CloudformationProgramIr) {
        for import in ir.imports {
            println!(
                "import * as {} from '{}';",
                import.name,
                import.path.join("/")
            )
        }

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
        for reference in parse_tree.resources.resources.iter() {
            let mut split_ref = reference.resource_type.split("::");
            split_ref.next();
            let service = split_ref.next().unwrap().to_ascii_lowercase();
            let rtype = split_ref.next().unwrap();
            println!(
                "let {} = new {}.Cfn{}(this, '{}', {{",
                camel_case(&reference.name),
                service,
                rtype,
                reference.name
            );
            for (name, prop) in reference.properties.iter() {
                match to_string(prop) {
                    None => {}
                    Some(x) => {
                        println!("\t{}:{},", camel_case(name), x);
                    }
                }
            }
            println!("}});");
        }

        println!("\t}}");
        println!("}}");
    }
}
pub fn to_string(resource_value: &ResourceValue) -> Option<String> {
    match resource_value {
        ResourceValue::Null => Option::None,
        ResourceValue::Bool(b) => Option::Some(b.to_string()),
        ResourceValue::Number(n) => Option::Some(n.to_string()),
        ResourceValue::String(s) => Option::Some(format!("\"{}\"", s)),
        ResourceValue::Array(arr) => {
            let mut v = Vec::new();
            for a in arr {
                match to_string(a) {
                    None => {}
                    Some(s) => v.push(s),
                }
            }

            Option::Some(format!("[{}]", v.join(",\n")))
        }
        ResourceValue::Object(o) => {
            // We are transforming to typescript-json which will not have quotes.
            let mut v = Vec::new();
            for (s, rv) in o {
                match to_string(rv) {
                    None => {}
                    Some(r) => {
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
        ResourceValue::Sub(arr) => {
            // Sub has two ways of being built: Either resolution via a bunch of objects
            // or everything is in the first sub element, and that's it.
            // just resolve the objects.
            let val = to_string(&arr[0]).unwrap();

            let mut excess_map = HashMap::new();
            if arr.len() > 1 {
                let mut iter = arr.iter();
                iter.next();

                for obj in iter {
                    match obj {
                        ResourceValue::Object(obj) => {
                            for (key, val) in obj.iter() {
                                let val_str = to_string(val).unwrap();
                                excess_map.insert(key.to_string(), val_str);
                            }
                        }
                        _ => {
                            // these aren't possible, so panic
                            panic!("Isn't possible condition")
                        }
                    }
                }
            }
            let vars = sub_parse_tree(val.as_str()).unwrap();
            let r: Vec<String> = vars
                .iter()
                .map(|x| match x {
                    SubValue::String(x) => x.to_string(),
                    SubValue::Variable(x) => match x.as_str() {
                        "AWS::Region" => String::from("${this.region}"),
                        "AWS::Partition" => String::from("${this.partition}"),
                        "AWS::AccountId" => String::from("${this.account}"),
                        "AWS::StackId" => String::from("${this.stackId}"),
                        "AWS::StackName" => String::from("${this.stackName}"),
                        "AWS::URLSuffix" => String::from("${this.urlSuffix}"),

                        x => match excess_map.get(x) {
                            None => {
                                format!("${{props.{}}}", camel_case(x))
                            }
                            Some(x) => {
                                format!("${{{}}}", x)
                            }
                        },
                    },
                })
                .collect();

            Option::Some(format!("`{}`", r.join("")))
        }
        ResourceValue::FindInMap(mapper, first, second) => {
            let a: &ResourceValue = mapper.as_ref();
            let mapper_str = match a {
                ResourceValue::String(x) => camel_case(x),
                &_ => to_string(mapper).unwrap(),
            };
            let first_str = to_string(first).unwrap();
            let second_str = to_string(second).unwrap();

            Option::Some(format!("{}[{}][{}]", mapper_str, first_str, second_str))
        }
        ResourceValue::GetAtt(name, attribute) => {
            let name: &ResourceValue = name.as_ref();
            let attribute: &ResourceValue = attribute.as_ref();
            let resource_name = match name {
                ResourceValue::String(x) => x,
                _ => panic!("Can't happen"),
            };
            let attr_name = match attribute {
                ResourceValue::String(x) => x,
                _ => panic!("Can't happen"),
            };

            Option::Some(format!("{}.attr{}", camel_case(resource_name), attr_name))
        }
        ResourceValue::If(bool_expr, true_expr, false_expr) => {
            let bool_expr = to_string(bool_expr).unwrap();
            let bool_expr = bool_expr
                .strip_suffix('\"')
                .unwrap()
                .strip_prefix('\"')
                .unwrap();

            let bool_expr = camel_case(bool_expr);
            let true_expr = match to_string(true_expr) {
                None => String::from("{}"),
                Some(x) => x,
            };

            let false_expr = match to_string(false_expr) {
                None => String::from("{}"),
                Some(x) => x,
            };

            Option::Some(format!("({})?{}:{}", bool_expr, true_expr, false_expr))
        }
        ResourceValue::Join(x) => {
            let sep = x.get(0).unwrap();

            let sep = match sep {
                ResourceValue::String(x) => x,
                _ => panic!("Can't happen"),
            };

            let iterator = x.iter().skip(1);

            let mut strs = Vec::new();
            for rv in iterator {
                match to_string(rv) {
                    None => {}
                    Some(x_str) => strs.push(x_str),
                }
            }

            Option::Some(format!("{}.join(\"{}\")", strs.join(","), sep))
        }
        ResourceValue::Ref(x) => match x.as_str() {
            "AWS::Region" => Option::Some(String::from("this.region")),
            "AWS::Partition" => Option::Some(String::from("this.partition")),
            "AWS::AccountId" => Option::Some(String::from("this.account")),
            "AWS::StackId" => Option::Some(String::from("this.stackId")),
            "AWS::StackName" => Option::Some(String::from("this.stackName")),
            "AWS::URLSuffix" => Option::Some(String::from("this.urlSuffix")),
            x => Option::Some(format!("props.{}", camel_case(x))),
        },
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
        ConditionIr::Ref(x) => match &x.origin {
            Origin::Parameter => {
                format!("props.{}", camel_case(&x.name))
            }
            Origin::LogicalId => camel_case(&x.name),
            Origin::Condition => camel_case(&x.name),
            Origin::PseudoParameter(x) => match x {
                PseudoParameter::Partition => String::from("this.partition"),
                PseudoParameter::Region => String::from("this.region"),
                PseudoParameter::StackId => String::from("this.stackId"),
                PseudoParameter::StackName => String::from("this.stackName"),
                PseudoParameter::URLSuffix => String::from("this.urlSuffix"),
            },
        },
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
