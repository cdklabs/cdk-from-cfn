use super::*;

#[test]
fn test_pull_json_spec() {
    let specification = Specification::default();
    let policy = specification
        .property_types
        .get("AWS::IAM::Role.Policy")
        .unwrap();
    let policy_properties = policy.as_properties().unwrap();

    assert_eq!(
        TypeRule::Primitive(CfnType::Json),
        policy_properties.get("PolicyDocument").unwrap().type_rule
    );
    assert_eq!(
        TypeRule::Primitive(CfnType::String),
        policy_properties.get("PolicyName").unwrap().type_rule
    );
}
