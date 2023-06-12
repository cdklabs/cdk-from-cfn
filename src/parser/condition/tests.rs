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
        "Map".into(),
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
fn condition_split() {
    let expected = ConditionValue::Split(
        ",".into(),
        Box::new(ConditionValue::String("hello,world".into())),
    );
    assert_eq!(
        expected,
        serde_yaml::from_str("!Split [\",\", \"hello,world\"]").unwrap()
    );
    assert_eq!(
        expected,
        serde_yaml::from_str("Fn::Split: [\",\", \"hello,world\"]").unwrap()
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

// Functions are boolean operators and Conditions top level must end in a boolean, so this tests
// confirm failures for using intrinsics incorrectly.
#[test]
fn condition_function_failure() {
    let x: serde_yaml::Result<ConditionFunction> = serde_yaml::from_str("!Ref LogicalID");
    let y: serde_yaml::Result<ConditionFunction> =
        serde_yaml::from_str("Fn::Cidr: [\"192.168.0.0/24\", 6, 5]");
    let x = x.err().unwrap().to_string();
    let y = y.err().unwrap().to_string();

    assert!(x.contains("unknown variant"));
    assert!(y.contains("unknown variant"));
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
