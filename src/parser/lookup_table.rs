use crate::TransmuteError;
use serde_json::{Map, Value};
use std::collections::HashMap;

#[derive(Debug)]
pub struct MappingsParseTree {
    pub mappings: HashMap<String, HashMap<String, HashMap<String, MappingInnerValue>>>,
}

#[derive(Debug)]
pub enum MappingInnerValue {
    String(String),
    List(Vec<String>),
}

pub fn build_mappings(vals: &Map<String, Value>) -> Result<MappingsParseTree, TransmuteError> {
    let mut mappings = MappingsParseTree {
        mappings: HashMap::new(),
    };
    for (name, obj) in vals {
        let outer_mapping = build_outer_mapping(name, obj)?;
        mappings.mappings.insert(name.clone(), outer_mapping);
    }
    Ok(mappings)
}

fn build_outer_mapping(name: &str, obj: &Value) -> Result<HashMap<String, HashMap<String, MappingInnerValue>>, TransmuteError> {
    let val = match obj {
        Value::Object(x) => x,
        _ => {
            return Err(TransmuteError {
                details: format!("Mapping must be an object {}, {:?}", name, obj),
            })
        }
    };

    let mut outer_mapping: HashMap<String, HashMap<String, MappingInnerValue>> = HashMap::new();
    #[allow(clippy::never_loop)]
    for (outer_key, inner_mapping_obj) in val {
        let inner_mapping = build_inner_mapping(outer_key, inner_mapping_obj)?;
        outer_mapping.insert(outer_key.clone(), inner_mapping);
    }
    return Ok(outer_mapping);
}

fn build_inner_mapping(name: &str, obj: &Value) -> Result<HashMap<String, MappingInnerValue>, TransmuteError> {
    let val = match obj {
        Value::Object(x) => x,
        _ => {
            return Err(TransmuteError {
                details: format!("Mapping must be an object. Found {}, {:?}", name, obj),
            })
        }
    };

    let mut inner_mapping: HashMap<String, MappingInnerValue> = HashMap::new();
    #[allow(clippy::never_loop)]
    for (inner_key, inner_mapping_obj) in val {
        let val  = match inner_mapping_obj {
            Value::String(x) => MappingInnerValue::String(x.to_string()),
            Value::Number(x) => MappingInnerValue::String(x.to_string()),
            Value::Array(x) => MappingInnerValue::List(convert_to_string_vector(x, inner_key)?),
            _ => {
                return Err(TransmuteError {
                    details: format!("Inner mapping value must be a string or array. Found {:?}, for {}", name, inner_mapping_obj),
                })
            }
        };

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



