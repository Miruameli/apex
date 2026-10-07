//! PyO3 bridge exposing apex-core to Python.
//!
//! Every function here is a thin facade: real logic lives in `apex-core`.
//! The bridge exists so Python can call Rust without reimplementing it.

use pyo3::prelude::*;

/// Return the `apex-core` greeting, proving Python reached Rust code.
#[pyfunction]
fn core_hello() -> String {
    apex_core::hello()
}

/// Return the `apex-core` crate version as reported by `apex-core` itself.
#[pyfunction]
fn core_version() -> &'static str {
    apex_core::VERSION
}

/// Python module `apex_py`.
#[pymodule]
fn apex_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(core_hello, m)?)?;
    m.add_function(wrap_pyfunction!(core_version, m)?)?;
    Ok(())
}
