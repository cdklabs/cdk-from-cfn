use super::resource::ResourceValue;
use serde::de::{Error, VariantAccess};

#[derive(Clone, Debug, PartialEq)]
pub enum IntrinsicFunction {
    // Standard built-ins
    Base64(ResourceValue),
    Cidr {
        ip_block: ResourceValue,
        count: ResourceValue,
        cidr_bits: ResourceValue,
    },
    FindInMap {
        map_name: ResourceValue,
        top_level_key: ResourceValue,
        second_level_key: ResourceValue,
    },
    GetAtt {
        logical_name: String,
        attribute_name: String,
    },
    GetAZs(ResourceValue),
    If {
        condition_name: String,
        value_if_true: ResourceValue,
        value_if_false: ResourceValue,
    },
    ImportValue(ResourceValue),
    Join {
        sep: String,
        list: ResourceValue,
    },
    Select {
        index: ResourceValue,
        list: ResourceValue,
    },
    Split {
        sep: String,
        string: ResourceValue,
    },
    Sub {
        string: String,
        replaces: Option<ResourceValue>,
    },
    Ref(String),

    // Special semantics
    Transform,

    // Provided by the `AWS::LanguageExtensions` transform
    Length,
    ToJsonString,
}

static INTRINSIC_FUNCTION_TAGS: &[&str] = &[
    "Base64",
    "Cidr",
    "FindInMap",
    "GetAtt",
    "GetAZs",
    "ImportValue",
    "Join",
    "Select",
    "Split",
    "Sub",
    "Ref",
];

impl IntrinsicFunction {
    pub(super) fn from_enum<'de, A: serde::de::EnumAccess<'de>>(data: A) -> Result<Self, A::Error> {
        let (tag, data): (String, _) = data.variant()?;

        Ok(match tag.as_str() {
            "Base64" => Self::Base64(data.newtype_variant()?),
            "Cidr" => {
                let (ip_block, count, cidr_bits) = data.newtype_variant()?;
                Self::Cidr {
                    ip_block,
                    count,
                    cidr_bits,
                }
            }
            "FindInMap" => {
                let (map_name, top_level_key, second_level_key) = data.newtype_variant()?;
                Self::FindInMap {
                    map_name,
                    top_level_key,
                    second_level_key,
                }
            }
            "GetAtt" => {
                let (logical_name, attribute_name) =
                    data.newtype_variant::<StringOrPair>()?.into_pair()?;
                Self::GetAtt {
                    logical_name,
                    attribute_name,
                }
            }
            "GetAZs" => Self::GetAZs(data.newtype_variant()?),
            "ImportValue" => Self::ImportValue(data.newtype_variant()?),
            "Join" => {
                let (sep, list) = data.newtype_variant()?;
                Self::Join { sep, list }
            }
            "Select" => {
                let (index, list) = data.newtype_variant()?;
                Self::Select { index, list }
            }
            "Split" => {
                let (sep, string) = data.newtype_variant()?;
                Self::Split { sep, string }
            }
            "Sub" => {
                let (string, replaces) = data.newtype_variant::<SubPayload>()?.into_pair();
                Self::Sub { string, replaces }
            }
            "Ref" => Self::Ref(data.newtype_variant()?),
            unknown => return Err(A::Error::unknown_variant(unknown, INTRINSIC_FUNCTION_TAGS)),
        })
    }

    pub(super) fn from_singleton_map<'de, A: serde::de::MapAccess<'de>>(
        key: &str,
        data: &mut A,
    ) -> Result<Option<Self>, A::Error> {
        Ok(match key {
            "!Base64" | "Fn::Base64" => Some(Self::Base64(data.next_value()?)),
            "!Cidr" | "Fn::Cidr" => {
                let (ip_block, count, cidr_bits) = data.next_value()?;
                Some(Self::Cidr {
                    ip_block,
                    count,
                    cidr_bits,
                })
            }
            "!FindInMap" | "Fn::FindInMap" => {
                let (map_name, top_level_key, second_level_key) = data.next_value()?;
                Some(Self::FindInMap {
                    map_name,
                    top_level_key,
                    second_level_key,
                })
            }
            "!GetAtt" | "Fn::GetAtt" => {
                let (logical_name, attribute_name) =
                    data.next_value::<StringOrPair>()?.into_pair()?;
                Some(Self::GetAtt {
                    logical_name,
                    attribute_name,
                })
            }
            "!GetAZs" | "Fn::GetAZs" => Some(Self::GetAZs(data.next_value()?)),
            "!ImportValue" | "Fn::ImportValue" => Some(Self::ImportValue(data.next_value()?)),
            "!Join" | "Fn::Join" => {
                let (sep, list) = data.next_value()?;
                Some(Self::Join { sep, list })
            }
            "!Select" | "Fn::Select" => {
                let (index, list) = data.next_value()?;
                Some(Self::Select { index, list })
            }
            "!Split" | "Fn::Split" => {
                let (sep, string) = data.next_value()?;
                Some(Self::Split { sep, string })
            }
            "!Sub" | "Fn::Sub" => {
                let (string, replaces) = data.next_value::<SubPayload>()?.into_pair();
                Some(Self::Sub { string, replaces })
            }
            "!Ref" | "Ref" => Some(Self::Ref(data.next_value()?)),
            _ => None,
        })
    }
}

#[derive(Debug, serde::Deserialize)]
#[serde(untagged)]
enum StringOrPair {
    String(String),
    Pair(String, String),
}

impl StringOrPair {
    fn into_pair<E: serde::de::Error>(self) -> Result<(String, String), E> {
        match self {
            Self::String(string) => match string.split_once('.') {
                Some((left, right)) => Ok((left.into(), right.into())),
                None => Err(E::invalid_value(
                    serde::de::Unexpected::Str(&string),
                    &"<logicalNameOfResource>.<attributeName>",
                )),
            },
            Self::Pair(left, right) => Ok((left, right)),
        }
    }
}

#[derive(Debug, serde::Deserialize)]
#[serde(untagged)]
enum SubPayload {
    String(String),
    SingletonList((String,)),
    StringAndObject(String, Option<ResourceValue>),
}

impl SubPayload {
    fn into_pair(self) -> (String, Option<ResourceValue>) {
        match self {
            Self::String(string) => (string, None),
            Self::SingletonList((string,)) => (string, None),
            Self::StringAndObject(string, object) => (string, object),
        }
    }
}
