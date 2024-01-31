use indexmap::IndexMap;

use crate::ir::mappings::OutputType::{Complex, Consistent};
use crate::parser::lookup_table::{MappingInnerValue, MappingTable};
use crate::Hasher;

pub struct MappingInstruction {
    pub name: String,
    pub map: IndexMap<String, IndexMap<String, MappingInnerValue, Hasher>, Hasher>,
}

// When printing out to a file, sometimes there are non ordinal types in mappings.
// An example of this is something like:
//    {
//       "DisableScaleIn": true,
//       "ScaleInCooldown": 10
//    }
//
// The above example has both a number and a bool. This is considered "Complex".
#[derive(Clone, Debug, PartialEq)]
pub enum OutputType {
    Consistent(MappingInnerValue),
    Complex,
}

impl MappingInstruction {
    pub(super) fn from(
        parse_tree: IndexMap<String, MappingTable, Hasher>,
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
mod tests;
