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
// Using github cli
gh repo fork cdklabs/cdk-from-cfn
cd cdk-from-cfn
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

Following guidance is for making changes in your fork and pushing changes to your fork's remote:

```console
git status
git add <file-name or .>
git commit -m "<commit message following https://www.conventionalcommits.org/en/v1.0.0/#summary>"
git push
```

Once you have done the above, you can then [create a PR from your fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork).
