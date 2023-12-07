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
use cdk_from_cfn::synthesizer::*;
use cdk_from_cfn::CloudformationParseTree;

use nom::AsBytes;
use walkdir::WalkDir;
use zip::ZipArchive;

mod cdk_app_code_writers;
use cdk_app_code_writers::CdkAppCodeWriter;

struct TestOptions<'a> {
    // in synth
    cdk_stack_classname: &'a str,
    // in check stack def
    // in synth
    // in update snapshots
    cdk_stack_filename: &'a str,
    // in synth
    // in update snapshots
    cdk_app_filename: &'a str,
    // in synth
    language_boilerplate_dir: &'a str,
    // in synth
    // in update snapshots
    test_working_dir: &'a str,
    // in check stack def
    // in synth
    // in update snapshots
    expected_outputs_dir: &'a str,
    // in synth
    cdk_app_code_writer: &'a dyn CdkAppCodeWriter,
}

struct CreateStackOptions<'a> {
    template: &'a str,
    stack_name: &'a str,
}

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
                "src/main/java/com/myorg/Stack.java",
                "src/main/java/com/myorg/MyApp.java"
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
            test_case!(
                $name,
                csharp,
                &CSharp {},
                $stack_name,
                "Stack.cs",
                "Program.cs"
            );
        }
    };

    ($name:ident, $lang:ident, $synthesizer:expr, $stack_name:literal, $cdk_stack_filename:literal, $cdk_app_filename:literal) => {
        #[test]
        fn $lang() {

            let mut snapshots_zip = get_zip_archive_from_bytes(include_bytes!("./end-to-end-test-snapshots.zip"));
            let expected_outputs_dir = format!("{}/{}", stringify!($name), stringify!($lang));
            let test_working_dir = format!(
                "tests/end-to-end/{}-{}-working-dir",
                stringify!($name),
                stringify!($lang)
            );
            let language_boilerplate_dir = format!(
                "tests/end-to-end/app-boilerplate-files/{}",
                stringify!($lang)
            );
            let cdk_app_code_writer: Box<dyn CdkAppCodeWriter> = match stringify!($lang) {
                "typescript" => Box::new(cdk_app_code_writers::Typescript {}),
                "python" => Box::new(cdk_app_code_writers::Python {}),
                "java" => Box::new(cdk_app_code_writers::Java {}),
                "csharp" => Box::new(cdk_app_code_writers::CSharp {}),
                "golang" => Box::new(cdk_app_code_writers::Go {}),
                &_ => todo!(),
            };
            let options = TestOptions {
                cdk_stack_classname : $stack_name,
                cdk_stack_filename : $cdk_stack_filename,
                cdk_app_filename : $cdk_app_filename,
                language_boilerplate_dir : &language_boilerplate_dir,
                test_working_dir : &test_working_dir,
                expected_outputs_dir : &expected_outputs_dir,
                cdk_app_code_writer : cdk_app_code_writer.as_ref(),
            };

            // Check that the original cloudformation template is valid
            println!("Verifying a CloudFormation stack can be created from original template");
            let original_template =
                include_str!(concat!("end-to-end/", stringify!($name), "/template.json"));
            create_stack(CreateStackOptions {
                template: original_template,
                stack_name: $stack_name,
            });

            println!("Creating the cdk stack definition");
            let cdk_stack_definition = {
                let mut output = Vec::new();
                let cfn: CloudformationParseTree =
                    serde_yaml::from_str(original_template).expect(&format!(
                        "{} should be valid json",
                        concat!("end-to-end/", stringify!($name), "/template.json")
                    ));
                let ir = CloudformationProgramIr::from(cfn)
                    .expect("failed to convert cfn template into CloudformationProgramIr");
                ir.synthesize($synthesizer, &mut output, $stack_name)
                    .expect(
                        "failed to synthesize cdk stack definition from cloudformation template",
                    );
                String::from_utf8(output).expect("ir.synthesize() output should be utf8")
            };

            
            println!("Checking for cdk stack definition in the expected output");
            check_cdk_stack_def_matches_expected(&cdk_stack_definition, &options, &mut snapshots_zip);

            synth_cdk_app(&cdk_stack_definition, &options, &mut snapshots_zip);

            diff_original_template_with_new_templates(stringify!($name), &test_working_dir);

            // update snapshots
            update_snapshots(&options, &mut snapshots_zip);
            // clean up test working dir
            if std::env::var_os("SKIP_CLEAN").is_some() {
                println!("Skipping test cleanup because SKIP_CLEAN=true");
            } else {
                remove_dir_all(&test_working_dir).expect(&format!(
                    "failed to remove test working directory: {}",
                    &test_working_dir
                ));
            }
        }
    };
}

test_case!(simple, "SimpleStack");

#[tokio::main]
async fn create_stack(options: CreateStackOptions) {
    let CreateStackOptions { template, stack_name } = options;
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

fn check_cdk_stack_def_matches_expected(actual_cdk_stack_def: &str, options: &TestOptions, snapshots_zip: &mut ZipArchive<Cursor<&[u8]>>) {
    let TestOptions { cdk_stack_filename, expected_outputs_dir, .. } = options;
    let expected_cdk_stack_def_filename = &format!("{expected_outputs_dir}/{cdk_stack_filename}");
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

fn synth_cdk_app(cdk_stack_definition: &str, options: &TestOptions, snapshots_zip: &mut ZipArchive<Cursor<&[u8]>>) {
    println!("Synth CDK app");
    let TestOptions {
        cdk_stack_classname,
        cdk_stack_filename,
        cdk_app_filename,
        language_boilerplate_dir,
        test_working_dir,
        expected_outputs_dir,
        cdk_app_code_writer,
        ..
    } = options;

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
}

fn diff_original_template_with_new_templates(test_name: &str, test_working_dir: &str) {
    let walkdir = WalkDir::new(format!("{test_working_dir}/cdk.out/"));

    for entry in walkdir.into_iter().map(|e| e.expect("walkdir failed")) {
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

fn update_snapshots(options: &TestOptions, snapshots_zip: &mut ZipArchive<Cursor<&[u8]>>) {
    let TestOptions {cdk_stack_filename, cdk_app_filename, test_working_dir, expected_outputs_dir, ..} = options;

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
    let app_file_src = &format!("{test_working_dir}/{cdk_app_filename}");
    let app_file_dst = &format!("{expected_outputs_dir}/{cdk_app_filename}");
    if snapshots_zip
        .by_name(&format!("{expected_outputs_dir}/{cdk_app_filename}"))
        .is_err()
    {
        println!("Updating app file snapshot");
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
    println!("Updating template and diff file(s) snapshot(s)");
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
