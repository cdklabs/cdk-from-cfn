use clap::{Arg, ArgAction, Command};
use noctilucent::ir::CloudformationProgramIr;
use noctilucent::synthesizer::*;
use noctilucent::CloudformationParseTree;
use std::{fs, io};

#[cfg(not(any(feature = "typescript", feature = "golang")))]
compile_error!("At least one language target feature must be enabled!");

fn main() -> anyhow::Result<()> {
    let matches = Command::new("Translates cfn templates to cdk typescript")
        .version("1.0")
        .author("Sean Tyler Myers <seanmyers0608@gmail.com>")
        .about("Reads cfn templates and translates them to typescript")
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
        );
    #[cfg(feature = "typescript")]
    let matches = matches.arg(
        Arg::new("language")
            .long("language")
            .short('l')
            .help("Sets the output language to use (defaults to typescript)")
            .required(false)
            .value_parser(["typescript"])
            .action(ArgAction::Set),
    );
    #[cfg(feature = "golang")]
    let matches = matches.arg(
        Arg::new("experimental-language")
            .long("experimental-language")
            .help("Sets the output language to use with an experimental target")
            .required(false)
            .value_parser(Vec::<&str>::from([
                #[cfg(feature = "golang")]
                "go",
            ]))
            .conflicts_with("language")
            .action(ArgAction::Set),
    );
    let matches = matches.get_matches();

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
        .or_else(|| matches.get_one("experimental-language"))
        .map(String::as_str)
        .unwrap_or("typescript")
    {
        #[cfg(feature = "typescript")]
        "typescript" => Box::new(Typescript {}),
        #[cfg(feature = "golang")]
        "go" => Box::<Golang>::default(),
        unsupported => panic!("unsupported language: {}", unsupported),
    };

    ir.synthesize(synthesizer.as_ref(), &mut output)?;

    Ok(())
}
