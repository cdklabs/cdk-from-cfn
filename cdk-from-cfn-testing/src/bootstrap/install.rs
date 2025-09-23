// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use crate::{
    filesystem::{Files, Paths, Zip},
    Scope,
};

use super::app::AppFile;

/// Installer for CDK application boilerplate and configuration files.
/// 
/// Manages the extraction and generation of language-specific CDK application
/// files needed for end-to-end testing, including boilerplate code and app files.
pub struct Install<'a> {
    /// Test scope containing language and test metadata
    scope: &'a Scope,
}

impl<'a> Install<'a> {
    /// Creates a new installer for the specified test scope.
    /// 
    /// # Arguments
    /// * `scope` - Test scope containing language and test information
    /// 
    /// # Returns
    /// A new `Install` instance for the given scope
    pub fn new(scope: &'a Scope) -> Self {
        Self { scope }
    }

    /// Extracts language-specific boilerplate files for CDK applications.
    /// 
    /// Unpacks pre-packaged boilerplate files (package.json, requirements.txt, etc.)
    /// that are needed for the CDK application to build and run properly.
    pub fn boilerplate_files(&self) {
        Zip::extract_boilerplate_files(&self.scope.lang, &self.scope.normalized);
    }

    /// Generates and writes the main CDK application file.
    /// 
    /// Creates a language-specific app file by rendering a template with the
    /// provided stack name and environment configuration.
    /// 
    /// # Arguments
    /// * `stack_name` - Name of the CDK stack class to generate
    /// * `include_env` - Whether to include environment configuration in the app
    pub fn app_file(&self, stack_name: &str, include_env: bool) {
        let lang = &self.scope.lang;
        let app_writer = Zip::extract_app_writer(lang);
        let mut app_file = AppFile::new();
        app_file
            .set("STACK_CLASS_NAME", stack_name)
            .set("STACK_NAME", &Paths::e2e_name(stack_name))
            .set_bool("INCLUDE_ENV", include_env);

        let rendered = app_file.render(&app_writer);
        Files::write_app_file(&self.scope.normalized, lang, &rendered);
    }
}
