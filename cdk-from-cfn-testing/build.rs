// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use std::env;
use std::fs::{create_dir_all, read_dir, File};
use std::io::{self, Read, Write};
use std::path::{Path, PathBuf};
use std::process::Command;

use walkdir::WalkDir;
use zip::write::SimpleFileOptions;
use zip::ZipWriter;

fn main() {
    let out_dir = env::var("OUT_DIR").unwrap();
    let shared_dir = PathBuf::from(&out_dir).join("shared_installations");
    
    if let Err(e) = create_dir_all(&shared_dir) {
        println!("cargo:warning=Failed to create shared directory: {}", e);
        return;
    }

    #[cfg(feature = "pre-install")]
    {
        #[cfg(feature = "golang")]
        install_go(&shared_dir);
        
        #[cfg(feature = "python")]
        install_python(&shared_dir);
        
        #[cfg(feature = "java")]
        install_java(&shared_dir);
        
        #[cfg(feature = "csharp")]
        install_csharp(&shared_dir);
        
        #[cfg(feature = "typescript")]
        install_typescript(&shared_dir);
    }
    
    println!("cargo:rustc-env=SHARED_INSTALLATIONS_DIR={}", shared_dir.display());
    
    zip_test_snapshots().ok();
}

fn install_go(shared_dir: &PathBuf) {
    println!("cargo:rerun-if-changed=boilerplate/golang");
    
    let go_cache = shared_dir.join("go-mod-cache");
    let cache_empty = !go_cache.exists() || read_dir(&go_cache).map_or(true, |entries| {
        entries.filter_map(|entry| entry.ok()).count() == 0
    });
    
    if cache_empty {
        println!("cargo:warning=Downloading Go modules");
        create_dir_all(&go_cache).ok();
        Command::new("go").args(["mod", "download"]).current_dir(&go_cache).env("GOMODCACHE", &go_cache).output().ok();
    }
}

fn install_python(shared_dir: &PathBuf) {
    println!("cargo:rerun-if-changed=boilerplate/python");
    
    let python_venv = shared_dir.join(".python-venv");
    if !python_venv.exists() {
        println!("cargo:warning=Creating Python venv");
        Command::new("python3").args(["-m", "venv"]).arg(&python_venv).output().ok();
        Command::new(python_venv.join("bin/pip")).args(["install", "-q", "-r", "boilerplate/python/requirements.txt"]).output().ok();
    }
}

fn install_java(shared_dir: &PathBuf) {
    println!("cargo:rerun-if-changed=boilerplate/java");
    
    let maven_repo = shared_dir.join(".m2/repository");
    let maven_empty = !maven_repo.exists() || read_dir(&maven_repo).map_or(true, |entries| {
        entries.filter_map(|entry| entry.ok()).count() == 0
    });
    
    if maven_empty {
        println!("cargo:warning=Downloading Maven dependencies");
        create_dir_all(&maven_repo).ok();
        let output = Command::new("mvn")
            .args(["dependency:resolve"])
            .current_dir("boilerplate/java")
            .env("MAVEN_OPTS", format!("-Dmaven.repo.local={}", maven_repo.display()))
            .status()
            .ok();
        if let Some(status) = output {
            if !status.success() {
                println!("cargo:warning=Maven dependency resolution failed");
            }
        }
    }
}

fn install_csharp(shared_dir: &PathBuf) {
    println!("cargo:rerun-if-changed=boilerplate/csharp");
    
    let nuget_cache = shared_dir.join(".nuget");
    let nuget_empty = !nuget_cache.exists() || read_dir(&nuget_cache).map_or(true, |entries| {
        entries.filter_map(|entry| entry.ok()).count() == 0
    });
    
    if nuget_empty {
        println!("cargo:warning=Downloading NuGet packages");
        create_dir_all(&nuget_cache).ok();
        Command::new("dotnet").args(["restore", "--packages"]).arg(&nuget_cache).current_dir("boilerplate/csharp").output().ok();
    }
}

fn install_typescript(shared_dir: &PathBuf) {
    println!("cargo:rerun-if-changed=boilerplate/typescript");
    
    let cdk_bin = shared_dir.join("node_modules/.bin/cdk");
    if !cdk_bin.exists() {
        println!("cargo:warning=Installing npm packages");
        std::fs::copy("boilerplate/typescript/package.json", shared_dir.join("package.json")).ok();
        Command::new("npm").args(["install", "--silent"]).current_dir(shared_dir).output().ok();
    }
}

fn zip_test_snapshots() -> io::Result<()> {
    println!("cargo:rerun-if-changed=./cases");
    println!("cargo:rerun-if-changed=./expected");
    println!("cargo:rerun-if-changed=./boilerplate");

    let out_dir = PathBuf::from(env::var("OUT_DIR").unwrap()).join("test");
    create_dir_all(&out_dir)?;
    let out_file = out_dir.join("end-to-end-test-snapshots.zip");

    let file = File::create(&out_file)?;
    let mut zip = ZipWriter::new(file);
    let options = SimpleFileOptions::default();
    let mut buffer = Vec::new();

    for (dir_name, dir_path) in [("cases", Path::new("cases")), ("expected", Path::new("expected")), ("boilerplate", Path::new("boilerplate"))] {
        if dir_path.exists() {
            for entry in WalkDir::new(dir_path).into_iter().filter_map(|e| e.ok()) {
                let path = entry.path();
                let name = format!("{}/{}", dir_name, path.strip_prefix(dir_path).unwrap().to_str().unwrap());

                if path.is_file() {
                    zip.start_file(&name, options)?;
                    let mut f = File::open(path)?;
                    f.read_to_end(&mut buffer)?;
                    zip.write_all(&buffer)?;
                    buffer.clear();
                } else if path.is_dir() && path != dir_path {
                    zip.add_directory(&name, options)?;
                }
            }
        }
    }

    zip.finish()?;
    println!("cargo:rustc-env=END_TO_END_SNAPSHOTS={}", out_file.display());
    Ok(())
}

