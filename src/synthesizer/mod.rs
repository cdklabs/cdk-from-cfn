// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use std::io;
use std::str::FromStr;

use crate::{ir::CloudformationProgramIr, Error};

#[derive(Clone, Copy, Debug, PartialEq, Default)]
pub enum ClassType {
    #[default]
    Stack,
    Construct,
}

impl FromStr for ClassType {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "stack" => Ok(ClassType::Stack),
            "construct" => Ok(ClassType::Construct),
            _ => Err(format!(
                "Invalid class type: '{}'. Expected 'stack' or 'construct'",
                s
            )),
        }
    }
}

#[cfg(feature = "csharp")]
mod csharp;
#[cfg(feature = "csharp")]
#[doc(inline)]
pub use csharp::*;

#[cfg(feature = "golang")]
mod golang;
#[cfg(feature = "golang")]
#[doc(inline)]
pub use golang::*;

#[cfg(feature = "java")]
mod java;
#[cfg(feature = "java")]
#[doc(inline)]
pub use java::*;

#[cfg(feature = "typescript")]
mod typescript;
#[cfg(feature = "typescript")]
#[doc(inline)]
pub use typescript::*;

#[cfg(feature = "python")]
mod python;
#[cfg(feature = "python")]
#[doc(inline)]
pub use python::*;

pub trait Synthesizer {
    fn synthesize(
        &self,
        ir: CloudformationProgramIr,
        into: &mut dyn io::Write,
        stack_name: &str,
        class_type: ClassType,
    ) -> Result<(), Error>;
}

impl CloudformationProgramIr {
    #[inline(always)]
    pub fn synthesize(
        self,
        language: &str,
        into: &mut impl io::Write,
        stack_name: &str,
        class_type: ClassType,
    ) -> Result<(), Error> {
        let synthesizer: Box<dyn Synthesizer> = match language {
            #[cfg(feature = "csharp")]
            "csharp" => Box::<CSharp>::default(),
            #[cfg(feature = "golang")]
            "go" => Box::<Golang>::default(),
            #[cfg(feature = "java")]
            "java" => Box::<Java>::default(),
            #[cfg(feature = "python")]
            "python" => Box::new(Python {}),
            #[cfg(feature = "typescript")]
            "typescript" => Box::new(Typescript {}),
            _ => {
                return Err(Error::UnsupportedLanguageError {
                    language: language.into(),
                })
            }
        };
        synthesizer.synthesize(self, into, stack_name, class_type)
    }
}

#[cfg(test)]
mod tests;
