// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

mod filter;
mod test;

pub use filter::{SkipSynthList, TestFilter, TestSkip};
pub use test::{CdkAppTestCase, CdkAppTestGroup};

use std::{
    env::{temp_dir, var},
    error::Error,
    path::{Path, PathBuf},
    process::{id, Command, Output},
    sync::atomic::{AtomicU64, Ordering},
};

use crate::{
    filesystem::{Files, Paths},
    Scope,
};

/// CDK synthesis orchestrator for generating CloudFormation templates.
///
/// Manages the CDK synthesis process including workspace setup, environment configuration,
/// and execution of the CDK CLI to generate CloudFormation templates from CDK code.
pub struct Synthesizer<'a> {
    /// Test scope containing language and test metadata
    scope: &'a Scope,
    /// AWS region for synthesis environment
    region: &'a str,
    /// Optional temporary directory for C# builds
    temp_dir: Option<PathBuf>,
}

impl<'a> Synthesizer<'a> {
    /// Creates a new CDK synthesizer for the specified scope and region.
    ///
    /// # Arguments
    /// * `scope` - Test scope containing language and test metadata
    /// * `region` - AWS region for synthesis environment
    ///
    /// # Returns
    /// A new `Synthesizer` instance
    pub fn new(scope: &'a Scope, region: &'a str) -> Self {
        Self {
            scope,
            region,
            temp_dir: None,
        }
    }

    /// Executes CDK synthesis to generate CloudFormation templates.
    ///
    /// Sets up the working directory, runs CDK synthesis with appropriate environment
    /// variables, and cleans up temporary files. Handles language-specific requirements
    /// like C# temporary directory setup.
    ///
    /// # Panics
    /// Panics if CDK synthesis fails or produces errors
    pub fn synth(&mut self) {
        self.temp_dir = self.setup_working_directory();
        let output = self.run_cdk_synth();

        if let Some(ref temp_dir) = self.temp_dir {
            Files::cleanup_temp_directory(temp_dir, &self.scope).ok();
        }

        assert!(
            output.status.success(),
            "❌ CDK synth failed for {} ({}) \n{}{}",
            self.scope.test,
            self.scope.lang,
            format!(
                "{std_out}",
                std_out = if !output.stdout.is_empty() {
                    format!("STDOUT:\n{}\n", String::from_utf8_lossy(&output.stdout))
                } else {
                    "".to_string()
                }
            ),
            format!(
                "{std_err}",
                std_err = if !output.stderr.is_empty() {
                    format!("STDERR:\n{}\n", String::from_utf8_lossy(&output.stderr))
                } else {
                    "".to_string()
                }
            )
        );
    }

    /// Sets up a working directory for synthesis, if needed.
    ///
    /// Creates a temporary directory for C# projects to handle build artifacts
    /// and avoid conflicts. Other languages use the actual directory directly.
    ///
    /// # Returns
    /// Optional path to temporary directory (C# only)
    fn setup_working_directory(&self) -> Option<PathBuf> {
        if self.scope.lang == "csharp" {
            Files::setup_temp_directory(&self.scope).ok()
        } else {
            None
        }
    }
    /// Executes the CDK synthesis command with appropriate environment setup.
    ///
    /// Configures environment variables for shared installations, language-specific
    /// tools, and AWS region settings before running CDK synthesis.
    ///
    /// # Returns
    /// Command output from CDK synthesis
    ///
    /// # Panics
    /// Panics if the CDK command cannot be executed
    fn run_cdk_synth(&self) -> Output {
        let cdk_path = Paths::cdk_path();

        let result = Command::new(&cdk_path)
            .args([
                "synth",
                "--no-path-metadata",
                "--no-version-reporting",
                "--no-notices",
            ])
            .current_dir(
                self.temp_dir
                    .as_ref()
                    .unwrap_or(&Paths::actual_dir_path(&self.scope.normalized)),
            )
            .env("CDK_DEFAULT_REGION", &self.region)
            .env("AWS_DEFAULT_REGION", &self.region)
            .env("PROJECT_ROOT", Paths::project_root())
            .env("CDK_PATH", &cdk_path)
            .env("PYTHON_EXECUTABLE", Paths::python_executable())
            .env("MAVEN_REPO", Paths::maven_repository())
            .env("GOMODCACHE", Paths::go_mod_cache())
            .env("NODE_PATH", Paths::shared_node_modules())
            .env(
                "PATH",
                format!(
                    "{}:{}",
                    Paths::shared_node_modules().join(".bin").display(),
                    var("PATH").unwrap_or_default()
                ),
            )
            .output();

        assert!(
            result.is_ok(),
            "❌ Failed to execute 'cdk synth' on {}: {:?}",
            cdk_path.display(),
            result.err()
        );
        result.unwrap()
    }
}

// Paths that are unique to cdk synth
impl Paths {
    /// Returns the shared installations directory path.
    ///
    /// # Returns
    /// Path to shared language installations and tools
    fn shared_installations_dir() -> PathBuf {
        PathBuf::from(option_env!("SHARED_INSTALLATIONS_DIR").unwrap())
    }

    /// Returns the Python executable path from shared installations.
    ///
    /// # Returns
    /// Path to the Python3 executable in the shared virtual environment
    fn python_executable() -> PathBuf {
        Self::shared_installations_dir()
            .join(Self::PYTHON_VENV)
            .join(Self::BIN)
            .join("python3")
    }

    /// Returns the shared Node.js modules directory path.
    ///
    /// # Returns
    /// Path to shared node_modules directory
    fn shared_node_modules() -> PathBuf {
        Self::shared_installations_dir().join(Self::NODE_MODULES)
    }

    /// Returns the Go module cache directory path.
    ///
    /// # Returns
    /// Path to Go module cache for dependency management
    fn go_mod_cache() -> PathBuf {
        Self::shared_installations_dir().join(Self::GO_CACHE_DIR)
    }

    /// Returns the Maven repository directory path.
    ///
    /// # Returns
    /// Path to Maven local repository for Java dependencies
    fn maven_repository() -> PathBuf {
        Self::shared_installations_dir().join(".m2/repository")
    }

    /// Returns the CDK CLI executable path.
    ///
    /// # Returns
    /// Path to the CDK binary in shared Node.js installations
    fn cdk_path() -> PathBuf {
        Self::shared_installations_dir()
            .join(Self::NODE_MODULES)
            .join(".bin")
            .join(Self::CDK)
    }
}

// Files that are unique to cdk synth
impl Files {
    /// Sets up a temporary directory for C# synthesis.
    ///
    /// Creates a unique temporary directory, cleans build artifacts from the source,
    /// and copies the source files to the temporary location for isolated builds.
    ///
    /// # Arguments
    /// * `scope` - Test scope containing test metadata
    ///
    /// # Returns
    /// Result containing the temporary directory path or error
    pub fn setup_temp_directory(scope: &Scope) -> Result<PathBuf, Box<dyn Error>> {
        static TEMP_COUNTER: AtomicU64 = AtomicU64::new(0);

        let counter = TEMP_COUNTER.fetch_add(1, Ordering::SeqCst);
        let temp_dir = temp_dir().join(format!("cdk_test_{}_{}", id(), counter));
        let source_dir = Paths::actual_dir_path(&scope.normalized);
        Self::create_dir_all(&temp_dir);

        // Clean build artifacts from source before copying
        Command::new("rm")
            .args(["-rf", &format!("{}/bin", source_dir.to_string_lossy())])
            .output()?;
        Command::new("rm")
            .args(["-rf", &format!("{}/obj", source_dir.to_string_lossy())])
            .output()?;

        Command::new("cp")
            .args([
                "-a",
                &format!("{}/.", source_dir.to_string_lossy()),
                &temp_dir.to_string_lossy(),
            ])
            .output()?;

        Ok(temp_dir)
    }

    /// Cleans up temporary directory and copies synthesis results back.
    ///
    /// Copies the CDK output directory from the temporary location back to the
    /// original directory, then removes the temporary directory.
    ///
    /// # Arguments
    /// * `temp_dir` - Temporary directory to clean up
    /// * `scope` - Test scope containing test metadata
    ///
    /// # Returns
    /// Result indicating success or error
    pub fn cleanup_temp_directory(temp_dir: &Path, scope: &Scope) -> Result<(), Box<dyn Error>> {
        let cdk_out_src = temp_dir.join(Paths::CDK_OUT_DIR);
        let original_dir = Paths::actual_dir_path(&scope.normalized);

        if cdk_out_src.exists() {
            Command::new("cp")
                .args([
                    "-r",
                    &cdk_out_src.to_string_lossy(),
                    &original_dir.to_string_lossy(),
                ])
                .output()?;
        }

        Self::cleanup_directory(temp_dir);
        Ok(())
    }
}
