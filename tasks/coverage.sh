#/usr/bin/env bash
set -euo pipefail

COVERAGE_ROOT="${PWD}/target/coverage"

mkdir -p ${COVERAGE_ROOT}/profraw

if ! command -v grcov >/dev/null; then
  echo 'Installing grcov...'
  cargo install grcov
fi

if ! rustup component list --installed | grep -e '^llvm-tools' >/dev/null; then
  echo 'Installing the llvm-tools-preview rustup component...'
  rustup component add llvm-tools-preview
fi

# We trap EXIT to collect coverage & clean-up profraw files...
function after_tests(){
  echo 'Generating coverage reports...'
  grcov "${COVERAGE_ROOT}/profraw"                                              \
    --binary-path "${COVERAGE_ROOT}/deps"                                       \
    --source-dir "${PWD}"                                                       \
    --output-types "html,lcov"                                                  \
    --branch                                                                    \
    --ignore-not-existing                                                       \
    --keep-only "src/*"                                                         \
    --ignore "src/main.rs"                                                      \
    --output-path "${COVERAGE_ROOT}"                                            \
    --commit-sha $(git rev-parse HEAD)                                          \
    --service-name "noctilucent"

  # Rename `lcov` to a name that is aligned with what IDEs usually look for...
  mv "${COVERAGE_ROOT}/lcov" "${COVERAGE_ROOT}/lcov.info"

  echo 'Cleaning up...'
  rm -rf "${COVERAGE_ROOT}/profraw"
}
trap after_tests EXIT

echo 'Running tests with coverage instrumentation...'
RUSTFLAGS='-Cinstrument-coverage'                                               \
LLVM_PROFILE_FILE="${COVERAGE_ROOT}/profraw/%p-%m.profraw"                      \
cargo test --profile=coverage
