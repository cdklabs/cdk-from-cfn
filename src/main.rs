use clap::{Arg, ArgAction, Command};
use noctilucent::ir::CloudformationProgramIr;
use noctilucent::synthesizer::typescript_synthesizer::TypescriptSynthesizer;
use noctilucent::synthesizer::Synthesizer;
use noctilucent::CloudformationParseTree;
use serde_json::Value;
use std::{fs, io};

fn main() {
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
        .arg(
            Arg::new("inputFormat")
                .help("Sets the input template format")
                .short('f')
                .long("input-format")
                .required(false)
                .value_parser(["json", "yaml"])
                .default_value("json")
                .action(ArgAction::Set),
        )
        .get_matches();

    let txt_location: &str = matches.get_one::<&str>("INPUT").unwrap();
    let contents = fs::read_to_string(txt_location).unwrap();
    let input_format: &str = matches.get_one::<&str>("inputFormat").unwrap();

    let value: Value = if input_format.eq("json") {
        serde_json::from_str(contents.as_str()).unwrap()
    } else {
        serde_yaml::from_str::<Value>(contents.as_str()).unwrap()
    };

    let cfn_tree = CloudformationParseTree::build(&value).unwrap();
    let ir = CloudformationProgramIr::new_from_parse_tree(&cfn_tree).unwrap();
    let synthesizer: &dyn Synthesizer = &TypescriptSynthesizer {};

    if let Some(output_file) = matches.get_one::<&str>("OUTPUT") {
        fs::write(output_file, output).expect("Unable to write file");
    } else {
        Box::new(io::stdout())
    };

    ir.synthesize(synthesizer, &mut output)
        .expect("unable to synthesize");
}
