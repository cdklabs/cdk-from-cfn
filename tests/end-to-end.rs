use aws_sdk_cloudformation::types::OnFailure;
use serde_with::DurationSeconds;
use tokio::task;

use aws_sdk_cloudformation::config::Region;
use aws_sdk_cloudformation::types::StackStatus;
use aws_sdk_cloudformation::types::error::StackNotFoundException;
use cdk_from_cfn::ir::CloudformationProgramIr;
use cdk_from_cfn::synthesizer::*;
use cdk_from_cfn::CloudformationParseTree;
use aws_config::meta::region::RegionProviderChain;
use aws_sdk_cloudformation::{Client, Error};


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

            let template = include_str!(concat!("end-to-end/", stringify!($name), "/template.yml"));
            let _res = deployTemplate(stringify!($name), template);
            println!("{:?}", _res);

            let expected = include_str!(concat!("end-to-end/", stringify!($name), "/", $expected));
            let actual = {
                let mut output = Vec::with_capacity(expected.len());
                let cfn: CloudformationParseTree = serde_yaml::from_str(include_str!(concat!(
                    "end-to-end/",
                    stringify!($name),
                    "/template.yml"
                )))
                .unwrap();
                let ir = CloudformationProgramIr::from(cfn).unwrap();
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

            // Add app creation
            // instantiate a stack for each possible combination of parameters
            // add the synth call
        }
    };
}

#[tokio::main]
async fn deployTemplate(stack_name: &str, template: &str) -> Result<(), Error> {
    println!("deploy template");
    let region_provider = RegionProviderChain::default_provider().or_else("us-east-1");
    let config = aws_config::from_env().region(region_provider).load().await;
    let client = Client::new(&config);

    let resp = client.create_stack()
        .stack_name(stack_name)
        .template_body(template)
        .on_failure(OnFailure::Delete)
        .send().await?;



    println!("Stacks:");

    let id = resp.stack_id.unwrap_or_default();
    println!();
    println!("stack id {}", id);

    let mut status = check_stack_status(&id, &client).await?;

    while let StackStatus::CreateInProgress = status {
        println!("create in progress");
        tokio::time::sleep(std::time::Duration::new(2, 0)).await;
        status = check_stack_status(&id, &client).await?;
    }

    Ok(())
}

async fn check_stack_status(id: &String, client: &Client) -> Result<StackStatus, Error> {
    let resp = client.describe_stacks().stack_name(id).send().await?;
    if let Some(stacks) = resp.stacks {
        if let Some(stack) = stacks.first() {
            if let Some(status) = &stack.stack_status {
                return Ok(status.clone())
            }
        }
    }
    Err(Error::StackNotFoundException(StackNotFoundException::builder().message("ugh").build()))
}

test_case!(simple, "SimpleStack");

test_case!(vpc, "VpcStack");

test_case!(resource_w_json_type_properties, "JsonPropsStack");

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
