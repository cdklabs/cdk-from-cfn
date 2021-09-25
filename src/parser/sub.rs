use crate::TransmuteError;
use nom::branch::alt;
use nom::bytes::complete::{tag, take, take_until};
use nom::combinator::map;
use nom::multi::many1;
use nom::sequence::delimited;
use nom::Err;
use nom::IResult;

#[derive(Debug, Clone, PartialEq)]
pub enum SubValue {
    String(String),
    Variable(String),
}

pub fn sub_parse_tree(str: &str) -> Result<Vec<SubValue>, TransmuteError> {
    let mut full_resolver = many1(inner_resolver);
    let str = match str.strip_prefix('\"') {
        None => str,
        Some(x) => x,
    };
    let str = match str.strip_suffix('\"') {
        None => str,
        Some(x) => x,
    };
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
fn inner_resolver(str: &str) -> IResult<&str, SubValue> {
    let ir = alt((
        map(
            delimited(tag("${"), take_until("}"), take(1usize)),
            |var: &str| SubValue::Variable(var.to_string()),
        ),
        map(take_until("${"), |static_str: &str| {
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
    fn it_works() -> Result<(), TransmuteError> {
        let prefix = String::from("arn:");
        let var = String::from("some_value");
        let postfix = String::from(":constant");

        let v = sub_parse_tree(format!("{}${{{}}}{}", prefix, var, postfix).as_str())?;
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
}
