// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use std::env;
use std::io;

use std::fs;
use std::io::{Read, Write};
use std::path;
use std::path::Path;

use walkdir::WalkDir;
use zip::write::SimpleFileOptions;
use zip::ZipWriter;

fn main() -> io::Result<()> {
    cdk::update_schema()?;
    zip_test_snapshots()?;
    Ok(())
}

mod util {
    include!("src/util.rs");
}

#[allow(unused)]
mod cdk {
    use std::io::Write;
    use std::{env, fmt, fs, io, path};

    include!("src/cdk/schema.rs");

    pub fn update_schema() -> io::Result<()> {
        static RESOURCES: &str = include_str!("src/specification/cdk-resources.json");
        static TYPES: &str = include_str!("src/specification/cdk-types.json");

        let out_dir = path::PathBuf::from(env::var("OUT_DIR").unwrap()).join("gen");
        fs::create_dir_all(&out_dir)?;
        let out_file = out_dir.join("cdk-schema.rs");
        let mut file = fs::File::create(&out_file)?;

        println!("cargo:rerun-if-changed=src/specification/cdk-resources.json");
        println!("cargo:rerun-if-changed=src/specification/cdk-types.json");

        let resource_schema = serde_json::from_str::<Map<CfnResource>>(RESOURCES).unwrap();

        let mut resources = phf_codegen::Map::new();
        for (cfn_name, construct) in &resource_schema {
            let mut properties = phf_codegen::Map::new();
            for (name, prop) in &construct.properties {
                properties.entry(name, format!("&{prop:#?}"));
            }

            let mut attributes = phf_codegen::Map::new();
            for (name, prop) in &construct.attributes {
                attributes.entry(name, format!("&{prop:#?}"));
            }

            let name = voca_rs::case::shouty_snake_case(&cfn_name.replace("::", "_"));
            let static_props = format!("{name}__PROPERTIES");
            let static_attrs = format!("{name}__ATTRIBUTES");

            writeln!(
                file,
                "static {static_props}: phf::Map<&str, &Property> = {};",
                properties.build()
            )?;
            writeln!(
                file,
                "static {static_attrs}: phf::Map<&str, &Property> = {};",
                properties.build()
            )?;
            writeln!(
                file,
                "static {name}: CfnResource = {:#?};",
                WrappedCfnResource(construct, static_props, static_attrs)
            )?;
            writeln!(file)?;

            resources.entry(cfn_name, format!("&{name}"));
        }

        let types_schema = serde_json::from_str::<Map<DataType>>(TYPES).unwrap();

        let mut types = phf_codegen::Map::new();
        for (cfn_name, named_type) in &types_schema {
            let mut properties = phf_codegen::Map::new();
            for (name, prop) in &named_type.properties {
                properties.entry(name, format!("&{prop:#?}"));
            }
            let name =
                voca_rs::case::shouty_snake_case(&cfn_name.replace("::", "_").replace('.', "_"));
            let static_props = format!("{name}__PROPERTIES");

            writeln!(
                file,
                "static {static_props}: phf::Map<&str, &Property> = {};",
                properties.build()
            )?;
            writeln!(
                file,
                "static {name}: DataType = {:#?};",
                WrappedDataType(named_type, static_props)
            )?;
            writeln!(file)?;

            types.entry(cfn_name, format!("&{name}"));
        }

        writeln!(
            file,
            "static RESOURCES: phf::Map<&str, &CfnResource> = {};",
            resources.build()
        )?;
        writeln!(file)?;

        writeln!(
            file,
            "static TYPES: phf::Map<&str, &DataType> = {};",
            types.build()
        )?;
        writeln!(file)?;

        writeln!(file, "static SCHEMA: Schema = Schema {{")?;
        writeln!(file, "    resources: Map::PhfMap(&RESOURCES),")?;
        writeln!(file, "    types: Map::PhfMap(&TYPES),")?;
        writeln!(file, "}};")?;
        writeln!(file)?;

        writeln!(file, "impl Schema {{")?;
        writeln!(file, "    #[inline]")?;
        writeln!(file, "    pub fn builtin() -> &'static Self {{")?;
        writeln!(file, "        &SCHEMA")?;
        writeln!(file, "    }}")?;
        writeln!(file, "}}")?;

        println!(
            "cargo:rustc-env=GENERATED_CDK_SCHEMA_PATH={}",
            out_file.display()
        );

        Ok(())
    }

    struct BorrowedCow<'a>(&'a std::borrow::Cow<'a, str>);
    impl fmt::Debug for BorrowedCow<'_> {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            write!(f, "std::borrow::Cow::Borrowed({:?})", self.0)
        }
    }

    impl<V: fmt::Debug> fmt::Debug for Map<V> {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            let mut builder = phf_codegen::Map::new();
            for (k, v) in self {
                builder.entry(k, format!("&{v:#?}").replace('\n', "\n        "));
            }
            write!(f, "Map::PhfMap({})", builder.build())
        }
    }

    struct WrappedCfnResource<'a>(&'a CfnResource, String, String);
    impl fmt::Debug for WrappedCfnResource<'_> {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            f.debug_struct("CfnResource")
                .field("construct", &self.0.construct)
                .field("properties", &PhfMap(&self.1))
                .field("attributes", &PhfMap(&self.2))
                .finish()
        }
    }

    struct WrappedDataType<'a>(&'a DataType, String);
    impl fmt::Debug for WrappedDataType<'_> {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            f.debug_struct("DataType")
                .field("name", &self.0.name)
                .field("properties", &PhfMap(&self.1))
                .finish()
        }
    }

    struct PhfMap<'a>(&'a str);
    impl fmt::Debug for PhfMap<'_> {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            write!(f, "Map::PhfMap(&{})", self.0)
        }
    }

    impl fmt::Debug for Property {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            f.debug_struct("Property")
                .field("name", &BorrowedCow(&self.name))
                .field("required", &self.required)
                .field("value_type", &WrappedTypeReference(&self.value_type))
                .finish()
        }
    }

    struct WrappedTypeReference<'a>(&'a TypeReference);
    impl fmt::Debug for WrappedTypeReference<'_> {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            match self.0 {
                TypeReference::Primitive(t) => f
                    .debug_tuple("TypeReference::Primitive")
                    .field(&WrappedPrimitive(*t))
                    .finish(),
                TypeReference::List(t) => f
                    .debug_tuple("TypeReference::List")
                    .field(&WrappedItemType(t))
                    .finish(),
                TypeReference::Map(t) => f
                    .debug_tuple("TypeReference::Map")
                    .field(&WrappedItemType(t))
                    .finish(),
                TypeReference::Union(t) => f
                    .debug_tuple("TypeReference::Union")
                    .field(&WrappedTypeUnion(t))
                    .finish(),
                TypeReference::Named(t) => f
                    .debug_tuple("TypeReference::Named")
                    .field(&BorrowedCow(t))
                    .finish(),
            }
        }
    }

    struct WrappedItemType<'a>(&'a ItemType);
    impl fmt::Debug for WrappedItemType<'_> {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            write!(f, "ItemType::Static(&{:#?})", WrappedTypeReference(self.0))
        }
    }

    struct WrappedTypeUnion<'a>(&'a TypeUnion);
    impl fmt::Debug for WrappedTypeUnion<'_> {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            write!(
                f,
                "TypeUnion::Static(&{:#?})",
                self.0.iter().map(WrappedTypeReference).collect::<Vec<_>>()
            )
        }
    }

    struct Boxed<'a>(&'a dyn fmt::Debug);
    impl fmt::Debug for Boxed<'_> {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            write!(f, "Box::new({:#?})", self.0)
        }
    }

    struct Vector<'a, T: fmt::Debug>(&'a Vec<T>);
    impl<T: fmt::Debug> fmt::Debug for Vector<'_, T> {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            write!(f, "vec!{:#?}", self.0)
        }
    }

    struct WrappedPrimitive(Primitive);
    impl fmt::Debug for WrappedPrimitive {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            f.debug_tuple(match self.0 {
                Primitive::Unknown => "Primitive::Unknown",
                Primitive::Boolean => "Primitive::Boolean",
                Primitive::Number => "Primitive::Number",
                Primitive::String => "Primitive::String",
                Primitive::Timestamp => "Primitive::Timestamp",
                Primitive::Json => "Primitive::Json",
            })
            .finish()
        }
    }

    impl fmt::Debug for TypeName {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            let mut dbg = f.debug_struct("TypeName");
            #[cfg(feature = "typescript")]
            dbg.field("typescript", &self.typescript);
            #[cfg(feature = "csharp")]
            dbg.field("csharp", &self.csharp);
            #[cfg(feature = "golang")]
            dbg.field("golang", &self.golang);
            #[cfg(feature = "java")]
            dbg.field("java", &self.java);
            #[cfg(feature = "python")]
            dbg.field("python", &self.python);
            dbg.finish()
        }
    }

    #[cfg(feature = "typescript")]
    impl fmt::Debug for TypeScriptName {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            f.debug_struct("TypeScriptName")
                .field("module", &BorrowedCow(&self.module))
                .field("name", &BorrowedCow(&self.name))
                .finish()
        }
    }

    #[cfg(feature = "csharp")]
    impl fmt::Debug for DotNetName {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            f.debug_struct("DotNetName")
                .field("namespace", &BorrowedCow(&self.namespace))
                .field("name", &BorrowedCow(&self.name))
                .finish()
        }
    }

    #[cfg(feature = "golang")]
    impl fmt::Debug for GolangName {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            f.debug_struct("GolangName")
                .field("module", &BorrowedCow(&self.module))
                .field("package", &BorrowedCow(&self.package))
                .field("name", &BorrowedCow(&self.name))
                .finish()
        }
    }

    #[cfg(feature = "java")]
    impl fmt::Debug for JavaName {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            f.debug_struct("JavaName")
                .field("package", &BorrowedCow(&self.package))
                .field("name", &BorrowedCow(&self.name))
                .finish()
        }
    }

    #[cfg(feature = "python")]
    impl fmt::Debug for PythonName {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            f.debug_struct("PythonName")
                .field("module", &BorrowedCow(&self.module))
                .field("name", &BorrowedCow(&self.name))
                .finish()
        }
    }

    impl<'a, V: 'static> IntoIterator for &'a Map<V> {
        type Item = (&'a str, &'a V);
        type IntoIter = Box<dyn Iterator<Item = Self::Item> + 'a>;

        fn into_iter(self) -> Self::IntoIter {
            match self {
                Map::PhfMap(map) => Box::new(map.into_iter().map(|(k, v)| (*k, *v))),
                Map::HashMap(map) => Box::new(map.iter().map(|(k, v)| (k.as_str(), v))),
            }
        }
    }
}

fn zip_test_snapshots() -> io::Result<()> {
    // Zip the expected output files for the end-to-end tests so that they can be included in the test binary. This will not affect the size of the cdk-from-cfn binary.

    let src_dir = "./tests/end-to-end";
    let out_dir = path::PathBuf::from(env::var("OUT_DIR").unwrap()).join("test");
    fs::create_dir_all(&out_dir)?;
    let out_file = out_dir.join("end-to-end-test-snapshots.zip");
    let do_not_zip = ["app-boiler-plate-files", "working-dir"];

    let file = fs::File::create(&out_file)?;

    let walkdir = WalkDir::new(src_dir);
    let mut zip = ZipWriter::new(file);
    let options = SimpleFileOptions::default();
    let mut buffer = Vec::new();

    'dir_entries: for entry in walkdir.into_iter().map(|e| e.unwrap()) {
        let path = entry.path();
        let name = path
            .strip_prefix(Path::new(src_dir))
            .unwrap_or_else(|_| panic!("{src_dir} should be a prefix of {path:?}"))
            .to_str()
            .expect("failed to convert filename to string");

        for d in do_not_zip {
            if name.contains(d) {
                continue 'dir_entries;
            };
        }

        if path.is_file() && entry.depth() > 1 {
            zip.start_file(name, options)
                .expect("failed to start zip file");
            let mut f = fs::File::open(path).unwrap_or_else(|_| panic!("failed to open {path:?}"));
            f.read_to_end(&mut buffer)
                .unwrap_or_else(|_| panic!("failed to read {path:?}"));
            zip.write_all(&buffer)
                .unwrap_or_else(|_| panic!("failed to write {path:?} to the zip file"));
            buffer.clear();
        } else if path.is_dir() {
            zip.add_directory(name, options)
                .unwrap_or_else(|_| panic!("failed to add directory {path:?} to the zip file"));
        }
    }
    zip.finish().expect("failed to write zip file");

    println!(
        "cargo:rustc-env=END_TO_END_SNAPSHOTS={}",
        out_file.display()
    );

    Ok(())
}
