use clap::{Arg, ArgAction, Command};
use noctilucent::ir::CloudformationProgramIr;
use noctilucent::synthesizer::*;
use noctilucent::CloudformationParseTree;
use std::{fs, io};

// Ensure at least one target language is enabled...
#[cfg(not(any(feature = "typescript", feature = "golang", feature = "python")))]
compile_error!("At least one language target feature must be enabled!");

fn main() -> anyhow::Result<()> {
    let targets = [
        #[cfg(feature = "typescript")]
        "typescript",
        #[cfg(feature = "golang")]
        "go",
        #[cfg(feature = "python")]
        "python",
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
        .get_matches();

    let cfn_tree: CloudformationParseTree = {
        let reader: Box<dyn std::io::Read> =
            match matches.get_one::<String>("INPUT").map(String::as_str) {
                None | Some("-") => Box::new(io::stdin()),
                Some(file) => Box::new(fs::File::open(file)?),
            };

        serde_yaml::from_reader(reader)?
    };

    let ir = CloudformationProgramIr::from(cfn_tree)?;

    let mut output: Box<dyn io::Write> = match matches
        .get_one::<String>("OUTPUT")
        .map(String::as_str)
        .unwrap_or("-")
    {
        "-" => Box::new(io::stdout()),
        output_file => Box::new(fs::File::create(output_file)?),
    };

    let synthesizer: Box<dyn Synthesizer> = match matches
        .get_one::<String>("language")
        .map(String::as_str)
        .unwrap_or(targets[0])
    {
        #[cfg(feature = "typescript")]
        "typescript" => Box::new(Typescript {}),
        #[cfg(feature = "golang")]
        "go" => Box::<Golang>::default(),
        #[cfg(feature = "python")]
        "python" => Box::new(Python {}),
        unsupported => panic!("unsupported language: {}", unsupported),
    };

    ir.synthesize(synthesizer.as_ref(), &mut output)?;

    Ok(())
}
