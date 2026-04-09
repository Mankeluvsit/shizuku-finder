from pathlib import Path

from shizuku_finder.diffing import compute_diff
from shizuku_finder.models import AppRecord


def test_compute_diff_detects_added_removed_and_changed() -> None:
    previous = [
        AppRecord(canonical_id="1", name="Old", primary_url="https://a", source="x", confidence=0.4),
        AppRecord(canonical_id="2", name="Stable", primary_url="https://b", source="x", confidence=0.4),
    ]
    current = [
        AppRecord(canonical_id="2", name="Stable", primary_url="https://b", source="x", confidence=0.9),
        AppRecord(canonical_id="3", name="New", primary_url="https://c", source="x", confidence=0.8),
    ]
    diff = compute_diff(previous, current)
    assert [app.canonical_id for app in diff.added] == ["3"]
    assert [app.canonical_id for app in diff.removed] == ["1"]
    assert [app.canonical_id for app in diff.changed] == ["2"]
