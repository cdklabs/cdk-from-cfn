use crate::specification::Complexity::{Complex, Simple};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Rule {
    #[serde(alias = "PrimitiveType")]
    primitive_type: Option<SimpleType>,
    #[serde(alias = "ItemType")]
    item_type: Option<String>,
    #[serde(alias = "Type")]
    property_type: Option<String>,
    #[serde(alias = "Properties")]
    pub properties: Option<HashMap<String, PropertyRule>>,
}

// Complexity is used in the overarching program.
// CDK uses anything that is not a "SimpleType" (defined below)
// to camel_case their interfaces. We have to manipulate
// that same structure backwards, in order to emit
// the correct output.
//
// Simple is essentially "primitive" -- leave it alone.
// Complex means there are deeper structures, and CDK
// has enough information to actually camel case, so
// you have to camelcase as well.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Complexity {
    Simple(SimpleType),
    Complex(String),
}

// SimpleType is the primitives in the CloudFormation specification.
// They are when CFN just "doesn't care anymore" and doesn't do anything
// outside of parse-classification-errors.
#[derive(Serialize, Deserialize, Debug, PartialEq, Eq, Copy, Clone)]
pub enum SimpleType {
    Boolean,
    Integer,
    String,
    Long,
    Double,
    Timestamp,
    Json,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct PropertyRule {
    #[serde(alias = "Required")]
    required: bool,
    #[serde(alias = "PrimitiveType")]
    primitive_type: Option<SimpleType>,
    #[serde(alias = "PrimitiveItemType")]
    primitive_item_type: Option<SimpleType>,
    #[serde(alias = "ItemType")]
    item_type: Option<String>,
    #[serde(alias = "Type")]
    pub property_type: Option<String>,
}

impl PropertyRule {
    // get_complexity will take a look at the current property and return the complexity of it's
    // structure, as well as the type.
    //
    // The branching paths are as follows:
    //
    // A List or Map will have a "Type" field (which is deserialized in property_type).
    //    - If you have a list/map, and if the PrimitiveItemType field exists, it is that primitive type.
    //    - If you have a list/map and it does not have PrimitiveItemType, "ItemType" will store
    //      it's complex type name
    //   <enough about lists / maps>
    //    - If a "Type" exists, it is a Complex type.
    //    - Otherwise, it is simple and will always have a "PrimitiveType" (different from "PrimitiveItemType")
    pub fn get_complexity(&self) -> Complexity {
        if let Some(x) = &self.property_type {
            let simple_map_type = match x.as_str() {
                "List" | "Map" => &self.primitive_item_type,
                &_ => return Complex(x.to_string()),
            };

            return match simple_map_type {
                None => {
                    let complex_item = self.item_type.as_ref().unwrap();
                    Complex(complex_item.to_string())
                }
                Some(x) => Complexity::Simple(*x),
            };
        }

        Simple(self.primitive_type.unwrap())
    }
}

#[derive(Serialize, Deserialize, Debug)]
pub struct Specification {
    #[serde(alias = "PropertyTypes")]
    pub property_types: HashMap<String, Rule>,

    #[serde(alias = "ResourceTypes")]
    pub resource_types: HashMap<String, Rule>,
}

impl Specification {
    // Resource Properties in Specification look something like:
    // `AWS::Iam::Role.Policy` yet are represented in the specification
    // as "Policy". full_property_name transforms that property name
    // and complexity property into the correct type.
    pub fn full_property_name(complexity: &Complexity, resource_type: &str) -> Option<String> {
        match complexity {
            Complexity::Simple(_) => Option::None,
            Complexity::Complex(x) => {
                let mut full_rule_name = format!("{}.{}", resource_type, x);
                // Every type in CloudFormation has the form: {resource}.{resource_type}
                // e.g. AWS::Iam::Role.Policy . Tag's lookup name in the specification is "Tag".
                // no one can explain why. Thanks CFN.
                if x == "Tag" {
                    full_rule_name = "Tag".to_string();
                }

                Option::Some(full_rule_name)
            }
        }
    }

    pub fn get_resource(&self, resource_type: &str) -> Option<ResourceSpecification> {
        if resource_type.starts_with("Custom::") {
            let rules = self
                .resource_types
                .get("AWS::CloudFormation::CustomResource")
                .and_then(|t| t.properties.as_ref());
            return rules.map(|x| ResourceSpecification::new(x, ResourceType::Custom));
        }
        let rules = self
            .resource_types
            .get(resource_type)
            .and_then(|t| t.properties.as_ref());
        rules.map(|x| ResourceSpecification::new(x, ResourceType::Normal))
    }
}

// Custom Resources have no specification to them, so we will not have them.
#[derive(Serialize, Deserialize, Debug, Clone)]
enum ResourceType {
    Normal,
    Custom,
}

#[derive(Debug, Clone)]
pub struct ResourceSpecification<'a> {
    properties: &'a HashMap<String, PropertyRule>,
    resource_type: ResourceType,
}

impl<'a> ResourceSpecification<'a> {
    fn new(
        props: &HashMap<String, PropertyRule>,
        resource_type: ResourceType,
    ) -> ResourceSpecification {
        ResourceSpecification {
            properties: props,
            resource_type,
        }
    }
    pub fn property_complexity(&self, property_name: &str) -> Option<Complexity> {
        match self.resource_type {
            ResourceType::Normal => {
                let property_rule = self.properties.get(property_name);
                property_rule.map(PropertyRule::get_complexity)
            }
            ResourceType::Custom => {
                if property_name == "ServiceToken" {
                    return Option::Some(Complexity::Simple(SimpleType::String));
                }
                Option::Some(Complexity::Simple(SimpleType::Json))
            }
        }
    }
}

fn read_specification() -> String {
    let str = include_str!("spec.json");
    str.to_string()
}

// Fully reads the specification from the stored json file
pub fn spec() -> Specification {
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
