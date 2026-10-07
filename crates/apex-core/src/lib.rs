//! apex-core: pure core logic for Apex.
//!
//! Holds domain types and operations shared by the CLI, the PyO3 bridge, and
//! the TUI. It must stay free of LLM calls and terminal I/O.

pub mod protocol;

/// Version of the `apex-core` crate, reported to Python through the bridge.
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Greeting used to prove the bridge actually reaches Rust code.
///
/// # Examples
///
/// ```
/// assert_eq!(apex_core::hello(), "hello from apex-core");
/// ```
#[must_use]
pub fn hello() -> String {
    "hello from apex-core".to_owned()
}
