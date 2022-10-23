use crate::primitives::WrapperF64;
use crate::TransmuteError;
use serde_json::{Map, Value};
use std::collections::HashMap;
use std::fmt::{Display, Formatter};

#[derive(Debug)]
pub struct MappingsParseTree {
    pub mappings: HashMap<String, MappingParseTree>,
}

impl Default for MappingsParseTree {
    fn default() -> Self {
        MappingsParseTree::new()
    }
}

impl MappingsParseTree {
    pub fn new() -> MappingsParseTree {
        MappingsParseTree {
            mappings: HashMap::new(),
        }
    }

    pub fn insert(&mut self, mapping_name: String, mapping: MappingParseTree) {
        self.mappings.insert(mapping_name, mapping);
    }
}

#[derive(Debug)]
pub struct MappingParseTree {
    pub mappings: HashMap<String, HashMap<String, MappingInnerValue>>,
}

impl MappingParseTree {
    fn new() -> MappingParseTree {
        MappingParseTree {
            mappings: HashMap::new(),
        }
    }

    fn insert(
        &mut self,
        outer_mapping_key: String,
        inner_mapping: HashMap<String, MappingInnerValue>,
    ) {
        self.mappings.insert(outer_mapping_key, inner_mapping);
    }
}

/**
 * MappingInnerValue tracks the allowed value types in a Mapping as defined by CloudFormation in the
 * link below. The values are allowed to only be a String or List:
 *
 * https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html#mappings-section-structure-syntax
 *
 * In reality, all values are allowed from the json specification. If we detect any other conflicting
 * numbers, then the type becomes "Any" to allow for the strangeness.
 */
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum MappingInnerValue {
    Number(i64),
    Float(WrapperF64),
    Bool(bool),
    String(String),
    List(Vec<String>),
}

impl Display for MappingInnerValue {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        return match self {
            MappingInnerValue::String(string_val) => write!(f, "'{}'", string_val),
            MappingInnerValue::List(list_val) => {
                let quoted_list_values: Vec<String> =
                    list_val.iter().map(|val| format!("'{}'", val)).collect();
                write!(f, "[{}]", quoted_list_values.join(","))
            }
            MappingInnerValue::Number(val) => write!(f, "{}", val),
            MappingInnerValue::Float(val) => write!(f, "{}", val),
            MappingInnerValue::Bool(val) => write!(f, "{}", val),
        };
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

fn build_outer_mapping(name: &str, obj: &Value) -> Result<MappingParseTree, TransmuteError> {
    let val = ensure_object(name, obj)?;

    let mut outer_mapping: MappingParseTree = MappingParseTree::new();
    #[allow(clippy::never_loop)]
    for (outer_key, inner_mapping_obj) in val {
        let inner_mapping = build_inner_mapping(outer_key, inner_mapping_obj)?;
        outer_mapping.insert(outer_key.clone(), inner_mapping);
    }
    Ok(outer_mapping)
}

fn build_inner_mapping(
    name: &str,
    obj: &Value,
) -> Result<HashMap<String, MappingInnerValue>, TransmuteError> {
    let val = ensure_object(name, obj)?;

    let mut inner_mapping: HashMap<String, MappingInnerValue> = HashMap::new();
    #[allow(clippy::never_loop)]
    for (inner_key, inner_mapping_obj) in val {
        let val = ensure_mapping_value_type(inner_key, inner_mapping_obj)?;
        inner_mapping.insert(inner_key.clone(), val);
    }
    Ok(inner_mapping)
}

fn convert_to_string_vector(
    json_vector: &[Value],
    inner_key: &str,
) -> Result<Vec<String>, TransmuteError> {
    let mut string_vector = Vec::new();
    for vector_val in json_vector {
        let converted_val = match vector_val {
            Value::String(x) => x.to_string(),
            Value::Number(x) => x.to_string(),
            _ => {
                return Err(TransmuteError {
                    details: format!(
                        "List values for mappings must be a string. Found {:?}, for key {}",
                        inner_key, vector_val
                    ),
                });
            }
        };
        string_vector.push(converted_val);
    }
    Ok(string_vector)
}

fn ensure_object<'a>(name: &str, obj: &'a Value) -> Result<&'a Map<String, Value>, TransmuteError> {
    match obj {
        Value::Object(x) => Ok(x),
        _ => Err(TransmuteError {
            details: format!("Mapping must be an object {}, {:?}", name, obj),
        }),
    }
}

fn ensure_mapping_value_type(name: &str, obj: &Value) -> Result<MappingInnerValue, TransmuteError> {
    match obj {
        Value::String(x) => Ok(MappingInnerValue::String(x.to_string())),
        Value::Number(x) => match x.is_f64() {
            true => Ok(MappingInnerValue::Float(WrapperF64::new(
                x.as_f64().unwrap(),
            ))),
            false => Ok(MappingInnerValue::Number(x.as_i64().unwrap())),
        },
        Value::Bool(x) => Ok(MappingInnerValue::Bool(*x)),
        Value::Array(x) => Ok(MappingInnerValue::List(convert_to_string_vector(x, name)?)),
        _ => Err(TransmuteError {
            details: format!(
                "Inner mapping value must be a string or array. Found {:?}, for {}",
                name, obj
            ),
        }),
    }
}
