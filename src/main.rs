use clap::{Arg, ArgAction, Command};
use noctilucent::ir::CloudformationProgramIr;
use noctilucent::synthesizer::typescript_synthesizer::TypescriptSynthesizer;
use noctilucent::synthesizer::Synthesizer;
use noctilucent::CloudformationParseTree;
use serde_yaml::Value;
use std::{fs, io};

fn main() -> anyhow::Result<()> {
    let matches = Command::new("Translates cfn templates to cdk typescript")
        .version("1.0")
        .author("Sean Tyler Myers <seanmyers0608@gmail.com>")
        .about("Reads cfn templates and translates them to typescript")
        .arg(
            Arg::new("INPUT")
                .help("Sets the input file to use")
                .required(true)
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

    let txt_location: &str = matches.get_one::<&str>("INPUT").unwrap();
    let contents = fs::read_to_string(txt_location)?;

    let value: Value = serde_yaml::from_str::<Value>(contents.as_str())?;

    let cfn_tree = CloudformationParseTree::build(&value)?;
    let ir = CloudformationProgramIr::new_from_parse_tree(&cfn_tree)?;
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
