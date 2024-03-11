// use serde::de::Error;

// #[test]
// fn test_transmute_error() {
//     let error = crate::Error::TransmuteError {
//         details: "Test error message".to_string(),
//     };

//     assert_eq!(error.details, "Test error message");
//     assert_eq!(error.to_string(), "TransmuteError: Test error message");
// }

// #[test]
// fn test_transmute_error_from() {
//     let yaml_error = serde_yaml::Error::custom("YAML parsing error");
//     let transmute_error: crate::Error = yaml_error.into();

//     assert_eq!(transmute_error.details, "YAML parsing error");
// }
