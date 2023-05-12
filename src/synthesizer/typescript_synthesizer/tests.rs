use super::*;

#[test]
fn pretty_name_fixes() {
    assert_eq!("vpc", pretty_name("VPC"));
    assert_eq!("vpcs", pretty_name("VPCs"));
    assert_eq!("objectAccess", pretty_name("GetObject"));
    assert_eq!("equalTo", pretty_name("Equals"));
    assert_eq!("providerArns", pretty_name("ProviderARNs"));
    assert_eq!("targetAZs", pretty_name("TargetAZs"));
    assert_eq!("diskSizeMBs", pretty_name("DiskSizeMBs"));
}
