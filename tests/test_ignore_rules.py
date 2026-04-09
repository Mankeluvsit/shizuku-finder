from pathlib import Path

from shizuku_finder.ignore_rules import IgnoreRules
from shizuku_finder.models import AppRecord


def test_ignore_rules_match_by_name(tmp_path: Path) -> None:
    rules_path = tmp_path / "ignore_rules.yaml"
    rules_path.write_text(
        "rules:\n  - type: name\n    value: Aurora\n    category: duplicate\n    reason: duplicate fork\n",
        encoding="utf-8",
    )
    rules = IgnoreRules.load(rules_path)
    app = AppRecord(canonical_id="1", name="Aurora", primary_url="https://example.com", source="test")
    assert rules.should_ignore(app) is True
