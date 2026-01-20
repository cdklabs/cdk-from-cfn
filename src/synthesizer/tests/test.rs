// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

/// Macro for generating IR synthesizer test cases across multiple languages
#[macro_export]
macro_rules! ir_synthesizer_test {
    ($name:ident, $class_name:literal) => {
        mod $name {
            use super::*;

            #[cfg(feature = "csharp")]
            ir_synthesizer_test!($name, csharp, $class_name);

            #[cfg(feature = "golang")]
            ir_synthesizer_test!($name, golang, $class_name);

            #[cfg(feature = "java")]
            ir_synthesizer_test!($name, java, $class_name);

            #[cfg(feature = "python")]
            ir_synthesizer_test!($name, python, $class_name);

            #[cfg(feature = "typescript")]
            ir_synthesizer_test!($name, typescript, $class_name);
        }
    };

    ($name:ident, $lang:ident, $class_name:literal) => {
        mod $lang {
            use super::*;

            #[tokio::test]
            async fn test_stack() {
                let lang = stringify!($lang);

                let test = ClassTestCase::new(
                    module_path!(),
                    lang,
                    $class_name,
                    <Stack as IrClass>::generate_stack,
                );

                test.generated_class_file_matches_expected();

                if !cfg!(feature = "skip-clean") {
                    test.clean();
                }
            }

            #[tokio::test]
            async fn test_construct() {
                let lang = stringify!($lang);
                // Convert "BucketStack" to "BucketConstruct"
                let construct_name = $class_name.replace("Stack", "Construct");

                let test = ClassTestCase::new(
                    module_path!(),
                    lang,
                    &construct_name,
                    <Stack as IrClass>::generate_construct,
                );

                test.generated_class_file_matches_expected();

                if !cfg!(feature = "skip-clean") {
                    test.clean();
                }
            }
        }
    };
}
