use super::*;
use crate::Error;

#[test]
fn substitute_arn() -> Result<(), Error> {
    let prefix = String::from("arn:");
    let var = String::from("some_value");
    let postfix = String::from(":constant");
    // for those who don't want to read: arn:${some_value}:constant
    let v = sub_parse_tree(format!("{prefix}${{{var}}}{postfix}").as_str())?;
    assert_eq!(
        v,
        vec![
            SubValue::String(prefix),
            SubValue::Variable(var),
            SubValue::String(postfix)
        ]
    );

    Ok(())
}

#[test]
fn error_on_missing_brackets() {
    let v = sub_parse_tree("arn:${variable");
    assert!(v.is_err());
}

#[test]
fn sub_parse_error() {
    let error = sub_parse_tree("").unwrap_err();
    assert_eq!(
        "Parsing Error: Error { input: \"\", code: Eof }",
        error.to_string(),
    );
}

#[test]
fn empty_variable() -> Result<(), Error> {
    let v = sub_parse_tree("arn:${}")?;
    assert_eq!(
        v,
        vec![
            SubValue::String("arn:".to_string()),
            SubValue::Variable(String::new())
        ]
    );

    Ok(())
}

#[test]
fn test_suffix_substitution() -> Result<(), Error> {
    let v = sub_parse_tree("${Tag}-Concatenated")?;
    assert_eq!(
        v,
        vec![
            SubValue::Variable("Tag".to_string()),
            SubValue::String(String::from("-Concatenated"))
        ]
    );

    Ok(())
}

#[test]
fn test_no_substitution() -> Result<(), Error> {
    let v = sub_parse_tree("NoSubstitution")?;
    assert_eq!(v, vec![SubValue::String(String::from("NoSubstitution"))]);

    Ok(())
}

#[test]
fn test_quotes() -> Result<(), Error> {
    let v = sub_parse_tree("echo \"${lol}\"")?;
    assert_eq!(
        v,
        vec![
            SubValue::String(String::from("echo \"")),
            SubValue::Variable(String::from("lol")),
            SubValue::String(String::from("\"")),
        ]
    );

    Ok(())
}

// As quoted in the sub docs: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-sub.html
// To write a dollar sign and curly braces (${}) literally, add an exclamation point (!) after the open curly brace, such as ${!Literal}. CloudFormation resolves this text as ${Literal}.
#[test]
fn test_literal() -> Result<(), Error> {
    let v = sub_parse_tree("echo ${!lol}")?;
    assert_eq!(
        v,
        vec![
            SubValue::String(String::from("echo ")),
            SubValue::String(String::from("${lol}"))
        ]
    );

    Ok(())
}
