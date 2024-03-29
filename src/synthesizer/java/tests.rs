use crate::ir::importer::ImportInstruction;

#[test]
fn test_invalid_organization() {
    let bad_org = "NotAws";
    let import_instruction = ImportInstruction {
      organization: bad_org.to_string(),
      service: Option::None,
    };
    let result = import_instruction.to_java_import().unwrap_err();
    let expected = format!("Expected organization to be AWS or Alexa. Found {bad_org}");
    assert_eq!(expected, result.to_string());
}
