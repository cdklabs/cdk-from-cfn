// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use std::collections::{BTreeSet, HashMap};

use indexmap::IndexMap;

use crate::ir::reference::{Origin, Reference};
use crate::ir::resources::{order, ResourceInstruction, ResourceIr, ResourceType};
use crate::ir::ReferenceOrigins;
use crate::parser::resource::{IntrinsicFunction, ResourceValue};
use crate::primitives::WrapperF64;
use crate::Hasher;

use super::{Primitive, ResourceTranslator, Schema, TypeReference};

#[test]
fn test_ir_ordering() {
    let ir_instruction = ResourceInstruction {
        name: "A".to_string(),
        condition: None,
        metadata: None,
        deletion_policy: None,
        update_policy: None,
        dependencies: Vec::new(),
        resource_type: ResourceType::Custom("Dummy".into()),
        references: BTreeSet::default(),
        properties: IndexMap::default(),
    };

    let later = ResourceInstruction {
        name: "B".to_string(),
        condition: None,
        dependencies: Vec::new(),
        metadata: None,
        deletion_policy: None,
        update_policy: None,
        resource_type: ResourceType::Custom("Dummy".into()),
        references: BTreeSet::default(),
        properties: create_property(
            "something",
            ResourceIr::Ref(Reference::new(
                "A",
                Origin::LogicalId { conditional: false },
            )),
        ),
    };

    let misordered = vec![later.clone(), ir_instruction.clone()];

    let actual = order(misordered).unwrap();
    assert_eq!(actual, vec![ir_instruction, later]);
}

#[test]
fn test_ref_links() {
    let mut ir_instruction = ResourceInstruction {
        name: "A".to_string(),
        condition: None,
        metadata: None,
        deletion_policy: None,
        update_policy: None,
        dependencies: vec!["foo".to_string()],
        resource_type: ResourceType::Custom("Dummy".into()),
        references: BTreeSet::default(),
        properties: create_property(
            "something",
            ResourceIr::Ref(Reference::new(
                "bar",
                Origin::LogicalId { conditional: false },
            )),
        ),
    };

    ir_instruction.generate_references();

    assert_eq!(
        ir_instruction.references,
        BTreeSet::from([String::from("foo"), String::from("bar")])
    );
}

#[test]
fn parse_resource_type() {
    // Classical resource
    assert_eq!(
        ResourceType::parse("AWS::S3::Bucket").unwrap(),
        ResourceType::AWS {
            service: "S3".into(),
            type_name: "Bucket".into()
        },
    );

    // Custom resource with user-defined name
    assert_eq!(
        ResourceType::parse("Custom::FancyResource").unwrap(),
        ResourceType::Custom("FancyResource".into()),
    );

    // Invalid syntax
    assert!(ResourceType::parse("Custom").is_err());
    assert!(ResourceType::parse("Custom::").is_err());
    assert!(ResourceType::parse("Custom::With::").is_err());
    assert!(ResourceType::parse("Custom::With::TooManyItems").is_err());
    assert!(ResourceType::parse("AWS").is_err());
    assert!(ResourceType::parse("AWS::").is_err());
    assert!(ResourceType::parse("AWS::S3").is_err());
    assert!(ResourceType::parse("AWS::S3::").is_err());
    assert!(ResourceType::parse("AWS::S3::Bucket::").is_err());

    // Unknown namespace
    assert!(ResourceType::parse("SWA::3S::tekcuB").is_err());
}

#[test]
fn invalid_custom_resource_type() {
    let bad_resource_type = "Custom::First::Second";
    let result = ResourceType::parse(bad_resource_type).unwrap_err();
    let expected =
        format!("Invalid resource type \"{bad_resource_type}\" (only two segments expected)");
    assert_eq!(expected, result.to_string());
}

#[test]
fn alexa_resource_type_missing_service_name() {
    let bad_resource_type = "Alexa::";
    let result = ResourceType::parse(bad_resource_type).unwrap_err();
    let expected = format!("Invalid resource type \"{bad_resource_type}\" (missing service name)");
    assert_eq!(expected, result.to_string());
}

#[test]
fn alexa_resource_type_missing_resource_type() {
    let bad_resource_type = "Alexa::ASK";
    let result = ResourceType::parse(bad_resource_type).unwrap_err();
    let expected =
        format!("Invalid resource type \"{bad_resource_type}\" (missing resource type name)");
    assert_eq!(expected, result.to_string());
}

#[test]
fn invalid_alexa_resource_type() {
    let bad_resource_type = "Alexa::ASK::Skill::Invalid";
    let result = ResourceType::parse(bad_resource_type).unwrap_err();
    let expected =
        format!("Invalid resource type \"{bad_resource_type}\" (only three segments expected)");
    assert_eq!(expected, result.to_string());
}

#[test]
fn aws_resource_type_missing_service_name() {
    let bad_resource_type = "AWS::";
    let result = ResourceType::parse(bad_resource_type).unwrap_err();
    let expected = format!("Invalid resource type \"{bad_resource_type}\" (missing service name)");
    assert_eq!(expected, result.to_string());
}

#[test]
fn aws_resource_type_missing_resource_type() {
    let bad_resource_type = "AWS::Dynamo::";
    let result = ResourceType::parse(bad_resource_type).unwrap_err();
    let expected =
        format!("Invalid resource type \"{bad_resource_type}\" (missing resource type name)");
    assert_eq!(expected, result.to_string());
}

#[test]
fn invalid_aws_resource_type() {
    let bad_resource_type = "AWS::Dynamo::GlobalTable::Invalid";
    let result = ResourceType::parse(bad_resource_type).unwrap_err();
    let expected =
        format!("Invalid resource type \"{bad_resource_type}\" (only three segments expected)");
    assert_eq!(expected, result.to_string());
}

#[test]
fn unknown_resource_type() {
    let bad_resource_type = "Unknown::Resource::Type";
    let result = ResourceType::parse(bad_resource_type).unwrap_err();
    let expected = format!("Unknown resource type namespace Unknown in \"{bad_resource_type}\"");
    assert_eq!(expected, result.to_string());
}

#[test]
fn test_boolean_parse_error() {
    let origins = ReferenceOrigins {
        origins: HashMap::default(),
    };
    let translator = ResourceTranslator {
        schema: Schema::builtin(),
        origins: &origins,
        value_type: Some(TypeReference::Primitive(Primitive::Boolean)),
    };
    let resource_value = ResourceValue::String("fals".into());
    let result = translator.translate(resource_value).unwrap_err();
    assert_eq!(
        "provided string was not `true` or `false`",
        result.to_string()
    );
}

#[test]
fn test_number_parse_float() {
    let origins = ReferenceOrigins {
        origins: HashMap::default(),
    };
    let translator = ResourceTranslator {
        schema: Schema::builtin(),
        origins: &origins,
        value_type: Some(TypeReference::Primitive(Primitive::Number)),
    };
    let resource_value = ResourceValue::String("1.5".into());
    let result = translator.translate(resource_value).unwrap();
    assert_eq!(ResourceIr::Double(WrapperF64::new(1.5)), result);
}

#[test]
fn test_number_parse_error() {
    let origins = ReferenceOrigins {
        origins: HashMap::default(),
    };
    let translator = ResourceTranslator {
        schema: Schema::builtin(),
        origins: &origins,
        value_type: Some(TypeReference::Primitive(Primitive::Number)),
    };
    let resource_value = ResourceValue::String("15abc".into());
    let result = translator.translate(resource_value).unwrap_err();
    assert_eq!("invalid digit found in string", result.to_string());
}

#[test]
fn test_sub_excess_map_error() {
    let origins = ReferenceOrigins {
        origins: HashMap::default(),
    };
    let translator = ResourceTranslator {
        schema: Schema::builtin(),
        origins: &origins,
        value_type: Some(TypeReference::Primitive(Primitive::Number)),
    };
    let resource_value = ResourceValue::IntrinsicFunction(Box::new(IntrinsicFunction::Sub {
        string: "BadSub".into(),
        replaces: Some(ResourceValue::String("Invalid".into())),
    }));
    let result = translator.translate(resource_value).unwrap_err();
    assert_eq!("Sub excess map must be an object", result.to_string());
}

#[test]
fn test_invalid_base_64() {
    let origins = ReferenceOrigins {
        origins: HashMap::default(),
    };
    let translator = ResourceTranslator {
        schema: Schema::builtin(),
        origins: &origins,
        value_type: Some(TypeReference::Primitive(Primitive::Number)),
    };
    let resource_value = ResourceValue::IntrinsicFunction(Box::new(IntrinsicFunction::Base64(
        ResourceValue::String("Base64".into()),
    )));
    let result = translator.translate(resource_value).unwrap_err();
    assert_eq!(
        "Invalid base64 \"Base64\" -- Invalid padding",
        result.to_string()
    );
}

#[test]
fn test_invalid_select_index() {
    let origins = ReferenceOrigins {
        origins: HashMap::default(),
    };
    let translator = ResourceTranslator {
        schema: Schema::builtin(),
        origins: &origins,
        value_type: Some(TypeReference::Primitive(Primitive::Number)),
    };
    let resource_value = ResourceValue::IntrinsicFunction(Box::new(IntrinsicFunction::Select {
        index: ResourceValue::String("two".into()),
        list: ResourceValue::Array(Vec::new()),
    }));
    let result = translator.translate(resource_value).unwrap_err();
    assert_eq!("Index must be int for Select", result.to_string());
}

#[test]
fn test_invalid_select_index_range_error() {
    let origins = ReferenceOrigins {
        origins: HashMap::default(),
    };
    let translator = ResourceTranslator {
        schema: Schema::builtin(),
        origins: &origins,
        value_type: Some(TypeReference::Primitive(Primitive::Number)),
    };
    let resource_value = ResourceValue::IntrinsicFunction(Box::new(IntrinsicFunction::Select {
        index: ResourceValue::Number(-1),
        list: ResourceValue::Array(Vec::new()),
    }));
    let result = translator.translate(resource_value).unwrap_err();
    assert_eq!("Index is out of range for Select", result.to_string());
}

#[test]
fn test_select_index_int_error() {
    let origins = ReferenceOrigins {
        origins: HashMap::default(),
    };
    let translator = ResourceTranslator {
        schema: Schema::builtin(),
        origins: &origins,
        value_type: Some(TypeReference::Primitive(Primitive::Number)),
    };
    let resource_value = ResourceValue::IntrinsicFunction(Box::new(IntrinsicFunction::Select {
        index: ResourceValue::Bool(false),
        list: ResourceValue::Array(Vec::new()),
    }));
    let result = translator.translate(resource_value).unwrap_err();
    assert_eq!("Index must be int for Select", result.to_string());
}

#[inline]
fn create_property(name: &str, resource: ResourceIr) -> IndexMap<String, ResourceIr, Hasher> {
    IndexMap::from_iter([(name.into(), resource)])
}
