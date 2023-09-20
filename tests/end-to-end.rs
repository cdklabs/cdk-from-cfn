use cdk_from_cfn::ir::CloudformationProgramIr;
use cdk_from_cfn::synthesizer::*;
use cdk_from_cfn::CloudformationParseTree;

macro_rules! test_case {
    ($name:ident, $stack_name:literal) => {
        mod $name {
            use super::*;

            #[cfg(feature = "golang")]
            test_case!(
                $name,
                golang,
                &Golang::new(stringify!($name)),
                $stack_name,
                "app.go"
            );

            #[cfg(feature = "java")]
            test_case!(
                $name,
                java,
                &Java::new(concat!("com.acme.test.", stringify!($name))),
                $stack_name,
                "App.java"
            );

            #[cfg(feature = "python")]
            test_case!($name, python, &Python {}, $stack_name, "app.py");

            #[cfg(feature = "typescript")]
            test_case!($name, typescript, &Typescript {}, $stack_name, "app.ts");

            #[cfg(feature = "csharp")]
            test_case!($name, csharp, &CSharp::default(), $stack_name, "App.cs");
        }
    };

    ($name:ident, $lang:ident, $synthesizer:expr, $stack_name:literal, $expected:literal) => {
        #[test]
        fn $lang() {
            let expected = include_str!(concat!("end-to-end/", stringify!($name), "/", $expected));
            let actual = {
                let mut output = Vec::with_capacity(expected.len());
                let cfn: CloudformationParseTree = serde_yaml::from_str(include_str!(concat!(
                    "end-to-end/",
                    stringify!($name),
                    "/template.yml"
                )))
                .unwrap();
                let ir = CloudformationProgramIr::from(cfn).unwrap();
                ir.synthesize($synthesizer, &mut output, $stack_name)
                    .unwrap();
                String::from_utf8(output).unwrap()
            };

            let _update_snapshots = UpdateSnapshot::new(
                concat!("end-to-end/", stringify!($name), "/", $expected),
                &actual,
                &expected,
            );
            assert_eq!(expected, actual);

            // Add app creation
            // instantiate a stack for each possible combination of parameters
            // add the synth call
        }
    };
}

test_case!(simple, "SimpleStack");

test_case!(vpc, "VpcStack");

struct UpdateSnapshot<'a> {
    path: &'static str,
    actual: &'a str,
    expected: &'a str,
}

impl<'a> UpdateSnapshot<'a> {
    fn new(path: &'static str, actual: &'a str, expected: &'a str) -> Self {
        Self {
            path,
            actual,
            expected,
        }
    }
}

impl Drop for UpdateSnapshot<'_> {
    fn drop(&mut self) {
        use std::fs::File;
        use std::io::Write;
        use std::path::PathBuf;

        if std::env::var_os("UPDATE_SNAPSHOTS").is_some() && self.actual != self.expected {
            let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("tests")
                .join(self.path);
            let mut file = File::create(path).unwrap();
            file.write_all(self.actual.as_bytes()).unwrap();
        }
    }
}
