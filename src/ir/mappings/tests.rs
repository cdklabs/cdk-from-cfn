// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
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
