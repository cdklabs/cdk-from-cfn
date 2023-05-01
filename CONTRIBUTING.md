# Contributing

This document describes how to set up a development environment and submit your changes.

## Getting Started

### Setup

#### Required

- [Rust](https://www.rust-lang.org/tools/install)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [GitHub account](https://github.com/join)

#### Recommended

- [Brew](https://docs.brew.sh/Installation)
- IDE
  - [VSCode](https://code.visualstudio.com/download)
  - [IntelliJ](https://www.jetbrains.com/idea/download)
- [GitHub CLI](https://cli.github.com/)

```console
gh repo fork iph/noctilucent
cd noctilucent
cargo build
```

### Tests

```console
cargo test
```

```console
./tasks/coverage.sh
```

### Making changes

```console
git status
git add CONTRIBUTING.md
git commit -m "chore: Adding a contributing guide"
git push
```

