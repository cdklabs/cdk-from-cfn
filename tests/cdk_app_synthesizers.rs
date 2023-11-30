use std::{fs::canonicalize, process::Command};

pub trait CdkAppSynthesizer {
    fn synthesize(&self, test_working_dir: &str);
}

pub struct Typescript {}

impl CdkAppSynthesizer for Typescript {
    fn synthesize(&self, test_working_dir: &str) {
        println!("Synthesizing typescript app");
        // lang-specific install or setup commands
        let test_working_dir_abs_path = canonicalize(test_working_dir).unwrap();
        Command::new("npm")
            .arg("install")
            .arg("--no-package-lock")
            .current_dir(&test_working_dir_abs_path)
            .output()
            .expect("npm install failed");

        // Synth the app
        Command::new("npx")
            .args([
                "cdk",
                "synth",
                "--no-version-reporting",
                "--no-path-metadata",
                "--app",
                "npx ts-node ./app.ts",
            ])
            .current_dir(&test_working_dir_abs_path)
            .output()
            .expect("synth failed");
    }
}

pub struct Python {}

impl CdkAppSynthesizer for Python {
    fn synthesize(&self, test_working_dir: &str) {
        println!("Synthesizing python app")
    }
}
