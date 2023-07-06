use std::io;
use std::process::Command;

fn main() -> io::Result<()> {
    #[cfg(feature = "cdk-schema-default")]
    cdk::bake_in()?;

    // Install some TypeScript stuff in the right places for IDE comfort. Silently ignore if failing...
    match Command::new("npm")
        .args(["install", "--no-save", "aws-cdk-lib", "@types/node"])
        .current_dir("tests/end-to-end")
        .status()
    {
        Ok(npm_exit) => {
            if !npm_exit.success() {
                eprintln!("npm install failed with {npm_exit:?}");
            }
        }
        Err(cause) => {
            eprintln!("npm install failed with {cause:?}");
        }
    }

    Ok(())
}

mod util {
    include!("src/util.rs");
}

#[cfg(feature = "cdk-schema-default")]
#[allow(unused)]
mod cdk {
    use std::io::Write;
    use std::{env, fmt, fs, io, path};

    include!("src/cdk/schema.rs");

    pub fn bake_in() -> io::Result<()> {
        println!("cargo:rerun-if-changed=tests/end-to-end/cdk-schema.json");

        // TODO: Replace with reference to the GitHub artifact
        const SCHEMA_JSON: &str = include_str!("tests/end-to-end/cdk-schema.json");
        let schema = serde_json::from_str::<Schema>(SCHEMA_JSON).unwrap();

        let out_dir = path::PathBuf::from(env::var("OUT_DIR").unwrap()).join("gen");
        fs::create_dir_all(&out_dir)?;
        let out_file = out_dir.join("cdk-schema.rs");
        let mut file = fs::File::create(&out_file)?;

        let mut resources = phf_codegen::Map::new();
        // We are generating code in separate small expressions for two reasons:
        // 1. The rust compiler would require EXTRAORDINARY amounts of memory to
        //    process a single, gigantic expression (upstream of 180GiB);
        // 2. The phf::Map values include inline slice expressions which are
        //    deemed "temporary expressions" unless they immediately resolve
        //    within a `static` context (this is where they're designed to
        //    exist anyway).
        for (cfn_name, construct) in &schema.resources {
            let mut properties = phf_codegen::Map::new();
            for (name, prop) in &construct.properties {
                properties.entry(name, &format!("&{prop:#?}"));
            }

            let mut attributes = phf_codegen::Map::new();
            for (name, prop) in &construct.attributes {
                attributes.entry(name, &format!("&{prop:#?}"));
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

            resources.entry(cfn_name, &format!("&{name}"));
        }

        let mut types = phf_codegen::Map::new();
        for (cfn_name, named_type) in &schema.types {
            let mut properties = phf_codegen::Map::new();
            for (name, prop) in &named_type.properties {
                properties.entry(name, &format!("&{prop:#?}"));
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

            types.entry(cfn_name, &format!("&{name}"));
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
        writeln!(file, "    version: {:#?},", BorrowedCow(&schema.version))?;
        writeln!(file, "}};")?;
        writeln!(file)?;

        writeln!(file, "impl Schema {{")?;
        writeln!(
            file,
            "    /// The baked-in version of the CDK resources schema"
        )?;
        writeln!(file, "    #[inline]")?;
        writeln!(file, "    pub fn default() -> &'static Self {{")?;
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
                builder.entry(k, &format!("&{v:#?}").replace('\n', "\n        "));
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
                .field("nullable", &self.nullable)
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
            #[cfg(feature = "dotnet")]
            dbg.field("dotnet", &self.dotnet);
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

    #[cfg(feature = "dotnet")]
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
