use clap::{Arg, ArgAction, Command};
use noctilucent::ir::CloudformationProgramIr;
use noctilucent::synthesizer::golang::Golang;
use noctilucent::synthesizer::typescript::Typescript;
use noctilucent::synthesizer::Synthesizer;
use noctilucent::CloudformationParseTree;
use std::{fs, io};

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
        )
        .arg(
            Arg::new("language")
                .long("language")
                .short('l')
                .help("Sets the output language to use")
                .default_value("typescript")
                .value_parser(["typescript", "go"])
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
        .unwrap_or("typescript")
    {
        "typescript" => Box::new(Typescript {}),
        "go" => Box::<Golang>::default(),
        unsupported => panic!("unsupported language: {}", unsupported),
    };

    ir.synthesize(synthesizer.as_ref(), &mut output)?;

    Ok(())
}
