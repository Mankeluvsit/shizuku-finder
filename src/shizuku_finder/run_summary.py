from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from shizuku_finder.diffing import DiffResult
from shizuku_finder.models import AppRecord


@dataclass(slots=True)
class ScannerFailure:
    scanner: str
    error: str


def write_run_summary(path: Path, apps: list[AppRecord], diff: DiffResult, failures: list[ScannerFailure]) -> None:
    by_source = Counter(app.source for app in apps)
    summary = {
        "total_apps": len(apps),
        "confirmed": sum(1 for app in apps if not app.review_needed),
        "review_needed": sum(1 for app in apps if app.review_needed),
        "by_source": dict(sorted(by_source.items())),
        "diff": {
            "added": len(diff.added),
            "removed": len(diff.removed),
            "changed": len(diff.changed),
        },
        "failures": [asdict(failure) for failure in failures],
    }
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
