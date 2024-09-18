// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0 OR MIT
use super::*;

#[test]
fn test_from_u64() {
    let value: u64 = 42;
    let wrapper: WrapperF64 = value.into();
    let expected: WrapperF64 = WrapperF64::new(42.0);

    assert_eq!(wrapper, expected);
}

#[test]
fn test_from_i128() {
    let value: i128 = -10;
    let wrapper: WrapperF64 = value.into();
    let expected: WrapperF64 = WrapperF64::new(-10.0);

    assert_eq!(wrapper, expected);
}

#[test]
fn test_from_u128() {
    let value: u128 = 1000;
    let wrapper: WrapperF64 = value.into();
    let expected: WrapperF64 = WrapperF64::new(1000.0);

    assert_eq!(wrapper, expected);
}
