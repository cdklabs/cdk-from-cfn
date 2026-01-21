// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use std::fs::{
    create_dir_all, read_dir, read_to_string, remove_dir, remove_dir_all, remove_file, write, File,
};
use std::io::Read;
use std::path::{Path, PathBuf};
use std::sync::Mutex;

use zip::read::ZipFile;
use zip::ZipArchive;

use crate::Scope;

use super::paths::Paths;

/// Thread-safe lock for directory creation to prevent race conditions
static DIR_CREATION_LOCK: Mutex<()> = Mutex::new(());

/// File system operations for test case management.
///
/// Provides thread-safe file I/O operations for reading and writing test files,
/// managing test directories, and handling cleanup operations.
pub struct Files;

impl Files {
    /// Reads a file and returns its contents as a string.
    ///
    /// # Arguments
    /// * `path` - Path to the file to read
    ///
    /// # Returns
    /// Result containing file contents or error message
    fn read(path: &Path) -> Result<String, String> {
        read_to_string(path).map_err(|e| format!("Failed to read file {}: {}", path.display(), e))
    }

    /// Writes content to a file, creating parent directories if needed.
    ///
    /// # Arguments
    /// * `path` - Path where to write the file
    /// * `content` - Content to write to the file
    ///
    /// # Panics
    /// Panics if the file cannot be written
    fn write(path: &Path, content: &str) {
        Self::create_parent_dirs(path);
        let result = write(path, content);
        assert!(
            result.is_ok(),
            "❌ Failed to write file {}: {}",
            path.display(),
            result.err().unwrap()
        );
    }

    /// Creates parent directories for a file path if they don't exist.
    ///
    /// Uses a mutex lock to prevent race conditions during concurrent directory creation.
    ///
    /// # Arguments
    /// * `path` - File path whose parent directories should be created
    fn create_parent_dirs(path: &Path) {
        if let Some(parent) = path.parent() {
            let _lock = DIR_CREATION_LOCK.lock().unwrap_or_else(|e| e.into_inner());
            Self::create_dir_all(parent);
        }
    }

    /// Recursively cleans up a test directory and empty parent directories.
    ///
    /// Removes the specified directory and walks up the parent chain,
    /// removing empty directories until reaching the actual directory root.
    ///
    /// # Arguments
    /// * `test_working_dir` - Directory to clean up
    pub(crate) fn cleanup_directory(test_working_dir: &Path) {
        let _lock = DIR_CREATION_LOCK.lock().unwrap_or_else(|e| e.into_inner());

        remove_dir_all(test_working_dir).ok();

        let mut parent = test_working_dir.parent();
        while let Some(dir) = parent {
            if dir
                .read_dir()
                .map_or(true, |mut entries| entries.next().is_none())
            {
                remove_dir(dir).ok();
                parent = dir.parent();
            } else {
                break;
            }
            if let Some(name) = dir.file_name() {
                if name == Paths::ACTUAL_DIR {
                    break;
                }
            }
        }
    }

    /// Loads the actual generated class file for a test case.
    ///
    /// # Arguments
    /// * `scope` - Test scope containing language and test metadata
    /// * `class_name` - Name of the class to load
    ///
    /// # Returns
    /// Contents of the actual class file
    ///
    /// # Panics
    /// Panics if the file cannot be read
    pub fn load_actual_class(scope: &Scope, class_name: &str) -> String {
        let path = Paths::actual_class_path(&scope.normalized, &scope.lang, class_name);
        let result = Self::read(&path);
        assert!(
            result.is_ok(),
            "❌ Failed to read actual output {}: {}",
            path.display(),
            result.err().unwrap()
        );
        result.unwrap()
    }

    /// Loads the expected class file for a test case.
    ///
    /// Used when updating snapshots to load the current expected output.
    ///
    /// # Arguments
    /// * `test_name` - Name of the test case
    /// * `lang` - Programming language
    /// * `class_name` - Name of the class (stack or construct)
    ///
    /// # Returns
    /// Contents of the expected class file
    ///
    /// # Panics
    /// Panics if the file cannot be found or read
    #[cfg_attr(not(feature = "update-snapshots"), allow(dead_code))]
    pub fn load_expected_class(test_name: &str, lang: &str, class_name: &str) -> String {
        let expected_path = Paths::expected_class_path(test_name, lang, class_name);
        let result = Self::read(&expected_path);
        assert!(
            result.is_ok(),
            "❌ Failed to read expected class file at {:?}: {}",
            expected_path.display(),
            result.err().unwrap(),
        );
        result.unwrap()
    }

    /// Writes the expected class file for a test case.
    ///
    /// # Arguments
    /// * `scope` - Test scope containing language and test metadata
    /// * `class_name` - Name of the class
    /// * `content` - class content to write
    pub fn write_expected_class(scope: &Scope, class_name: &str, content: &str) {
        let path = Paths::expected_class_path(&scope.test, &scope.lang, class_name);
        Self::write(&path, content);
    }

    /// Writes the actual generated class file for a test case.
    ///
    /// # Arguments
    /// * `scope` - Test scope containing language and test metadata
    /// * `class_name` - Name of the class
    /// * `content` - Class content to write
    pub fn write_actual_class(scope: &Scope, class_name: &str, content: &str) {
        let path = Paths::actual_class_path(&scope.normalized, &scope.lang, class_name);
        Self::write(&path, content);
    }

    /// Loads the CDK-synthesized CloudFormation template.
    ///
    /// # Arguments
    /// * `scope` - Test scope containing language and test metadata
    /// * `class_name` - Name of the class
    ///
    /// # Returns
    /// Contents of the synthesized CloudFormation template
    ///
    /// # Panics
    /// Panics if the template cannot be read
    pub fn load_actual_synthesized_template(scope: &Scope, class_name: &str) -> String {
        let path = Paths::synthesized_template_path(&scope.normalized, class_name);
        let result = Self::read(&path);
        assert!(
            result.is_ok(),
            "❌ Failed to read synthesized template from {}: {}",
            path.display(),
            result.err().unwrap()
        );
        result.unwrap()
    }

    /// Cleans up all files and directories for a test case.
    ///
    /// # Arguments
    /// * `scope` - Test scope containing test metadata
    pub fn cleanup_test(scope: &Scope) {
        let test_dir = Paths::actual_dir_path(&scope.normalized);
        Self::cleanup_directory(&test_dir);
    }

    /// Creates a directory and all parent directories.
    ///
    /// # Arguments
    /// * `path` - Directory path to create
    ///
    /// # Panics
    /// Panics if the directory cannot be created
    pub fn create_dir_all(path: &Path) {
        let result = create_dir_all(path);
        assert!(
            result.is_ok(),
            "❌ Failed to create directory {}: {}",
            path.display(),
            result.err().unwrap()
        );
    }

    /// Checks if an acceptable diff file exists for a test case.
    ///
    /// # Arguments
    /// * `test_name` - Name of the test case
    ///
    /// # Returns
    /// `true` if the acceptable diff file exists, `false` otherwise
    pub fn acceptable_diff_exists(test_name: &str) -> bool {
        let path = Paths::acceptable_diff_path(test_name);
        path.exists()
    }

    /// Deletes the acceptable diff file for a test case.
    ///
    /// # Arguments
    /// * `test_name` - Name of the test case
    ///
    /// # Panics
    /// Panics if the file cannot be deleted
    pub fn delete_acceptable_diff(test_name: &str) {
        let path = Paths::acceptable_diff_path(test_name);
        let result = remove_file(&path);
        assert!(
            result.is_ok(),
            "❌ Failed to delete acceptable diff {}: {}",
            path.display(),
            result.err().unwrap()
        );
    }

    /// Writes an acceptable diff file for a test case.
    ///
    /// # Arguments
    /// * `test_name` - Name of the test case
    /// * `content` - Diff content to write
    pub fn write_acceptable_diff(test_name: &str, content: &str) {
        Self::write(&Paths::acceptable_diff_path(test_name), content);
        println!("  🪄  Updated {} for {test_name}", Paths::ACCEPTABLE_DIFF);
    }

    /// Writes the main CDK application file.
    ///
    /// # Arguments
    /// * `normalized` - Normalized test identifier
    /// * `lang` - Programming language
    /// * `content` - Application file content
    pub fn write_app_file(normalized: &str, lang: &str, content: &str) {
        let dest_path = Paths::app(normalized, lang);
        Self::write(&dest_path, content);
    }
}

/// ZIP archive operations for extracting test case data.
///
/// Provides methods to extract templates, class files, and boilerplate code
/// from compressed test case archives.
pub struct Zip;

impl Zip {
    /// Extracts the main CloudFormation template for a test case.
    ///
    /// # Arguments
    /// * `test_name` - Name of the test case
    ///
    /// # Returns
    /// CloudFormation template content as a string
    ///
    /// # Panics
    /// Panics if the template cannot be extracted or is missing
    pub fn extract_template(test_name: &str) -> String {
        let result = Self::extract(&Paths::zip_case_path(test_name, Paths::TEMPLATE));
        assert!(
            result.is_ok(),
            "❌ Failed to extract template due to error: {}. Please ensure you have added your test case (a '{}' file) to {}",
            result.err().unwrap(),
            Paths::TEMPLATE,
            Paths::cases_dir(test_name).to_string_lossy()
        );
        result.unwrap()
    }

    /// Extracts the dependency class template for a test case, if it exists.
    ///
    /// # Arguments
    /// * `test_name` - Name of the test case
    ///
    /// # Returns
    /// Optional dependency template content
    pub fn extract_dependency_template(test_name: &str) -> Option<String> {
        let result = Self::extract(&Paths::zip_case_path(test_name, Paths::DEPENDENCY_TEMPLATE));
        result.ok()
    }

    /// Extracts the expected class file for a specific language.
    ///
    /// # Arguments
    /// * `test_name` - Name of the test case
    /// * `lang` - Programming language
    /// * `class_name` - Name of the class (stack or construct)
    ///
    /// # Returns
    /// Expected class file content
    ///
    /// # Panics
    /// Panics if the class file cannot be found or extracted
    pub fn extract_class_file(test_name: &str, lang: &str, class_name: &str) -> String {
        let archive = Self::open_zip_archive();
        let expected_filename = crate::Language::class_filename(lang, class_name);
        let expected_path = format!(
            "{}{}",
            Paths::zip_expected_dir(test_name, lang),
            expected_filename
        );

        let result = Self::extract_by_name(&expected_path, archive);
        if result.is_err() {
            // Fall back to finding any file in the directory (for backward compatibility)
            let archive = Self::open_zip_archive();
            let dir_prefix = Paths::zip_expected_dir(test_name, lang);
            let class_file = archive
                .file_names()
                .find(|name| name.starts_with(&dir_prefix) && !name.ends_with('/'))
                .unwrap_or_else(|| {
                    panic!(
                        "❌ No class file found in directory {} in zip (looking for {})",
                        dir_prefix, expected_filename
                    )
                })
                .to_string();

            let result = Self::extract_by_name(&class_file, Self::open_zip_archive());
            assert!(
                result.is_ok(),
                "❌ Failed to extract class file: {}",
                result.err().unwrap()
            );
            return result.unwrap();
        }
        result.unwrap()
    }

    /// Extracts the acceptable diff file for a test case.
    ///
    /// # Arguments
    /// * `test_name` - Name of the test case
    ///
    /// # Returns
    /// Result containing acceptable diff content or error message
    pub fn extract_acceptable_diff(test_name: &str) -> Result<String, String> {
        Self::extract(&Paths::zip_case_path(test_name, Paths::ACCEPTABLE_DIFF))
    }

    /// Extracts the application template file for a programming language.
    ///
    /// # Arguments
    /// * `lang` - Programming language
    ///
    /// # Returns
    /// Application template content
    ///
    /// # Panics
    /// Panics if the app writer template cannot be extracted
    pub fn extract_app_writer(lang: &str) -> String {
        let path = Paths::zip_app_writer_path(lang);
        let result = Self::extract(&path);
        assert!(
            result.is_ok(),
            "❌ Failed to extract app writer from {path} in zip: {}",
            result.err().unwrap()
        );
        result.unwrap()
    }

    /// Extracts all boilerplate files for a programming language.
    ///
    /// Extracts package.json, requirements.txt, and other language-specific
    /// files needed for CDK application setup.
    ///
    /// # Arguments
    /// * `lang` - Programming language
    /// * `normalized` - Normalized test identifier for destination directory
    ///
    /// # Panics
    /// Panics if boilerplate files cannot be extracted
    pub fn extract_boilerplate_files(lang: &str, normalized: &str) {
        let mut archive = Self::open_zip_archive();
        let dest_dir = Paths::actual_dir_path(normalized);
        let pattern = Paths::zip_boilerplate_dir(lang);

        for i in 0..archive.len() {
            let file_result = archive.by_index(i);
            assert!(
                file_result.is_ok(),
                "❌ Failed to access zip entry: {}",
                file_result.err().unwrap()
            );
            let file = file_result.unwrap();
            let path = file.name();

            if let Some(start) = path.find(&pattern) {
                if !path.ends_with('/') {
                    let relative = &path[start + pattern.len()..];
                    let dest = dest_dir.join(relative);

                    let contents = Self::read_to_string(file);
                    Files::write(&dest, &contents);
                }
            }
        }
    }
}

impl Zip {
    /// Extracts a specific file from a ZIP archive by name.
    ///
    /// # Arguments
    /// * `path` - Path of the file within the ZIP archive
    /// * `archive` - ZIP archive to extract from
    ///
    /// # Returns
    /// Result containing file contents or error message
    fn extract_by_name(path: &str, mut archive: ZipArchive<File>) -> Result<String, String> {
        let file = archive
            .by_name(path)
            .map_err(|_| format!("{path} not found in zip"))?;
        Ok(Self::read_to_string(file))
    }

    /// Reads a ZIP file entry to a string.
    ///
    /// # Arguments
    /// * `file` - ZIP file entry to read
    ///
    /// # Returns
    /// File contents as a string
    ///
    /// # Panics
    /// Panics if the file cannot be read
    fn read_to_string(mut file: ZipFile<'_, File>) -> String {
        let mut contents = String::new();
        let result = file.read_to_string(&mut contents);

        // If a file is found but cannot be read, fail the test immediately.
        assert!(
            result.is_ok(),
            "❌ Failed to read file from zip: {}",
            result.err().unwrap()
        );
        contents
    }

    /// Extracts a file from the ZIP archive by path.
    ///
    /// # Arguments
    /// * `zip_path` - Path of the file within the ZIP archive
    ///
    /// # Returns
    /// Result containing file contents or error message
    fn extract(zip_path: &str) -> Result<String, String> {
        let archive = Self::open_zip_archive();
        Self::extract_by_name(zip_path, archive)
    }

    /// Opens the test case ZIP archive.
    ///
    /// Uses the END_TO_END_SNAPSHOTS environment variable to locate the archive.
    ///
    /// # Returns
    /// Opened ZIP archive ready for extraction
    ///
    /// # Panics
    /// Panics if the archive cannot be opened or read
    fn open_zip_archive() -> ZipArchive<File> {
        let zip_path = option_env!("END_TO_END_SNAPSHOTS")
            .unwrap_or_else(|| "END_TO_END_SNAPSHOTS environment variable not set");
        let file_result = File::open(&zip_path);

        // If ever the zip cannot be opened or read (below), the tests cannot be run
        // so we'll use an assert to immediately end the test here.
        assert!(
            file_result.is_ok(),
            "❌ {} not found: {}",
            zip_path,
            file_result.err().unwrap()
        );
        let archive_result = ZipArchive::new(file_result.unwrap());
        assert!(
            archive_result.is_ok(),
            "❌ Failed to read {}: {}",
            zip_path,
            archive_result.err().unwrap()
        );
        archive_result.unwrap()
    }
}
