use crate::primitives::WrapperF64;
use indexmap::map::Entry;
use indexmap::IndexMap;
use serde::de::Error;
use std::convert::TryInto;
use std::fmt;

pub use super::intrinsics::IntrinsicFunction;

#[derive(Clone, Debug, PartialEq)]
pub enum ResourceValue {
    Null,
    Bool(bool),
    Number(i64),
    Double(WrapperF64),
    String(String),
    Array(Vec<ResourceValue>),
    Object(IndexMap<String, ResourceValue>),

    IntrinsicFunction(Box<IntrinsicFunction>),
}

impl From<&str> for ResourceValue {
    fn from(s: &str) -> Self {
        ResourceValue::String(s.to_owned())
    }
}

impl From<IntrinsicFunction> for ResourceValue {
    fn from(i: IntrinsicFunction) -> Self {
        match i {
            IntrinsicFunction::Ref(ref_name) if ref_name == "AWS::NoValue" => ResourceValue::Null,
            i => ResourceValue::IntrinsicFunction(Box::new(i)),
        }
    }
}

impl<'de> serde::de::Deserialize<'de> for ResourceValue {
    fn deserialize<D: serde::de::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct ResourceValueVisitor;
        impl<'de> serde::de::Visitor<'de> for ResourceValueVisitor {
            type Value = ResourceValue;

            fn expecting(&self, formatter: &mut std::fmt::Formatter) -> std::fmt::Result {
                formatter.write_str("a CloudFormation resource value")
            }

            fn visit_bool<E: serde::de::Error>(self, val: bool) -> Result<Self::Value, E> {
                Ok(Self::Value::Bool(val))
            }

            fn visit_enum<A: serde::de::EnumAccess<'de>>(
                self,
                data: A,
            ) -> Result<Self::Value, A::Error> {
                IntrinsicFunction::from_enum(data).map(Into::into)
            }

            fn visit_f64<E: serde::de::Error>(self, val: f64) -> Result<Self::Value, E> {
                Ok(Self::Value::Double(val.into()))
            }

            fn visit_i64<E: serde::de::Error>(self, val: i64) -> Result<Self::Value, E> {
                Ok(Self::Value::Number(val))
            }

            fn visit_i128<E: serde::de::Error>(self, val: i128) -> Result<Self::Value, E> {
                if let Ok(val) = val.try_into() {
                    Ok(Self::Value::Number(val))
                } else {
                    Ok(Self::Value::Double(val.into()))
                }
            }

            fn visit_map<A: serde::de::MapAccess<'de>>(
                self,
                mut data: A,
            ) -> Result<Self::Value, A::Error> {
                let mut map = IndexMap::with_capacity(data.size_hint().unwrap_or_default());
                while let Some(key) = data.next_key::<String>()? {
                    if let Some(intrinsic) = IntrinsicFunction::from_singleton_map(&key, &mut data)?
                    {
                        if let Some(extraneous) = data.next_key()? {
                            return Err(A::Error::unknown_field(extraneous, &[]));
                        }
                        return Ok(intrinsic.into());
                    }
                    match map.entry(key) {
                        Entry::Vacant(entry) => {
                            entry.insert(data.next_value()?);
                        }
                        Entry::Occupied(entry) => {
                            return Err(A::Error::custom(&format!(
                                "duplicate object key {key:?}",
                                key = entry.key()
                            )))
                        }
                    }
                }
                Ok(Self::Value::Object(map))
            }

            fn visit_seq<A: serde::de::SeqAccess<'de>>(
                self,
                mut data: A,
            ) -> Result<Self::Value, A::Error> {
                let mut vec = Vec::with_capacity(data.size_hint().unwrap_or_default());
                while let Some(elem) = data.next_element()? {
                    vec.push(elem);
                }
                Ok(Self::Value::Array(vec))
            }

            fn visit_str<E: serde::de::Error>(self, val: &str) -> Result<Self::Value, E> {
                Ok(Self::Value::String(val.into()))
            }

            fn visit_u64<E: serde::de::Error>(self, val: u64) -> Result<Self::Value, E> {
                if let Ok(val) = val.try_into() {
                    Ok(Self::Value::Number(val))
                } else {
                    Ok(Self::Value::Double(val.into()))
                }
            }

            fn visit_u128<E: serde::de::Error>(self, val: u128) -> Result<Self::Value, E> {
                if let Ok(val) = val.try_into() {
                    Ok(Self::Value::Number(val))
                } else {
                    Ok(Self::Value::Double(val.into()))
                }
            }

            fn visit_unit<E: serde::de::Error>(self) -> Result<Self::Value, E> {
                Ok(Self::Value::Null)
            }
        }

        deserializer.deserialize_any(ResourceValueVisitor)
    }
}

#[derive(Debug, PartialEq, serde::Deserialize)]
#[serde(rename_all = "PascalCase")]
pub struct ResourceAttributes {
    #[serde(rename = "Type")]
    pub resource_type: String,

    pub condition: Option<String>,

    pub metadata: Option<ResourceValue>,

    #[serde(default)]
    pub depends_on: Vec<String>,

    pub update_policy: Option<ResourceValue>,

    pub deletion_policy: Option<DeletionPolicy>,

    #[serde(default)]
    pub properties: IndexMap<String, ResourceValue>,
}

#[derive(Clone, Copy, Debug, PartialEq, serde_enum_str::Deserialize_enum_str)]
pub enum DeletionPolicy {
    Delete,
    Retain,
    Snapshot,
}

impl fmt::Display for DeletionPolicy {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Delete => write!(f, "DELETE"),
            Self::Retain => write!(f, "RETAIN"),
            Self::Snapshot => write!(f, "SNAPSHOT"),
        }
    }
}

#[cfg(test)]
mod test {
    use serde_yaml::Value;

    use super::*;

    // Bring in the json! macro
    include!("../../tests/json.rs");

    #[test]
    fn intrinsic_base64() {
        const BASE64_TEXT: &str = "dGVzdAo=";
        assert_eq!(
            ResourceValue::from_value(json!({ "Fn::Base64": BASE64_TEXT })).unwrap(),
            IntrinsicFunction::Base64(ResourceValue::String(BASE64_TEXT.to_string())).into(),
        );
        assert_eq!(
            ResourceValue::from_value(
                serde_yaml::from_str(&format!("!Base64 {BASE64_TEXT:?}")).unwrap()
            )
            .unwrap(),
            IntrinsicFunction::Base64(ResourceValue::String(BASE64_TEXT.to_string())).into(),
        );
    }

    #[test]
    fn intrinsic_cidr() {
        const IP_BLOCK: &str = "10.0.0.0";
        const COUNT: i64 = 3;
        const CIDR_BITS: i64 = 8;

        assert_eq!(
            ResourceValue::from_value(json!({"Fn::Cidr": [IP_BLOCK, COUNT, CIDR_BITS] })).unwrap(),
            IntrinsicFunction::Cidr {
                ip_block: ResourceValue::String(IP_BLOCK.to_string()),
                count: ResourceValue::Number(COUNT),
                cidr_bits: ResourceValue::Number(CIDR_BITS)
            }
            .into(),
        );
        assert_eq!(
            ResourceValue::from_value(
                serde_yaml::from_str(&format!("!Cidr [{IP_BLOCK:?}, {COUNT}, {CIDR_BITS}]"))
                    .unwrap()
            )
            .unwrap(),
            IntrinsicFunction::Cidr {
                ip_block: ResourceValue::String(IP_BLOCK.to_string()),
                count: ResourceValue::Number(COUNT),
                cidr_bits: ResourceValue::Number(CIDR_BITS)
            }
            .into(),
        );

        assert_eq!(
            ResourceValue::from_value(
                json!({"Fn::Cidr": [IP_BLOCK, COUNT.to_string(), CIDR_BITS.to_string()] })
            )
            .unwrap(),
            IntrinsicFunction::Cidr {
                ip_block: ResourceValue::String(IP_BLOCK.to_string()),
                count: ResourceValue::String(COUNT.to_string()),
                cidr_bits: ResourceValue::String(CIDR_BITS.to_string())
            }
            .into(),
        );
        assert_eq!(
            ResourceValue::from_value(
                serde_yaml::from_str(&format!(
                    "!Cidr [{IP_BLOCK:?}, {:?}, {:?}]",
                    COUNT.to_string(),
                    CIDR_BITS.to_string()
                ))
                .unwrap()
            )
            .unwrap(),
            IntrinsicFunction::Cidr {
                ip_block: ResourceValue::String(IP_BLOCK.to_string()),
                count: ResourceValue::String(COUNT.to_string()),
                cidr_bits: ResourceValue::String(CIDR_BITS.to_string())
            }
            .into(),
        );
    }

    #[test]
    fn intrinsic_find_in_map() {
        const MAP_NAME: &str = "MapName";
        const FIRST_KEY: &str = "FirstKey";
        const SECOND_KEY: &str = "SecondKey";
        assert_eq!(
            ResourceValue::from_value(json!({"Fn::FindInMap": [MAP_NAME, FIRST_KEY, SECOND_KEY]}))
                .unwrap(),
            IntrinsicFunction::FindInMap {
                map_name: MAP_NAME.to_string(),
                top_level_key: ResourceValue::String(FIRST_KEY.to_string()),
                second_level_key: ResourceValue::String(SECOND_KEY.to_string())
            }
            .into(),
        );
        assert_eq!(
            ResourceValue::from_value(
                serde_yaml::from_str(&format!(
                    "!FindInMap [{MAP_NAME}, {FIRST_KEY}, {SECOND_KEY}]"
                ))
                .unwrap()
            )
            .unwrap(),
            IntrinsicFunction::FindInMap {
                map_name: MAP_NAME.to_string(),
                top_level_key: ResourceValue::String(FIRST_KEY.to_string()),
                second_level_key: ResourceValue::String(SECOND_KEY.to_string())
            }
            .into(),
        );
    }

    #[test]
    fn intrinsic_get_att() {
        const LOGICAL_NAME: &str = "MapName";
        const ATTRIBUTE_NAME: &str = "FirstKey";
        assert_eq!(
            ResourceValue::from_value(json!({"Fn::GetAtt": [LOGICAL_NAME, ATTRIBUTE_NAME]}))
                .unwrap(),
            IntrinsicFunction::GetAtt {
                logical_name: LOGICAL_NAME.into(),
                attribute_name: ATTRIBUTE_NAME.into(),
            }
            .into(),
        );
        // TODO: Confirm the below actually works in CloudFormation (it's not documented!)
        assert_eq!(
            ResourceValue::from_value(
                serde_yaml::from_str(&format!("!GetAtt [{LOGICAL_NAME}, {ATTRIBUTE_NAME}]"))
                    .unwrap()
            )
            .unwrap(),
            IntrinsicFunction::GetAtt {
                logical_name: LOGICAL_NAME.into(),
                attribute_name: ATTRIBUTE_NAME.into(),
            }
            .into(),
        );
        assert_eq!(
            ResourceValue::from_value(
                serde_yaml::from_str(&format!("!GetAtt {LOGICAL_NAME}.{ATTRIBUTE_NAME}")).unwrap()
            )
            .unwrap(),
            IntrinsicFunction::GetAtt {
                logical_name: LOGICAL_NAME.into(),
                attribute_name: ATTRIBUTE_NAME.into(),
            }
            .into(),
        );
    }

    #[test]
    fn intrinsic_get_azs() {
        const REGION: &str = "test-dummy-1337";
        assert_eq!(
            ResourceValue::from_value(json!({ "Fn::GetAZs": REGION })).unwrap(),
            IntrinsicFunction::GetAZs(ResourceValue::String(REGION.to_string())).into(),
        );
        assert_eq!(
            ResourceValue::from_value(serde_yaml::from_str(&format!("!GetAZs {REGION}")).unwrap())
                .unwrap(),
            IntrinsicFunction::GetAZs(ResourceValue::String(REGION.to_string())).into(),
        );
    }

    #[test]
    fn intrinsic_import_value() {
        const SHARED_VALUE: &str = "SharedValue.ToImport";
        assert_eq!(
            ResourceValue::from_value(json!({ "Fn::ImportValue": SHARED_VALUE })).unwrap(),
            IntrinsicFunction::ImportValue(SHARED_VALUE.into()).into(),
        );
        assert_eq!(
            ResourceValue::from_value(
                serde_yaml::from_str(&format!("!ImportValue {SHARED_VALUE}")).unwrap()
            )
            .unwrap(),
            IntrinsicFunction::ImportValue(SHARED_VALUE.into()).into(),
        );
    }

    #[test]
    fn intrinsic_join() {
        const DELIMITER: &str = "/";
        const VALUES: [&str; 3] = ["a", "b", "c"];

        assert_eq!(
            ResourceValue::from_value(json!({"Fn::Join": [DELIMITER, VALUES]})).unwrap(),
            IntrinsicFunction::Join {
                sep: DELIMITER.into(),
                list: ResourceValue::Array(
                    VALUES
                        .iter()
                        .map(|v| ResourceValue::String(v.to_string()))
                        .collect()
                )
            }
            .into(),
        );
        assert_eq!(
            ResourceValue::from_value(
                serde_yaml::from_str(&format!("!Join [{DELIMITER}, {VALUES:?}]",)).unwrap()
            )
            .unwrap(),
            IntrinsicFunction::Join {
                sep: DELIMITER.into(),
                list: ResourceValue::Array(
                    VALUES
                        .iter()
                        .map(|v| ResourceValue::String(v.to_string()))
                        .collect()
                )
            }
            .into(),
        );
    }

    #[test]
    fn intrinsic_select() {
        const INDEX: i64 = 1337;
        const VALUES: [&str; 3] = ["a", "b", "c"];

        assert_eq!(
            ResourceValue::from_value(json!({"Fn::Select": [INDEX, VALUES]})).unwrap(),
            IntrinsicFunction::Select {
                index: ResourceValue::Number(INDEX),
                list: ResourceValue::Array(
                    VALUES
                        .iter()
                        .map(|v| ResourceValue::String(v.to_string()))
                        .collect()
                )
            }
            .into(),
        );
        assert_eq!(
            ResourceValue::from_value(
                serde_yaml::from_str(&format!("!Select [{INDEX}, {VALUES:?}]",)).unwrap()
            )
            .unwrap(),
            IntrinsicFunction::Select {
                index: ResourceValue::Number(INDEX),
                list: ResourceValue::Array(
                    VALUES
                        .iter()
                        .map(|v| ResourceValue::String(v.to_string()))
                        .collect()
                )
            }
            .into(),
        );
    }

    #[test]
    fn intrinsic_split() {
        const DELIMITER: &str = "/";
        const VALUE: &str = "a/b/c";

        assert_eq!(
            ResourceValue::from_value(json!({"Fn::Split": [DELIMITER, VALUE]})).unwrap(),
            IntrinsicFunction::Split {
                sep: DELIMITER.into(),
                string: ResourceValue::String(VALUE.to_string())
            }
            .into(),
        );
        assert_eq!(
            ResourceValue::from_value(
                serde_yaml::from_str(&format!("!Split [{DELIMITER}, {VALUE}]",)).unwrap()
            )
            .unwrap(),
            IntrinsicFunction::Split {
                sep: DELIMITER.into(),
                string: ResourceValue::String(VALUE.to_string())
            }
            .into(),
        );
    }

    #[test]
    fn intrinsic_sub() {
        const STRING: &str = "String ${AWS::Region} with ${CUSTOM_VARIABLE}";
        const CUSTOM: i64 = 1337;

        assert_eq!(
            ResourceValue::from_value(json!({ "Fn::Sub": STRING })).unwrap(),
            IntrinsicFunction::Sub {
                string: STRING.into(),
                replaces: None
            }
            .into(),
        );
        assert_eq!(
            ResourceValue::from_value(json!({ "Fn::Sub": [STRING] })).unwrap(),
            IntrinsicFunction::Sub {
                string: STRING.into(),
                replaces: None
            }
            .into(),
        );
        assert_eq!(
            ResourceValue::from_value(serde_yaml::from_str(&format!("!Sub {STRING}")).unwrap())
                .unwrap(),
            IntrinsicFunction::Sub {
                string: STRING.into(),
                replaces: None
            }
            .into(),
        );
        assert_eq!(
            ResourceValue::from_value(serde_yaml::from_str(&format!("!Sub [{STRING:?}]")).unwrap())
                .unwrap(),
            IntrinsicFunction::Sub {
                string: STRING.into(),
                replaces: None
            }
            .into(),
        );

        assert_eq!(
            ResourceValue::from_value(json!({ "Fn::Sub": [STRING, {"CUSTOM_VARIABLE": CUSTOM}] }))
                .unwrap(),
            IntrinsicFunction::Sub {
                string: STRING.into(),
                replaces: Some(ResourceValue::Object(IndexMap::from([(
                    "CUSTOM_VARIABLE".to_string(),
                    ResourceValue::Number(CUSTOM)
                )])))
            }
            .into(),
        );
        assert_eq!(
            ResourceValue::from_value(
                serde_yaml::from_str(&format!(
                    "!Sub [{STRING:?}, {{ CUSTOM_VARIABLE: {CUSTOM} }}]"
                ))
                .unwrap()
            )
            .unwrap(),
            IntrinsicFunction::Sub {
                string: STRING.into(),
                replaces: Some(ResourceValue::Object(IndexMap::from([(
                    "CUSTOM_VARIABLE".to_string(),
                    ResourceValue::Number(CUSTOM)
                )]))),
            }
            .into(),
        );
    }

    #[test]
    fn intrinsic_ref() {
        const LOGICAL_NAME: &str = "LogicalName";

        assert_eq!(
            ResourceValue::from_value(json!({ "Ref": LOGICAL_NAME })).unwrap(),
            IntrinsicFunction::Ref(LOGICAL_NAME.to_string()).into(),
        );
        assert_eq!(
            ResourceValue::from_value(
                serde_yaml::from_str(&format!("!Ref {LOGICAL_NAME}")).unwrap()
            )
            .unwrap(),
            IntrinsicFunction::Ref(LOGICAL_NAME.to_string()).into(),
        );
    }

    impl ResourceValue {
        #[inline(always)]
        fn from_value(value: Value) -> Result<Self, serde_yaml::Error> {
            serde_yaml::from_value(value)
        }
    }
}
