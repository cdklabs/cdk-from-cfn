use core::panic;
use std::fs::{self, canonicalize, copy, create_dir_all, remove_dir_all, File};
use std::io::{Cursor, Read, Write};
use std::process::Command;

use aws_sdk_cloudformation::types::OnFailure;

use aws_config::meta::region::RegionProviderChain;
use aws_sdk_cloudformation::types::StackStatus;
use aws_sdk_cloudformation::{Client, Error};
use cdk_from_cfn::code::CodeBuffer;
use cdk_from_cfn::ir::CloudformationProgramIr;
use cdk_from_cfn::synthesizer::{self, *};
use cdk_from_cfn::CloudformationParseTree;

use nom::AsBytes;
use walkdir::WalkDir;
use zip::ZipArchive;

mod cdk_app_code_writers;
use cdk_app_code_writers::CdkAppCodeWriter;

macro_rules! include_template_str {
    ($name:expr) => {
        include_str!(concat!("end-to-end/", $name, "/template.json"))
    };
}

macro_rules! test_case {
    ($name:ident, $lang:ident, $stack_name:literal) => {
        mod $name {
            use super::*;
            #[test]
            fn $lang() {
                actual_test_case(
                    stringify!($name), 
                    include_template_str!(stringify!($name)),
                    stringify!($lang),
                    $stack_name,
                )
            }
        }
    }
}

test_case!(simple, typescript, "SimpleStack");

struct LanguageDependentOptions <'a> {
    cdk_app_code_writer: Box<dyn CdkAppCodeWriter>,
    cdk_from_cfn_synthesizer: Box<dyn Synthesizer>,
    cdk_stack_filename: &'a str,
    cdk_app_filename: &'a str,
}

struct TestDirectories <'a> {
    language_boilerplate_dir: &'a str,
    test_working_dir: &'a str,
    expected_outputs_dir: &'a str,
}

fn actual_test_case(
    name: &str,
    original_template: &str,
    lang: &str,
    stack_name: &str,
) {
    let lang_options = match lang {
        "typescript" => LanguageDependentOptions {
            cdk_app_code_writer: Box::new(cdk_app_code_writers::Typescript {}),
            cdk_from_cfn_synthesizer: Box::new(synthesizer::Typescript {}),
            cdk_stack_filename: "stack.ts",
            cdk_app_filename: "app.ts",
        },
        "python" => LanguageDependentOptions {
            cdk_app_code_writer: Box::new(cdk_app_code_writers::Python {}),
            cdk_from_cfn_synthesizer: Box::new(Python {}),
            cdk_stack_filename: "stack.ts",
            cdk_app_filename: "app.ts",
        },
        "java" => LanguageDependentOptions {
            cdk_app_code_writer: Box::new(cdk_app_code_writers::Java {}),
            cdk_from_cfn_synthesizer: Box::<Java>::default(),
            cdk_stack_filename: "stack.ts",
            cdk_app_filename: "app.ts",
        },
        "csharp" => LanguageDependentOptions {
            cdk_app_code_writer: Box::new(cdk_app_code_writers::CSharp {}),
            cdk_from_cfn_synthesizer: Box::new(CSharp {}),
            cdk_stack_filename: "stack.ts",
            cdk_app_filename: "app.ts",
        },
        "golang" => LanguageDependentOptions {
            cdk_app_code_writer: Box::new(cdk_app_code_writers::Golang {}),
            cdk_from_cfn_synthesizer: Box::<Golang>::default(),
            cdk_stack_filename: "stack.ts",
            cdk_app_filename: "app.ts",
        },
        other => panic!("Unsupported language: {other}"),
    };

    let test_dirs = TestDirectories {
        language_boilerplate_dir: &format!("tests/end-to-end/app-boilerplate-files/{lang}"),
        test_working_dir:  &format!("tests/end-to-end/{name}-{lang}-working-dir"),
        expected_outputs_dir: &format!("{name}/{lang}"),
    };

    // Check that the original cloudformation template is valid
    println!("Verifying a CloudFormation stack can be created from original template");

    create_stack(original_template, stack_name);

    println!("Creating the cdk stack definition");
    let cdk_stack_definition = {
        let mut output = Vec::new();
        let cfn: CloudformationParseTree = serde_yaml::from_str(original_template).expect(
            &format!("end-to-end/{name}/template.json should be valid json"),
        );
        let ir = CloudformationProgramIr::from(cfn)
            .expect("failed to convert cfn template into CloudformationProgramIr");
        ir.synthesize(lang_options.cdk_from_cfn_synthesizer.as_ref(), &mut output, stack_name)
            .expect("failed to synthesize cdk stack definition from cloudformation template");
        String::from_utf8(output).expect("ir.synthesize() output should be utf8")
    };

    println!("Checking for cdk stack definition in the expected output");
    let mut snapshots_zip =
        get_zip_archive_from_bytes(include_bytes!("./end-to-end-test-snapshots.zip"));
    check_cdk_stack_def_matches_expected(&cdk_stack_definition, &test_dirs, &lang_options, &mut snapshots_zip);

    synth_cdk_app(&cdk_stack_definition, stack_name, &test_dirs, &lang_options, &mut snapshots_zip);

    diff_original_template_with_new_templates(name, test_dirs.test_working_dir);

    // update snapshots
    update_snapshots(&test_dirs, &lang_options, &mut snapshots_zip);
    // clean up test working dir
    if std::env::var_os("SKIP_CLEAN").is_some() {
        println!("Skipping test cleanup because SKIP_CLEAN=true");
    } else {
        println!("Cleaning up test working directory: {}", test_dirs.test_working_dir);
        remove_dir_all(&test_dirs.test_working_dir).expect(&format!(
            "failed to remove test working directory: {}",
            test_dirs.test_working_dir
        ));
    }
}

#[tokio::main]
async fn create_stack(template: &str, stack_name: &str) {
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
        .expect("cfn create stack failed");
    let id = resp.stack_id.unwrap_or_default();
    print!("Stack {id} create in progress...");
    std::io::stdout().flush().expect("failed to flush stdout");

    let mut status = check_stack_status(&id, &client)
        .await
        .expect(&format!("failed to check stack status: {id}"));

    while let StackStatus::CreateInProgress = status {
        print!(".");
        std::io::stdout().flush().expect("failed to flush stdout");
        tokio::time::sleep(std::time::Duration::new(2, 0)).await;
        status = check_stack_status(&id, &client)
            .await
            .expect(&format!("failed to check stack status: {}", &id));
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

fn check_cdk_stack_def_matches_expected(
    actual_cdk_stack_def: &str,
    test_dirs: &TestDirectories,
    lang_options: &LanguageDependentOptions,
    snapshots_zip: &mut ZipArchive<Cursor<&[u8]>>,
) {
    let expected_cdk_stack_def_filename = &format!("{}/{}", test_dirs.expected_outputs_dir, lang_options.cdk_stack_filename);
    println!(
        "Checking cdk stack definition matches the expected output in {}",
        expected_cdk_stack_def_filename
    );
    if std::env::var_os("UPDATE_SNAPSHOTS").is_some() {
        // If UPDATE_SNAPSHOTS is set, then don't bother checking the expected output files, because they will be over-written. This environment variable is for development purposes, and will not be used in CI/CD.
        println!("Skipping cdk stack definition check because UPDATE_SNAPSHOTS=true");
        return;
    }
    if let Ok(mut expected_cdk_stack_def) = snapshots_zip.by_name(expected_cdk_stack_def_filename) {
        let mut expected = String::new();
        expected_cdk_stack_def.read_to_string(&mut expected).expect(
            "failed to read expected cdk stack definition from end-to-end-test-snapshots.zip",
        );
        assert_eq!(expected, actual_cdk_stack_def);
    } else {
        // Fail the test to prevent tests without snapshots from succeeding in CI/CD
        panic!("Did not find the expected cdk stack definition in end-to-end-test-snapshots.zip at {expected_cdk_stack_def_filename}. If you are developing a new test, set UPDATE_SNAPSHOTS=true in your environment variables and the test will automatically create snapshot files.");
    }
}

fn get_zip_archive_from_bytes(zip: &[u8]) -> ZipArchive<Cursor<&[u8]>> {
    let cursor = std::io::Cursor::new(zip);
    zip::read::ZipArchive::new(cursor)
        .expect("failed to convert end-to-end-test-snapshots.zip contents into ZipArchive")
}

fn synth_cdk_app(
    cdk_stack_definition: &str,
    cdk_stack_classname: &str,
    test_dirs: &TestDirectories,
    lang_options: &LanguageDependentOptions,
    snapshots_zip: &mut ZipArchive<Cursor<&[u8]>>,
) {
    println!("Synth CDK app");
    let LanguageDependentOptions {
        cdk_stack_filename,
        cdk_app_filename,
        cdk_app_code_writer,
        ..
    } = lang_options;
    let TestDirectories {
        test_working_dir,
        language_boilerplate_dir,
        expected_outputs_dir,
    } = test_dirs;

    // Create a temporary working directory, and copy language-specific boiler plate files into it
    create_dir_all(test_working_dir).expect(&format!(
        "failed to create test working directory: {test_working_dir}"
    ));
    let walkdir = WalkDir::new(language_boilerplate_dir);
    for entry in walkdir.into_iter().map(|e| e.expect("walkdir failed")) {
        if entry.path().is_file() {
            let filename = entry.file_name().to_str().expect(&format!(
                "{:?} should be convertible to a string",
                entry.file_name()
            ));
            println!("Copying {filename} into {}", test_working_dir);

            let from = entry.path();
            let to = format!("{test_working_dir}/{filename}");
            copy(from, &to).expect(&format!("failed to copy {:?} to {}", from, &to));
        }
    }

    // App file
    let cdk_app_file_path = format!("{expected_outputs_dir}/{cdk_app_filename}");
    println!("Checking for cdk app file in snapshots: {cdk_app_file_path}",);

    let test_working_dir_abs_path = canonicalize(test_working_dir).expect(&format!(
        "failed to get absolute path for {test_working_dir}"
    ));
    let app_dst_path = test_working_dir_abs_path.join(cdk_app_filename);
    // The parent directory for the app file might not exist yet. Example: Java uses src/main/java/com/myorg/MyApp.java
    let prefix = app_dst_path
        .parent()
        .expect("failed to get parent path for cdk app file");
    create_dir_all(prefix).expect("failed to create parent directory for cdk app file");

    if let Ok(mut cdk_app_file) = snapshots_zip.by_name(&cdk_app_file_path) {
        println!(
            "An app file already exists. Copying it to: {:?}",
            app_dst_path
        );
        let mut contents = Vec::<u8>::new();
        cdk_app_file
            .read_to_end(&mut contents)
            .expect("failed to read cdk app file from end-to-end-test-snapshots.zip");
        let mut file = File::create(app_dst_path).expect("failed to create cdk app file");
        file.write_all(contents.as_bytes())
            .expect("failed to write contents into cdk app file");
    } else if std::env::var_os("UPDATE_SNAPSHOTS").is_some() {
        println!("UPDATE_SNAPSHOTS=true, and there is no existing app file, creating default one at {}...", app_dst_path.to_str().unwrap_or(""));
        let mut file = File::create(app_dst_path).expect("failed to create cdk app file");
        let code: CodeBuffer = CodeBuffer::default();
        cdk_app_code_writer.app_file(&code, cdk_stack_classname);
        code.write(&mut file)
            .expect("failed to write contents into cdk app file");
    } else {
        // Fail the test to prevent tests without snapshots from succeeding in CI/CD
        panic!("CDK App file not found at {}. If you are developing a new test, set UPDATE_SNAPSHOTS=true in your environment variables and the test will create a default app file.", cdk_app_filename);
    }

    // Stack file
    let stack_dst_path = test_working_dir_abs_path.join(cdk_stack_filename);
    println!(
        "Writing cdk stack definition to file: {}",
        stack_dst_path.to_str().unwrap_or("")
    );

    let mut file = File::create(stack_dst_path).expect("failed to create cdk stack file");
    file.write_all(cdk_stack_definition.as_bytes())
        .expect("failed to write contents into cdk stack file");

    println!("Executing {language_boilerplate_dir}/setup-and-synth.sh in {test_working_dir}");
    let res = Command::new("bash")
        .arg("setup-and-synth.sh")
        .current_dir(&test_working_dir_abs_path)
        .output()
        .expect("cdk app setup or synth failed");
    if !res.status.success() {
        println!("===== cdk synth stdout ===== START =====");
        println!(
            "{}",
            String::from_utf8(res.stdout).expect("failed to convert stdout to utf8")
        );
        println!("===== cdk synth stdout ===== END =======\n");

        println!("===== cdk synth stderr ===== START =====");
        println!(
            "{}",
            String::from_utf8(res.stderr).expect("failed to convert stderr to utf8")
        );
        println!("===== cdk synth stderr ===== END =======\n");

        panic!("cdk app setup or synth failed");
    }
    println!("CDK synth complete");
}

fn diff_original_template_with_new_templates(test_name: &str, test_working_dir: &str) {
    let walkdir = WalkDir::new(format!("{test_working_dir}/cdk.out/"));

    for entry in walkdir.into_iter().map(|e| e.expect("walkdir failed - this could indicate that cdk synth did not execute correctly")) {
        let filename = entry.file_name().to_str().expect(&format!(
            "{:?} should be convertible to a string",
            entry.file_name()
        ));
        if filename.contains("template.json") {
            println!("Comparing {filename} to the original template");
            let expected = &format!("./tests/end-to-end/{test_name}/template.json");
            let actual = entry.path().to_str().expect(&format!(
                "{:?} should be convertible to a string",
                entry.path()
            ));
            let res = std::process::Command::new("git")
                .args(["diff", "--no-index", actual, expected])
                .output()
                .expect("git diff failed");

            let stack_name = filename
                .split(".")
                .next()
                .expect(&format!("failed to extract stack name from {filename}"));
            let diff_filename = &format!("{test_working_dir}/{stack_name}.diff");
            let mut f = fs::File::create(diff_filename)
                .expect(&format!("failed to create diff file: {diff_filename}"));
            f.write_all(&res.stdout).expect(&format!(
                "failed to write contents to diff file: {diff_filename}"
            ));
        }
    }
}

fn update_snapshots(test_dirs: &TestDirectories, lang_options: &LanguageDependentOptions, snapshots_zip: &mut ZipArchive<Cursor<&[u8]>>) {
    let TestDirectories {
        test_working_dir,
        expected_outputs_dir,
        ..
    } = test_dirs;
    let LanguageDependentOptions {
        cdk_app_filename,
        cdk_stack_filename,
        ..
    } = lang_options;

    if std::env::var_os("UPDATE_SNAPSHOTS").is_none() {
        // By default, and in CI/CD, skip updating the snapshots
        println!("Not updating snapshots because UPDATE_SNAPSHOTS is none.");
        return;
    }
    println!("Updating snapshots because UPDATE_SNAPSHOTS=true...");

    let expected_outputs_path = &format!("tests/end-to-end/{expected_outputs_dir}/");
    create_dir_all(expected_outputs_path).expect(&format!(
        "failed to create directory for updated snapshots at: {expected_outputs_path}"
    ));

    // App file
    // If the app file does not already exist in the snapshot, copy the one generated by this test run to the test's directory
    if snapshots_zip
        .by_name(&format!("{expected_outputs_dir}/{cdk_app_filename}"))
        .is_err()
    {
        println!("Updating app file snapshot");
        let app_file_src = &format!("{test_working_dir}/{cdk_app_filename}");
        let app_file_dst = &format!("{expected_outputs_path}/{cdk_app_filename}");
        copy(app_file_src, app_file_dst)
            .expect(&format!("failed to copy {app_file_src} to {app_file_dst}"));
    }

    // Stack file
    let stack_file_src = &format!("{test_working_dir}/{cdk_stack_filename}");
    let stack_file_dst = &format!("{expected_outputs_path}/{cdk_stack_filename}");
    println!("Updating stack file snapshot");
    copy(stack_file_src, stack_file_dst).expect(&format!(
        "failed to copy {stack_file_src} to {stack_file_dst}"
    ));

    // Template and diff files
    println!("Updating template and diff file snapshot(s)");
    let walkdir = WalkDir::new(test_working_dir);
    for entry in walkdir.into_iter().map(|e| e.expect("walkdir failed")) {
        let filename = entry.file_name().to_str().expect(&format!(
            "{:?} should be convertible to a string",
            entry.file_name()
        ));
        let src_path = entry.path().to_str().expect(&format!(
            "{:?} should be convertible to a string",
            entry.path()
        ));

        if src_path.contains("node_modules") {
            continue;
        }
        if filename.contains("template.json") || filename.contains(".diff") {
            let dst_path = &format!("{expected_outputs_path}/{filename}");
            copy(src_path, dst_path).expect(&format!("failed to copy {src_path} to {dst_path}"));
        }
    }
}
