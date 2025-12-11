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

clippy *args:
    cargo clippy --tests {{args}} -- -Adead-code -Dwarnings -Dclippy::dbg_macro

fix: (clippy "--fix --allow-dirty")
	cargo fmt

test-cov:
		cargo llvm-cov --features update-snapshots,skip-clean --no-fail-fast --lcov --output-path target/lcov.info

install-tools:
		cargo install cargo-llvm-cov
