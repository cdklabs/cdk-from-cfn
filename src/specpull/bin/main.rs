// The purpose of this binary is to pull the cloudformation specification system.

use serde_json::Value;
use std::io::Write;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = reqwest::Client::builder().gzip(true).build().unwrap();
    let resp = client.get("https://d1uauaxba7bl26.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json").send()
        .await?;
    let txt = resp.text().await.unwrap();
    let mut file = std::fs::File::create("src/specification/spec.json")?;
    file.write_all(txt.as_bytes())?;

    if let Ok(x) = serde_json::from_str::<Value>(&txt) {
        println!("{:#?}", x);
    }
    Ok(())
}
