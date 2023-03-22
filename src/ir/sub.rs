use crate::TransmuteError;
use nom::branch::alt;
use nom::bytes::complete::{tag, take, take_until};
use nom::combinator::{map, rest};
use nom::error::{Error, ErrorKind};
use nom::multi::many1;
use nom::sequence::delimited;
use nom::Err;
use nom::IResult;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SubValue {
    String(String),
    Variable(String),
}

pub fn sub_parse_tree(str: &str) -> Result<Vec<SubValue>, TransmuteError> {
    let mut full_resolver = many1(inner_resolver);

    match full_resolver(str) {
        Ok((remaining, built_subs)) => {
            let mut subs = built_subs;
            if !remaining.is_empty() {
                subs.push(SubValue::String(remaining.to_string()))
            }
            Ok(subs)
        }

        Err(err) => match err {
            Err::Incomplete(_) => Err(TransmuteError::new("Should never enter this state")),
            Err::Error(e) => Err(TransmuteError::new(e.code.description())),
            Err::Failure(e) => Err(TransmuteError::new(e.code.description())),
        },
    }
}

/// inner_resolver will do one of the following:
/// * take until you see a ${ which is the start of the variable bits.
/// * take something like ${ ... }
/// TODO -- there are some Sub strings that will escape the $, that are not captured yet.
///         Will need to rewrite the parse tree to handle character escapes.
fn inner_resolver(str: &str) -> IResult<&str, SubValue> {
    // Due to the caller being many1, we will need to create out own EOF error to
    // stop the call pattern.
    if str.is_empty() {
        return IResult::Err(Err::Error(Error::new(str, ErrorKind::Eof)));
    }

    let ir = alt((
        map(
            delimited(tag("${!"), take_until("}"), take(1usize)),
            |var: &str| SubValue::String(format!("${{{var}}}")),
        ),
        // Attempt to find ${...} and eat those tokens.
        map(
            delimited(tag("${"), take_until("}"), take(1usize)),
            |var: &str| SubValue::Variable(var.to_string()),
        ),
        // Attempt to eat anything before ${
        map(take_until("${"), |static_str: &str| {
            SubValue::String(static_str.to_string())
        }),
        // Anything else is probably "the remaining tokens", consume the remaining tokens as no
        // other values were found.
        map(rest, |static_str: &str| {
            SubValue::String(static_str.to_string())
        }),
    ))(str);

    let (remaining, res) = ir?;
    IResult::Ok((remaining, res))
}

#[cfg(test)]
mod tests {

    use super::*;

    #[test]
    fn substitute_arn() -> Result<(), TransmuteError> {
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
    fn empty_variable() -> Result<(), TransmuteError> {
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
    fn test_suffix_substitution() -> Result<(), TransmuteError> {
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
    fn test_no_substitution() -> Result<(), TransmuteError> {
        let v = sub_parse_tree("NoSubstitution")?;
        assert_eq!(v, vec![SubValue::String(String::from("NoSubstitution"))]);

        Ok(())
    }

    #[test]
    fn test_quotes() -> Result<(), TransmuteError> {
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
    fn test_literal() -> Result<(), TransmuteError> {
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
}
