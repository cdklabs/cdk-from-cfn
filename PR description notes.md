PR description

I moved some logic out of the test_case macro and into functions to make it easier to work with, because auto-complete does not work inside macros. The macro is still necessary to avoid having to write a test module for each end-to-end test and a test fn for each language. https://github.com/rust-lang/rust-analyzer/issues/12524

Using environment variables instead of cli flags to configure the end to end test workflow, because passing cli args through to your test functions is not supported by Rust's libtest. (We could do this with a custom test binary implementation as a future improvement.)


I am keeping the generated CDK stack code in the snapshots, because this has been very helpful for reviewing changes to the code-gen. With this update, manual review of the generated CDK code is not necessary to verify that the generated code works, because the end-to-end tests now actually run `cdk synth` on them. The manual review is only for reviewing style, format, etc. of the generated code.


