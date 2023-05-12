#/usr/bin/env bash
set -euo pipefail

# Install llvm-tools component if needed...
rustup component add llvm-tools

# Install cargo-llvm-cov if it's not already there...
if ! command -v cargo-llvm-cov >/dev/null; then
  echo 'Installing cargo-llvm-cov...'
  cargo install cargo-llvm-cov
fi

cargo llvm-cov                                                                  \
  --all-features                                                                \
  --ignore-filename-regex '^(tests/.*\.rs|.*/tests\.rs)$'                       \
  --no-fail-fast                                                                \
  --lcov --output-path target/lcov.info

cargo llvm-cov report                                                           \
  --hide-instantiations                                                         \
  --ignore-filename-regex '^(tests/.*\.rs|.*/tests\.rs)$'                       \
  --codecov --output-path target/codecov.json

cargo llvm-cov report                                                           \
  --hide-instantiations                                                         \
  --ignore-filename-regex '^(tests/.*\.rs|.*/tests\.rs)$'                       \
  --html --output-dir target/coverage

cargo llvm-cov report                                                           \
  --ignore-filename-regex '^(tests/.*\.rs|.*/tests\.rs)$'
