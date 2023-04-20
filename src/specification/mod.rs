use crate::specification::Structure::{Composite, Simple};
use serde::{Deserialize, Serialize};
use serde_yaml::Value;
use std::collections::HashMap;

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Rule {
    #[serde(alias = "PrimitiveType")]
    pub primitive_type: Option<CfnType>,
    #[serde(alias = "ItemType")]
    pub item_type: Option<String>,
    #[serde(alias = "Type")]
    pub property_type: Option<String>,
    #[serde(alias = "Properties")]
    pub properties: Option<HashMap<String, PropertyRule>>,
}

/// Structure is used in the overarching program.
/// CDK uses anything that is not a "CfnType" (defined below)
/// to camel_case their interfaces. We have to manipulate
/// that same structure backwards, in order to emit
/// the correct output.
///
/// CfnType is essentially "primitive" -- leave it alone.
/// Composite means there are deeper structures, and CDK
/// has enough information to actually camel case, so
/// you have to camelcase as well.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Structure {
    Simple(CfnType),
    Composite(String),
}

/// CfnType is the primitives in the CloudFormation specification.
/// They are when CFN just "doesn't care anymore" and doesn't do anything
/// outside of parse-classification-errors.
#[derive(Serialize, Deserialize, Debug, PartialEq, Eq, Copy, Clone)]
pub enum CfnType {
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
    pub required: Option<bool>,
    #[serde(alias = "PrimitiveType")]
    pub primitive_type: Option<CfnType>,
    #[serde(alias = "PrimitiveItemType")]
    pub primitive_item_type: Option<CfnType>,
    #[serde(alias = "ItemType")]
    pub item_type: Option<String>,
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
    pub fn get_structure(&self) -> Structure {
        if let Some(x) = &self.property_type {
            let simple_map_type = match x.as_str() {
                "List" | "Map" => &self.primitive_item_type,
                &_ => return Composite(x.to_string()),
            };

            return match simple_map_type {
                None => {
                    let complex_item = self.item_type.as_ref().unwrap();
                    Composite(complex_item.to_string())
                }
                Some(x) => Structure::Simple(*x),
            };
        }

        Simple(self.primitive_type.unwrap())
    }
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct RawRule {
    #[serde(flatten, with = "::serde_with::rust::maps_first_key_wins")]
    all: HashMap<String, Value>,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct RawSpecification {
    #[serde(
        alias = "PropertyTypes",
        rename = "PropertyTypes",
        with = "::serde_with::rust::maps_first_key_wins"
    )]
    pub property_types: HashMap<String, RawRule>,

    #[serde(alias = "ResourceTypes", rename = "ResourceTypes")]
    pub resource_types: HashMap<String, RawRule>,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct Specification {
    #[serde(
        alias = "PropertyTypes",
        with = "::serde_with::rust::maps_first_key_wins"
    )]
    pub property_types: HashMap<String, Rule>,

    #[serde(alias = "ResourceTypes")]
    pub resource_types: HashMap<String, Rule>,
}

impl Specification {
    pub fn new() -> Specification {
        let str = include_str!("spec.json");
        let raw = serde_yaml::from_str::<RawSpecification>(str).unwrap();
        let compressed_str = serde_yaml::to_string::<RawSpecification>(&raw).unwrap();
        serde_yaml::from_str::<Specification>(&compressed_str).unwrap()
    }

    // Resource Properties in Specification look something like:
    // `AWS::Iam::Role.Policy` yet are represented in the specification
    // as "Policy". full_property_name transforms that property name
    // and complexity property into the correct type.
    pub fn full_property_name(complexity: &Structure, resource_type: &str) -> Option<String> {
        match complexity {
            Structure::Simple(_) => Option::None,
            Structure::Composite(x) => {
                let mut full_rule_name = format!("{resource_type}.{x}");
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

    pub fn get_resource(&self, resource_type: &str) -> Option<ResourceProperties> {
        if resource_type.starts_with("Custom::") {
            let rules = self
                .resource_types
                .get("AWS::CloudFormation::CustomResource")
                .and_then(|t| t.properties.as_ref());
            return rules.map(|x| ResourceProperties::new(x, ResourceType::Custom));
        }
        let rules = self
            .resource_types
            .get(resource_type)
            .and_then(|t| t.properties.as_ref());
        rules.map(|x| ResourceProperties::new(x, ResourceType::Normal))
    }
}

impl Default for Specification {
    fn default() -> Self {
        Self::new()
    }
}

// Internal enum to look specifically for CustomResources, as they have to be treated differently
// in the CFN Spec.
#[derive(Serialize, Deserialize, Debug, Clone)]
enum ResourceType {
    Normal,
    Custom,
}

#[derive(Debug, Clone)]
pub struct ResourceProperties<'a> {
    pub properties: &'a HashMap<String, PropertyRule>,
    resource_type: ResourceType,
}

impl<'a> ResourceProperties<'a> {
    fn new(
        props: &HashMap<String, PropertyRule>,
        resource_type: ResourceType,
    ) -> ResourceProperties {
        ResourceProperties {
            properties: props,
            resource_type,
        }
    }
    /// structure will return a <Structure> object, that tells the user
    /// if the individual property is either <Simple>, such as the common primitive
    /// types, or if it's actually a more deeply nested complext type.
    /// Take for example a DynamoDB Table. Let's assume that it only supported 3 properties:
    /// - TableName: string
    /// - ProvisionedThroughput: ProvisionedThroughput
    /// - KeySchema: List<KeySchema>
    ///
    /// In this example, the following would occur:
    /// ```rust
    /// use noctilucent::specification::{CfnType, Specification, Structure};
    /// let specification = Specification::new();
    /// let resource = specification.get_resource("AWS::DynamoDB::Table").unwrap();
    /// assert_eq!(resource.structure("TableName"), Option::Some(Structure::Simple(CfnType::String)));
    /// assert_eq!(resource.structure("ProvisionedThroughput"), Option::Some(Structure::Composite("ProvisionedThroughput".into())));
    /// assert_eq!(resource.structure("KeySchema"), Option::Some(Structure::Composite("KeySchema".into())));
    /// ```
    pub fn structure(&self, property_name: &str) -> Option<Structure> {
        match self.resource_type {
            ResourceType::Normal => {
                let property_rule = self.properties.get(property_name);
                property_rule.map(PropertyRule::get_structure)
            }
            ResourceType::Custom => {
                // Custom resource types have multiple fields, but all are arbitrary json structs
                // except ServiceToken.
                if property_name == "ServiceToken" {
                    return Option::Some(Structure::Simple(CfnType::String));
                }
                Option::Some(Structure::Simple(CfnType::Json))
            }
        }
    }
}

#[test]
fn test_pull_json_spec() {
    let specification = Specification::new();
    let policy = specification
        .property_types
        .get("AWS::IAM::Role.Policy")
        .unwrap();
    let policy_properties = policy.properties.as_ref().unwrap();

    assert_eq!(
        CfnType::Json,
        policy_properties
            .get("PolicyDocument")
            .unwrap()
            .primitive_type
            .unwrap()
    );
    assert_eq!(
        CfnType::String,
        policy_properties
            .get("PolicyName")
            .unwrap()
            .primitive_type
            .unwrap()
    );
}
