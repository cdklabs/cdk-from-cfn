// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
mod schema;

#[doc(inline)]
pub use schema::*;

include!(env!("GENERATED_CDK_SCHEMA_PATH"));
