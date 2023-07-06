use std::collections::HashSet;

use indexmap::IndexMap;

use crate::ir::reference::{Origin, Reference};
use crate::ir::resources::{order, ResourceInstruction, ResourceIr, ResourceType};
use crate::util::Hasher;

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
        references: HashSet::default(),
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
        references: HashSet::default(),
        properties: create_property(
            "something",
            ResourceIr::Ref(Reference::new(
                "A",
                Origin::LogicalId { conditional: false },
            )),
        ),
    };

    let misordered = vec![later.clone(), ir_instruction.clone()];

    let actual = order(misordered);
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
        references: HashSet::default(),
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
        HashSet::from(["foo".into(), "bar".into()])
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

#[inline]
fn create_property(name: &str, resource: ResourceIr) -> IndexMap<String, ResourceIr, Hasher> {
    IndexMap::from_iter([(name.into(), resource)])
}
