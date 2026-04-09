from __future__ import annotations

from dataclasses import dataclass

from shizuku_finder.models import AppRecord


@dataclass(slots=True)
class DiffResult:
    added: list[AppRecord]
    removed: list[AppRecord]
    changed: list[AppRecord]


def compute_diff(previous: list[AppRecord], current: list[AppRecord]) -> DiffResult:
    previous_map = {app.canonical_id: app for app in previous}
    current_map = {app.canonical_id: app for app in current}

    added = [app for key, app in current_map.items() if key not in previous_map]
    removed = [app for key, app in previous_map.items() if key not in current_map]
    changed = []
    for key, app in current_map.items():
        old = previous_map.get(key)
        if old is None:
            continue
        if old.confidence != app.confidence or old.review_needed != app.review_needed or old.primary_url != app.primary_url:
            changed.append(app)
    return DiffResult(
        added=sorted(added, key=lambda app: app.name.lower()),
        removed=sorted(removed, key=lambda app: app.name.lower()),
        changed=sorted(changed, key=lambda app: app.name.lower()),
    )
