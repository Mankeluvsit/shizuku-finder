from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from shizuku_finder.ignore_rules import IgnoreRules
from shizuku_finder.models import AppRecord
from shizuku_finder.run_summary import ScannerFailure
from shizuku_finder.scanners.base import BaseScanner


@dataclass(slots=True)
class ScanRunResult:
    apps: list[AppRecord]
    failures: list[ScannerFailure]


class ScanOrchestrator:
    def __init__(self, scanners: list[BaseScanner], ignore_rules_path: Path | None = None) -> None:
        self.scanners = scanners
        self.ignore_rules = IgnoreRules.load(ignore_rules_path) if ignore_rules_path and ignore_rules_path.exists() else None

    def run(self) -> list[AppRecord]:
        return self.run_detailed().apps

    def run_detailed(self) -> ScanRunResult:
        collected: dict[str, AppRecord] = {}
        failures: list[ScannerFailure] = []
        for scanner in self.scanners:
            try:
                results = scanner.scan()
            except Exception as exc:
                failures.append(ScannerFailure(scanner=scanner.__class__.__name__, error=str(exc)))
                continue
            for app in results:
                if self.ignore_rules and self.ignore_rules.should_ignore(app):
                    continue
                collected[app.canonical_id] = app
        return ScanRunResult(apps=sorted(collected.values(), key=lambda item: item.name.lower()), failures=failures)
