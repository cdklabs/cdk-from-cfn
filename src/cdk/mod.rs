mod schema;

#[doc(inline)]
pub use schema::*;

#[cfg(feature = "builtin-schema")]
include!(env!("GENERATED_CDK_SCHEMA_PATH"));
