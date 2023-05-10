#/usr/bin/env bash
set -euo pipefail

COVERAGE_ROOT="${PWD}/target/coverage"

mkdir -p ${COVERAGE_ROOT}/profraw

if ! command -v grcov >/dev/null; then
  echo 'Installing grcov...'
  cargo install grcov
fi

# We trap EXIT to collect coverage & clean-up profraw files...
function after_tests(){
  echo 'Generating coverage reports...'
  grcov "${COVERAGE_ROOT}"                                                      \
    --binary-path "${COVERAGE_ROOT}"                                            \
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
  rm -rf "${COVERAGE_ROOT}/deps/*.gcda"
}
trap after_tests EXIT

echo 'Running tests with coverage instrumentation...'
RUSTC_BOOTSTRAP=1                                                               \
RUSTFLAGS='-Zprofile -Clink-dead-code -Coverflow-checks=off'                    \
cargo test --profile=coverage
