use std::collections::HashSet;

use indexmap::IndexMap;

use crate::ir::reference::{Origin, Reference};
use crate::ir::resources::{order, ResourceInstruction, ResourceIr, ResourceType};

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

#[inline]
fn create_property(name: &str, resource: ResourceIr) -> IndexMap<String, ResourceIr> {
    IndexMap::from([(name.into(), resource)])
}
