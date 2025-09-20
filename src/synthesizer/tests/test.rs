// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

/// Macro for generating IR synthesizer test cases across multiple languages
#[macro_export]
macro_rules! ir_synthesizer_test {
    ($name:ident, $stack_name:literal) => {
        mod $name {
            use super::*;

            #[cfg(feature = "csharp")]
            ir_synthesizer_test!($name, csharp, $stack_name);

            #[cfg(feature = "golang")]
            ir_synthesizer_test!($name, golang, $stack_name);

            #[cfg(feature = "java")]
            ir_synthesizer_test!($name, java, $stack_name);

            #[cfg(feature = "python")]
            ir_synthesizer_test!($name, python, $stack_name);

            #[cfg(feature = "typescript")]
            ir_synthesizer_test!($name, typescript, $stack_name);
        }
    };

    ($name:ident, $lang:ident, $stack_name:literal) => {
        mod $lang {
            use super::*;

            #[tokio::test]
            async fn test() {
                let lang = stringify!($lang);

                let test = StackTestCase::new(
                    module_path!(),
                    lang,
                    $stack_name,
                    <Stack as IrStack>::generate_stack,
                );

                test.generated_stack_file_matches_expected();

                if !cfg!(feature = "skip-clean") {
                    test.clean();
                }
            }
        }
    };
}
