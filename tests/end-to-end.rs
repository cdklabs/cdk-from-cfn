use core::panic;
use std::fs::{self, canonicalize, copy, create_dir_all, remove_dir_all, File};
use std::io::{Cursor, Read, Write};
use std::path::{Path, PathBuf};
use std::process::Command;

use aws_sdk_cloudformation::types::{OnFailure, Capability};

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
    ($name:ident, $stack_name:literal) => {
        test_case!($name, $stack_name, &[]);
    };

    ($name:ident, $stack_name:literal, $skip_cdk_synth:expr) => {
        mod $name {
            use super::*;
            test_case!($name, csharp, $stack_name, $skip_cdk_synth);
            test_case!($name, golang, $stack_name, $skip_cdk_synth);
            test_case!($name, java, $stack_name, $skip_cdk_synth);
            test_case!($name, python, $stack_name, $skip_cdk_synth);
            test_case!($name, typescript, $stack_name, $skip_cdk_synth);
        }
    };

    ($name: ident, $lang:ident, $stack_name:literal, $skip_cdk_synth:expr) => {
        #[test]
        fn $lang() {
            // GIVEN
            let mut test = EndToEndTest::new(
                stringify!($name),
                stringify!($lang),
                $stack_name,
                $skip_cdk_synth,
                include_template_str!(stringify!($name)),
            );
            // GIVEN & WHEN & THEN
            test.run();
        }
    };
}

test_case!(simple, "SimpleStack", &["golang"]);
test_case!(bucket, "BucketStack");
test_case!(config, "ConfigStack", &["golang", "java"]); //java fails cdk synth bc template produced has non-deterministic order
test_case!(documentdb, "DocumentDbStack", &["golang"]);
test_case!(resource_w_json_type_properties, "JsonPropsStack", &["golang", "java"]); //java fails cdk synth bc template produced has non-deterministic order
test_case!(vpc, "VpcStack");

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
                    "app.go",
                ),
                "java" => (
                    Box::new(cdk_app_code_writers::Java {}) as Box<dyn CdkAppCodeWriter>,
                    Box::<Java>::default() as Box<dyn Synthesizer>,
                    "src/main/java/com/myorg/Stack.java",
                    "src/main/java/com/myorg/MyApp.java",
                ),
                "python" => (
                    Box::new(cdk_app_code_writers::Python {}) as Box<dyn CdkAppCodeWriter>,
                    Box::new(Python {}) as Box<dyn Synthesizer>,
                    "stack.py",
                    "app.py",
                ),
                "typescript" => (
                    Box::new(cdk_app_code_writers::Typescript {}) as Box<dyn CdkAppCodeWriter>,
                    Box::new(synthesizer::Typescript {}) as Box<dyn Synthesizer>,
                    "stack.ts",
                    "app.ts",
                ),
                other => panic!("Unsupported language: {other}"),
            };

        let cursor: Cursor<&[u8]> =
            std::io::Cursor::new(include_bytes!("./end-to-end-test-snapshots.zip"));
        let snapshots_zip = zip::read::ZipArchive::new(cursor)
            .expect("Failed to convert end-to-end-test-snapshots.zip contents into ZipArchive");

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
        // GIVEN
        self.create_stack();

        // WHEN
        let cdk_stack_definition = self.run_cdk_from_cfn();

        // THEN
        self.check_cdk_stack_def_matches_expected(&cdk_stack_definition);

        if self.skip_cdk_synth {
            self.update_cdk_stack_def_snapshot(&cdk_stack_definition);
        } else {
            self.synth_cdk_app(&cdk_stack_definition);

            self.diff_original_template_with_new_templates();

            self.check_new_templates_and_diffs_match_expected();

            self.update_snapshots(&cdk_stack_definition);

            self.clean();
        }
    }

    #[tokio::main]
    async fn create_stack(&mut self) {
        if std::env::var_os("CREATE_STACK").is_none() {
            // By default, and in CI/CD, skip creating a CloudFormation stack
            // with the original template.
            println!("Skipping create stack because CREATE_STACK is none");
            return;
        }
        println!("Verifying a CloudFormation stack can be created from original template");
        let region_provider = RegionProviderChain::default_provider().or_else("us-east-1");
        let config = aws_config::from_env().region(region_provider).load().await;
        let client = Client::new(&config);

        if let Ok(mut create_first_template) = self
            .snapshots_zip
            .by_name(&format!("{}/create_first.json", self.name))
        {
            let mut create_first_template_str = String::new();
            create_first_template
                .read_to_string(&mut create_first_template_str)
                .expect("failed to read create_first.json from end-to-end-test-snapshots.zip");
            let stack_name = &format!("{}CreateFirst", self.stack_name);
            EndToEndTest::create_stack_from_template(
                &client,
                stack_name,
                &create_first_template_str,
            )
            .await
            .expect(&format!("failed to create stack: {stack_name}"));
        }

        EndToEndTest::create_stack_from_template(&client, self.stack_name, self.original_template)
            .await
            .expect(&format!("failed to create stack: {}", self.stack_name));
    }

    async fn create_stack_from_template(
        client: &Client,
        stack_name: &str,
        template: &str,
    ) -> Result<StackStatus, Error> {
        let resp = client
            .create_stack()
            .stack_name(stack_name)
            .template_body(template)
            .capabilities(Capability::CapabilityIam)
            .on_failure(OnFailure::Delete)
            .send()
            .await?;
        let id = resp.stack_id.unwrap_or_default();
        print!("Stack {id} create in progress...");
        std::io::stdout().flush().expect("failed to flush stdout");

        let mut status = EndToEndTest::check_stack_status(&id, &client).await?;

        while let StackStatus::CreateInProgress = status {
            print!(".");
            std::io::stdout().flush().expect("failed to flush stdout");
            tokio::time::sleep(std::time::Duration::new(2, 0)).await;
            status = EndToEndTest::check_stack_status(&id, &client).await?;
        }
        match status {
            StackStatus::CreateFailed
            | StackStatus::DeleteComplete
            | StackStatus::DeleteFailed
            | StackStatus::DeleteInProgress => {
                panic!("stack creation failed. stack status: {}", status.as_str())
            }
            StackStatus::CreateComplete => {
                println!("create complete!");
                Ok(status)
            }
            _ => panic!("unexpected stack status: {}", status.as_str()),
        }
    }

    async fn check_stack_status(id: &str, client: &Client) -> Result<StackStatus, Error> {
        let resp = client.describe_stacks().stack_name(id).send().await?;
        if let Some(stacks) = resp.stacks {
            if let Some(stack) = stacks.first() {
                if let Some(status) = &stack.stack_status {
                    return Ok(status.clone());
                }
            }
        }
        panic!("describe_stacks returned no valid stacks");
    }

    fn run_cdk_from_cfn(&self) -> String {
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
        let mut cdk_stack_definition =
            String::from_utf8(output).expect("ir.synthesize() output should be utf8");

        // Go is the only language that includes a main function defining a CDK App in the same file as the stack definition.
        // If this is a Go test, we need to remove the main function in order to use a different main function definition
        // specific for the end to end tests.
        if self.lang.eq("golang") {
            if let Some(main_fn) = cdk_stack_definition.find("func main()") {
                cdk_stack_definition.truncate(main_fn);
            }
        }
        cdk_stack_definition
    }

    fn check_cdk_stack_def_matches_expected(&mut self, actual_cdk_stack_def: &str) {
        if std::env::var_os("UPDATE_SNAPSHOTS").is_some() {
            // If UPDATE_SNAPSHOTS is set, then don't bother checking the
            // expected output files, because they will be over-written. This
            // environment variable is for development purposes, and will not be
            // used in CI/CD.
            println!("Skipping cdk stack definition check because UPDATE_SNAPSHOTS=true");
            return;
        }

        let expected_cdk_stack_def_filename =
            &format!("{}/{}", self.expected_outputs_dir, self.cdk_stack_filename);
        println!("Checking cdk stack definition matches the expected output in {expected_cdk_stack_def_filename}");

        if let Ok(mut expected_cdk_stack_def) =
            self.snapshots_zip.by_name(expected_cdk_stack_def_filename)
        {
            let mut expected = String::new();
            expected_cdk_stack_def.read_to_string(&mut expected).expect(
                "failed to read expected cdk stack definition from end-to-end-test-snapshots.zip",
            );
            assert_eq!(expected, actual_cdk_stack_def);
        } else {
            // Fail the test to prevent tests without snapshots from succeeding
            // in CI/CD
            panic!("Did not find the expected cdk stack definition in end-to-end-test-snapshots.zip at {expected_cdk_stack_def_filename}. If you are developing a new test, set UPDATE_SNAPSHOTS=true in your environment variables and the test will automatically create snapshot files.");
        }
    }

    fn update_cdk_stack_def_snapshot(&mut self, actual_cdk_stack_def: &str) {
        if std::env::var_os("UPDATE_SNAPSHOTS").is_none() {
            // By default, and in CI/CD, skip updating the snapshots
            println!("Not updating snapshots because UPDATE_SNAPSHOTS is none.");
            return;
        }
        println!("Updating cdk stack definition snapshot because UPDATE_SNAPSHOTS=true");

        let expected_outputs_path = &format!("tests/end-to-end/{}", self.expected_outputs_dir);
        create_dir_all(expected_outputs_path).expect(&format!(
            "failed to create directory for updated snapshots at: {expected_outputs_path}"
        ));

        // The parent directory for the stack file might not exist yet. Example:
        // Java uses src/main/java/com/myorg/stack.java
        let stack_file_dst = &format!("{expected_outputs_path}/{}", self.cdk_stack_filename);
        let prefix = Path::new(stack_file_dst)
            .parent()
            .expect("failed to get parent path for cdk src files");
        create_dir_all(prefix).expect("failed to create parent directory for cdk src files");

        let mut stack_file = File::create(stack_file_dst).expect("failed to create cdk stack file");
        stack_file
            .write_all(actual_cdk_stack_def.as_bytes())
            .expect("failed to write contents into cdk stack file");
    }

    fn synth_cdk_app(&mut self, actual_cdk_stack_def: &str) {
        println!("Executing cdk synth");

        // Create a temporary working directory to execute cdk synth
        if Path::new(&self.test_working_dir).exists() {
            remove_dir_all(&self.test_working_dir).expect("failed to remove working dir");
        }
        create_dir_all(&self.test_working_dir).expect(&format!(
            "failed to create test working directory: {}",
            self.test_working_dir
        ));

        let test_working_dir_abs_path = canonicalize(&self.test_working_dir).expect(&format!(
            "failed to get absolute path for {}",
            self.test_working_dir
        ));

        // Write Stack definition to a file in the working directory
        let stack_dst_path = test_working_dir_abs_path.join(self.cdk_stack_filename);
        // The parent directory for the src files might not exist yet. Example:
        // Java uses src/main/java/com/myorg/*.java
        let prefix = stack_dst_path
            .parent()
            .expect("failed to get parent path for cdk app file");
        create_dir_all(prefix).expect("failed to create parent directory for cdk app file");
        let mut file = File::create(stack_dst_path).expect("failed to create cdk stack file");
        file.write_all(actual_cdk_stack_def.as_bytes())
            .expect("failed to write contents into cdk stack file");

        // Write App definition to a file
        self.create_or_copy_app_file(&test_working_dir_abs_path);

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

    fn create_or_copy_app_file(&mut self, test_working_dir_abs_path: &PathBuf) {
        let cdk_app_file_path = format!("{}/{}", self.expected_outputs_dir, self.cdk_app_filename);

        let app_dst_path = test_working_dir_abs_path.join(self.cdk_app_filename);
        if let Ok(mut cdk_app_file) = self.snapshots_zip.by_name(&cdk_app_file_path) {
            println!(
                "An app file already exists. Copying it from {cdk_app_file_path} to {}",
                app_dst_path.to_str().unwrap_or("")
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
            let mut file: File = File::create(app_dst_path).expect("failed to create cdk app file");
            let code: CodeBuffer = CodeBuffer::default();
            self.cdk_app_code_writer.app_file(&code, self.stack_name);
            code.write(&mut file)
                .expect("failed to write contents into cdk app file");
        } else {
            // Fail the test to prevent tests without snapshots from succeeding
            // in CI/CD
            panic!("CDK App file not found in snapshots at {cdk_app_file_path}. If you are developing a new test, set UPDATE_SNAPSHOTS=true in your environment variables and the test will create a default app file.");
        }
    }

    fn diff_original_template_with_new_templates(&self) {
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
                    .args(["diff", "--no-index", "--ignore-all-space", expected, actual])
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

    fn check_new_templates_and_diffs_match_expected(&self) {
        if std::env::var_os("UPDATE_SNAPSHOTS").is_some() {
            // If UPDATE_SNAPSHOTS is set, then don't bother checking the
            // expected output files, because they will be over-written. This
            // environment variable is for development purposes, and will not be
            // used in CI/CD.
            println!("Skipping template files and diff files check because UPDATE_SNAPSHOTS=true");
            return;
        }

        println!("Checking the diff between new template(s) and the original template match expected diff file(s)");
        println!("Checking new template(s) match expected template file(s)");
        let mut actual_outputs = self.get_template_and_diff_dir_entries(&self.test_working_dir);
        let mut expected_outputs = self.get_template_and_diff_dir_entries(&format!(
            "tests/end-to-end/{}",
            self.expected_outputs_dir
        ));

        // Iterate over the actual and expected template and diff files, and
        // remove entries from the vector as they are proven to be correct. Any
        // remaining entries in `actual_outputs` or `expected_outputs` will
        // result in test failure.
        let mut actual_index = 0;
        let mut stacks_with_empty_diffs: Vec<String> = Vec::new();
        while actual_index < actual_outputs.len() {
            let actual = actual_outputs.get(actual_index).expect(&format!(
                "{actual_index} should be less than {}",
                actual_outputs.len()
            ));

            // Look for an expected file to match the current actual file
            let mut index_of_expected_file_that_matches_actual_file = None;
            for expected_index in 0..expected_outputs.len() {
                let expected = expected_outputs.get(expected_index).expect(&format!(
                    "{expected_index} should be less than {}",
                    expected_outputs.len()
                ));
                if expected.file_name() == actual.file_name() {
                    println!("Checking if {:?} matches {:?} ", expected, actual);
                    let expected =
                        fs::read_to_string(expected.path()).expect("failed to read file");
                    let actual = fs::read_to_string(actual.path()).expect("failed to read file");
                    assert_eq!(expected, actual);
                    index_of_expected_file_that_matches_actual_file = Some(expected_index);
                    break;
                }
            }

            // If a match was found, or if the diff file is empty, we can remove
            // the relevant files from the vector. Otherwise, increment the
            // index counter.
            if let Some(i) = index_of_expected_file_that_matches_actual_file {
                actual_outputs.remove(actual_index);
                expected_outputs.remove(i);
            } else if actual
                .file_name()
                .to_str()
                .expect("failed to convert filename to str")
                .contains(".diff")
                && fs::read_to_string(actual.path())
                    .expect("failed to read file")
                    .len()
                    == 0
            {
                let stack_name = String::from(
                    actual
                        .file_name()
                        .to_str()
                        .expect("failed to convert filename to string")
                        .split(".")
                        .next()
                        .expect(&format!(
                            "filename should have a '.' in it: {:?}",
                            actual.file_name()
                        )),
                );
                stacks_with_empty_diffs.push(stack_name);
                actual_outputs.remove(actual_index);
            } else {
                actual_index += 1;
            }
        }

        // Remove template files that correspond to empty diff files. If there
        // is no difference between the original template and the new template
        // (generated by the cdk app generated by cdk_from_cfn), then the new
        // template is not stored in the snapshot, to reduce cognitive load when
        // reviewing test snapshots. So, if the actual diff file was empty, then
        // we expect there to be no diff or template file in the expected
        // outputs.
        let mut actual_index = 0;
        while actual_index < actual_outputs.len() {
            let actual = actual_outputs.get(actual_index).expect(&format!(
                "{actual_index} should be less than {}",
                actual_outputs.len()
            ));
            let stack_name = String::from(
                actual
                    .file_name()
                    .to_str()
                    .expect("failed to convert filename to string")
                    .split(".")
                    .next()
                    .unwrap(),
            );
            if stacks_with_empty_diffs.contains(&stack_name) {
                actual_outputs.remove(actual_index);
            } else {
                actual_index += 1;
            }
        }

        // Finally print out the name of the files that are remaining, which
        // means they do not have a corresponding match in either the expected
        // output or the actual output.
        if actual_outputs.len() > 0 || expected_outputs.len() > 0 {
            actual_outputs.iter().for_each(|e| {
                println!(
                    "Test run created an unexpected file: {:?}",
                    e.path().to_str()
                );
            });
            expected_outputs.iter().for_each(|e| {
                println!(
                    "Test run did not create an expected file: {:?}",
                    e.path().to_str()
                );
            });
            panic!("Test failed because expected and actual files did not match. See above output for details.");
        }
    }

    fn get_template_and_diff_dir_entries(&self, dir: &str) -> Vec<walkdir::DirEntry> {
        // Returns an owned vector of directory entries that are .diff or .template.json files
        let walkdir = WalkDir::new(dir);
        let template_and_diff_files = walkdir.sort_by_file_name().into_iter().filter(|e| {
            let entry = e.as_ref().expect("d");
            let filename = entry.file_name().to_str().unwrap();
            let path = entry.path().to_str().unwrap();
            filename.contains(".diff")
                || (filename.contains(".template.json") && !path.contains("node_modules"))
        });
        let template_and_diff_files = template_and_diff_files.map(|e| e.expect("failed"));
        template_and_diff_files.collect::<Vec<_>>().to_owned()
    }

    fn update_snapshots(&mut self, actual_cdk_stack_def: &str) {
        if std::env::var_os("UPDATE_SNAPSHOTS").is_none() {
            // By default, and in CI/CD, skip updating the snapshots
            println!("Not updating snapshots because UPDATE_SNAPSHOTS is none.");
            return;
        }
        println!("Updating snapshots because UPDATE_SNAPSHOTS=true");
        self.update_cdk_stack_def_snapshot(actual_cdk_stack_def);

        let expected_outputs_path = &format!("tests/end-to-end/{}", self.expected_outputs_dir);

        // If the app file does not already exist in the snapshot, copy
        // the one generated by this test run to the test's directory
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
            // Check if the app file exists before trying to copy it. It may not exist if the test did not run cdk synth.
            if Path::new(app_file_src).exists() {
                copy(app_file_src, app_file_dst)
                    .expect(&format!("failed to copy {app_file_src} to {app_file_dst}"));
            }
        }

        // Template and diff files
        println!("Updating template and diff file snapshot(s)");
        let walkdir = self.get_template_and_diff_dir_entries(&self.test_working_dir);
        for entry in walkdir {
            let filename = entry.file_name().to_str().expect(&format!(
                "{:?} should be convertible to a string",
                entry.file_name()
            ));

            if filename.contains(".diff") {
                let diff_dst_path = &format!("{expected_outputs_path}/{filename}");
                let stack_name = String::from(
                    filename
                        .split(".")
                        .next()
                        .expect(&format!("filename should have a '.' in it: {filename}")),
                );
                let template_filename = format!("{stack_name}.template.json");
                let template_dst_path = &format!("{expected_outputs_path}/{template_filename}");
                if fs::metadata(entry.path())
                    .expect("failed to get metadata")
                    .len()
                    > 0
                {
                    // If the diff is not empty, save it, and the corresponding template file
                    copy(entry.path(), diff_dst_path)
                        .expect(&format!("failed to copy {filename} to {diff_dst_path}"));
                    let template_src_path =
                        format!("{}/cdk.out/{}", self.test_working_dir, template_filename);
                    copy(template_src_path, template_dst_path).expect("iugh");
                } else {
                    // If the diff is empty - delete the previous snapshots if there are any
                    println!("diff file is 0");
                    if Path::new(diff_dst_path).exists() {
                        fs::remove_file(diff_dst_path).expect("failed to remove file");
                    }
                    if Path::new(template_dst_path).exists() {
                        fs::remove_file(template_dst_path).expect("failed to remove file");
                    }
                }
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
