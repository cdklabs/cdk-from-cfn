// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use cdk_from_cfn::cdk::Schema;
use cdk_from_cfn::ir::CloudformationProgramIr;
use cdk_from_cfn::CloudformationParseTree;
use cdk_from_cfn::Error;
use cdk_from_cfn::synthesizer::StackType;
use clap::{Arg, ArgAction, Command};
use std::borrow::Cow;
use std::{fs, io};

// Ensure at least one target language is enabled...
#[cfg(not(any(
    feature = "typescript",
    feature = "golang",
    feature = "java",
    feature = "python",
    feature = "csharp",
)))]
compile_error!("At least one language target feature must be enabled!");

fn main() -> Result<(), Error> {
    let targets = [
        #[cfg(feature = "typescript")]
        "typescript",
        #[cfg(feature = "golang")]
        "go",
        #[cfg(feature = "python")]
        "python",
        #[cfg(feature = "java")]
        "java",
        #[cfg(feature = "csharp")]
        "csharp",
    ];

    let matches = Command::new(env!("CARGO_BIN_NAME"))
        .about(clap::crate_description!())
        .version(clap::crate_version!())
        .arg(
            Arg::new("INPUT")
                .help("Sets the input file to use (use - to read from STDIN)")
                .default_value("-")
                .index(1)
                .action(ArgAction::Set),
        )
        .arg(
            Arg::new("OUTPUT")
                .help("Sets the output file to use (use - to write to STDOUT)")
                .default_value("-")
                .required(false)
                .index(2)
                .action(ArgAction::Set),
        )
        .arg(
            Arg::new("language")
                .long("language")
                .short('l')
                .help("Sets the output language to use")
                .required(false)
                .default_value(targets[0])
                .value_parser(targets)
                .action(ArgAction::Set),
        )
        .arg(
            Arg::new("stack-name")
                .help("Sets the name of the stack")
                .required(false)
                .long("stack-name")
                .short('s')
                .action(ArgAction::Set),
        )
        .arg(
            Arg::new("stack-type")
                .help("Sets the output class type: 'stack' or 'construct'")
                .long("stack-type")
                .short('t')
                .default_value("stack")
                .value_parser(["stack", "construct"])
                .action(ArgAction::Set),
        )
        .get_matches();

    let cfn_tree: CloudformationParseTree = {
        let reader: Box<dyn std::io::Read> =
            match matches.get_one::<String>("INPUT").map(String::as_str) {
                None | Some("-") => Box::new(io::stdin()),
                Some(file) => Box::new(fs::File::open(file)?),
            };

        serde_yaml::from_reader(reader)?
    };

    let schema = Cow::Borrowed(Schema::builtin());

    let ir = CloudformationProgramIr::from(cfn_tree, &schema)?;

    let mut output: Box<dyn io::Write> = match matches
        .get_one::<String>("OUTPUT")
        .map(String::as_str)
        .unwrap_or("-")
    {
        "-" => Box::new(io::stdout()),
        output_file => Box::new(fs::File::create(output_file)?),
    };

    let language = matches
        .get_one::<String>("language")
        .map(String::as_str)
        .unwrap_or(targets[0]);

    let stack_name = matches
        .get_one::<String>("stack-name")
        .map(String::as_str)
        .unwrap_or("NoctStack");

    let stack_type: StackType = matches
        .get_one::<String>("stack-type")
        .map(|s| s.parse().unwrap())
        .unwrap_or_default();

    ir.synthesize(language, &mut output, stack_name, stack_type)?;

    Ok(())
}
