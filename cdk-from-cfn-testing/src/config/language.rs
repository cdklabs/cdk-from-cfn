// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

/// Configuration data for a specific programming language.
///
/// Contains language-specific file paths, naming conventions, and
/// other metadata needed for CDK code generation and testing.
struct LanguageData {
    /// Internal name used to identify the language
    pub name: &'static str,
    /// Path to the main application file for this language
    pub app_file: &'static str,
    /// Language name used in cdk-from-cfn command line arguments
    pub lang_name: &'static str,
    /// Template path for stack files (with {} placeholder for stack name)
    pub stack_path: &'static str,
}

/// Language configuration manager for CDK code generation.
///
/// Provides language-specific configuration, file naming conventions,
/// and post-processing logic for different programming languages
/// supported by cdk-from-cfn.
pub struct Language;

impl Language {
    /// TypeScript language identifier
    pub const TYPESCRIPT: &'static str = "typescript";
    /// Python language identifier
    pub const PYTHON: &'static str = "python";
    /// Java language identifier
    pub const JAVA: &'static str = "java";
    /// Go language identifier
    pub const GOLANG: &'static str = "golang";
    /// C# language identifier
    pub const CSHARP: &'static str = "csharp";

    /// Configuration data for all supported programming languages
    const CONFIGS: &'static [LanguageData] = &[
        LanguageData {
            name: Self::TYPESCRIPT,
            app_file: "app.ts",
            lang_name: Self::TYPESCRIPT,
            stack_path: "{}.ts",
        },
        LanguageData {
            name: Self::PYTHON,
            app_file: "app.py",
            lang_name: Self::PYTHON,
            stack_path: "{}.py",
        },
        LanguageData {
            name: Self::JAVA,
            app_file: "src/main/java/com/myorg/MyApp.java",
            lang_name: Self::JAVA,
            stack_path: "src/main/java/com/myorg/{}.java",
        },
        LanguageData {
            name: Self::GOLANG,
            app_file: "main.go",
            lang_name: "go",
            stack_path: "{}.go",
        },
        LanguageData {
            name: Self::CSHARP,
            app_file: "Program.cs",
            lang_name: Self::CSHARP,
            stack_path: "{}.cs",
        },
    ];

    /// Retrieves a language-specific property using a selector function.
    ///
    /// # Arguments
    /// * `lang` - Language identifier
    /// * `property_fn` - Function to extract the desired property from LanguageData
    ///
    /// # Returns
    /// The requested property value
    ///
    /// # Panics
    /// Panics if the language is not found in the configuration
    fn get_property<T, F>(lang: &str, property_fn: F) -> T
    where
        F: FnOnce(&LanguageData) -> T,
    {
        Self::CONFIGS
            .iter()
            .find(|config| config.name == lang)
            .map(property_fn)
            .unwrap()
    }

    /// Returns the command-line argument name for cdk-from-cfn.
    ///
    /// # Arguments
    /// * `lang` - Language identifier
    ///
    /// # Returns
    /// Language name to use in cdk-from-cfn --language argument
    pub fn lang_arg(lang: &str) -> &str {
        Self::get_property(lang, |config| config.lang_name)
    }

    /// Returns the main application file name for the language.
    ///
    /// # Arguments
    /// * `lang` - Language identifier
    ///
    /// # Returns
    /// Path to the main application file (e.g., "app.ts", "app.py")
    pub fn app_name(lang: &str) -> &'static str {
        Self::get_property(lang, |config| config.app_file)
    }

    /// Applies language-specific post-processing to generated code.
    ///
    /// Performs cleanup and modifications needed for specific languages,
    /// such as removing unwanted code sections or formatting adjustments.
    ///
    /// This is mainly for go.
    ///
    /// # Arguments
    /// * `lang` - Language identifier
    /// * `content` - Generated code content to process
    ///
    /// # Returns
    /// Post-processed code content
    pub fn post_process_output(lang: &str, mut content: String) -> String {
        if lang == Self::GOLANG {
            if let Some(main) = content.find("func main()") {
                content.truncate(main);
            }
        }
        content
    }

    /// Generates the stack file name for the specified language and stack.
    ///
    /// # Arguments
    /// * `lang` - Language identifier
    /// * `stack_name` - Name of the stack
    ///
    /// # Returns
    /// Complete file path for the stack file (e.g., "MyStack.ts", "my_stack.py")
    pub fn stack_filename(lang: &str, stack_name: &str) -> String {
        let stack_path = Self::get_property(lang, |config| config.stack_path);
        stack_path.replace("{}", stack_name)
    }

    /// Returns a list of all enabled programming languages.
    ///
    /// Languages are included based on compile-time feature flags,
    /// allowing selective compilation of language support.
    ///
    /// # Returns
    /// Vector of enabled language identifiers
    pub fn get_enabled_languages() -> Vec<String> {
        [
            #[cfg(feature = "typescript")]
            Self::TYPESCRIPT,
            #[cfg(feature = "golang")]
            Self::GOLANG,
            #[cfg(feature = "python")]
            Self::PYTHON,
            #[cfg(feature = "java")]
            Self::JAVA,
            #[cfg(feature = "csharp")]
            Self::CSHARP,
        ]
        .iter()
        .map(|&lang| lang.to_string())
        .collect()
    }
}
