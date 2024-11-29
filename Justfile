alias b := build
alias r := release

release: build test lint

build:
		cargo build --all-features

test *TEST:
    cargo test {{TEST}}

lint: fmt clippy

fmt:
		cargo fmt -- --version && cargo fmt --check

clippy:
    cargo clippy --tests -- -Adead-code -Dwarnings -Dclippy::dbg_macro

test-cov:
		cargo llvm-cov --all-features --ignore-filename-regex '^(tests/.*\.rs|.*/tests\.rs)$' --no-fail-fast --lcov --output-path target/lcov.info

install-tools:
		cargo install cargo-llvm-cov