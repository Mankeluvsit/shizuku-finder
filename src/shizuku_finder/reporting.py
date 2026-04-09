from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from .diffing import DiffResult
from .models import AppRecord


def _sort(apps: Iterable[AppRecord]) -> list[AppRecord]:
    return sorted(apps, key=lambda app: (app.review_needed, -app.confidence, app.name.lower()))


def _format_entry(app: AppRecord) -> str:
    suffix = f" - {app.description}" if app.description else ""
    return f"* [{app.name}]({app.primary_url}) — confidence `{app.confidence:.2f}`{suffix}"


def write_markdown(path: Path, apps: Iterable[AppRecord]) -> None:
    sorted_apps = _sort(apps)
    confirmed = [app for app in sorted_apps if not app.review_needed]
    review = [app for app in sorted_apps if app.review_needed]
    lines = [
        "## Shizuku Finder Report",
        "",
        "> [!IMPORTANT]",
        "> This file is generated. Do not edit manually.",
        "",
        f"Generated entries: **{len(sorted_apps)}**",
        "",
        "### Confirmed / likely matches",
        "",
    ]
    for app in confirmed:
        lines.append(_format_entry(app))
    lines.extend(["", "### Review-needed matches", ""])
    for app in review:
        lines.append(_format_entry(app))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_review_markdown(path: Path, apps: Iterable[AppRecord]) -> None:
    review = [app for app in _sort(apps) if app.review_needed]
    lines = ["## Review Needed", ""]
    for app in review:
        lines.append(_format_entry(app))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_diff_markdown(path: Path, diff: DiffResult) -> None:
    lines = [
        "## Run Diff",
        "",
        f"Added: **{len(diff.added)}**",
        f"Removed: **{len(diff.removed)}**",
        f"Changed: **{len(diff.changed)}**",
        "",
        "### Added",
        "",
    ]
    lines.extend(_format_entry(app) for app in diff.added)
    lines.extend(["", "### Removed", ""])
    lines.extend(_format_entry(app) for app in diff.removed)
    lines.extend(["", "### Changed", ""])
    lines.extend(_format_entry(app) for app in diff.changed)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_json(path: Path, apps: Iterable[AppRecord]) -> None:
    data = [
        {
            "canonical_id": app.canonical_id,
            "name": app.name,
            "source": app.source,
            "primary_url": app.primary_url,
            "description": app.description,
            "has_downloads": app.has_downloads,
            "confidence": app.confidence,
            "review_needed": app.review_needed,
            "evidence": [
                {
                    "source": evidence.source,
                    "kind": evidence.kind,
                    "detail": evidence.detail,
                    "confidence_delta": evidence.confidence_delta,
                }
                for evidence in app.evidence
            ],
        }
        for app in _sort(apps)
    ]
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(path: Path, apps: Iterable[AppRecord]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["canonical_id", "name", "source", "primary_url", "has_downloads", "confidence", "review_needed"],
        )
        writer.writeheader()
        for app in _sort(apps):
            writer.writerow(
                {
                    "canonical_id": app.canonical_id,
                    "name": app.name,
                    "source": app.source,
                    "primary_url": app.primary_url,
                    "has_downloads": app.has_downloads,
                    "confidence": app.confidence,
                    "review_needed": app.review_needed,
                }
            )
