use clap::{Arg, ArgAction, Command};
use noctilucent::ir::CloudformationProgramIr;
use noctilucent::synthesizer::typescript_synthesizer::TypescriptSynthesizer;
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
                .help("Sets the output file to use")
                .required(false)
                .index(2)
                .action(ArgAction::Set),
        )
        .get_matches();

    let cfn_tree: CloudformationParseTree = {
        let reader: Box<dyn std::io::Read> =
            match matches.get_one::<String>("INPUT").map(|s| s.as_str()) {
                None | Some("-") => Box::new(io::stdin()),
                Some(file) => Box::new(fs::File::open(file)?),
            };

        serde_yaml::from_reader(reader)?
    };

    let ir = CloudformationProgramIr::from(cfn_tree)?;
    let synthesizer: &dyn Synthesizer = &TypescriptSynthesizer {};

    let mut output: Box<dyn io::Write> =
        if let Some(output_file) = matches.get_one::<&str>("OUTPUT") {
            Box::new(fs::File::create(output_file)?)
        } else {
            Box::new(io::stdout())
        };

    ir.synthesize(synthesizer, &mut output)?;

    Ok(())
}
