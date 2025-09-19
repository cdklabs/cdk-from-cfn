// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use cdk_from_cfn_macros::generate_cdk_tests;
use cdk_from_cfn_testing::{CdkAppTestCase, CdkAppTestGroup, Language, Scope, SkipSynthList};
#[cfg(feature = "end-to-end")]
use cdk_from_cfn_testing_end_to_end::EndToEndTest;

use futures::future::join_all;

/// Macro for generating CDK stack synthesis test cases across multiple languages
#[macro_export]
macro_rules! cdk_stack_synth_test {
    ($name:ident, $stack_name:literal) => {
        cdk_stack_synth_test!($name, $stack_name, &[]);
    };

    ($name:ident, $stack_name:literal, $skip_cdk_synth:expr) => {
        mod $name {
            use super::*;

            #[tokio::test]
            async fn test() {
                let test_name = stringify!($name);

                eprintln!("🚀 Starting test group: {}", test_name);
                // Installs everything
                let app = CdkAppTestCase::new(module_path!(), $stack_name, $skip_cdk_synth);

                #[cfg(feature = "end-to-end")]
                let end_to_end = EndToEndTest::generate(&app).await;

                let mut language_futures = Vec::new();
                let languages = Language::get_enabled_languages();
                for lang in languages {
                    language_futures.push(run_language_test(
                        lang.clone(),
                        &app,
                        #[cfg(feature = "end-to-end")]
                        &end_to_end,
                    ));
                }

                // Run all language tests
                join_all(language_futures).await;
                eprintln!("✅ Test group {} completed", stringify!($name));

                // Cleanup
                if !cfg!(feature = "skip-clean") {
                    #[cfg(feature = "end-to-end")]
                    end_to_end.clean().await;

                    for scope in app.scopes {
                        CdkAppTestCase::clean(&scope);
                    }
                }
            }

            async fn run_language_test(
                lang: String,
                app: &CdkAppTestGroup<'_>,
                #[cfg(feature = "end-to-end")] end_to_end: &EndToEndTest<'_>,
            ) {
                {
                    eprintln!(
                        "🚀 Starting test: cdk_stack_synth {}::{}",
                        app.test_name, lang
                    );

                    let scope = Scope::new(module_path!(), &lang);
                    let test = CdkAppTestCase::from_scope(&scope, &app);

                    test.generated_stack_file_matches_expected();
                    if test.did_synth {
                        test.cdk_out_matches_cfn_stack_file();
                        test.synthesized_apps_match_each_other();
                        #[cfg(feature = "end-to-end")]
                        end_to_end.run(&scope).await;
                    }
                }

                eprintln!(
                    "  ✅ Completed: cdk_stack_synth {}::{}",
                    app.test_name, lang
                );
            }
        }
    };
}

generate_cdk_tests!();
