use std::fs::{self, File};
use std::io::Write;
use std::path::{PathBuf, Path};
use std::process::Command;

pub fn typescript(
    name: &str,
    stack_name: &str,
    cdk_stack_definition: &str,
    cdk_stack_filename: &str,
    cdk_app_filename: &str,
) {
    let language_dir_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("tests/end-to-end/")
        .join(name)
        .join("typescript");
    println!("{:?}", language_dir_path);

    // create the typescript directory if it doesn't exist 

    
    let cdk_stack_path = Path::join(&language_dir_path, cdk_stack_filename);
    let r = fs::write(&cdk_stack_path, cdk_stack_definition);
    println!("{:?}", r);

    //if app.ts doesn't exist yet, write one.
    // and print a message to let the user know. 
    // tell them to consider different regions,  different values for the ocnditionals and parameters 

    let cdk_app_path = Path::join(&language_dir_path, cdk_app_filename);
    if !Path::exists(&cdk_app_path) {
        println!("This test does not have an app file yet. Creating  one...");
        let result = fs::write(&cdk_app_path, format!("import * as cdk from 'aws-cdk-lib';
        import {{ {stack_name} }} from './stack-under-test';
        
        const app = new cdk.App({{
          analyticsReporting: false,
          defaultStackSynthesizer: new cdk.DefaultStackSynthesizer({{
            generateBootstrapVersionRule: false,
          }}),
        }});
        
        new {stack_name}(app, 'Stack', {{}});
        app.synth();
        "));
    }

    // npm install
    let result = Command::new("npm")
        .args([
            "install",
            "--package-lock false"    
        ])
        .current_dir(fs::canonicalize("./tests/end-to-end/").unwrap())
        .output();

    println!("{:?}", result);

    // cdk synth
    let result = Command::new("npx")
        .args([
            "cdk",
            "synth",
            "--path-metadata",
            "false",
            "--app",
            "npx ts-node --prefer-ts-exts",
            cdk_app_filename,
        ])
        .current_dir(fs::canonicalize(language_dir_path).unwrap())
        .status();

    match result {
        Ok(status) => println!("{}", status),
        Err(e) => panic!("{e}"),
    }
}
pub fn golang(
    name: impl Into<String>,
    stack_name: &str,
    cdk_stack_definition: impl Into<String>,
    cdk_stack_filename: impl Into<String>,
    cdk_app_filename: impl Into<String>,
) {}
pub fn csharp(
    name: impl Into<String>,
    stack_name: &str,
    cdk_stack_definition: impl Into<String>,
    cdk_stack_filename: impl Into<String>,
    cdk_app_filename: impl Into<String>,
) {}
pub fn java(
    name: impl Into<String>,
    stack_name: &str,
    cdk_stack_definition: impl Into<String>,
    cdk_stack_filename: impl Into<String>,
    cdk_app_filename: impl Into<String>,
) {}
pub fn python(
    name: impl Into<String>,
    stack_name: &str,
    cdk_stack_definition: impl Into<String>,
    cdk_stack_filename: impl Into<String>,
    cdk_app_filename: impl Into<String>,
) {}
