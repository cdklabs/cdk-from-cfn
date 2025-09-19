// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use proc_macro::TokenStream;
use quote::quote;

const BATCH: &str = "batch";
const BUCKET: &str = "bucket";
const CLOUDWATCH: &str = "cloudwatch";
const CONFIG: &str = "config";
const DOCUMENT_DB: &str = "documentdb";
const EC2: &str = "ec2";
const EC2_ENCRYPTION: &str = "ec2_encryption";
const ECS: &str = "ecs";
const EFS: &str = "efs";
const GROUNDSTATION: &str = "groundstation";
const RESOURCE_W_JSON_TYPE_PROPERTIES: &str = "resource_w_json_type_properties";
const SAM_NODEJS_LAMBDA: &str = "sam_nodejs_lambda";
const SAM_NODEJS_LAMBDA_ARR_TRANSFORM: &str = "sam_nodejs_lambda_arr_transform";
const SIMPLE: &str = "simple";
const VPC: &str = "vpc";

const TEST_DEFINITIONS: &[(&str, &str)] = &[
    (BATCH, "BatchStack"),
    (BUCKET, "BucketStack"),
    (CLOUDWATCH, "CloudwatchStack"),
    (CONFIG, "ConfigStack"),
    (DOCUMENT_DB, "DocumentDbStack"),
    (EC2, "Ec2Stack"),
    (EC2_ENCRYPTION, "Ec2EncryptionStack"),
    (ECS, "EcsStack"),
    (EFS, "EfsStack"),
    (GROUNDSTATION, "GroundStationStack"),
    (RESOURCE_W_JSON_TYPE_PROPERTIES, "JsonPropsStack"),
    (SAM_NODEJS_LAMBDA, "SAMNodeJSLambdaStack"),
    (SAM_NODEJS_LAMBDA_ARR_TRANSFORM, "SAMNodeJSLambdaArrStack"),
    (SIMPLE, "SimpleStack"),
    (VPC, "VpcStack"),
];

#[proc_macro]
pub fn generate_cdk_tests(_input: TokenStream) -> TokenStream {
    let tests = TEST_DEFINITIONS.iter().map(|(test_name, stack_name)| {
        let test_ident = syn::Ident::new(test_name, proc_macro2::Span::call_site());
        quote! {
            cdk_stack_synth_test!(#test_ident, #stack_name, SkipSynthList::get(#test_name));
        }
    });

    let expanded = quote! {
        #(#tests)*
    };

    TokenStream::from(expanded)
}

#[proc_macro]
pub fn generate_ir_tests(_input: TokenStream) -> TokenStream {
    let tests = TEST_DEFINITIONS.iter().map(|(test_name, stack_name)| {
        let test_ident = syn::Ident::new(test_name, proc_macro2::Span::call_site());
        quote! {
            ir_synthesizer_test!(#test_ident, #stack_name);
        }
    });

    let expanded = quote! {
        #(#tests)*
    };

    TokenStream::from(expanded)
}

#[proc_macro]
pub fn test_name_enum(_input: TokenStream) -> TokenStream {
    quote! {
        #[derive(Debug, Clone, Copy, PartialEq, Eq)]
        pub enum TestName {
            Batch,
            Bucket,
            Cloudwatch,
            Config,
            DocumentDb,
            Ec2,
            Ec2Encryption,
            Ecs,
            Efs,
            Groundstation,
            ResourceWJsonTypeProperties,
            SamNodejsLambda,
            SamNodejsLambdaArrTransform,
            Simple,
            Vpc,
        }

        impl std::fmt::Display for TestName {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                let s = match self {
                    TestName::Batch => #BATCH,
                    TestName::Bucket => #BUCKET,
                    TestName::Cloudwatch => #CLOUDWATCH,
                    TestName::Config => #CONFIG,
                    TestName::DocumentDb => #DOCUMENT_DB,
                    TestName::Ec2 => #EC2,
                    TestName::Ec2Encryption => #EC2_ENCRYPTION,
                    TestName::Ecs => #ECS,
                    TestName::Efs => #EFS,
                    TestName::Groundstation => #GROUNDSTATION,
                    TestName::ResourceWJsonTypeProperties => #RESOURCE_W_JSON_TYPE_PROPERTIES,
                    TestName::SamNodejsLambda => #SAM_NODEJS_LAMBDA,
                    TestName::SamNodejsLambdaArrTransform => #SAM_NODEJS_LAMBDA_ARR_TRANSFORM,
                    TestName::Simple => #SIMPLE,
                    TestName::Vpc => #VPC,
                };
                write!(f, "{}", s)
            }
        }

        impl TestName {
            pub fn from_str(s: &str) -> Self {
                match s {
                    #BATCH => TestName::Batch,
                    #BUCKET => TestName::Bucket,
                    #CLOUDWATCH => TestName::Cloudwatch,
                    #CONFIG => TestName::Config,
                    #DOCUMENT_DB => TestName::DocumentDb,
                    #EC2 => TestName::Ec2,
                    #EC2_ENCRYPTION => TestName::Ec2Encryption,
                    #ECS => TestName::Ecs,
                    #EFS => TestName::Efs,
                    #GROUNDSTATION => TestName::Groundstation,
                    #RESOURCE_W_JSON_TYPE_PROPERTIES => TestName::ResourceWJsonTypeProperties,
                    #SAM_NODEJS_LAMBDA => TestName::SamNodejsLambda,
                    #SAM_NODEJS_LAMBDA_ARR_TRANSFORM => TestName::SamNodejsLambdaArrTransform,
                    #SIMPLE => TestName::Simple,
                    #VPC => TestName::Vpc,
                    _ => panic!("Unknown test name: {}", s),
                }
            }
        }
    }
    .into()
}
