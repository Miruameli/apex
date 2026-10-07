//! Contract tests for the public JSONL protocol parser.
//!
//! These exercise `parse_request` and `parse_event` themselves rather than
//! calling `serde_json::from_str` directly. Serde is a third-party crate: a
//! test that round-trips through it proves that serde works, not that Apex
//! accepts the right input. The TypeScript parser once let `constructor` and
//! `__proto__` through its allowlist while every fixture test still passed, and
//! these cases exist so the same drift cannot return unnoticed.

use apex_core::protocol::{AgentEvent, AgentRequest, parse_event, parse_request};
use serde::Serialize;
use serde_json::Value;
use std::path::PathBuf;

/// Parse every fixture in `dir` and assert nothing is lost in the round trip.
fn check_dir<T, F>(dir: PathBuf, parse: F)
where
    T: Serialize,
    F: Fn(&str) -> Result<T, serde_json::Error>,
{
    for entry in std::fs::read_dir(&dir).expect("fixture dir") {
        let path = entry.expect("entry").path();
        if path.extension().and_then(|e| e.to_str()) != Some("json") {
            continue;
        }
        let raw = std::fs::read_to_string(&path).expect("read fixture");
        let parsed =
            parse(&raw).unwrap_or_else(|error| panic!("{} rejected: {error}", path.display()));
        let reparsed: Value =
            serde_json::from_str(&serde_json::to_string(&parsed).expect("serialize"))
                .expect("reparse");
        let original: Value = serde_json::from_str(&raw).expect("parse original");
        assert_eq!(original, reparsed, "round-trip drift in {path:?}");
    }
}

fn fixtures() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../tests/fixtures/protocol")
}

#[test]
fn request_fixtures_round_trip() {
    check_dir::<AgentRequest, _>(fixtures().join("requests"), parse_request);
}

#[test]
fn event_fixtures_round_trip() {
    check_dir::<AgentEvent, _>(fixtures().join("events/stream"), parse_event);
    check_dir::<AgentEvent, _>(fixtures().join("events/terminal"), parse_event);
}

/// Prototype member names are not protocol types; the tag must be a real one.
#[test]
fn rejects_names_that_are_not_protocol_types() {
    for tag in ["constructor", "toString", "__proto__", "valueOf", "Bogus"] {
        let line = format!(r#"{{"type":"{tag}","message":"hi"}}"#);
        assert!(
            parse_request(&line).is_err(),
            "request accepted a non-protocol type: {tag}"
        );
    }
}

/// A required field that is absent must fail rather than default silently.
#[test]
fn rejects_request_missing_a_required_field() {
    assert!(parse_request(r#"{"type":"Chat"}"#).is_err());
}

/// A required field carrying the wrong JSON type must fail.
#[test]
fn rejects_request_with_a_wrongly_typed_field() {
    assert!(parse_request(r#"{"type":"Chat","message":123}"#).is_err());
}

/// `Done.usage` is a nested object, so it is validated one level deeper.
#[test]
fn rejects_event_with_incomplete_usage() {
    assert!(parse_event(r#"{"type":"Done","usage":{}}"#).is_err());
    assert!(
        parse_event(r#"{"type":"Done","usage":{"prompt_tokens":1,"completion_tokens":2}}"#).is_ok()
    );
}

/// Text that is not JSON must surface as an error, not a panic.
#[test]
fn rejects_malformed_json() {
    assert!(parse_request("{not json").is_err());
    assert!(parse_event("").is_err());
}
