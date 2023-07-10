use crate::primitives::WrapperF64;
use indexmap::map::Entry;
use indexmap::IndexMap;
use serde::de::Error;
use serde::{de, Deserialize, Deserializer};
use std::convert::TryInto;
use std::fmt;
use std::marker::PhantomData;

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

            #[inline]
            fn expecting(&self, formatter: &mut std::fmt::Formatter) -> std::fmt::Result {
                formatter.write_str("a CloudFormation resource value")
            }

            #[inline]
            fn visit_bool<E: serde::de::Error>(self, val: bool) -> Result<Self::Value, E> {
                Ok(Self::Value::Bool(val))
            }

            #[inline]
            fn visit_enum<A: serde::de::EnumAccess<'de>>(
                self,
                data: A,
            ) -> Result<Self::Value, A::Error> {
                IntrinsicFunction::from_enum(data).map(Into::into)
            }

            #[inline]
            fn visit_f64<E: serde::de::Error>(self, val: f64) -> Result<Self::Value, E> {
                Ok(Self::Value::Double(val.into()))
            }

            #[inline]
            fn visit_i64<E: serde::de::Error>(self, val: i64) -> Result<Self::Value, E> {
                Ok(Self::Value::Number(val))
            }

            #[cold]
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

            #[inline]
            fn visit_str<E: serde::de::Error>(self, val: &str) -> Result<Self::Value, E> {
                Ok(Self::Value::String(val.into()))
            }

            #[inline]
            fn visit_u64<E: serde::de::Error>(self, val: u64) -> Result<Self::Value, E> {
                if let Ok(val) = val.try_into() {
                    Ok(Self::Value::Number(val))
                } else {
                    Ok(Self::Value::Double(val.into()))
                }
            }

            #[cold]
            fn visit_u128<E: serde::de::Error>(self, val: u128) -> Result<Self::Value, E> {
                if let Ok(val) = val.try_into() {
                    Ok(Self::Value::Number(val))
                } else {
                    Ok(Self::Value::Double(val.into()))
                }
            }

            #[inline]
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

    #[serde(deserialize_with = "string_or_seq_string")]
    #[serde(default)]
    pub depends_on: Vec<String>,

    pub update_policy: Option<ResourceValue>,

    pub deletion_policy: Option<DeletionPolicy>,

    #[serde(default)]
    pub properties: IndexMap<String, ResourceValue>,
}

fn string_or_seq_string<'de, D>(deserializer: D) -> Result<Vec<String>, D::Error>
where
    D: Deserializer<'de>,
{
    struct StringOrVec(PhantomData<Vec<String>>);

    impl<'de> de::Visitor<'de> for StringOrVec {
        type Value = Vec<String>;

        fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
            formatter.write_str("string or list of strings")
        }

        fn visit_str<E>(self, value: &str) -> Result<Self::Value, E>
        where
            E: de::Error,
        {
            Ok(vec![value.to_owned()])
        }

        fn visit_seq<S>(self, visitor: S) -> Result<Self::Value, S::Error>
        where
            S: de::SeqAccess<'de>,
        {
            Deserialize::deserialize(de::value::SeqAccessDeserializer::new(visitor))
        }
    }

    deserializer.deserialize_any(StringOrVec(PhantomData))
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
mod tests;
