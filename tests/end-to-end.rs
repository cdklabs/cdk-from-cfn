use std::fs::{File, self};
use std::io::Write;
use std::path::PathBuf;
use std::process::Command;

use aws_sdk_cloudformation::types::OnFailure;

use aws_config::meta::region::RegionProviderChain;
use aws_sdk_cloudformation::types::StackStatus;
use aws_sdk_cloudformation::{Client, Error};
use cdk_from_cfn::ir::CloudformationProgramIr;
use cdk_from_cfn::synthesizer::*;
use cdk_from_cfn::CloudformationParseTree;

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
                "app.go"
            );

            #[cfg(feature = "java")]
            test_case!(
                $name,
                java,
                &Java::new(concat!("com.myorg")),
                $stack_name,
                "App.java"
            );

            #[cfg(feature = "python")]
            test_case!($name, python, &Python {}, $stack_name, "app.py");

            #[cfg(feature = "typescript")]
            test_case!($name, typescript, &Typescript {}, $stack_name, "app.ts");

            #[cfg(feature = "csharp")]
            test_case!($name, csharp, &CSharp {}, $stack_name, "App.cs");
        }
    };

    ($name:ident, $lang:ident, $synthesizer:expr, $stack_name:literal, $expected:literal) => {
        #[test]
        fn $lang() {
            // ? Does cloudformation template deploy successfully
            // allow disabling with a flag
            // allow cleaning up and deleting the template at the end with a flag
            let template = include_str!(concat!("end-to-end/", stringify!($name), "/template.yml"));
            /*
            let result = deploy_template(stringify!($name), template);
            match result {
                Err(e) => panic!("{}", e),
                Ok(_) => {}
            }
            println!("{:?}", result);
            */

            let expected = include_str!(concat!("end-to-end/", stringify!($name), "/", $expected));
            let actual = {
                let mut output = Vec::with_capacity(expected.len());
                // Does IR succeed
                let cfn: CloudformationParseTree = serde_yaml::from_str(include_str!(concat!(
                    "end-to-end/",
                    stringify!($name),
                    "/template.yml"
                )))
                .unwrap();
                let ir = CloudformationProgramIr::from(cfn).unwrap();
                // Does it synthesize
                ir.synthesize($synthesizer, &mut output, $stack_name)
                    .unwrap();
                String::from_utf8(output).unwrap()
            };

            let _update_snapshots = UpdateSnapshot::new(
                concat!("end-to-end/", stringify!($name), "/", $expected),
                &actual,
                &expected,
            );
            assert_eq!(expected, actual);

            // Add CDK boiler plate stuff
            // instantiate a stack for each possible combination of parameters
            // Synth the app - does that succeed?

            synth_app(&actual);

            // Compare each stack to the original

            // What is the delta?

            // Can delta be auto approved?

            // Is there already a file with approved diff?

            // If not, is the flag set to update snapshots? interactive show file to user to approve

            // Make sure it works in each language
        }
    };
}

#[tokio::main]
async fn deploy_template(
    stack_name: impl Into<String>,
    template: impl Into<String>,
) -> Result<(), Error> {
    println!("deploy template");
    let region_provider = RegionProviderChain::default_provider().or_else("us-east-1");
    let config = aws_config::from_env().region(region_provider).load().await;
    let client = Client::new(&config);

    let resp = client
        .create_stack()
        .stack_name(stack_name)
        .template_body(template)
        .on_failure(OnFailure::Delete)
        .send()
        .await?;
    let id = resp.stack_id.unwrap_or_default();
    print!("Stack {id} create in progress...");
    std::io::stdout().flush().unwrap();

    let mut status = check_stack_status(&id, &client).await?;

    while let StackStatus::CreateInProgress = status {
        print!(".");
        std::io::stdout().flush().unwrap();
        tokio::time::sleep(std::time::Duration::new(2, 0)).await;
        status = check_stack_status(&id, &client).await?;
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
    Ok(())
}

async fn check_stack_status(id: impl Into<String>, client: &Client) -> Result<StackStatus, Error> {
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

fn synth_app(actual: &str) {
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("tests/end-to-end/typescript-app-scaffolding")
        .join("stack-under-test.ts");
    println!("{:?}", path);
    let mut file = File::create(path).unwrap();
    file.write_all(actual.as_bytes()).unwrap();

    //npm install
    let result = Command::new("npm")
        .arg("install")
        .current_dir(fs::canonicalize("./tests/end-to-end/typescript-app-scaffolding").unwrap())
        .output();

    println!("{:?}", result);

    // cdk synth
    let result = Command::new("npx")
        .args(["cdk", "synth", "--path-metadata", "false", "--app", "npx ts-node --prefer-ts-exts ./app.ts" ])
        .current_dir(fs::canonicalize("./tests/end-to-end/typescript-app-scaffolding").unwrap())
        .status();

    match result {
        Ok(status) => todo!(),
        Err(e) => panic!("{e}"),
    }
}

test_case!(simple, "StackUnderTest");

test_case!(vpc, "VpcStack");

test_case!(resource_w_json_type_properties, "JsonPropsStack");

test_case!(config, "ConfigStack");

test_case!(documentdb, "DocumentDbStack");

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
