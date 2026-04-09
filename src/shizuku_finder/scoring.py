from __future__ import annotations

from shizuku_finder.models import AppRecord


def classify_review_needed(app: AppRecord) -> AppRecord:
    review_needed = app.confidence < 0.6 or not app.has_downloads
    return AppRecord(
        canonical_id=app.canonical_id,
        name=app.name,
        primary_url=app.primary_url,
        source=app.source,
        description=app.description,
        alternate_urls=app.alternate_urls,
        has_downloads=app.has_downloads,
        last_updated=app.last_updated,
        confidence=app.confidence,
        evidence=app.evidence,
        review_needed=review_needed,
    )


def apply_review_classification(apps: list[AppRecord]) -> list[AppRecord]:
    return [classify_review_needed(app) for app in apps]
