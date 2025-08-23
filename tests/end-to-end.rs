// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use std::env;
use std::fs::{self, canonicalize, copy, create_dir_all, remove_dir_all, File};
use std::io::{self, Read, Write};
use std::panic::{self, AssertUnwindSafe};
use std::path::{Path, PathBuf};
use std::process::Command;
use std::time::Duration;

use aws_config::BehaviorVersion;
use aws_sdk_cloudformation::types::{Capability, OnFailure};

use aws_config::meta::region::RegionProviderChain;
use aws_sdk_cloudformation::error::ProvideErrorMetadata;
use aws_sdk_cloudformation::types::StackStatus;
use aws_sdk_cloudformation::{Client, Error};
use aws_sdk_s3::Client as S3Client;
use cdk_from_cfn::cdk::Schema;
use cdk_from_cfn::code::CodeBuffer;
use cdk_from_cfn::ir::CloudformationProgramIr;
use cdk_from_cfn::synthesizer::{self, *};
use cdk_from_cfn::CloudformationParseTree;

use nom::AsBytes;
use serial_test::serial;
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
        #[serial($name)]
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
test_case!(
    resource_w_json_type_properties,
    "JsonPropsStack",
    &["golang", "java"]
); //java fails cdk synth bc template produced has non-deterministic order
test_case!(vpc, "VpcStack");

test_case!(sam_nodejs_lambda, "SAMNodeJSLambda");
// These stack should be identical to the ones above
test_case!(sam_nodejs_lambda_arr_transform, "SAMNodeJSLambdaArr");
test_case!(batch, "BatchStack", &["golang", "java"]); //java fails cdk synth bc template produced has non-deterministic order
test_case!(cloudwatch, "CloudwatchStack", &["golang"]);
test_case!(ecs, "EcsStack", &["java", "golang"]);
test_case!(ec2, "Ec2Stack", &["java", "golang"]);
test_case!(efs, "EfsStack", &["java", "golang"]);
test_case!(ec2_encryption, "Ec2EncryptionStack", &["golang", "java"]);

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
    snapshots_zip: ZipArchive<File>,
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
                    Box::<CSharp>::default() as Box<dyn Synthesizer>,
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

        let source = File::open(PathBuf::from(env::var("END_TO_END_SNAPSHOTS").unwrap())).unwrap();
        let snapshots_zip = ZipArchive::new(source)
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
            language_boilerplate_dir: format!("tests/end-to-end/app-boilerplate-files/{lang}"),
            test_working_dir: format!("tests/end-to-end/{name}-{lang}-working-dir"),
            expected_outputs_dir: format!("{name}/{lang}"),
            snapshots_zip,
            skip_cdk_synth: skip_cdk_synth.contains(&lang),
        }
    }

    fn run(&mut self) {
        let should_create_stacks = env::var_os("CREATE_CFN_STACK").is_some();
        let mut errors = Vec::new();
        let mut cdk_synth_successful = false;
        let mut cleanup_stacks = false;

        let result = panic::catch_unwind(AssertUnwindSafe(|| {
            // WHEN
            let cdk_stack_definition =
                match panic::catch_unwind(AssertUnwindSafe(|| self.run_cdk_from_cfn())) {
                    Ok(def) => def,
                    Err(e) => {
                        errors.push(format!("CDK synthesis failed: {:?}", e));
                        return;
                    }
                };

            // THEN
            if env::var_os("UPDATE_SNAPSHOTS").is_none() {
                if let Err(e) = panic::catch_unwind(AssertUnwindSafe(|| {
                    self.check_cdk_stack_def_matches_expected(&cdk_stack_definition);
                })) {
                    errors.push(format!("Stack definition check failed: {:?}", e));
                }
            }

            if self.skip_cdk_synth || env::var_os("SKIP_SYNTH").is_some() {
                if env::var_os("SKIP_SYNTH").is_some() {
                    let _ = writeln!(
                        io::stderr(),
                        "✓ Test passed for {}/{} - CDK synthesis skipped (SKIP_SYNTH set)",
                        self.name,
                        self.lang
                    );
                } else {
                    let _ = writeln!(
                        io::stderr(),
                        "✓ Test passed for {}/{} - CDK synthesis skipped (configured)",
                        self.name,
                        self.lang
                    );
                }
                if env::var_os("UPDATE_SNAPSHOTS").is_some() {
                    if let Err(e) = panic::catch_unwind(AssertUnwindSafe(|| {
                        self.update_cdk_stack_def_snapshot(&cdk_stack_definition);
                    })) {
                        errors.push(format!("Snapshot update failed: {:?}", e));
                    }
                }
            } else {
                if let Err(e) = panic::catch_unwind(AssertUnwindSafe(|| {
                    self.synth_cdk_app(&cdk_stack_definition);
                })) {
                    errors.push(format!("CDK synth failed: {:?}", e));
                } else {
                    cdk_synth_successful = true;
                }

                // Only create CloudFormation stacks after successful CDK synthesis
                if should_create_stacks && cdk_synth_successful {
                    match tokio::runtime::Runtime::new()
                        .unwrap()
                        .block_on(self.create_cfn_stack())
                    {
                        Ok(_) => {
                            cleanup_stacks = true;
                        }
                        Err(e) => {
                            errors.push(format!("Stack creation failed: {}", e));
                        }
                    }
                } else if should_create_stacks && !cdk_synth_successful {
                    println!(
                        "Skipping CloudFormation stack deployment due to CDK synthesis failure"
                    );
                } else if !should_create_stacks {
                    println!("Skipping CloudFormation stack deployment (CREATE_CFN_STACK not set)");
                }

                if let Err(e) = panic::catch_unwind(AssertUnwindSafe(|| {
                    self.diff_original_template_with_new_templates();
                })) {
                    errors.push(format!("Template diff failed: {:?}", e));
                }

                if env::var_os("UPDATE_SNAPSHOTS").is_some() {
                    if let Err(e) = panic::catch_unwind(AssertUnwindSafe(|| {
                        self.update_snapshots(&cdk_stack_definition);
                    })) {
                        errors.push(format!("Snapshot update failed: {:?}", e));
                    }
                } else if let Err(e) = panic::catch_unwind(AssertUnwindSafe(|| {
                    self.check_new_templates_and_diffs_match_expected();
                })) {
                    errors.push(format!("Template/diff check failed: {:?}", e));
                }

                if env::var_os("SKIP_CLEAN").is_none() {
                    if let Err(e) = panic::catch_unwind(AssertUnwindSafe(|| {
                        self.clean();
                    })) {
                        errors.push(format!("Cleanup failed: {:?}", e));
                    }
                } else {
                    println!("Skipping test directory cleanup because SKIP_CLEAN=true");
                }
            }
        }));

        // Cleanup stacks regardless of test success or failure
        if cleanup_stacks {
            if let Err(e) = panic::catch_unwind(AssertUnwindSafe(|| {
                if env::var_os("FAIL_FAST").is_some() {
                    tokio::runtime::Runtime::new()
                        .unwrap()
                        .block_on(self.initiate_cfn_stack_deletion());
                } else {
                    tokio::runtime::Runtime::new()
                        .unwrap()
                        .block_on(self.cleanup_cfn_stacks());
                }
            })) {
                errors.push(format!("Stack cleanup failed: {:?}", e));
            }
        }

        // Report all errors at the end
        if !errors.is_empty() {
            println!(
                "\n=== TEST FAILURE SUMMARY for {}/{} ===",
                self.name, self.lang
            );
            for (i, error) in errors.iter().enumerate() {
                println!("{}. {}", i + 1, error);
            }
            println!("=== END FAILURE SUMMARY ===\n");
            panic!("Test failed with {} error(s)", errors.len());
        }

        // Re-panic if there was an uncaught error
        if let Err(e) = result {
            panic::resume_unwind(e);
        }
    }

    async fn create_cfn_stack(&mut self) -> Result<(), String> {
        println!("Verifying a CloudFormation stack can be created from original template");
        let region_provider = RegionProviderChain::default_provider().or_else("us-east-1");
        let config = aws_config::defaults(BehaviorVersion::latest())
            .region(region_provider)
            .load()
            .await;
        let client = Client::new(&config);

        if let Ok(mut create_first_template) = self
            .snapshots_zip
            .by_name(&format!("{}/create_first.json", self.name))
        {
            let mut create_first_template_str = String::new();
            create_first_template
                .read_to_string(&mut create_first_template_str)
                .map_err(|e| format!("failed to read create_first.json: {e}"))?;
            let stack_name = &format!("{}CreateFirst", self.stack_name);
            EndToEndTest::create_cfn_stack_from_template(
                &client,
                stack_name,
                &create_first_template_str,
            )
            .await
            .map_err(|e| format!("failed to create stack {stack_name}: {e}"))?;
        }

        EndToEndTest::create_cfn_stack_from_template(
            &client,
            self.stack_name,
            self.original_template,
        )
        .await
        .map_err(|e| format!("failed to create stack {}: {e}", self.stack_name))?;

        Ok(())
    }

    async fn cleanup_cfn_stacks(&mut self) {
        println!("Cleaning up CloudFormation stacks");
        let region_provider = RegionProviderChain::default_provider().or_else("us-east-1");
        let config = aws_config::defaults(BehaviorVersion::latest())
            .region(region_provider)
            .load()
            .await;
        let client = Client::new(&config);
        let s3_client = S3Client::new(&config);

        // Delete main stack
        let _ = EndToEndTest::delete_cfn_stack(&client, &s3_client, self.stack_name).await;

        // Delete create_first stack if it exists
        let create_first_stack_name = &format!("{}CreateFirst", self.stack_name);
        let _ = EndToEndTest::delete_cfn_stack(&client, &s3_client, create_first_stack_name).await;
    }

    async fn initiate_cfn_stack_deletion(&mut self) {
        println!("Initiating CloudFormation stack deletion (FAIL_FAST mode - not waiting for completion)");
        let region_provider = RegionProviderChain::default_provider().or_else("us-east-1");
        let config = aws_config::defaults(BehaviorVersion::latest())
            .region(region_provider)
            .load()
            .await;
        let client = Client::new(&config);
        let s3_client = S3Client::new(&config);

        // Initiate deletion of main stack
        let _ =
            EndToEndTest::initiate_cfn_stack_deletion_only(&client, &s3_client, self.stack_name)
                .await;

        // Initiate deletion of create_first stack if it exists
        let create_first_stack_name = &format!("{}CreateFirst", self.stack_name);
        let _ = EndToEndTest::initiate_cfn_stack_deletion_only(
            &client,
            &s3_client,
            create_first_stack_name,
        )
        .await;
    }

    async fn delete_cfn_stack(
        client: &Client,
        s3_client: &S3Client,
        stack_name: &str,
    ) -> Result<(), Error> {
        println!("Deleting stack: {stack_name}");

        // Empty S3 buckets before deleting stack
        let _ = EndToEndTest::empty_stack_buckets(client, s3_client, stack_name).await;

        let _ = client.delete_stack().stack_name(stack_name).send().await?;

        // Wait for deletion to complete
        loop {
            match EndToEndTest::check_stack_status(stack_name, client).await {
                Ok(status) => match status {
                    StackStatus::DeleteInProgress => {
                        print!(".");
                        io::stdout().flush().expect("failed to flush stdout");
                        tokio::time::sleep(Duration::new(2, 0)).await;
                    }
                    StackStatus::DeleteComplete => {
                        println!("\nStack {stack_name} deleted successfully");
                        break;
                    }
                    StackStatus::DeleteFailed => {
                        println!("\nStack {stack_name} deletion failed");
                        break;
                    }
                    _ => {
                        println!(
                            "\nUnexpected stack status during deletion: {}",
                            status.as_str()
                        );
                        break;
                    }
                },
                Err(_) => {
                    // Stack not found - deletion complete
                    println!("\nStack {stack_name} deleted successfully");
                    break;
                }
            }
        }
        Ok(())
    }

    async fn initiate_cfn_stack_deletion_only(
        client: &Client,
        s3_client: &S3Client,
        stack_name: &str,
    ) -> Result<(), Error> {
        println!("Initiating deletion of stack: {stack_name}");

        // Empty S3 buckets before deleting stack
        let _ = EndToEndTest::empty_stack_buckets(client, s3_client, stack_name).await;

        // Start deletion but don't wait for completion
        let _ = client.delete_stack().stack_name(stack_name).send().await?;
        println!("Stack deletion initiated for: {stack_name}");

        Ok(())
    }

    async fn empty_stack_buckets(
        cfn_client: &Client,
        s3_client: &S3Client,
        stack_name: &str,
    ) -> Result<(), Box<dyn std::error::Error>> {
        // Get stack resources
        let resources = cfn_client
            .list_stack_resources()
            .stack_name(stack_name)
            .send()
            .await?;

        if let Some(summaries) = resources.stack_resource_summaries {
            for resource in summaries {
                if resource.resource_type == Some("AWS::S3::Bucket".to_string()) {
                    if let Some(bucket_name) = resource.physical_resource_id {
                        println!("Emptying S3 bucket: {bucket_name}");
                        let _ = EndToEndTest::empty_bucket(s3_client, &bucket_name).await;
                    }
                }
            }
        }
        Ok(())
    }

    async fn empty_bucket(
        s3_client: &S3Client,
        bucket_name: &str,
    ) -> Result<(), Box<dyn std::error::Error>> {
        // List and delete all objects
        let mut continuation_token = None;
        loop {
            let mut list_request = s3_client.list_objects_v2().bucket(bucket_name);
            if let Some(token) = continuation_token {
                list_request = list_request.continuation_token(token);
            }

            let objects = list_request.send().await?;

            if let Some(contents) = objects.contents {
                if !contents.is_empty() {
                    let delete_objects: Vec<_> = contents
                        .iter()
                        .filter_map(|obj| obj.key.as_ref())
                        .map(|key| {
                            aws_sdk_s3::types::ObjectIdentifier::builder()
                                .key(key)
                                .build()
                                .unwrap()
                        })
                        .collect();

                    if !delete_objects.is_empty() {
                        let delete_request = aws_sdk_s3::types::Delete::builder()
                            .set_objects(Some(delete_objects))
                            .build()?;
                        let _ = s3_client
                            .delete_objects()
                            .bucket(bucket_name)
                            .delete(delete_request)
                            .send()
                            .await?;
                    }
                }
            }

            if !objects.is_truncated.unwrap_or(false) {
                break;
            }
            continuation_token = objects.next_continuation_token;
        }
        Ok(())
    }

    async fn create_cfn_stack_from_template(
        client: &Client,
        stack_name: &str,
        template: &str,
    ) -> Result<StackStatus, String> {
        let resp = client
            .create_stack()
            .stack_name(stack_name)
            .template_body(template)
            .capabilities(Capability::CapabilityIam)
            .capabilities(Capability::CapabilityNamedIam)
            .capabilities(Capability::CapabilityAutoExpand)
            .on_failure(OnFailure::Delete)
            .send()
            .await
            .map_err(|e| {
                let error_code = e.code().unwrap_or("Unknown");
                let error_message = e.message().unwrap_or("No message");
                format!(
                    "CreateStack API failed - Code: {}, Message: {}, Full Error: {}",
                    error_code, error_message, e
                )
            })?;
        let id = resp.stack_id.unwrap_or_default();
        print!("Stack {id} create in progress...");
        io::stdout().flush().expect("failed to flush stdout");

        let mut status = EndToEndTest::check_stack_status(&id, client)
            .await
            .map_err(|e| {
                let error_code = e.code().unwrap_or("Unknown");
                let error_message = e.message().unwrap_or("No message");
                format!(
                    "DescribeStacks API failed - Code: {}, Message: {}, Full Error: {}",
                    error_code, error_message, e
                )
            })?;

        while let StackStatus::CreateInProgress = status {
            print!(".");
            io::stdout().flush().expect("failed to flush stdout");
            tokio::time::sleep(Duration::new(2, 0)).await;
            status = EndToEndTest::check_stack_status(&id, client)
                .await
                .map_err(|e| {
                    let error_code = e.code().unwrap_or("Unknown");
                    let error_message = e.message().unwrap_or("No message");
                    format!(
                        "DescribeStacks API failed - Code: {}, Message: {}, Full Error: {}",
                        error_code, error_message, e
                    )
                })?;
        }
        match status {
            StackStatus::CreateFailed
            | StackStatus::DeleteComplete
            | StackStatus::DeleteFailed
            | StackStatus::DeleteInProgress => Err(format!(
                "stack creation failed. stack status: {}",
                status.as_str()
            )),
            StackStatus::CreateComplete => {
                println!("create complete!");
                Ok(status)
            }
            _ => Err(format!("unexpected stack status: {}", status.as_str())),
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
        let cfn: CloudformationParseTree = serde_yaml::from_str(self.original_template)
            .unwrap_or_else(|_| {
                panic!(
                    "end-to-end/{}/template.json should be valid json",
                    self.name
                )
            });
        let schema = Schema::builtin();

        let ir = CloudformationProgramIr::from(cfn, schema)
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
        println!("Updating cdk stack definition snapshot because UPDATE_SNAPSHOTS=true");

        let expected_outputs_path = &format!("tests/end-to-end/{}", self.expected_outputs_dir);
        create_dir_all(expected_outputs_path).unwrap_or_else(|_| {
            panic!("failed to create directory for updated snapshots at: {expected_outputs_path}")
        });

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
        create_dir_all(&self.test_working_dir).unwrap_or_else(|_| {
            panic!(
                "failed to create test working directory: {}",
                self.test_working_dir
            )
        });

        let test_working_dir_abs_path = canonicalize(&self.test_working_dir).unwrap_or_else(|_| {
            panic!("failed to get absolute path for {}", self.test_working_dir)
        });

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
                let filename = entry.file_name().to_str().unwrap_or_else(|| {
                    panic!("{:?} should be convertible to a string", entry.file_name())
                });
                println!("Copying {filename} into {}", self.test_working_dir);

                let from = entry.path();
                let to = format!("{}/{filename}", self.test_working_dir);
                copy(from, &to).unwrap_or_else(|_| panic!("failed to copy {:?} to {}", from, &to));
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

    fn create_or_copy_app_file(&mut self, test_working_dir_abs_path: &Path) {
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
        } else if env::var_os("UPDATE_SNAPSHOTS").is_some() {
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
            let filename = entry.file_name().to_str().unwrap_or_else(|| {
                panic!("{:?} should be convertible to a string", entry.file_name())
            });
            if filename.contains("template.json") {
                println!("Comparing {filename} to the original template");
                let expected = &format!("./tests/end-to-end/{}/template.json", self.name);
                let actual = entry.path().to_str().unwrap_or_else(|| {
                    panic!("{:?} should be convertible to a string", entry.path())
                });
                let res = Command::new("git")
                    .args(["diff", "--no-index", "--ignore-all-space", expected, actual])
                    .output()
                    .expect("git diff failed");

                let stack_name = filename
                    .split('.')
                    .next()
                    .unwrap_or_else(|| panic!("failed to extract stack name from {filename}"));
                let diff_filename = &format!("{}/{stack_name}.diff", self.test_working_dir);
                let mut f = fs::File::create(diff_filename)
                    .unwrap_or_else(|_| panic!("failed to create diff file: {diff_filename}"));
                f.write_all(&res.stdout).unwrap_or_else(|_| {
                    panic!("failed to write contents to diff file: {diff_filename}")
                });
            }
        }
    }

    fn check_new_templates_and_diffs_match_expected(&self) {
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
            let actual = actual_outputs.get(actual_index).unwrap_or_else(|| {
                panic!(
                    "{actual_index} should be less than {}",
                    actual_outputs.len()
                )
            });

            // Look for an expected file to match the current actual file
            let mut index_of_expected_file_that_matches_actual_file = None;
            for expected_index in 0..expected_outputs.len() {
                let expected = expected_outputs.get(expected_index).unwrap_or_else(|| {
                    panic!(
                        "{expected_index} should be less than {}",
                        expected_outputs.len()
                    )
                });
                if expected.file_name() == actual.file_name() {
                    println!("Checking if {expected:?} matches {actual:?} ");
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
                    .is_empty()
            {
                let stack_name = String::from(
                    actual
                        .file_name()
                        .to_str()
                        .expect("failed to convert filename to string")
                        .split('.')
                        .next()
                        .unwrap_or_else(|| {
                            panic!("filename should have a '.' in it: {:?}", actual.file_name())
                        }),
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
            let actual = actual_outputs.get(actual_index).unwrap_or_else(|| {
                panic!(
                    "{actual_index} should be less than {}",
                    actual_outputs.len()
                )
            });
            let stack_name = String::from(
                actual
                    .file_name()
                    .to_str()
                    .expect("failed to convert filename to string")
                    .split('.')
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
        if !actual_outputs.is_empty() || !expected_outputs.is_empty() {
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
                    .unwrap_or_else(|_| panic!("failed to copy {app_file_src} to {app_file_dst}"));
            }
        }

        // Template and diff files
        println!("Updating template and diff file snapshot(s)");
        let walkdir = self.get_template_and_diff_dir_entries(&self.test_working_dir);
        for entry in walkdir {
            let filename = entry.file_name().to_str().unwrap_or_else(|| {
                panic!("{:?} should be convertible to a string", entry.file_name())
            });

            if filename.contains(".diff") {
                let diff_dst_path = &format!("{expected_outputs_path}/{filename}");
                let stack_name = String::from(
                    filename
                        .split('.')
                        .next()
                        .unwrap_or_else(|| panic!("filename should have a '.' in it: {filename}")),
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
                        .unwrap_or_else(|_| panic!("failed to copy {filename} to {diff_dst_path}"));
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
        println!(
            "Cleaning up test working directory: {}",
            self.test_working_dir
        );
        remove_dir_all(&self.test_working_dir).unwrap_or_else(|_| {
            panic!(
                "failed to remove test working directory: {}",
                self.test_working_dir
            )
        });
    }
}
