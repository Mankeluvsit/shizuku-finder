from __future__ import annotations

from pathlib import Path

from shizuku_finder.ignore_rules import IgnoreRules
from shizuku_finder.models import AppRecord
from shizuku_finder.scanners.base import BaseScanner


class ScanOrchestrator:
    def __init__(self, scanners: list[BaseScanner], ignore_rules_path: Path | None = None) -> None:
        self.scanners = scanners
        self.ignore_rules = IgnoreRules.load(ignore_rules_path) if ignore_rules_path and ignore_rules_path.exists() else None

    def run(self) -> list[AppRecord]:
        collected: dict[str, AppRecord] = {}
        for scanner in self.scanners:
            for app in scanner.scan():
                if self.ignore_rules and self.ignore_rules.should_ignore(app):
                    continue
                collected[app.canonical_id] = app
        return sorted(collected.values(), key=lambda item: item.name.lower())
