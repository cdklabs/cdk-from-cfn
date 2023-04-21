mod spec;

pub use spec::*;

#[derive(Debug)]
pub enum Rule {
    Primitive(CfnType),
    List(ItemTypeRule),
    Map(ItemTypeRule),
    PropertyType(&'static str),
    Properties(phf::Map<&'static str, PropertyRule>),
}

impl Rule {
    pub(crate) fn as_properties(&self) -> Option<&phf::Map<&'static str, PropertyRule>> {
        match self {
            Self::Properties(properties) => Some(properties),
            _ => None,
        }
    }
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
#[derive(Debug, PartialEq, Eq, Copy, Clone)]
pub enum CfnType {
    Boolean,
    Integer,
    String,
    Long,
    Double,
    Timestamp,
    Json,
}

#[derive(Debug, PartialEq, Eq, Copy, Clone)]
pub enum TypeRule {
    Primitive(CfnType),
    PropertyType(&'static str),
    List(ItemTypeRule),
    Map(ItemTypeRule),
}

impl TypeRule {
    fn to_primitive(self) -> Option<CfnType> {
        match self {
            Self::Primitive(cfn_type) => Some(cfn_type),
            _ => None,
        }
    }

    fn to_structure(self) -> Structure {
        match self {
            Self::List(item_type) => item_type.as_structure(),
            Self::Map(item_type) => item_type.as_structure(),
            Self::PropertyType(property_type) => Structure::Composite(property_type.to_string()),
            Self::Primitive(primitive) => Structure::Simple(primitive),
        }
    }
}

#[derive(Debug, PartialEq, Eq, Copy, Clone)]
pub enum ItemTypeRule {
    Primitive(CfnType),
    PropertyType(&'static str),
}

#[derive(Debug, Clone)]
pub struct PropertyRule {
    pub required: bool,
    pub type_rule: TypeRule,
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
        self.type_rule.to_structure()
    }
}

impl ItemTypeRule {
    fn as_structure(&self) -> Structure {
        match self {
            Self::Primitive(primitive) => Structure::Simple(*primitive),
            Self::PropertyType(property_type) => Structure::Composite(property_type.to_string()),
        }
    }
}

#[derive(Debug)]
pub struct Specification {
    property_types: phf::Map<&'static str, Rule>,
    resource_types: phf::Map<&'static str, phf::Map<&'static str, PropertyRule>>,
}

impl Specification {
    #[inline(always)]
    fn new(
        property_types: phf::Map<&'static str, Rule>,
        resource_types: phf::Map<&'static str, phf::Map<&'static str, PropertyRule>>,
    ) -> Specification {
        Specification {
            property_types,
            resource_types,
        }
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
                .get("AWS::CloudFormation::CustomResource");
            return rules.map(|x| ResourceProperties::new(x, ResourceType::Custom));
        }
        let rules = self.resource_types.get(resource_type);
        rules.map(|x| ResourceProperties::new(x, ResourceType::Normal))
    }

    /// Returns the `Rule` for the PropertyType with the provided name, if such a property type exists.
    pub fn property_type(&self, property_type: &'_ str) -> Option<&Rule> {
        self.property_types.get(property_type)
    }
}

impl Default for Specification {
    fn default() -> Self {
        Self::new(spec::PROPERTY_TYPES, spec::RESOURCE_TYPES)
    }
}

// Internal enum to look specifically for CustomResources, as they have to be treated differently
// in the CFN Spec.
#[derive(Debug, Clone)]
enum ResourceType {
    Normal,
    Custom,
}

#[derive(Debug, Clone)]
pub struct ResourceProperties<'a> {
    pub properties: &'a phf::Map<&'static str, PropertyRule>,
    resource_type: ResourceType,
}

impl<'a> ResourceProperties<'a> {
    fn new(
        properties: &'a phf::Map<&'static str, PropertyRule>,
        resource_type: ResourceType,
    ) -> ResourceProperties<'a> {
        ResourceProperties {
            properties,
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
    /// let specification = Specification::default();
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
    let specification = Specification::default();
    let policy = specification
        .property_types
        .get("AWS::IAM::Role.Policy")
        .unwrap();
    let policy_properties = policy.as_properties().unwrap();

    assert_eq!(
        CfnType::Json,
        policy_properties
            .get("PolicyDocument")
            .unwrap()
            .type_rule
            .to_primitive()
            .unwrap()
    );
    assert_eq!(
        CfnType::String,
        policy_properties
            .get("PolicyName")
            .unwrap()
            .type_rule
            .to_primitive()
            .unwrap()
    );
}
