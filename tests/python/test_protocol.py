"""Round-trip protocol fixtures against the shared schema."""

import json
from pathlib import Path

import pytest

from apex.protocol import event_adapter, request_adapter

FIXTURES = Path(__file__).parents[2] / "tests" / "fixtures" / "protocol"


def fixture_files(*subdirs: str) -> list[Path]:
    return [p for sub in subdirs for p in sorted((FIXTURES / sub).glob("*.json"))]


@pytest.mark.parametrize("path", fixture_files("requests"))
def test_request_fixtures_round_trip(path: Path) -> None:
    original = json.loads(path.read_text(encoding="utf-8"))
    parsed = request_adapter.validate_python(original)
    reparsed = json.loads(parsed.model_dump_json())
    assert original == reparsed


@pytest.mark.parametrize("path", fixture_files("events/stream", "events/terminal"))
def test_event_fixtures_round_trip(path: Path) -> None:
    original = json.loads(path.read_text(encoding="utf-8"))
    parsed = event_adapter.validate_python(original)
    reparsed = json.loads(parsed.model_dump_json())
    assert original == reparsed
