use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Serialize, Deserialize, Debug)]
struct Rule {
    #[serde(alias = "PrimitiveType")]
    primitive_type: Option<SimpleType>,
    #[serde(alias = "ItemType")]
    item_type: Option<String>,
    #[serde(alias = "Type")]
    property_type: Option<String>,
    #[serde(alias = "Properties")]
    properties: Option<HashMap<String, PropertyRule>>,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Copy, Clone)]
enum SimpleType {
    Boolean,
    Integer,
    String,
    Long,
    Double,
    Timestamp,
    Json,
}

#[derive(Serialize, Deserialize, Debug)]
struct PropertyRule {
    #[serde(alias = "Required")]
    required: bool,
    #[serde(alias = "PrimitiveType")]
    primitive_type: Option<SimpleType>,
    #[serde(alias = "ItemType")]
    item_type: Option<String>,
    #[serde(alias = "Type")]
    property_type: Option<String>,
}

#[derive(Serialize, Deserialize, Debug)]
struct Specification {
    #[serde(alias = "PropertyTypes")]
    property_types: HashMap<String, Rule>,

    #[serde(alias = "ResourceTypes")]
    resource_types: HashMap<String, Rule>,
}

fn read_specification() -> String {
    let str = include_str!("spec.json");
    str.to_string()
}
fn spec() -> Specification {
    let str = read_specification();
    let res = serde_json::from_str::<Specification>(str.as_str()).unwrap();

    res
}

#[test]
fn test_pull_json_spec() {
    let specification = spec();
    let policy = specification
        .property_types
        .get("AWS::IAM::Role.Policy")
        .unwrap();
    let policy_properties = policy.properties.as_ref().unwrap();

    assert_eq!(
        SimpleType::Json,
        policy_properties
            .get("PolicyDocument")
            .unwrap()
            .primitive_type
            .unwrap()
    );
    assert_eq!(
        SimpleType::String,
        policy_properties
            .get("PolicyName")
            .unwrap()
            .primitive_type
            .unwrap()
    );
}
