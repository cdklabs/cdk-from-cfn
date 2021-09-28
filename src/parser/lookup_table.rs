use crate::TransmuteError;
use serde_json::{Map, Value};
use std::collections::HashMap;
use std::fmt::{Display, Formatter};

#[derive(Debug)]
pub struct MappingsParseTree {
    pub mappings: HashMap<String, MappingParseTree>
}

impl MappingsParseTree {
    pub fn new() -> MappingsParseTree {
        return MappingsParseTree {
            mappings: HashMap::new()
        }
    }

    pub fn insert(&mut self, mapping_name: String, mapping: MappingParseTree) {
        self.mappings.insert(mapping_name, mapping);
    }

    pub fn synthesize(&self) -> String {
        let mut mappings_ts_str = String::new();
        for (mapping_name, mapping) in self.mappings.iter() {
            mappings_ts_str.push_str(&format!("const {} = {}", mapping_name, mapping.synthesize()));
        }
        return mappings_ts_str;
    }
}

#[derive(Debug)]
pub struct MappingParseTree {
    mappings: HashMap<String, HashMap<String, MappingInnerValue>>
}

impl MappingParseTree {
    fn new() -> MappingParseTree {
        return MappingParseTree {
            mappings: HashMap::new()
        }
    }

    fn insert(&mut self, outer_mapping_key: String, inner_mapping: HashMap<String, MappingInnerValue>) {
        self.mappings.insert(outer_mapping_key, inner_mapping);
    }

    fn synthesize(&self) -> String {
        let mut mapping_parse_tree_ts = String::new();
        mapping_parse_tree_ts.push_str(&format!("new Map(\n"));
        for (outer_mapping_key, inner_mapping) in self.mappings.iter() {
            mapping_parse_tree_ts.push_str(&format!("\t[{}\t],\n", synthesize_outer_mapping(outer_mapping_key, inner_mapping)));
        }
        mapping_parse_tree_ts.push_str(&format!(")\n"));
        return mapping_parse_tree_ts;
    }
}

fn synthesize_outer_mapping(outer_mapping_entry : &String, inner_mapping: &HashMap<String, MappingInnerValue>) -> String {
    format!("\"{}\", {}", outer_mapping_entry, synthesize_inner_mapping(inner_mapping))
}

fn synthesize_inner_mapping(inner_mapping: &HashMap<String, MappingInnerValue>) -> String {
    let mut inner_mapping_ts_str = String::from("new Map(\n");
    let mut inner_mapping_entries = Vec::new();
    for (inner_mapping_key, inner_mapping_value) in inner_mapping {
        inner_mapping_entries.push(format!("\t\t[\"{}\", {}]", inner_mapping_key, inner_mapping_value));
    }
    inner_mapping_ts_str.push_str(&inner_mapping_entries.join(",\n"));
    inner_mapping_ts_str.push_str(")\n");
    return inner_mapping_ts_str;
}

/**
 * MappingInnerValue tracks the allowed value types in a Mapping as defined by CloudFormation in the
 * link below. Right now that is either a String or List.
 *
 * https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html#mappings-section-structure-syntax
 */
#[derive(Debug)]
enum MappingInnerValue {
    String(String),
    List(Vec<String>),
}

impl Display for MappingInnerValue {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            MappingInnerValue::String(string_val) => {
                return write!(f, "\"{}\"", string_val);
            }
            MappingInnerValue::List(list_val) => {
                let quoted_list_values : Vec<String> = list_val.iter().map(|val| format!("\"{}\"", val)).collect();
                return write!(f, "[{}]", quoted_list_values.join(","));
            }
        }
    }
}

pub fn build_mappings(vals: &Map<String, Value>) -> Result<MappingsParseTree, TransmuteError> {
    let mut mappings = MappingsParseTree::new();
    for (name, obj) in vals {
        let outer_mapping = build_outer_mapping(name, obj)?;
        mappings.insert(name.clone(), outer_mapping);
    }
    Ok(mappings)
}

fn build_outer_mapping(name: &String, obj: &Value) -> Result<MappingParseTree, TransmuteError> {
    let val = ensure_object(name, obj)?;

    let mut outer_mapping: MappingParseTree = MappingParseTree::new();
    #[allow(clippy::never_loop)]
    for (outer_key, inner_mapping_obj) in val {
        let inner_mapping = build_inner_mapping(outer_key, inner_mapping_obj)?;
        outer_mapping.insert(outer_key.clone(), inner_mapping);
    }
    return Ok(outer_mapping);
}

fn build_inner_mapping(name: &String, obj: &Value) -> Result<HashMap<String, MappingInnerValue>, TransmuteError> {
    let val = ensure_object(name, obj)?;

    let mut inner_mapping: HashMap<String, MappingInnerValue> = HashMap::new();
    #[allow(clippy::never_loop)]
    for (inner_key, inner_mapping_obj) in val {
        let val  = ensure_mapping_value_type(inner_key, inner_mapping_obj)?;
        inner_mapping.insert(inner_key.clone(), val);
    }
    return Ok(inner_mapping);
}

fn convert_to_string_vector(json_vector: &Vec<Value>, inner_key: &String) -> Result<Vec<String>, TransmuteError> {
    let mut string_vector = Vec::new();
    for vector_val in json_vector {
        let converted_val = match vector_val {
            Value::String(x) => x.to_string(),
            Value::Number(x) => x.to_string(),
            _ => {
                return Err(TransmuteError {
                    details: format!("List values for mappings must be a string. Found {:?}, for key {}", inner_key, vector_val),
                })
            }
        };
        string_vector.push(converted_val);
    }
    return Ok(string_vector);
}

fn ensure_object<'a>(name: &String, obj: &'a Value) -> Result<&'a Map<String, Value>, TransmuteError> {
    return match obj {
        Value::Object(x) => Ok(x),
        _ => {
            Err(TransmuteError {
                details: format!("Mapping must be an object {}, {:?}", name, obj),
            })
        }
    };
}

fn ensure_mapping_value_type(name: &String, obj: &Value) -> Result<MappingInnerValue, TransmuteError> {
    return match obj {
        Value::String(x) => Ok(MappingInnerValue::String(x.to_string())),
        Value::Number(x) => Ok(MappingInnerValue::String(x.to_string())),
        Value::Array(x) => Ok(MappingInnerValue::List(convert_to_string_vector(x,  name)?)),
        _ => {
            Err(TransmuteError {
                details: format!("Inner mapping value must be a string or array. Found {:?}, for {}", name, obj),
            })
        }
    };
}



