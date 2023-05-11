use super::*;

#[test]
fn test_parameter_type_display() {
    assert_eq!(ParameterType::String.to_string(), "String");
    assert_eq!(ParameterType::Number.to_string(), "Number");
    assert_eq!(ParameterType::ListOfNumbers.to_string(), "List<Number>");
    assert_eq!(
        ParameterType::CommaDelimitedList.to_string(),
        "CommaDelimitedList"
    );
    assert_eq!(
        ParameterType::Other("CustomType".to_string()).to_string(),
        "CustomType"
    );
}
