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
    ($name:ident, $stack_name:literal, $skip_cdk_synth:expr) => {
        mod $name {
            use super::*;
            test_case!($name, typescript, $stack_name, $skip_cdk_synth);
            test_case!($name, java, $stack_name, $skip_cdk_synth);
            test_case!($name, golang, $stack_name, $skip_cdk_synth);
            test_case!($name, csharp, $stack_name, $skip_cdk_synth);
            test_case!($name, python, $stack_name, $skip_cdk_synth);
        }
    };

    ($name: ident, $lang:ident, $stack_name:literal, $skip_cdk_synth:expr) => {
        #[test]
        fn $lang() {
            let mut test = EndToEndTest::new(
                stringify!($name),
                stringify!($lang),
                $stack_name,
                $skip_cdk_synth,
                include_template_str!(stringify!($name)),
            );
            test.run();
        }
    };
}

const SKIP_SYNTH: [&str; 1] = ["golang"];

test_case!(simple, "SimpleStack", &SKIP_SYNTH);
// Add new test cases here

struct EndToEndTest<'a> {
    name: &'a str,
    lang: &'a str,
    original_template: &'a str,
    stack_name: &'a str,
    cdk_app_code_writer: Box<dyn CdkAppCodeWriter>,
    cdk_from_cfn_synthesizer: Box<dyn Synthesizer>,
    cdk_stack_filename: &'a str,
    cdk_app_filename: &'a str,
    language_boilerplate_dir: String,
    test_working_dir: String,
    expected_outputs_dir: String,
    snapshots_zip: ZipArchive<Cursor<&'a [u8]>>,
    skip_cdk_synth: bool,
}

impl EndToEndTest<'_> {
    fn new<'a>(
        name: &'a str,
        lang: &'a str,
        stack_name: &'a str,
        skip_cdk_synth: &[&str],
        original_template: &'a str,
    ) -> EndToEndTest<'a> {
        let (cdk_app_code_writer, cdk_from_cfn_synthesizer, cdk_stack_filename, cdk_app_filename) =
            match lang {
                "typescript" => (
                    Box::new(cdk_app_code_writers::Typescript {}) as Box<dyn CdkAppCodeWriter>,
                    Box::new(synthesizer::Typescript {}) as Box<dyn Synthesizer>,
                    "stack.ts",
                    "app.ts",
                ),
                "python" => (
                    Box::new(cdk_app_code_writers::Python {}) as Box<dyn CdkAppCodeWriter>,
                    Box::new(Python {}) as Box<dyn Synthesizer>,
                    "stack.py",
                    "app.py",
                ),
                "java" => (
                    Box::new(cdk_app_code_writers::Java {}) as Box<dyn CdkAppCodeWriter>,
                    Box::<Java>::default() as Box<dyn Synthesizer>,
                    "src/main/java/com/myorg/Stack.java",
                    "src/main/java/com/myorg/MyApp.java",
                ),
                "csharp" => (
                    Box::new(cdk_app_code_writers::CSharp {}) as Box<dyn CdkAppCodeWriter>,
                    Box::new(CSharp {}) as Box<dyn Synthesizer>,
                    "Stack.cs",
                    "Program.cs",
                ),
                "golang" => (
                    Box::new(cdk_app_code_writers::Golang {}) as Box<dyn CdkAppCodeWriter>,
                    Box::<Golang>::default() as Box<dyn Synthesizer>,
                    "stack.go",
                    "",
                ),
                other => panic!("Unsupported language: {other}"),
            };

        let cursor: Cursor<&[u8]> =
            std::io::Cursor::new(include_bytes!("./end-to-end-test-snapshots.zip"));
        let snapshots_zip = zip::read::ZipArchive::new(cursor)
            .expect("failed to convert end-to-end-test-snapshots.zip contents into ZipArchive");

        EndToEndTest {
            name,
            lang,
            original_template,
            stack_name,
            cdk_app_code_writer,
            cdk_from_cfn_synthesizer,
            cdk_stack_filename,
            cdk_app_filename,
            language_boilerplate_dir: String::from(format!(
                "tests/end-to-end/app-boilerplate-files/{lang}"
            )),
            test_working_dir: String::from(format!("tests/end-to-end/{name}-{lang}-working-dir")),
            expected_outputs_dir: String::from(format!("{name}/{lang}")),
            snapshots_zip,
            skip_cdk_synth: skip_cdk_synth.contains(&lang),
        }
    }

    fn run(&mut self) {
        self.create_stack();

        let cdk_stack_definition = self.run_cdk_from_cfn();

        self.check_cdk_stack_def_matches_expected(&cdk_stack_definition);

        self.synth_cdk_app(&cdk_stack_definition);

        self.diff_original_template_with_new_templates();

        self.update_snapshots();

        self.clean();
    }

    #[tokio::main]
    async fn create_stack(&self) {
        if std::env::var_os("CREATE_STACK").is_none() {
            // By default, and in CI/CD, skip creating a CloudFormation stack with the original template.
            println!("Skipping create stack because CREATE_STACK is none");
            return;
        }
        println!("Verifying a CloudFormation stack can be created from original template");
        let region_provider = RegionProviderChain::default_provider().or_else("us-east-1");
        let config = aws_config::from_env().region(region_provider).load().await;
        let client = Client::new(&config);

        let resp = client
            .create_stack()
            .stack_name(self.stack_name)
            .template_body(self.original_template)
            .on_failure(OnFailure::Delete)
            .send()
            .await
            .expect("cfn create stack failed");
        let id = resp.stack_id.unwrap_or_default();
        print!("Stack {id} create in progress...");
        std::io::stdout().flush().expect("failed to flush stdout");

        let mut status = EndToEndTest::check_stack_status(&id, &client)
            .await
            .expect(&format!("failed to check stack status: {id}"));

        while let StackStatus::CreateInProgress = status {
            print!(".");
            std::io::stdout().flush().expect("failed to flush stdout");
            tokio::time::sleep(std::time::Duration::new(2, 0)).await;
            status = EndToEndTest::check_stack_status(&id, &client)
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

    fn run_cdk_from_cfn(&self) -> String {
        println!("Creating the cdk stack definition");
        let mut output = Vec::new();
        let cfn: CloudformationParseTree =
            serde_yaml::from_str(self.original_template).expect(&format!(
                "end-to-end/{}/template.json should be valid json",
                self.name
            ));
        let ir = CloudformationProgramIr::from(cfn)
            .expect("failed to convert cfn template into CloudformationProgramIr");
        ir.synthesize(
            self.cdk_from_cfn_synthesizer.as_ref(),
            &mut output,
            self.stack_name,
        )
        .expect("failed to synthesize cdk stack definition from cloudformation template");
        String::from_utf8(output).expect("ir.synthesize() output should be utf8")
    }

    fn check_cdk_stack_def_matches_expected(&mut self, actual_cdk_stack_def: &str) {
        if std::env::var_os("UPDATE_SNAPSHOTS").is_some() {
            // If UPDATE_SNAPSHOTS is set, then don't bother checking the expected output files, because they will be over-written. This environment variable is for development purposes, and will not be used in CI/CD.
            println!("Skipping cdk stack definition check because UPDATE_SNAPSHOTS=true");
            return;
        }

        let expected_cdk_stack_def_filename =
            &format!("{}/{}", self.expected_outputs_dir, self.cdk_stack_filename);
        println!(
            "Checking cdk stack definition matches the expected output in {}",
            expected_cdk_stack_def_filename
        );

        if let Ok(mut expected_cdk_stack_def) =
            self.snapshots_zip.by_name(expected_cdk_stack_def_filename)
        {
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

    fn synth_cdk_app(&mut self, actual_cdk_stack_def: &str) {
        // Create a temporary working directory to execute cdk synth
        create_dir_all(&self.test_working_dir).expect(&format!(
            "failed to create test working directory: {}",
            self.test_working_dir
        ));
        let test_working_dir_abs_path = canonicalize(&self.test_working_dir).expect(&format!(
            "failed to get absolute path for {}",
            self.test_working_dir
        ));
        // Write Stack definition to file
        let stack_dst_path = test_working_dir_abs_path.join(self.cdk_stack_filename);
        println!(
            "Writing cdk stack definition to file: {}",
            stack_dst_path.to_str().unwrap_or("")
        );
        let mut file = File::create(stack_dst_path).expect("failed to create cdk stack file");
        file.write_all(actual_cdk_stack_def.as_bytes())
            .expect("failed to write contents into cdk stack file");

        if self.skip_cdk_synth {
            println!("Skipping cdk synth for {}::{}", self.name, self.lang);
            return;
        }
        println!("Synth CDK app");

        // Copy language-specific boiler plate files to the working directory
        let walkdir = WalkDir::new(&self.language_boilerplate_dir);
        for entry in walkdir.into_iter().map(|e| e.expect("walkdir failed")) {
            if entry.path().is_file() {
                let filename = entry.file_name().to_str().expect(&format!(
                    "{:?} should be convertible to a string",
                    entry.file_name()
                ));
                println!("Copying {filename} into {}", self.test_working_dir);

                let from = entry.path();
                let to = format!("{}/{filename}", self.test_working_dir);
                copy(from, &to).expect(&format!("failed to copy {:?} to {}", from, &to));
            }
        }

        // App file
        let cdk_app_file_path = format!("{}/{}", self.test_working_dir, self.cdk_app_filename);
        println!("Checking for cdk app file in snapshots: {cdk_app_file_path}",);

        let app_dst_path = test_working_dir_abs_path.join(self.cdk_app_filename);
        // The parent directory for the app file might not exist yet. Example: Java uses src/main/java/com/myorg/MyApp.java
        let prefix = app_dst_path
            .parent()
            .expect("failed to get parent path for cdk app file");
        create_dir_all(prefix).expect("failed to create parent directory for cdk app file");

        if let Ok(mut cdk_app_file) = self.snapshots_zip.by_name(&cdk_app_file_path) {
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
            println!("UPDATE_SNAPSHOTS=true, and there is no existing app file, creating default one at {}", app_dst_path.to_str().unwrap_or(""));
            let mut file = File::create(app_dst_path).expect("failed to create cdk app file");
            let code: CodeBuffer = CodeBuffer::default();
            self.cdk_app_code_writer.app_file(&code, self.stack_name);
            code.write(&mut file)
                .expect("failed to write contents into cdk app file");
        } else {
            // Fail the test to prevent tests without snapshots from succeeding in CI/CD
            panic!("CDK App file not found at {}. If you are developing a new test, set UPDATE_SNAPSHOTS=true in your environment variables and the test will create a default app file.", self.cdk_app_filename);
        }

        println!(
            "Executing {}/setup-and-synth.sh in {}",
            self.language_boilerplate_dir, self.test_working_dir
        );
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

    fn diff_original_template_with_new_templates(&self) {
        if self.skip_cdk_synth {
            println!("CDK synth was skipped; skipping template comparison as well");
            return;
        }
        let walkdir = WalkDir::new(format!("{}/cdk.out/", self.test_working_dir));

        for entry in walkdir.into_iter().map(|e| {
            e.expect(
                "walkdir failed - this could indicate that cdk synth did not execute correctly",
            )
        }) {
            let filename = entry.file_name().to_str().expect(&format!(
                "{:?} should be convertible to a string",
                entry.file_name()
            ));
            if filename.contains("template.json") {
                println!("Comparing {filename} to the original template");
                let expected = &format!("./tests/end-to-end/{}/template.json", self.name);
                let actual = entry.path().to_str().expect(&format!(
                    "{:?} should be convertible to a string",
                    entry.path()
                ));
                let res = std::process::Command::new("git")
                    .args(["diff", "--no-index", expected, actual])
                    .output()
                    .expect("git diff failed");

                let stack_name = filename
                    .split(".")
                    .next()
                    .expect(&format!("failed to extract stack name from {filename}"));
                let diff_filename = &format!("{}/{stack_name}.diff", self.test_working_dir);
                let mut f = fs::File::create(diff_filename)
                    .expect(&format!("failed to create diff file: {diff_filename}"));
                f.write_all(&res.stdout).expect(&format!(
                    "failed to write contents to diff file: {diff_filename}"
                ));
            }
        }
    }

    fn update_snapshots(&mut self) {
        if std::env::var_os("UPDATE_SNAPSHOTS").is_none() {
            // By default, and in CI/CD, skip updating the snapshots
            println!("Not updating snapshots because UPDATE_SNAPSHOTS is none.");
            return;
        }
        println!("Updating snapshots because UPDATE_SNAPSHOTS=true");

        let expected_outputs_path = &format!("tests/end-to-end/{}", self.expected_outputs_dir);
        create_dir_all(expected_outputs_path).expect(&format!(
            "failed to create directory for updated snapshots at: {expected_outputs_path}"
        ));

        // App file
        // If the app file does not already exist in the snapshot, copy the one generated by this test run to the test's directory
        if self
            .snapshots_zip
            .by_name(&format!(
                "{}/{}",
                self.expected_outputs_dir, self.cdk_app_filename
            ))
            .is_err()
        {
            println!("Updating app file snapshot");
            let app_file_src = &format!("{}/{}", self.test_working_dir, self.cdk_app_filename);
            let app_file_dst = &format!("{expected_outputs_path}/{}", self.cdk_app_filename);
            copy(app_file_src, app_file_dst)
                .expect(&format!("failed to copy {app_file_src} to {app_file_dst}"));
        }

        // Stack file
        let stack_file_src = &format!("{}/{}", self.test_working_dir, self.cdk_stack_filename);
        let stack_file_dst = &format!("{expected_outputs_path}/{}", self.cdk_stack_filename);
        println!("Updating stack file snapshot");
        copy(stack_file_src, stack_file_dst).expect(&format!(
            "failed to copy {stack_file_src} to {stack_file_dst}"
        ));

        // Template and diff files
        println!("Updating template and diff file snapshot(s)");
        let walkdir = WalkDir::new(&self.test_working_dir);
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
                copy(src_path, dst_path)
                    .expect(&format!("failed to copy {src_path} to {dst_path}"));
            }
        }
    }

    fn clean(&self) {
        if std::env::var_os("SKIP_CLEAN").is_some() {
            println!("Skipping test cleanup because SKIP_CLEAN=true");
            return;
        }

        println!(
            "Cleaning up test working directory: {}",
            self.test_working_dir
        );
        remove_dir_all(&self.test_working_dir).expect(&format!(
            "failed to remove test working directory: {}",
            self.test_working_dir
        ));
    }
}
