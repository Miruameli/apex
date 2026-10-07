//! Unit tests for the `apex-core` crate root.
//!
/// The greeting must stay stable: the bridge contract and docs depend on it.
#[test]
fn hello_returns_the_documented_greeting() {
    assert_eq!(apex_core::hello(), "hello from apex-core");
}

/// The version must match the crate manifest so Python and Rust agree.
#[test]
fn version_matches_the_manifest() {
    assert_eq!(apex_core::VERSION, env!("CARGO_PKG_VERSION"));
}
