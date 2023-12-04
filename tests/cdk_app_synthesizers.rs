use std::{fs::canonicalize, process::Command};

pub trait CdkAppSynthesizer {
  fn synthesize(&self, test_working_dir: &str);
}

pub struct Typescript {}

impl CdkAppSynthesizer for Typescript {
  fn synthesize(&self, test_working_dir: &str) {
    println!("Synthesizing typescript app");
    // lang-specific install or setup commands
    let test_working_dir_abs_path = canonicalize(test_working_dir).unwrap();
    Command::new("npm")
    .arg("install")
    .arg("--no-package-lock")
    .current_dir(&test_working_dir_abs_path)
    .output()
    .expect("npm install failed");
    
    // Synth the app
    Command::new("npx")
    .args([
      "cdk",
      "synth",
      "--no-version-reporting",
      "--no-path-metadata",
      "--app",
      "npx ts-node ./app.ts",
      ])
      .current_dir(&test_working_dir_abs_path)
      .output()
      .expect("typescript synth failed");
    }
  }
  
  pub struct Python {}
  
  impl CdkAppSynthesizer for Python {
    fn synthesize(&self, test_working_dir: &str) {
      println!("Synthesizing python app");
      let test_working_dir_abs_path = canonicalize(test_working_dir).unwrap();
      println!("{}", test_working_dir_abs_path.to_str().unwrap());
      // 
      // python3 -m venv .venv - NOT WORKING
      let res = Command::new("bash")
        .arg("setup.sh")
        .current_dir(&test_working_dir_abs_path)
        .output()
        .expect("command failed");

      println!("MADELINE: {:#?}", res);

      
      
      // source .venv/bin/activate - NOT WORKING
      // let res = Command::new("ls")
      //   .arg(".venv/bin/activate")
      //   .current_dir(&test_working_dir_abs_path)
      //   .output()
      //   .expect("source .venv/bin/activate failed");
      // println!("MADELINE: {:?}", res);

      // // pip install -r requirements.txt
      // Command::new("pip")
      // .arg("install")
      // .arg("-r requirements.txt")
      // .current_dir(&test_working_dir_abs_path)
      // .output()
      // .expect("pip install failed");
      // // cdk synth --no-version-reporting --no-path-metadata --app python3 app.py
      // Command::new("npx")
      // .args([
      //   "cdk",
      //   "synth",
      //   "--no-version-reporting",
      //   "--no-path-metadata",
      //   "--app",
      //   "python3 app.py",
      //   ])
      //   .current_dir(&test_working_dir_abs_path)
      //   .output()
      //   .expect("python synth failed");
      }
    }
    