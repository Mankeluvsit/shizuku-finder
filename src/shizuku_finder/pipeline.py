from __future__ import annotations

from shizuku_finder.models import AppRecord
from shizuku_finder.normalization import normalize_name, normalize_url

_SOURCE_PRIORITY = {
    "fdroid": 6,
    "github_code": 5,
    "github_meta": 4,
    "gitlab": 3,
    "bitbucket": 2,
    "codeberg": 1,
}


def normalize_and_dedupe(apps: list[AppRecord]) -> list[AppRecord]:
    normalized: list[AppRecord] = []
    for app in apps:
        primary = normalize_url(app.primary_url)
        alternates = tuple(dict.fromkeys(normalize_url(url) for url in app.alternate_urls))
        normalized.append(
            AppRecord(
                canonical_id=app.canonical_id,
                name=app.name,
                primary_url=primary,
                source=app.source,
                description=app.description,
                alternate_urls=alternates,
                has_downloads=app.has_downloads,
                last_updated=app.last_updated,
                confidence=app.confidence,
                evidence=app.evidence,
                review_needed=app.review_needed,
            )
        )

    deduped: dict[tuple[str, str], AppRecord] = {}
    for app in normalized:
        key = (normalize_name(app.name), app.primary_url)
        current = deduped.get(key)
        if current is None:
            deduped[key] = app
            continue
        current_priority = _SOURCE_PRIORITY.get(current.source, 0)
        app_priority = _SOURCE_PRIORITY.get(app.source, 0)
        if app.confidence > current.confidence or (app.confidence == current.confidence and app_priority > current_priority):
            deduped[key] = app
    return sorted(deduped.values(), key=lambda item: item.name.lower())
