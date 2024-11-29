// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use std::borrow::Cow;
use std::collections::HashMap;
use std::marker::PhantomData;
use std::ops::Deref;

use serde::de::Error;

use crate::util::Hasher;

// A schema of AWS CDK constructs and associated data structures, which can be
// used to drive improved conversion accuracy.
#[derive(serde::Deserialize)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
pub struct Schema {
    // The CloudFormation resource types present in this schema, indexed by
    // their CloudFormation resource type name (e.g: `"AWS::S3::Bucket"`).
    pub(super) resources: Map<CfnResource>,

    // The AWS CDK data structures present in this schema, indexed by their
    // jsii fully qualified name (e.g:
    // `"aws-cdk-lib.aws_s3.CfnBucket.DataExportProperty"`).
    pub(super) types: Map<DataType>,
}

impl Schema {
    // Builds a new schema with the provided elements.
    #[cfg(test)]
    pub const fn new(resources: Map<CfnResource>, types: Map<DataType>) -> Self {
        Self { resources, types }
    }

    // Attempts to retrieve the AWS CDK Construct for the provided
    // CloudFormation resource type name.
    pub fn resource_type(&self, type_name: &str) -> Option<&CfnResource> {
        self.resources.get(type_name)
    }

    // Attempts to retrieve the AWS CDK struct for the provided fully-qualified
    // type name.
    pub fn type_named(&self, fqn: &str) -> Option<&DataType> {
        if fqn == "CfnTag" {
            const NAME: Cow<str> = Cow::Borrowed("CfnTag");
            static CFN_TAG: DataType = DataType {
                name: TypeName {
                    #[cfg(feature = "typescript")]
                    typescript: TypeScriptName {
                        module: Cow::Borrowed("aws-cdk-lib"),
                        name: NAME,
                    },

                    #[cfg(feature = "csharp")]
                    csharp: DotNetName {
                        namespace: Cow::Borrowed("Amazon.CDK"),
                        name: NAME,
                    },

                    #[cfg(feature = "golang")]
                    golang: GolangName {
                        module: Cow::Borrowed("github.com/aws/aws-cdk-go/awscdk/v2"),
                        package: Cow::Borrowed("awscdk"),
                        name: NAME,
                    },

                    #[cfg(feature = "java")]
                    java: JavaName {
                        package: Cow::Borrowed("software.amazon.awscdk"),
                        name: NAME,
                    },

                    #[cfg(feature = "python")]
                    python: PythonName {
                        module: Cow::Borrowed("aws_cdk"),
                        name: NAME,
                    },
                },
                properties: Map::PhfMap(&phf::phf_map! {
                    "Key" => &Property {
                        name: Cow::Borrowed("key"),
                        required: false,
                        value_type: TypeReference::Primitive(Primitive::String),
                    },
                    "Value" => &Property {
                        name: Cow::Borrowed("value"),
                        required: false,
                        value_type: TypeReference::Primitive(Primitive::String),
                    },
                }),
            };
            return Some(&CFN_TAG);
        }
        let property_name = format!("{fqn}Property");
        self.types.get(&property_name)
    }
}

impl ToOwned for Schema {
    type Owned = Schema;

    fn to_owned(&self) -> Self::Owned {
        Schema {
            resources: self.resources.clone(),
            types: self.types.clone(),
        }
    }
}

// An arbitrary mapping from strings to some particular value type, which can
// be backed either by a `phf::Map` (for static data) or a `HashMap` (for
// dynamic or parsed data).
pub enum Map<V: 'static> {
    PhfMap(&'static phf::Map<&'static str, &'static V>),
    HashMap(HashMap<String, V, Hasher>),
}

impl<V: Clone> Clone for Map<V> {
    fn clone(&self) -> Self {
        match self {
            Map::PhfMap(map) => Map::PhfMap(map),
            Map::HashMap(map) => Map::HashMap(map.clone()),
        }
    }
}

impl<V> Default for Map<V> {
    fn default() -> Self {
        Map::HashMap(HashMap::default())
    }
}

impl<'de, V: serde::Deserialize<'de> + 'static> serde::Deserialize<'de> for Map<V> {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct MapVisitor<V>(PhantomData<V>);
        impl<'de, V: serde::Deserialize<'de> + 'static> serde::de::Visitor<'de> for MapVisitor<V> {
            type Value = Map<V>;

            fn expecting(&self, formatter: &mut std::fmt::Formatter) -> std::fmt::Result {
                formatter.write_str("a mapping of string to value")
            }

            fn visit_map<A: serde::de::MapAccess<'de>>(
                self,
                mut map: A,
            ) -> Result<Self::Value, A::Error> {
                let mut result: HashMap<String, V, Hasher> = HashMap::default();
                if let Some(hint) = map.size_hint() {
                    result.reserve(hint);
                }

                while let Some((key, value)) = map.next_entry()? {
                    result.insert(key, value);
                }

                Ok(result.into())
            }
        }

        deserializer.deserialize_map(MapVisitor::<V>(PhantomData))
    }
}

impl<V> Map<V> {
    // Retrieves the value associated with the provided key, if any.
    fn get(&self, key: &str) -> Option<&V> {
        match self {
            Map::PhfMap(map) => map.get(key).copied(),
            Map::HashMap(map) => map.get(key),
        }
    }
}

impl<V> From<&'static phf::Map<&'static str, &'static V>> for Map<V> {
    fn from(map: &'static phf::Map<&'static str, &'static V>) -> Self {
        Self::PhfMap(map)
    }
}

impl<V> From<HashMap<String, V, Hasher>> for Map<V> {
    fn from(map: HashMap<String, V, Hasher>) -> Self {
        Self::HashMap(map)
    }
}

pub trait PropertyBag {
    // Retrieves the property with the provided CloudFormation name, if any.
    fn property(&self, name: &str) -> Option<Property>;
}

// Information about an AWS CDK construct class.
#[derive(Clone, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CfnResource {
    // The type name of the construct class.
    pub construct: TypeName,

    // The properties declared by the construct class, indexed by their
    // CloudFormation name (e.g: `"BucketName"`).
    pub(super) properties: Map<Property>,

    // The attributes declared by the construct class, indexed by their
    // CloudFormation name (e.g: `"Arn"`).
    pub(super) attributes: Map<Property>,
}

impl CfnResource {
    // Creates a new `ConstructInfo` with the provided information.
    #[cfg(test)]
    pub const fn new(
        construct: TypeName,
        properties: Map<Property>,
        attributes: Map<Property>,
    ) -> Self {
        Self {
            construct,
            properties,
            attributes,
        }
    }

    // Retrieves the attribute with the provided CloudFormation name, if any.
    pub fn attribute(&self, name: &str) -> Option<&Property> {
        self.attributes.get(name)
    }
}

impl PropertyBag for CfnResource {
    fn property(&self, name: &str) -> Option<Property> {
        self.properties.get(name).cloned()
    }
}

// Information about an AWS CDK struct.
#[derive(Clone, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct DataType {
    /**
     * The name of the type.
     */
    pub name: TypeName,

    // The properties declared by the AWS CDK struct, indexed by their
    // CloudFormation name (e.g: `"BucketName"`).
    #[serde(bound(deserialize = "Map<Property>: serde::Deserialize<'de>"))]
    pub(super) properties: Map<Property>,
}

impl DataType {
    // Creates a new `StructInfo` with the provided properties.
    #[cfg(test)]
    pub const fn new(name: TypeName, properties: Map<Property>) -> Self {
        Self { name, properties }
    }
}

impl PropertyBag for DataType {
    fn property(&self, name: &str) -> Option<Property> {
        self.properties.get(name).cloned()
    }
}

// A multi-language aware type name.
#[derive(serde::Deserialize)]
pub struct TypeName {
    // The name of the type in TypeScript.
    #[cfg(feature = "typescript")]
    pub typescript: TypeScriptName,

    // The name of the type in .NET.
    #[cfg(feature = "csharp")]
    pub csharp: DotNetName,

    // The name of the type in Go.
    #[cfg(feature = "golang")]
    pub golang: GolangName,

    // The name of the type in Go.
    #[cfg(feature = "java")]
    pub java: JavaName,

    // The name of the type in Python.
    #[cfg(feature = "python")]
    pub python: PythonName,
}

impl Clone for TypeName {
    fn clone(&self) -> Self {
        Self {
            #[cfg(feature = "typescript")]
            typescript: self.typescript.clone(),
            #[cfg(feature = "csharp")]
            csharp: self.csharp.clone(),
            #[cfg(feature = "golang")]
            golang: self.golang.clone(),
            #[cfg(feature = "java")]
            java: self.java.clone(),
            #[cfg(feature = "python")]
            python: self.python.clone(),
        }
    }
}

#[cfg(feature = "typescript")]
// A qualified TypeScript type name.
#[derive(Clone, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct TypeScriptName {
    // The name of the module from which the type is imported (e.g:
    // `"aws-cdk-lib/aws-s3"`).
    pub module: Cow<'static, str>,

    // The name of the type (e.g: `"CfnBucket"`).
    pub name: Cow<'static, str>,
}

#[cfg(feature = "csharp")]
// A qualified .NET type name.
#[derive(Clone, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct DotNetName {
    // The .NET namespace from which the type is imported (e.g:
    // `"Amazon.CDK.AWS.S3"`)
    pub namespace: Cow<'static, str>,

    // The name of the type (e.g: `"CfnBucket"`).
    pub name: Cow<'static, str>,
}

#[cfg(feature = "golang")]
// A qualified Go type name.
#[derive(Clone, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct GolangName {
    // The name of the module from which the type is imported (e.g:
    // `"github.com/aws/aws-cdk-go/awscdk/v2/awss3"`).
    pub module: Cow<'static, str>,

    // The name of the package found in the designated module (e.g: `"awss3"`).
    pub package: Cow<'static, str>,

    // The name of the type (e.g: `"CfnBucket"`).
    pub name: Cow<'static, str>,
}

#[cfg(feature = "java")]
// A qualified Go type name.
#[derive(Clone, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct JavaName {
    // The name of the package from which the type is imported (e.g:
    // `"software.amazon.aws.awdcdk.services.s3"`).
    pub package: Cow<'static, str>,

    // The name of the type (e.g: `"CfnBucket"`).
    pub name: Cow<'static, str>,
}

#[cfg(feature = "python")]
// A qualified Python type name.
#[derive(Clone, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct PythonName {
    // The name of the module from which the type is imported (e.g:
    // `"aws_cdk.aws_s3"`)
    pub module: Cow<'static, str>,

    // The name of the type (e.g: `"CfnBucket"`).
    pub name: Cow<'static, str>,
}

// Information about a property of a construct class or struct.
#[derive(Clone, serde::Deserialize)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
pub struct Property {
    // The TypeScript name of the property.
    pub name: Cow<'static, str>,

    // Whether the property is nullable/optional.
    #[serde(default)]
    pub required: bool,

    // The declared type of the property's value.
    pub value_type: TypeReference,
}

// Possible types of property values.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum TypeReference {
    // A list of the specified values.
    List(ItemType),

    // A map of string to the specified value.
    Map(ItemType),

    // The designated primitive type.
    Primitive(Primitive),

    // The designated named type.
    Named(Cow<'static, str>),

    // Any of the designated types.
    Union(TypeUnion),
}

impl Default for TypeReference {
    #[inline]
    fn default() -> Self {
        Self::Primitive(Primitive::Unknown)
    }
}

impl<'de> serde::Deserialize<'de> for TypeReference {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct ValueTypeVisitor;
        impl<'de> serde::de::Visitor<'de> for ValueTypeVisitor {
            type Value = TypeReference;

            fn expecting(&self, formatter: &mut std::fmt::Formatter) -> std::fmt::Result {
                formatter.write_str("a value type")
            }

            fn visit_map<A: serde::de::MapAccess<'de>>(
                self,
                mut map: A,
            ) -> Result<Self::Value, A::Error> {
                let result = if let Some(key) = map.next_key::<String>()? {
                    match key.as_str() {
                        "listOf" => Self::Value::List(map.next_value::<TypeReference>()?.into()),
                        "mapOf" => Self::Value::Map(map.next_value::<TypeReference>()?.into()),
                        "named" => Self::Value::Named(map.next_value()?),
                        "primitive" => Self::Value::Primitive(map.next_value()?),
                        "unionOf" => {
                            Self::Value::Union(map.next_value::<Vec<TypeReference>>()?.into())
                        }
                        unknown => {
                            return Err(A::Error::unknown_field(
                                unknown,
                                &["listOf", "mapOf", "named", "primitive", "unionOf"],
                            ))
                        }
                    }
                } else {
                    return Err(A::Error::invalid_length(0, &Self));
                };

                // There can't be any more keys in that map...
                if map.next_key::<String>()?.is_some() {
                    return Err(A::Error::invalid_length(2, &Self));
                }

                Ok(result)
            }
        }

        deserializer.deserialize_map(ValueTypeVisitor)
    }
}

#[derive(Debug, Eq)]
pub enum ItemType {
    Static(&'static TypeReference),
    Boxed(Box<TypeReference>),
}

impl Deref for ItemType {
    type Target = TypeReference;

    fn deref(&self) -> &Self::Target {
        match self {
            ItemType::Static(v) => v,
            ItemType::Boxed(v) => v,
        }
    }
}

impl Clone for ItemType {
    fn clone(&self) -> Self {
        match self {
            ItemType::Static(v) => Self::Static(v),
            ItemType::Boxed(v) => Self::Boxed(v.clone()),
        }
    }
}

impl From<TypeReference> for ItemType {
    #[inline]
    fn from(v: TypeReference) -> Self {
        Self::Boxed(Box::new(v))
    }
}

impl From<&'static TypeReference> for ItemType {
    #[inline]
    fn from(v: &'static TypeReference) -> Self {
        Self::Static(v)
    }
}

impl From<Box<TypeReference>> for ItemType {
    #[inline]
    fn from(v: Box<TypeReference>) -> Self {
        Self::Boxed(v)
    }
}

impl PartialEq for ItemType {
    #[inline]
    fn eq(&self, other: &Self) -> bool {
        **self == **other
    }
}

#[derive(Debug, Eq)]
pub enum TypeUnion {
    Static(&'static [TypeReference]),
    Vec(Vec<TypeReference>),
}

impl Clone for TypeUnion {
    fn clone(&self) -> Self {
        match self {
            TypeUnion::Static(v) => Self::Static(v),
            TypeUnion::Vec(v) => Self::Vec(v.clone()),
        }
    }
}

impl Deref for TypeUnion {
    type Target = [TypeReference];

    fn deref(&self) -> &Self::Target {
        match self {
            TypeUnion::Static(v) => v,
            TypeUnion::Vec(v) => v,
        }
    }
}

impl From<&'static [TypeReference]> for TypeUnion {
    #[inline]
    fn from(v: &'static [TypeReference]) -> Self {
        Self::Static(v)
    }
}

impl From<Vec<TypeReference>> for TypeUnion {
    #[inline]
    fn from(v: Vec<TypeReference>) -> Self {
        Self::Vec(v)
    }
}

impl PartialEq for TypeUnion {
    #[inline]
    fn eq(&self, other: &Self) -> bool {
        **self == **other
    }
}

// A jsii primitive data type.
#[derive(Clone, Copy, Debug, PartialEq, Eq, serde_enum_str::Deserialize_enum_str)]
#[serde(rename_all = "lowercase")]
pub enum Primitive {
    // The "unknown" type.
    Unknown,

    // A boolean.
    Boolean,

    // A numeric value (integer or float).
    Number,

    // A string.
    String,

    // A timestamp
    #[serde(rename = "date-time")]
    Timestamp,

    // Arbitrary JSON data (un-transformed)
    Json,
}
