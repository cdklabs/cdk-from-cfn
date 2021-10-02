use clap::{App, Arg};
use noctilucent::semantic::importer::Importer;
use noctilucent::semantic::reference::ReferenceTable;
use noctilucent::semantic::to_string;
use noctilucent::CloudformationParseTree;
use serde_json::Value;
use std::fs;
use voca_rs::case::camel_case;

fn main() {
    let matches = App::new("Transmutes cfn templates to cdk")
        .version("1.0")
        .author("Sean Tyler Myers <seanmyers0608@gmail.com>")
        .about("Reads cfn templates and translates them to typescript")
        .arg(
            Arg::new("INPUT")
                .about("Sets the input file to use")
                .required(true)
                .index(1),
        )
        .get_matches();

    let txt_location: &str = matches.value_of("INPUT").unwrap();
    let contents = fs::read_to_string(txt_location).unwrap();
    let value: Value = serde_json::from_str(contents.as_str()).unwrap();

    let cfn_tree = CloudformationParseTree::build(&value).unwrap();
    let reference_table = ReferenceTable::new(&cfn_tree);

    let import = Importer::new(&cfn_tree);

    println!("{}", import.synthesize().join("\n"));
    println!("{}", cfn_tree.mappings.synthesize());

    for (_, cond) in cfn_tree.conditions.conditions.iter() {
        println!("{}", cond.synthesize());
    }

    for reference in cfn_tree.resources.resources.iter() {
        let mut split_ref = reference.resource_type.split("::");
        split_ref.next();
        let service = split_ref.next().unwrap().to_ascii_lowercase();
        let rtype = split_ref.next().unwrap();
        println!(
            "new {}.Cfn{}(this, '{}', {{",
            service, rtype, reference.name
        );
        for (name, prop) in reference.properties.iter() {
            match to_string(prop, &reference_table) {
                None => {}
                Some(x) => {
                    println!("\t{}:{},", camel_case(name), x);
                }
            }
        }
        println!("}});");
    }
    println!("====================================");
}
