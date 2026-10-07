"""E2E: protocol contract validated across Rust, Python, and TypeScript.

Each fixture must parse in all three languages, and each edge case must be
rejected by all three. A drift in any single language is a blocking
failure — this is the core value of the E2E layer over per-language unit tests.
"""

from __future__ import annotations

import json

import pytest
from conftest import run_rust_test, run_ts_test

from apex.protocol import event_adapter, request_adapter


def test_request_fixtures_round_trip(request_fixture) -> None:
    """Every request fixture must round-trip through pydantic."""
    original = json.loads(request_fixture.read_text(encoding="utf-8"))
    parsed = request_adapter.validate_python(original)
    reparsed = json.loads(parsed.model_dump_json())
    assert original == reparsed, f"round-trip drift in {request_fixture.name}"


def test_event_fixtures_round_trip(event_fixture) -> None:
    """Every event fixture must round-trip through pydantic."""
    original = json.loads(event_fixture.read_text(encoding="utf-8"))
    parsed = event_adapter.validate_python(original)
    reparsed = json.loads(parsed.model_dump_json())
    assert original == reparsed, f"round-trip drift in {event_fixture.name}"


def test_rust_contract_tests_pass() -> None:
    """Rust must accept every fixture that Python accepts."""
    result = run_rust_test()
    assert result.returncode == 0, f"Rust tests failed:\n{result.stdout}"
    assert "test result: ok" in result.stdout


def test_ts_contract_tests_pass() -> None:
    """TypeScript must accept every fixture that Python accepts."""
    result = run_ts_test()
    assert result.returncode == 0, f"TS tests failed:\n{result.stdout}"


@pytest.mark.parametrize("tag", ["constructor", "toString", "__proto__", "valueOf", "Bogus"])
def test_rejects_non_protocol_types(tag: str) -> None:
    """Prototype keys and bogus types must be rejected by Python."""
    line = json.dumps({"type": tag, "message": "hi"})
    with pytest.raises(ValueError):
        request_adapter.validate_python(json.loads(line))


def test_rejects_missing_required_field() -> None:
    """A request without its required field must fail validation."""
    with pytest.raises(ValueError):
        request_adapter.validate_python(json.loads('{"type":"Chat"}'))


def test_rejects_wrong_type_field() -> None:
    """A field with the wrong JSON type must fail validation."""
    with pytest.raises(ValueError):
        request_adapter.validate_python(json.loads('{"type":"Chat","message":123}'))


def test_rejects_incomplete_nested_usage() -> None:
    """A Done event with empty usage must fail validation."""
    with pytest.raises(ValueError):
        event_adapter.validate_python(json.loads('{"type":"Done","usage":{}}'))
