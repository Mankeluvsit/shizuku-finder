from pathlib import Path

from shizuku_finder.models import AppRecord
from shizuku_finder.orchestrator import ScanOrchestrator
from shizuku_finder.scanners.base import BaseScanner


class DummyScanner(BaseScanner):
    name = "dummy"

    def __init__(self, apps: list[AppRecord]) -> None:
        self.apps = apps

    def scan(self):
        return self.apps


def test_orchestrator_filters_ignored_app(tmp_path: Path) -> None:
    rules_path = tmp_path / "ignore_rules.yaml"
    rules_path.write_text(
        "rules:\n  - type: name\n    value: IgnoreMe\n    category: duplicate\n    reason: test exclusion\n",
        encoding="utf-8",
    )
    scanner = DummyScanner(
        [
            AppRecord(canonical_id="1", name="IgnoreMe", primary_url="https://example.com/1", source="dummy"),
            AppRecord(canonical_id="2", name="KeepMe", primary_url="https://example.com/2", source="dummy"),
        ]
    )
    results = ScanOrchestrator([scanner], rules_path).run()
    assert [app.name for app in results] == ["KeepMe"]
