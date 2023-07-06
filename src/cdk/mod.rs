mod schema;

#[doc(inline)]
pub use schema::*;

#[cfg(feature = "cdk-schema-default")]
include!(env!("GENERATED_CDK_SCHEMA_PATH"));
