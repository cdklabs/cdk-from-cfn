use clap::{App, Arg};
use noctilucent::semantic::reference::ReferenceTable;
use noctilucent::semantic::to_string;
use noctilucent::CloudformationParseTree;
use serde_json::Value;
use std::fs;

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

    println!("Amount of parameters: {}", cfn_tree.parameters.params.len());
    println!(
        "Amount of conditions: {}",
        cfn_tree.conditions.conditions.len()
    );
    println!(
        "Amount of resources:  {}",
        cfn_tree.resources.resources.len()
    );

    println!("====================================");
    for (_, cond) in cfn_tree.conditions.conditions.iter() {
        println!("{}", cond.synthesize());
    }
d
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
                    println!("\t{}:{},", name, x);
                }
            }
        }
        println!("}});");
    }
    println!("====================================");
}
