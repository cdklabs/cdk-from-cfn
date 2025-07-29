# Contributing to cdk-from-cfn

We welcome contributions to the cdk-from-cfn project! This guide will help you get started with contributing.

## Development Environment Setup

### Prerequisites

- [Rust](https://www.rust-lang.org/tools/install) (Latest stable version)
- [Wasm-Pack](https://github.com/rustwasm/wasm-pack?tab=readme-ov-file)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [GitHub Account](https://github.com/join)

### Getting the Project

```bash
# Clone your fork
gh repo fork cdklabs/cdk-from-cfn
# Or manually clone
git clone https://github.com/YOUR_USERNAME/cdk-from-cfn.git
cd cdk-from-cfn
```

## Building the Project

```bash
# build the debug target
cargo build

# build the release target
cargo build --release

# build the wasm release
wasm-pack build --all-features --target=nodejs
```

## Testing the Project

```bash
# run all tests
cargo test

# run clippy to lint
cargo clippy
```
