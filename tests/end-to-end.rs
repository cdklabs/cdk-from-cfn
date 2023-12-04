use std::borrow::Cow;
use std::fs::{self, copy, create_dir_all, remove_dir_all, File, canonicalize};
use std::io::{Cursor, Read, Write};
use std::path::PathBuf;
use std::process::Command;

use aws_sdk_cloudformation::types::OnFailure;

use aws_config::meta::region::RegionProviderChain;
use aws_sdk_cloudformation::types::StackStatus;
use aws_sdk_cloudformation::{Client, Error};
use cdk_from_cfn::code::{CodeBuffer, IndentOptions};
use cdk_from_cfn::ir::CloudformationProgramIr;
use cdk_from_cfn::synthesizer::*;
use cdk_from_cfn::CloudformationParseTree;

use nom::AsBytes;
use walkdir::WalkDir;
use zip::ZipArchive;

const INDENT: Cow<'static, str> = Cow::Borrowed("    ");

mod cdk_app_synthesizers;
use cdk_app_synthesizers::CdkAppSynthesizer;

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
            // Check that the original cloudformation template is valid
            println!("Verifying a CloudFormation stack can be created from original template");
            let original_template =
                include_str!(concat!("end-to-end/", stringify!($name), "/template.json"));
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

            let mut snapshots_zip =
                get_zip_archive_from_bytes(include_bytes!("./end-to-end-test-snapshots.zip"));

            println!("Checking for cdk stack definition in the expected output");
            let expected_outputs_dir = format!("{}/{}", stringify!($name), stringify!($lang));
            let expected_cdk_stack_def_filename =
                format!("{expected_outputs_dir}/{}", $cdk_stack_filename);
            check_cdk_stack_def_matches_expected(
                &cdk_stack_definition,
                &expected_cdk_stack_def_filename,
                &mut snapshots_zip,
            );

            let test_working_dir = format!(
                "tests/end-to-end/{}-{}-working-dir",
                stringify!($name),
                stringify!($lang)
            );
            let language_boilerplate_dir = format!(
                "tests/end-to-end/app-boilerplate-files/{}",
                stringify!($lang)
            );

            let cdk_app_synthesizer: Box<dyn CdkAppSynthesizer> = match stringify!($lang) {
                "typescript" => Box::new(cdk_app_synthesizers::Typescript {}),
                "python" => Box::new(cdk_app_synthesizers::Python {}),
                &_ => todo!(),
            };
            synth_cdk_app(
                &cdk_stack_definition,
                $stack_name,
                $cdk_stack_filename,
                $cdk_app_filename,
                &language_boilerplate_dir,
                &test_working_dir,
                &expected_outputs_dir,
                &mut snapshots_zip,
                cdk_app_synthesizer.as_ref(),
            );

            diff_original_template_with_new_templates(stringify!($name), &test_working_dir);

            // update snapshots
            update_snapshots(
                $cdk_stack_filename,
                $cdk_app_filename,
                &test_working_dir,
                &expected_outputs_dir,
                &mut snapshots_zip,
            );
            // clean up test working dir
            //remove_dir_all(&test_working_dir).unwrap();
        }
    };
}

test_case!(simple, "SimpleStack");

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

fn check_cdk_stack_def_matches_expected(
    actual_cdk_stack_def: &str,
    expected_cdk_stack_def_filename: &str,
    snapshots_zip: &mut ZipArchive<Cursor<&[u8]>>,
) {
    println!(
        "Checking cdk stack definition matches the expected output in {}",
        expected_cdk_stack_def_filename
    );
    if std::env::var_os("UPDATE_SNAPSHOTS").is_some() {
        // If UPDATE_SNAPSHOTS is set, then don't bother checking the expected output files, because they will be over-written. This environment variable is for development purposes, and will not be use in CI/CD.
        println!("Skipping cdk stack definition check because UPDATE_SNAPSHOTS=true");
        return;
    }
    if let Ok(mut expected_cdk_stack_def) = snapshots_zip.by_name(expected_cdk_stack_def_filename) {
        let mut expected = String::new();
        expected_cdk_stack_def
            .read_to_string(&mut expected)
            .unwrap();
        assert_eq!(expected, actual_cdk_stack_def);
    } else {
        // If the expected file does not exist, then assume this test is new, and there is no previous snapshot to compare against.
        // Fail the test to prevent tests without snapshots from succeeding in CI/CD
        panic!("There is no cdk stack expected file for this test. If you are developing a new test, set UPDATE_SNAPSHOTS=true in your environment variables and the test will automatically create snapshot files.");
    }
}

fn get_zip_archive_from_bytes(zip: &[u8]) -> ZipArchive<Cursor<&[u8]>> {
    let cursor = std::io::Cursor::new(zip);
    zip::read::ZipArchive::new(cursor).unwrap()
}

fn synth_cdk_app(
    cdk_stack_definition: &str,
    cdk_stack_classname: &str,
    cdk_stack_filename: &str,
    cdk_app_filename: &str,
    language_boilerplate_dir: &str,
    test_working_dir: &str,
    expected_outputs_dir: &str,
    snapshots_zip: &mut ZipArchive<Cursor<&[u8]>>,
    synthesizer: &dyn CdkAppSynthesizer,
) {
    println!("Synth CDK app");

    // Create a temporary working directory, and copy language-specific boiler plate files into it
    create_dir_all(test_working_dir).unwrap();
    let walkdir = WalkDir::new(language_boilerplate_dir);
    for entry in walkdir.into_iter().map(|e| e.unwrap()) {
        if entry.path().is_file() {
            let filename = entry.file_name().to_str().unwrap();
            println!("Copying {filename} into {test_working_dir}");
            copy(entry.path(), format!("{test_working_dir}/{filename}")).unwrap();
        }
    }

    let cdk_app_file_path = format!("{expected_outputs_dir}/{cdk_app_filename}");
    println!("Checking for cdk app file in snapshots: {cdk_app_file_path}",);

    // If the app file already exists in the snapshot, copy to the test's working dir
    let app_dst_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join(test_working_dir)
        .join(cdk_app_filename);
    println!("DEBUG: app_dst_path: {:?}", app_dst_path);
    if let Ok(mut cdk_app_file) = snapshots_zip.by_name(&cdk_app_file_path) {
        let mut contents = Vec::<u8>::new();
        cdk_app_file.read_to_end(&mut contents).unwrap();
        println!(
            "An app file already exists. Copying it to: {:?}",
            app_dst_path
        );
        let mut file = File::create(app_dst_path).unwrap();
        file.write_all(contents.as_bytes()).unwrap();
    } else if std::env::var_os("UPDATE_SNAPSHOTS").is_some() {
        // If it does not already exist, create new app file
        println!("UPDATE_SNAPSHOTS=true, and there is no existing app file, creating default one at {}...", app_dst_path.to_str().unwrap());
        let mut file = File::create(app_dst_path).unwrap();
        let code: CodeBuffer = CodeBuffer::default();
        code.line("# autogenerated");
        code.line("import aws_cdk as cdk");
        code.line("from stack import SimpleStack");
        code.line("app = cdk.App()");
        code.line("SimpleStack(app, 'Stack')");
        code.line("app.synth()");
        // Recommend to manually instantiate a stack for each combination of parameters/conditionals that should be tested
        // code.line("// auto-generated! a human should update this!");
        // code.line("import * as cdk from \"aws-cdk-lib\";");
        // code.line(format!(
        //     "import {{ {} }} from \"./stack\";",
        //     cdk_stack_classname
        // ));
        // let app = code.indent_with_options(IndentOptions {
        //     indent: INDENT,
        //     leading: Some("const app = new cdk.App({".into()),
        //     trailing: Some("});".into()),
        //     trailing_newline: true,
        // });
        // let app_props = app.indent_with_options(IndentOptions {
        //     indent: INDENT,
        //     leading: Some("defaultStackSynthesizer: new cdk.DefaultStackSynthesizer({".into()),
        //     trailing: Some("}),".into()),
        //     trailing_newline: true,
        // });
        // app_props.line("generateBootstrapVersionRule: false,");
        // code.line(format!("new {}(app, \"Stack\");", cdk_stack_classname));
        // code.line("app.synth();");
        code.write(&mut file).unwrap();
    } else {
        // Fail the test to prevent tests without snapshots from succeeding in CI/CD
        panic!("CDK App file not found at {}. If you are developing a new test, set UPDATE_SNAPSHOTS=true in your environment variables and the test will create a default app file.", cdk_app_filename);
    }

    // Stack file
    let stack_dst_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join(test_working_dir)
        .join(cdk_stack_filename);
    let mut file = File::create(stack_dst_path).unwrap();
    file.write_all(cdk_stack_definition.as_bytes()).unwrap();

    let test_working_dir_abs_path = canonicalize(test_working_dir).unwrap();
    let res = Command::new("bash")
        .arg("setup.sh")
        .current_dir(&test_working_dir_abs_path)
        .output()
        .expect("command failed");
    println!("MADELINE: {:#?}", res);

}

fn diff_original_template_with_new_templates(test_name: &str, test_working_dir: &str) {
    let walkdir = WalkDir::new(format!("{test_working_dir}/cdk.out/"));

    for entry in walkdir.into_iter().map(|e| e.unwrap()) {
        let filename = entry.file_name().to_str().unwrap();
        if filename.contains("template.json") {
            println!("Comparing {filename} to the original template");
            let res = std::process::Command::new("git")
                .args([
                    "diff",
                    "--no-index",
                    &format!("./tests/end-to-end/{test_name}/template.json"),
                    entry.path().to_str().unwrap(),
                ])
                .output()
                .expect("git diff failed");

            let stack_name = filename.split(".").next().unwrap();
            let mut f = fs::File::create(format!("{test_working_dir}/{stack_name}.diff")).unwrap();
            f.write_all(&res.stdout).unwrap();
        }
    }
}

fn update_snapshots(
    cdk_stack_filename: &str,
    cdk_app_filename: &str,
    test_working_dir: &str,
    expected_outputs_dir_name: &str,
    snapshots_zip: &mut ZipArchive<Cursor<&[u8]>>,
) {
    if std::env::var_os("UPDATE_SNAPSHOTS").is_none() {
        // By default, and in CI/CD, skip updating the snapshots
        println!("Not updating snapshots because UPDATE_SNAPSHOTS is none.");
        return;
    }
    println!("Updating snapshots...");

    let expected_outputs_path = &format!("tests/end-to-end/{expected_outputs_dir_name}/");
    create_dir_all(expected_outputs_path).unwrap();

    // App file
    // If the app file does not already exist in the snapshot, copy the one generated by this test run to the test's directory
    if snapshots_zip
        .by_name(&format!("{expected_outputs_dir_name}/{cdk_app_filename}"))
        .is_err()
    {
        copy(
            format!("{test_working_dir}/{cdk_app_filename}"),
            format!("{expected_outputs_path}/{cdk_app_filename}"),
        )
        .unwrap();
    }

    // Stack file
    copy(
        format!("{test_working_dir}/{cdk_stack_filename}"),
        format!("{expected_outputs_path}/{cdk_stack_filename}"),
    )
    .unwrap();

    // Template and diff files
    let walkdir = WalkDir::new(test_working_dir);
    for entry in walkdir.into_iter().map(|e| e.unwrap()) {
        let filename = entry.file_name().to_str().unwrap();
        if entry.path().to_str().unwrap().contains("node_modules") {
            continue;
        }
        if filename.contains("template.json") {
            copy(entry.path(), format!("{expected_outputs_path}/{filename}")).unwrap();
        }
        if filename.contains(".diff") {
            copy(entry.path(), format!("{expected_outputs_path}/{filename}")).unwrap();
        }
    }
}
