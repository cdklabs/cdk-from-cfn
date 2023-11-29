use std::borrow::Cow;
use std::fs::{self, File, canonicalize};
use std::io::{Write, Read, Cursor, stdout};
use std::path::{PathBuf, Path};
use std::process::{Command, Stdio};

use assert_json_diff::assert_json_eq;
use aws_sdk_cloudformation::types::OnFailure;

use aws_config::meta::region::RegionProviderChain;
use aws_sdk_cloudformation::types::StackStatus;
use aws_sdk_cloudformation::{Client, Error};
use cdk_from_cfn::ir::CloudformationProgramIr;
use cdk_from_cfn::synthesizer::*;
use cdk_from_cfn::CloudformationParseTree;
use cdk_from_cfn::code::{CodeBuffer, IndentOptions};

use nom::AsBytes;
use walkdir::WalkDir;
use zip::ZipArchive;

mod cdk_synthesizers;

const INDENT: Cow<'static, str> = Cow::Borrowed("    ");

macro_rules! test_case {
    ($name:ident, $stack_name:literal) => {
        mod $name { 
            use super::*;

            #[cfg(feature = "golang")]
            test_case!(
                $name,
                golang,
                &Golang::new(stringify!($name)),
                $stack_name,
                "stack.go",
                "app.go"
            );

            #[cfg(feature = "java")]
            test_case!(
                $name,
                java,
                &Java::new(concat!("com.myorg")),
                $stack_name,
                "Stack.java",
                "App.java"
            );

            #[cfg(feature = "python")]
            test_case!($name, python, &Python {}, $stack_name, "stack.py", "app.py");

            #[cfg(feature = "typescript")]
            test_case!(
                $name,
                typescript,
                &Typescript {},
                $stack_name,
                "stack.ts",
                "app.ts"
            );

            #[cfg(feature = "csharp")]
            test_case!($name, csharp, &CSharp {}, $stack_name, "Stack.cs", "App.cs");
        }
    };

    ($name:ident, $lang:ident, $synthesizer:expr, $stack_name:literal, $cdk_stack_filename:literal, $cdk_app_filename:literal) => {
        #[test]
        fn $lang() {
            // What needs to go in the macro:
            // - Anything that is using an ident as an ident
            // - anything using include_str

            // ? Does original cloudformation template deploy successfully
            println!("Verifying a CloudFormation stack can be created from original template");
            let original_template = include_str!(concat!("end-to-end/", stringify!($name), "/template.json"));
            create_stack($stack_name, original_template);

            println!("Creating the cdk stack definition");
            let cdk_stack_definition = {
                let mut output = Vec::new();
                let cfn: CloudformationParseTree = serde_yaml::from_str(original_template).unwrap();
                let ir = CloudformationProgramIr::from(cfn).unwrap();
                ir.synthesize($synthesizer, &mut output, $stack_name)
                    .unwrap();
                String::from_utf8(output).unwrap()
            };

            let mut snapshots_zip = get_zip_archive_from_bytes(include_bytes!("./snapshots.zip"));

            println!("Checking for cdk stack snapshot");
            let snapshot_dir = format!("{}/{}", stringify!($name), stringify!($lang));
            let snapshot_filename = format!("{snapshot_dir}/{}", $cdk_stack_filename);
            check_cdk_stack_snapshot(&cdk_stack_definition, &snapshot_filename, &mut snapshots_zip);

            let language_working_dir = concat!("end-to-end/", stringify!($lang), "-working-dir/");
            synth_cdk_app(&cdk_stack_definition, $stack_name, $cdk_stack_filename, $cdk_app_filename, language_working_dir, &snapshot_dir,  &mut snapshots_zip);

            // Compare each stack to the original
            //original is at /simple/template.json
            //new is at language-working-dir/cdk.out/*.template.json

            diff_original_template_with_new_templates(stringify!($name), language_working_dir);

            // What is the delta?

            // If not, is the flag set to update snapshots? interactive show file to user to approve

            // Make sure it works in each language

            // update snapshots
        }
    };
}

test_case!(simple, "SimpleStack");

fn diff_original_template_with_new_templates(test_name: &str, language_working_dir: &str) {
    
     let walkdir = WalkDir::new(format!("./tests/{language_working_dir}cdk.out/"));

     for entry in walkdir.into_iter().map(|e| e.unwrap()) {
        println!("{:?}", entry.path());
        if entry.file_name().to_str().unwrap().contains("template.json") {
            println!("    This is a template file. comparing it to the original");
            // use git diff 
            println!("{}", format!("tests/end-to-end/{test_name}"));
            let working_dir = canonicalize("./").unwrap();
            let res = std::process::Command::new("git")
                .args(["diff", "--no-index", &format!("./tests/end-to-end/{test_name}/template.json"), entry.path().to_str().unwrap()])
                .output()
                .expect("git diff failed");

            let mut f = fs::File::create(format!("./tests/end-to-end/{test_name}/simplestack.diff")).unwrap();
            f.write_all(&res.stdout);
            //println!("{:?}", res);
        }
     }
 
    //walk the cdk out dir
}

fn synth_cdk_app(cdk_stack_definition: &str, stack_classname: &str, cdk_stack_filename: &str, cdk_app_filename: &str, language_working_dir: &str, test_dir: &str, snapshots_zip: &mut ZipArchive<Cursor<&[u8]>>) {
    println!("Synth cdk app");

    // App file
    let cdk_app_file_path = format!("{test_dir}/{cdk_app_filename}");
    println!("Checking for cdk app file in snapshots: {cdk_app_file_path}", );
    snapshots_zip.file_names().for_each(|n| println!("{n}"));

    // If the app file already exists in the snapshot, copy to the languages working dir
    let app_dst_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("tests")
        .join(language_working_dir)
        .join(cdk_app_filename);
    if let Ok(mut cdk_app_file) = snapshots_zip.by_name(&cdk_app_file_path) {
        let mut contents = Vec::<u8>::new();
        let result = cdk_app_file.read_to_end(&mut contents);
        // copy app file
        println!("found an app file and copying it to: {:?}", app_dst_path);
        let mut file = File::create(app_dst_path).unwrap();
        file.write_all(contents.as_bytes()).unwrap();

    } else if std::env::var_os("UPDATE_SNAPSHOTS").is_some() {
        // create new app file
        println!("UPDATE_SNAPSHOTS=true, and there is no existing app file, creating default one at {:?}...", app_dst_path);
        let mut file = File::create(app_dst_path).unwrap();
        let code: CodeBuffer = CodeBuffer::default();
        // recommend to manually instantiate a stack for each combination of parameters that should be tested
        code.line("// auto-generated! a human should update this!");
        code.line("import * as cdk from \"aws-cdk-lib\";");
        code.line(format!("import {{ {} }} from \"./stack\";", stack_classname));
        let app = code.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some("const app = new cdk.App({".into()),
            trailing: Some("});".into()),
            trailing_newline: true
        });
        let app_props = app.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some("defaultStackSynthesizer: new cdk.DefaultStackSynthesizer({".into()),
            trailing: Some("}),".into()),
            trailing_newline: true
        });
        app_props.line("generateBootstrapVersionRule: false,");
        code.line(format!("new {}(app, \"Stack\");", stack_classname));
        code.line("app.synth();");
        code.write(&mut file);
    } else {
        // Fail the test to prevent tests without snapshots from succeeding in CI/CD
        panic!("CDK App file not found at {}. If you are developing a new test, set UPDATE_SNAPSHOTS=true in your environment variables and the test will create a default app file.", cdk_app_filename);
    }

    // Stack file
    let stack_dst_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("tests")
        .join(language_working_dir)
        .join(cdk_stack_filename);
    let mut file = File::create(stack_dst_path).unwrap();
    file.write_all(cdk_stack_definition.as_bytes());

    // lang-specific install or setup commands
    // npm install --no-package-lock
    let working_dir = canonicalize(format!("tests/{language_working_dir}")).unwrap();
    println!("{:?}", canonicalize(format!("tests/{language_working_dir}")));
    let res = Command::new("npm")
        .arg("install")
        .arg("--no-package-lock")
        .current_dir(&working_dir)
        .output()
        .expect("command failed");
    println!("{}", String::from_utf8(res.stdout).unwrap());

    // Synth the app
    let res = Command::new("npx")
        .args(["cdk", "synth", "--no-version-reporting", "--no-path-metadata", "--app", "npx ts-node ./app.ts"])
        .current_dir(&working_dir)
        .output()
        .expect("synth failed");
    println!("{}", String::from_utf8(res.stdout).unwrap());
    println!("{}", String::from_utf8(res.stderr).unwrap());


}

fn compare_templates(
    original_template: impl Into<String>,
    template_synthesized_by_cdk: impl Into<String>,
) {
}

#[tokio::main]
async fn create_stack(stack_name: &str, template: &str) {
    if std::env::var_os("CREATE_STACK").is_none() {
        // By default, and in CI/CD, skip creating a CloudFormation stack with the original template.
        println!("Skipping create stack because CREATE_STACK is none");
        return;
    }
    
    println!("Creating stack from original template");
    let region_provider = RegionProviderChain::default_provider().or_else("us-east-1");
    let config = aws_config::from_env().region(region_provider).load().await;
    let client = Client::new(&config);

    let resp = client
        .create_stack()
        .stack_name(stack_name)
        .template_body(template)
        .on_failure(OnFailure::Delete)
        .send()
        .await
        .unwrap();
    let id = resp.stack_id.unwrap_or_default();
    print!("Stack {id} create in progress...");
    std::io::stdout().flush().unwrap();

    let mut status = check_stack_status(&id, &client).await.unwrap();

    while let StackStatus::CreateInProgress = status {
        print!(".");
        std::io::stdout().flush().unwrap();
        tokio::time::sleep(std::time::Duration::new(2, 0)).await;
        status = check_stack_status(&id, &client).await.unwrap();
    }
    match status {
        StackStatus::CreateFailed
        | StackStatus::DeleteComplete
        | StackStatus::DeleteFailed
        | StackStatus::DeleteInProgress => {
            panic!("stack creation failed. stack status: {}", status.as_str())
        }
        StackStatus::CreateComplete => println!("create complete!"),
        _ => panic!("unexpected stack status: {}", status.as_str()),
    }
}

async fn check_stack_status(id: &str, client: &Client) -> Result<StackStatus, Error> {
    println!("Checking stack status: {}", id);
    let resp = client.describe_stacks().stack_name(id).send().await?;
    if let Some(stacks) = resp.stacks {
        if let Some(stack) = stacks.first() {
            if let Some(status) = &stack.stack_status {
                return Ok(status.clone());
            }
        }
    }
    panic!("describe_stacks returned no stacks");
}

fn check_cdk_stack_snapshot(actual_cdk_stack_def: &str, expected_cdk_stack_def_filename: &str, snapshots_zip: & mut ZipArchive<Cursor<&[u8]>>) {
    println!("Checking cdk stack snapshot for {}", expected_cdk_stack_def_filename);
    if std::env::var_os("UPDATE_SNAPSHOTS").is_some() {
        // If UPDATE_SNAPSHOTS is set, then don't bother checking the snapshots, because they will be over-written. This environment variable is for development purposes, and will not be use in CI/CD.
        println!("Skipping snapshot check because UPDATE_SNAPSHOTS=true");
        return;
   } 
    // If the snapshot file doesn't exist, then assume this test is new, and there is no previous snapshot to compare against.  
    if let Ok(mut expected_cdk_stack_def) = snapshots_zip.by_name(expected_cdk_stack_def_filename) {
      let mut contents = String::new();
      let result = expected_cdk_stack_def.read_to_string(&mut contents);
      println!("Finished reading snapshot file {:?}", result);
      // TODO check if it matches the snapshot
    } else {
        // Fail the test to prevent tests without snapshots from succeeding in CI/CD
        panic!("There is no cdk stack snapshot for this test. If you are developing a new test, set UPDATE_SNAPSHOTS=true in your environment variables and the test will automatically create snapshot files.");
    }
}

fn get_zip_archive_from_bytes(zip: &[u8]) -> ZipArchive<Cursor<&[u8]>> {
    let cursor = std::io::Cursor::new(zip);
    zip::read::ZipArchive::new(cursor).unwrap()
}

struct UpdateSnapshot<'a> {
    path: &'static str,
    actual: &'a str,
    expected: &'a str,
}

impl<'a> UpdateSnapshot<'a> {
    fn new(path: &'static str, actual: &'a str, expected: &'a str) -> Self {
        Self {
            path,
            actual,
            expected,
        }
    }
}

impl Drop for UpdateSnapshot<'_> {
    fn drop(&mut self) {
        use std::fs::File;
        use std::io::Write;
        use std::path::PathBuf;

        if std::env::var_os("UPDATE_SNAPSHOTS").is_some() && self.actual != self.expected {
            let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("tests")
                .join(self.path);
            let mut file = File::create(path).unwrap();
            file.write_all(self.actual.as_bytes()).unwrap();
        }
    }
}
