use crate::parser::resource::ResourceValue;
use crate::parser::sub::{sub_parse_tree, SubValue};
use crate::semantic::reference::ReferenceTable;
use std::collections::HashMap;

pub mod importer;
pub mod reference;

pub fn to_string(resource_value: &ResourceValue, ref_table: &ReferenceTable) -> Option<String> {
    match resource_value {
        ResourceValue::Null => Option::None,
        ResourceValue::Bool(b) => Option::Some(b.to_string()),
        ResourceValue::Number(n) => Option::Some(n.to_string()),
        ResourceValue::String(s) => Option::Some(format!("\"{}\"", s)),
        ResourceValue::Array(arr) => {
            let mut v = Vec::new();
            for a in arr {
                match to_string(a, ref_table) {
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
                match to_string(rv, ref_table) {
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
            let val = to_string(&arr[0], ref_table).unwrap();

            let mut excess_map = HashMap::new();
            if arr.len() > 1 {
                let mut iter = arr.iter();
                iter.next();

                for obj in iter {
                    match obj {
                        ResourceValue::Object(obj) => {
                            for (key, val) in obj.iter() {
                                let val_str = to_string(val, ref_table).unwrap();
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
                        x => match excess_map.get(x) {
                            None => {
                                format!("${{props.{}}}", x)
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
                ResourceValue::String(x) => x.to_string(),
                &_ => to_string(mapper, ref_table).unwrap(),
            };
            let first_str = to_string(first, ref_table).unwrap();
            let second_str = to_string(second, ref_table).unwrap();

            Option::Some(format!("{}[{}][{}]", mapper_str, first_str, second_str))
        }
        ResourceValue::GetAtt(_, _) => Option::None,
        ResourceValue::If(bool_expr, true_expr, false_expr) => {
            let bool_expr = to_string(bool_expr, ref_table).unwrap();
            let bool_expr = bool_expr
                .strip_suffix('\"')
                .unwrap()
                .strip_prefix('\"')
                .unwrap();
            let true_expr = to_string(true_expr, ref_table).unwrap();
            let false_expr = match to_string(false_expr, ref_table) {
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
                match to_string(rv, ref_table) {
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
            x => Option::Some(format!("props.{}", x)),
        },
    }
}
