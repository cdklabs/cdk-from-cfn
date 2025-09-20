// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT

use cdk_from_cfn_macros::test_name_enum;

test_name_enum!();
use std::sync::atomic::{AtomicUsize, Ordering};

/// Thread-safe counter for distributing tests across AWS regions
static REGION_COUNTER: AtomicUsize = AtomicUsize::new(0);

/// Environment configuration manager for AWS region selection and test dependencies.
/// 
/// Manages AWS region assignment for tests, ensuring environment-dependent tests
/// run in consistent regions while distributing other tests across multiple regions
/// for load balancing and isolation.
pub struct Environment;

impl Environment {
    /// Available AWS regions for test execution, ordered by preference
    const REGIONS: &'static [&'static str] = &[
        "us-east-1",
        "us-west-2",
        "eu-west-1",
        "ap-southeast-1",
        "us-east-2",
    ];

    /// Tests that require consistent environment/region for proper execution
    const ENV_DEPENDENT_TESTS: &'static [TestName] = &[TestName::Ec2Encryption, TestName::Simple];

    /// Determines if a test requires a consistent AWS environment.
    /// 
    /// Environment-dependent tests must run in the same region to ensure
    /// consistent behavior and avoid cross-region dependencies.
    /// 
    /// # Arguments
    /// * `test_name` - Name of the test to check
    /// 
    /// # Returns
    /// `true` if the test requires consistent environment, `false` otherwise
    pub fn is_env_dependent(test_name: &str) -> bool {
        let test = TestName::from_str(test_name);
        Self::ENV_DEPENDENT_TESTS.contains(&test)
    }

    /// Selects the appropriate AWS region for a test.
    /// 
    /// Environment-dependent tests always use the default region for consistency,
    /// while other tests are distributed across available regions for load balancing.
    /// 
    /// # Arguments
    /// * `test_name` - Name of the test requiring region assignment
    /// 
    /// # Returns
    /// AWS region identifier for the test
    pub fn region_for_test(test_name: &str) -> &'static str {
        if Self::is_env_dependent(test_name) {
            Self::default_region()
        } else {
            Self::next_region()
        }
    }

    /// Returns the default AWS region for environment-dependent tests.
    /// 
    /// # Returns
    /// The primary AWS region (us-east-1)
    fn default_region() -> &'static str {
        Self::REGIONS[0]
    }

    /// Returns the next AWS region in round-robin fashion for load distribution.
    /// 
    /// Uses atomic operations to ensure thread-safe region selection across
    /// concurrent test execution.
    /// 
    /// # Returns
    /// AWS region identifier selected in round-robin order
    fn next_region() -> &'static str {
        let index = REGION_COUNTER.fetch_add(1, Ordering::Relaxed) % Self::REGIONS.len();
        Self::REGIONS[index]
    }
}
