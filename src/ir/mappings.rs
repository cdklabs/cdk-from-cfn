use indexmap::IndexMap;

use crate::ir::mappings::OutputType::{Complex, Consistent};
use crate::parser::lookup_table::{MappingInnerValue, MappingTable};

pub struct MappingInstruction {
    pub name: String,
    pub map: IndexMap<String, IndexMap<String, MappingInnerValue>>,
}

/// When printing out to a file, sometimes there are non ordinal types in mappings.
/// An example of this is something like:
///    {
///       "DisableScaleIn": true,
///       "ScaleInCooldown": 10
///    }
///
/// The above example has both a number and a bool. This is considered "Complex".
#[derive(Clone, Debug, PartialEq)]
pub enum OutputType {
    Consistent(MappingInnerValue),
    Complex,
}

impl MappingInstruction {
    pub(super) fn from<S>(
        parse_tree: IndexMap<String, MappingTable, S>,
    ) -> Vec<MappingInstruction> {
        parse_tree
            .into_iter()
            .map(|(name, MappingTable { mappings: map, .. })| MappingInstruction { name, map })
            .collect()
    }

    pub fn output_type(&self) -> OutputType {
        let value = self.map.values().next().unwrap();
        let first_inner_value = value.values().next().unwrap();

        for _outer_map in self.map.values() {
            for inner_value in value.values() {
                if std::mem::discriminant(inner_value) != std::mem::discriminant(first_inner_value)
                {
                    return Complex;
                }
            }
        }
        Consistent(first_inner_value.clone())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    macro_rules! map {
        ($($key:expr => $value:expr),+) => {
            {
                let mut m = ::indexmap::IndexMap::<String,_,_>::default();
                $(
                    m.insert($key.into(), $value);
                )+
                m
            }
        };
    }

    #[test]
    fn test_mapping_consistent_string() {
        let mapping = MappingInstruction {
            name: "TableMappings".into(),
            map: map! {
                "Table" => map!{
                    "Key" => MappingInnerValue::String("Value".into()),
                    "Key2" => MappingInnerValue::String("Value2".into())
                }
            },
        };

        let actual_output = mapping.output_type();
        let expected_output = OutputType::Consistent(MappingInnerValue::String("Value".into()));
        // In the end, we only care if the output is Consistent(string), not the value that is used.
        assert_eq!(
            std::mem::discriminant(&expected_output),
            std::mem::discriminant(&actual_output)
        );
    }

    #[test]
    fn test_mapping_consistent_bool() {
        let mapping = MappingInstruction {
            name: "TableMappings".into(),
            map: map! {
                "Table" => map!{
                    "DisableScaleIn" => MappingInnerValue::Bool(true)
                }
            },
        };

        let actual_output = mapping.output_type();
        let expected_output = OutputType::Consistent(MappingInnerValue::Bool(true));
        assert_eq!(expected_output, actual_output);
    }

    #[test]
    fn test_mapping_complex() {
        let mapping = MappingInstruction {
            name: "TableMappings".into(),
            map: map! {
                "Table" => map!{
                    "DisableScaleIn" => MappingInnerValue::Bool(true),
                    "Cooldown" => MappingInnerValue::Number(10)
                }
            },
        };

        let actual_output = mapping.output_type();
        let expected_output = OutputType::Complex;
        assert_eq!(expected_output, actual_output);
    }
}
