mod schema;

#[doc(inline)]
pub use schema::*;

include!(env!("GENERATED_CDK_SCHEMA_PATH"));
