use std::borrow::Cow;

use indexmap::IndexMap;

use crate::{
    cdk::{ItemType, Primitive, Schema, TypeReference, TypeUnion},
    code::CodeBuffer,
    ir::{
        conditions::ConditionIr, importer::ImportInstruction, outputs::OutputInstruction,
        resources::ResourceIr,
    },
    primitives::WrapperF64,
};

use super::CsharpEmitter;

#[test]
fn test_fn_split() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Split(
        "-".into(),
        Box::new(ResourceIr::String("My-EC2-Instance".into())),
    );
    let result = resource_ir.emit_csharp(&output, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_fn_split_other() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Split(
        "-".into(),
        Box::new(ResourceIr::Join(
            ",".to_string(),
            vec![
                ResourceIr::String("a".into()),
                ResourceIr::String("b".into()),
                ResourceIr::String("c".into()),
            ],
        )),
    );
    let result = resource_ir.emit_csharp(&output, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_condition_ir_map() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let condition_ir = ConditionIr::Map(
        "ConditionIrMap".into(),
        Box::new(ConditionIr::Str("FirstLevelKey".into())),
        Box::new(ConditionIr::Str("SecondLevelKey".into())),
    );
    let result = condition_ir.emit_csharp(&output, &schema);
    assert_eq!((), result);
}

#[test]
fn test_condition_ir_split() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let condition_ir = ConditionIr::Split(
        "-".into(),
        Box::new(ConditionIr::Str("string-to-split".into())),
    );
    let result = condition_ir.emit_csharp(&output, &schema);
    assert_eq!((), result);
}

#[test]
fn test_alexa_org() {
    let import_instruction = ImportInstruction {
        organization: "Alexa".into(),
        service: Some("Ask".into()),
    };
    let result = import_instruction.to_csharp();
    assert_eq!("using Amazon.CDK.Alexa.Ask;", result.unwrap());
}

#[test]
fn test_resource_ir_double() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Double(WrapperF64::new(2.0));
    let result = resource_ir.emit_csharp(&output, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_select() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Select(1, Box::new(ResourceIr::String("Not an array".into())));
    let result = resource_ir.emit_csharp(&output, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_cidr() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Cidr(
        Box::new(ResourceIr::String("0.0.0.0".into())),
        Box::new(ResourceIr::String("16".into())),
        Box::new(ResourceIr::String("255.255.255.0".into())),
    );
    let result = resource_ir.emit_csharp(&output, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_invalid_resource_object_structure() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Object(
        TypeReference::Union(TypeUnion::Static(&[])),
        IndexMap::default(),
    );
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    let expected = "Type reference Union(\n    Static(\n        [],\n    ),\n) not implemented for ResourceIr::Object";
    assert_eq!(expected, result.to_string());
}

#[test]
fn test_invalid_resource_object_primitive() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Object(
        TypeReference::Primitive(Primitive::String),
        IndexMap::default(),
    );
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    let expected =
        "Type reference Primitive(\n    String,\n) not implemented for ResourceIr::Object";
    assert_eq!(expected, result.to_string());
}

#[test]
fn test_invalid_organization() {
    let bad_org = "NotAws";
    let import_instruction = ImportInstruction {
        organization: bad_org.to_string(),
        service: Option::None,
    };
    let result = import_instruction.to_csharp().unwrap_err();
    let expected = format!("Expected organization to be AWS or Alexa. Found {bad_org}");
    assert_eq!(expected, result.to_string());
}

#[test]
fn test_resource_ir_select_idx_greater_than_list_len() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let named_type = TypeReference::Named("AWS::Service::Resource".into());
    let resource_ir = ResourceIr::Select(
        1,
        Box::new(ResourceIr::Array(
            TypeReference::List(ItemType::Boxed(Box::new(named_type))),
            vec![],
        )),
    );
    let result = resource_ir.emit_csharp(&output, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_cidr_null_mask() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Cidr(
        Box::new(ResourceIr::String("0.0.0.0".into())),
        Box::new(ResourceIr::String("16".into())),
        Box::new(ResourceIr::Null),
    );
    let result = resource_ir.emit_csharp(&output, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_output_instruction() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let output_instruction = OutputInstruction {
        name: "instruction".to_string(),
        export: Some(ResourceIr::Number(2)),
        value: ResourceIr::Number(2),
        condition: Option::None,
        description: Option::None,
    };
    let result = output_instruction.emit_csharp(&output, &schema);
    assert_eq!((), result.unwrap());
}

#[test]
fn test_resource_ir_array_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Array(
        TypeReference::Primitive(Primitive::Json),
        vec![ResourceIr::Object(
            TypeReference::Union(TypeUnion::Vec(Vec::new())),
            IndexMap::new(),
        )],
    );
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    assert_eq!(
        "Type reference Union(\n    Vec(\n        [],\n    ),\n) not implemented for ResourceIr::Object",
        result.to_string(),
    );
}

#[test]
fn test_resource_ir_object_named_structure_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Object(
        TypeReference::Named("AWS::ACMPCA::CertificateAuthority.Subject".into()),
        IndexMap::from([(
            "map".into(),
            ResourceIr::Object(
                TypeReference::Union(TypeUnion::Vec(Vec::new())),
                IndexMap::new(),
            ),
        )]),
    );
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    assert_eq!(
        "Type reference Union(\n    Vec(\n        [],\n    ),\n) not implemented for ResourceIr::Object",
        result.to_string(),
    );
}

#[test]
fn test_resource_ir_object_primitive_structure_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Object(
        TypeReference::Primitive(Primitive::Json),
        IndexMap::from([(
            "map".into(),
            ResourceIr::Object(
                TypeReference::Union(TypeUnion::Vec(Vec::new())),
                IndexMap::new(),
            ),
        )]),
    );
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    assert_eq!(
        "Type reference Union(\n    Vec(\n        [],\n    ),\n) not implemented for ResourceIr::Object",
        result.to_string(),
    );
}

#[test]
fn test_resource_ir_object_map_structure_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Object(
        TypeReference::Map(ItemType::Boxed(Box::new(TypeReference::Primitive(
            Primitive::Json,
        )))),
        IndexMap::from([(
            "map".into(),
            ResourceIr::Object(
                TypeReference::Union(TypeUnion::Vec(Vec::new())),
                IndexMap::new(),
            ),
        )]),
    );
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    assert_eq!(
        "Type reference Union(\n    Vec(\n        [],\n    ),\n) not implemented for ResourceIr::Object",
        result.to_string(),
    );
}

#[test]
fn test_resource_ir_if_when_true_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::If(
        "if".into(),
        Box::new(ResourceIr::Object(
            TypeReference::Primitive(Primitive::Json),
            IndexMap::from([(
                "map".into(),
                ResourceIr::Object(
                    TypeReference::Union(TypeUnion::Vec(Vec::new())),
                    IndexMap::new(),
                ),
            )]),
        )),
        Box::new(ResourceIr::Null),
    );
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    assert_eq!(
        "Type reference Union(\n    Vec(\n        [],\n    ),\n) not implemented for ResourceIr::Object",
        result.to_string(),
    );
}

#[test]
fn test_resource_ir_if_when_false_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::If(
        "if".into(),
        Box::new(ResourceIr::Null),
        Box::new(ResourceIr::Object(
            TypeReference::Primitive(Primitive::Json),
            IndexMap::from([(
                "map".into(),
                ResourceIr::Object(
                    TypeReference::Union(TypeUnion::Vec(Vec::new())),
                    IndexMap::new(),
                ),
            )]),
        )),
    );
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    assert_eq!(
        "Type reference Union(\n    Vec(\n        [],\n    ),\n) not implemented for ResourceIr::Object",
        result.to_string(),
    );
}

#[test]
fn test_resource_ir_join_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Join(
        "-".into(),
        vec![ResourceIr::Object(
            TypeReference::Union(TypeUnion::Vec(Vec::new())),
            IndexMap::new(),
        )],
    );
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    assert_eq!(
        "Type reference Union(\n    Vec(\n        [],\n    ),\n) not implemented for ResourceIr::Object",
        result.to_string(),
    );
}

#[test]
fn test_resource_ir_split_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Split(
        "-".into(),
        Box::new(ResourceIr::Object(
            TypeReference::Union(TypeUnion::Vec(Vec::new())),
            IndexMap::new(),
        )),
    );
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    assert_eq!(
        "Type reference Union(\n    Vec(\n        [],\n    ),\n) not implemented for ResourceIr::Object",
        result.to_string(),
    );
}

#[test]
fn test_resource_ir_sub_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Sub(vec![ResourceIr::Object(
        TypeReference::Union(TypeUnion::Vec(Vec::new())),
        IndexMap::new(),
    )]);
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    assert_eq!(
        "Type reference Union(\n    Vec(\n        [],\n    ),\n) not implemented for ResourceIr::Object",
        result.to_string(),
    );
}

#[test]
fn test_resource_ir_map_top_level_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Map(
        "map".into(),
        Box::new(ResourceIr::Object(
            TypeReference::Union(TypeUnion::Vec(Vec::new())),
            IndexMap::new(),
        )),
        Box::new(ResourceIr::Null),
    );
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    assert_eq!(
        "Type reference Union(\n    Vec(\n        [],\n    ),\n) not implemented for ResourceIr::Object",
        result.to_string(),
    );
}

#[test]
fn test_resource_ir_map_second_level_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Map(
        "map".into(),
        Box::new(ResourceIr::Null),
        Box::new(ResourceIr::Object(
            TypeReference::Union(TypeUnion::Vec(Vec::new())),
            IndexMap::new(),
        )),
    );
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    assert_eq!(
        "Type reference Union(\n    Vec(\n        [],\n    ),\n) not implemented for ResourceIr::Object",
        result.to_string(),
    );
}

#[test]
fn test_resource_ir_base64_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::Base64(Box::new(ResourceIr::Object(
        TypeReference::Union(TypeUnion::Vec(Vec::new())),
        IndexMap::new(),
    )));
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    assert_eq!(
        "Type reference Union(\n    Vec(\n        [],\n    ),\n) not implemented for ResourceIr::Object",
        result.to_string(),
    );
}

#[test]
fn test_resource_ir_import_value_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::ImportValue(Box::new(ResourceIr::Object(
        TypeReference::Union(TypeUnion::Vec(Vec::new())),
        IndexMap::new(),
    )));
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    assert_eq!(
        "Type reference Union(\n    Vec(\n        [],\n    ),\n) not implemented for ResourceIr::Object",
        result.to_string(),
    );
}

#[test]
fn test_resource_ir_get_azs_error() {
    let output = CodeBuffer::default();
    let schema = Cow::Borrowed(Schema::builtin());
    let resource_ir = ResourceIr::GetAZs(Box::new(ResourceIr::Object(
        TypeReference::Union(TypeUnion::Vec(Vec::new())),
        IndexMap::new(),
    )));
    let result = resource_ir.emit_csharp(&output, &schema).unwrap_err();
    assert_eq!(
        "Type reference Union(\n    Vec(\n        [],\n    ),\n) not implemented for ResourceIr::Object",
        result.to_string(),
    );
}
