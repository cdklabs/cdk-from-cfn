use serde::de::{Error, VariantAccess};

#[derive(Clone, Debug, PartialEq)]
pub enum ConditionFunction {
    And(Vec<ConditionValue>),
    Or(Vec<ConditionValue>),
    Equals(ConditionValue, ConditionValue),
    If {
        condition_name: String,
        if_true: ConditionValue,
        if_false: ConditionValue,
    },
    Not(ConditionValue),
}

impl ConditionFunction {
    fn from_variant_access<'de, A: serde::de::VariantAccess<'de>>(
        variant: &str,
        data: A,
    ) -> Result<Self, A::Error> {
        match variant {
            "And" => Ok(Self::And(data.newtype_variant()?)),
            "Or" => Ok(Self::Or(data.newtype_variant()?)),
            "Equals" => {
                let (left, right) = data.newtype_variant()?;
                Ok(Self::Equals(left, right))
            }
            "If" => {
                let (condition_name, if_true, if_false) = data.newtype_variant()?;
                Ok(Self::If {
                    condition_name,
                    if_true,
                    if_false,
                })
            }
            "Not" => Ok(Self::Not(data.newtype_variant::<Singleton>()?.unwrap())),
            unknown => Err(A::Error::unknown_variant(
                unknown,
                &["And", "Or", "Equals", "If", "Not"],
            )),
        }
    }

    fn from_map_access<'de, A: serde::de::MapAccess<'de>>(
        variant: &str,
        data: &mut A,
    ) -> Result<Self, A::Error> {
        match variant {
            "!And" | "Fn::And" => Ok(Self::And(data.next_value()?)),
            "!Or" | "Fn::Or" => Ok(Self::Or(data.next_value()?)),
            "!Equals" | "Fn::Equals" => {
                let (left, right) = data.next_value()?;
                Ok(Self::Equals(left, right))
            }
            "!If" | "Fn::If" => {
                let (condition_name, if_true, if_false) = data.next_value()?;
                Ok(Self::If {
                    condition_name,
                    if_true,
                    if_false,
                })
            }
            "!Not" | "Fn::Not" => Ok(Self::Not(data.next_value::<Singleton>()?.unwrap())),
            unknown => Err(A::Error::unknown_variant(
                unknown,
                &["Fn::And", "Fn::Or", "Fn::Equals", "Fn::If", "Fn::Not"],
            )),
        }
    }
}

impl<'de> serde::Deserialize<'de> for ConditionFunction {
    fn deserialize<D: serde::Deserializer<'de>>(
        deserializer: D,
    ) -> Result<ConditionFunction, D::Error> {
        struct ConditionVisitor;
        impl<'de> serde::de::Visitor<'de> for ConditionVisitor {
            type Value = ConditionFunction;

            fn expecting(&self, formatter: &mut std::fmt::Formatter) -> std::fmt::Result {
                formatter.write_str("a CloudFormation condition function")
            }

            fn visit_enum<A: serde::de::EnumAccess<'de>>(
                self,
                data: A,
            ) -> Result<Self::Value, A::Error> {
                let (variant, data) = data.variant::<String>()?;
                Self::Value::from_variant_access(&variant, data)
            }

            fn visit_map<A: serde::de::MapAccess<'de>>(
                self,
                mut data: A,
            ) -> Result<Self::Value, A::Error> {
                let variant: String = match data.next_key()? {
                    Some(key) => key,
                    None => return Err(A::Error::invalid_length(0, &Self)),
                };
                let value = Self::Value::from_map_access(&variant, &mut data)?;
                if data.next_key::<String>()?.is_some() {
                    return Err(A::Error::invalid_length(2, &Self));
                }
                Ok(value)
            }
        }

        deserializer.deserialize_any(ConditionVisitor)
    }
}

#[derive(Debug, Clone, PartialEq)]
pub enum ConditionValue {
    // Higher level boolean operators
    Function(Box<ConditionFunction>),

    // Cloudformation meta-functions
    FindInMap(
        Box<ConditionValue>,
        Box<ConditionValue>,
        Box<ConditionValue>,
    ),

    // End of recursion, the base primitives to work with
    String(String),
    Ref(String),
    Condition(String),
}

impl From<ConditionFunction> for ConditionValue {
    fn from(f: ConditionFunction) -> Self {
        Self::Function(Box::new(f))
    }
}

impl<'de> serde::Deserialize<'de> for ConditionValue {
    fn deserialize<D: serde::Deserializer<'de>>(
        deserializer: D,
    ) -> Result<ConditionValue, D::Error> {
        struct ConditionValueVisitor;
        impl<'de> serde::de::Visitor<'de> for ConditionValueVisitor {
            type Value = ConditionValue;

            fn expecting(&self, formatter: &mut std::fmt::Formatter) -> std::fmt::Result {
                formatter.write_str("a CloudFormation condition value")
            }

            fn visit_bool<E: serde::de::Error>(self, val: bool) -> Result<Self::Value, E> {
                Ok(ConditionValue::String(val.to_string()))
            }

            fn visit_enum<A: serde::de::EnumAccess<'de>>(
                self,
                data: A,
            ) -> Result<Self::Value, A::Error> {
                let (variant, data) = data.variant::<String>()?;
                match variant.as_str() {
                    "Condition" => Ok(Self::Value::Condition(data.newtype_variant()?)),
                    "FindInMap" => {
                        let (map_name, top_level_key, second_level_key) = data.newtype_variant()?;
                        Ok(Self::Value::FindInMap(
                            map_name,
                            top_level_key,
                            second_level_key,
                        ))
                    }
                    "Ref" => Ok(Self::Value::Ref(data.newtype_variant()?)),
                    other => Ok(ConditionFunction::from_variant_access(other, data)?.into()),
                }
            }

            fn visit_f64<E: serde::de::Error>(self, val: f64) -> Result<Self::Value, E> {
                Ok(ConditionValue::String(val.to_string()))
            }

            fn visit_i128<E: serde::de::Error>(self, val: i128) -> Result<Self::Value, E> {
                Ok(ConditionValue::String(val.to_string()))
            }

            fn visit_i64<E: serde::de::Error>(self, val: i64) -> Result<Self::Value, E> {
                Ok(ConditionValue::String(val.to_string()))
            }

            fn visit_map<A: serde::de::MapAccess<'de>>(
                self,
                mut data: A,
            ) -> Result<Self::Value, A::Error> {
                let key: String = match data.next_key()? {
                    Some(key) => key,
                    None => return Err(A::Error::invalid_length(0, &Self)),
                };
                match key.as_str() {
                    "!Condition" | "Condition" => Ok(Self::Value::Condition(data.next_value()?)),
                    "!FindInMap" | "Fn::FindInMap" => {
                        let (map_name, top_level_key, second_level_key) = data.next_value()?;
                        Ok(Self::Value::FindInMap(
                            map_name,
                            top_level_key,
                            second_level_key,
                        ))
                    }
                    "!Ref" | "Ref" => Ok(Self::Value::Ref(data.next_value()?)),
                    other => Ok(ConditionFunction::from_map_access(other, &mut data)?.into()),
                }
            }

            fn visit_u128<E: serde::de::Error>(self, val: u128) -> Result<Self::Value, E> {
                Ok(ConditionValue::String(val.to_string()))
            }

            fn visit_str<E: serde::de::Error>(self, val: &str) -> Result<Self::Value, E> {
                Ok(ConditionValue::String(val.into()))
            }

            fn visit_u64<E: serde::de::Error>(self, val: u64) -> Result<Self::Value, E> {
                Ok(ConditionValue::String(val.to_string()))
            }
        }

        deserializer.deserialize_any(ConditionValueVisitor)
    }
}

#[derive(serde::Deserialize)]
#[serde(untagged)]
enum Singleton {
    Value(ConditionValue),
    SingletonTuple((ConditionValue,)),
}

impl Singleton {
    fn unwrap(self) -> ConditionValue {
        match self {
            Self::Value(value) => value,
            Self::SingletonTuple((value,)) => value,
        }
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn function_and() {
        let expected = Box::new(ConditionFunction::And(vec![
            ConditionValue::String("true".into()),
            ConditionValue::String("false".into()),
        ]));

        assert_eq!(
            expected,
            serde_yaml::from_str("!And [true, 'false']").unwrap(),
        );
        assert_eq!(
            expected,
            serde_yaml::from_str("Fn::And: [true, 'false']").unwrap(),
        );
    }

    #[test]
    fn function_or() {
        let expected = Box::new(ConditionFunction::Or(vec![
            ConditionValue::String("true".into()),
            ConditionValue::String("false".into()),
        ]));

        assert_eq!(
            expected,
            serde_yaml::from_str("!Or [true, 'false']").unwrap(),
        );
        assert_eq!(
            expected,
            serde_yaml::from_str("Fn::Or: [true, 'false']").unwrap(),
        );
    }

    #[test]
    fn function_equals() {
        let expected = Box::new(ConditionFunction::Equals(
            ConditionValue::String("true".into()),
            ConditionValue::String("false".into()),
        ));

        assert_eq!(
            expected,
            serde_yaml::from_str("!Equals [true, 'false']").unwrap(),
        );
        assert_eq!(
            expected,
            serde_yaml::from_str("Fn::Equals: [true, 'false']").unwrap(),
        );
    }

    #[test]
    fn function_if() {
        let expected = Box::new(ConditionFunction::If {
            condition_name: "condition".into(),
            if_true: ConditionValue::String("true".into()),
            if_false: ConditionValue::String("false".into()),
        });

        assert_eq!(
            expected,
            serde_yaml::from_str("!If [condition, true, 'false']").unwrap(),
        );
        assert_eq!(
            expected,
            serde_yaml::from_str("Fn::If: [condition, true, 'false']").unwrap(),
        );
    }

    #[test]
    fn function_not() {
        let expected = Box::new(ConditionFunction::Not(ConditionValue::String(
            "true".into(),
        )));

        assert_eq!(expected, serde_yaml::from_str("!Not [true]").unwrap());
        assert_eq!(expected, serde_yaml::from_str("Fn::Not: [true]").unwrap());

        assert_eq!(expected, serde_yaml::from_str("!Not true").unwrap());
        assert_eq!(expected, serde_yaml::from_str("Fn::Not: true").unwrap());
    }

    #[test]
    fn condition_function_and() {
        let expected = ConditionValue::Function(Box::new(ConditionFunction::And(vec![
            ConditionValue::String("true".into()),
            ConditionValue::String("false".into()),
        ])));

        assert_eq!(
            expected,
            serde_yaml::from_str("!And [true, 'false']").unwrap(),
        );
        assert_eq!(
            expected,
            serde_yaml::from_str("Fn::And: [true, 'false']").unwrap(),
        );
    }

    #[test]
    fn condition_function_or() {
        let expected = ConditionValue::Function(Box::new(ConditionFunction::Or(vec![
            ConditionValue::String("true".into()),
            ConditionValue::String("false".into()),
        ])));

        assert_eq!(
            expected,
            serde_yaml::from_str("!Or [true, 'false']").unwrap(),
        );
        assert_eq!(
            expected,
            serde_yaml::from_str("Fn::Or: [true, 'false']").unwrap(),
        );
    }

    #[test]
    fn condition_function_equals() {
        let expected = ConditionValue::Function(Box::new(ConditionFunction::Equals(
            ConditionValue::String("true".into()),
            ConditionValue::String("false".into()),
        )));

        assert_eq!(
            expected,
            serde_yaml::from_str("!Equals [true, 'false']").unwrap(),
        );
        assert_eq!(
            expected,
            serde_yaml::from_str("Fn::Equals: [true, 'false']").unwrap(),
        );
    }

    #[test]
    fn condition_function_if() {
        let expected = ConditionValue::Function(Box::new(ConditionFunction::If {
            condition_name: "condition".into(),
            if_true: ConditionValue::String("true".into()),
            if_false: ConditionValue::String("false".into()),
        }));

        assert_eq!(
            expected,
            serde_yaml::from_str("!If [condition, true, 'false']").unwrap(),
        );
        assert_eq!(
            expected,
            serde_yaml::from_str("Fn::If: [condition, true, 'false']").unwrap(),
        );
    }

    #[test]
    fn condition_function_not() {
        let expected = ConditionValue::Function(Box::new(ConditionFunction::Not(
            ConditionValue::String("true".into()),
        )));

        assert_eq!(expected, serde_yaml::from_str("!Not [true]").unwrap());
        assert_eq!(expected, serde_yaml::from_str("Fn::Not: [true]").unwrap());

        assert_eq!(expected, serde_yaml::from_str("!Not true").unwrap());
        assert_eq!(expected, serde_yaml::from_str("Fn::Not: true").unwrap());
    }

    #[test]
    fn condition_find_in_map() {
        let expected = ConditionValue::FindInMap(
            Box::new(ConditionValue::String("Map".into())),
            Box::new(ConditionValue::String("TLK".into())),
            Box::new(ConditionValue::String("SLK".into())),
        );
        assert_eq!(
            expected,
            serde_yaml::from_str("!FindInMap [Map, TLK, SLK]").unwrap()
        );
        assert_eq!(
            expected,
            serde_yaml::from_str("Fn::FindInMap: [Map, TLK, SLK]").unwrap()
        );
    }

    #[test]
    fn condition_str_bool() {
        let expected = ConditionValue::String("true".into());
        assert_eq!(expected, serde_yaml::from_str("true").unwrap());
    }
    #[test]
    fn condition_str_float() {
        let expected = ConditionValue::String("3.1415".into());
        assert_eq!(expected, serde_yaml::from_str("3.1415").unwrap());
    }
    #[test]
    fn condition_str_ilong() {
        let expected = ConditionValue::String("-184467440737095516150".into());
        assert_eq!(
            expected,
            serde_yaml::from_str("-184467440737095516150").unwrap()
        );
    }
    #[test]
    fn condition_str_int() {
        let expected = ConditionValue::String("-1337".into());
        assert_eq!(expected, serde_yaml::from_str("-1337").unwrap());
    }
    #[test]
    fn condition_str_uint() {
        let expected = ConditionValue::String("1337".into());
        assert_eq!(expected, serde_yaml::from_str("1337").unwrap());
    }
    #[test]
    fn condition_str_ulong() {
        let expected = ConditionValue::String("184467440737095516150".into());
        assert_eq!(
            expected,
            serde_yaml::from_str("184467440737095516150").unwrap()
        );
    }

    #[test]
    fn condition_str_string() {
        let expected = ConditionValue::String("Hello, world!".into());
        assert_eq!(expected, serde_yaml::from_str("'Hello, world!'").unwrap());
    }

    #[test]
    fn condition_ref() {
        let expected = ConditionValue::Ref("LogicalID".into());
        assert_eq!(expected, serde_yaml::from_str("!Ref LogicalID").unwrap());
        assert_eq!(expected, serde_yaml::from_str("Ref: LogicalID").unwrap());
    }

    #[test]
    fn condition_condition() {
        let expected = ConditionValue::Condition("LogicalID".into());
        assert_eq!(
            expected,
            serde_yaml::from_str("!Condition LogicalID").unwrap()
        );
        assert_eq!(
            expected,
            serde_yaml::from_str("Condition: LogicalID").unwrap()
        );
    }
}
