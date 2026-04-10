from __future__ import annotations

from shizuku_finder.models import AppRecord

_SOURCE_FLOOR = {
    'fdroid': 0.82,
    'github_code': 0.75,
    'github_meta': 0.72,
    'gitlab': 0.64,
    'bitbucket': 0.63,
    'codeberg': 0.62,
}


def _clone_app(app: AppRecord, confidence: float | None = None, review_needed: bool | None = None) -> AppRecord:
    return AppRecord(
        canonical_id=app.canonical_id,
        name=app.name,
        primary_url=app.primary_url,
        source=app.source,
        description=app.description,
        alternate_urls=app.alternate_urls,
        has_downloads=app.has_downloads,
        last_updated=app.last_updated,
        confidence=app.confidence if confidence is None else confidence,
        evidence=app.evidence,
        review_needed=app.review_needed if review_needed is None else review_needed,
    )


def calibrate_confidence(app: AppRecord) -> AppRecord:
    confidence = max(app.confidence, _SOURCE_FLOOR.get(app.source, app.confidence))
    if app.has_downloads:
        confidence += 0.08
    else:
        confidence -= 0.06
    if app.description:
        confidence += 0.02
    confidence += min(len(app.evidence) * 0.02, 0.08)
    confidence = max(0.0, min(1.0, round(confidence, 2)))
    return _clone_app(app, confidence=confidence)


def classify_review_needed(app: AppRecord) -> AppRecord:
    review_needed = app.confidence < 0.65 or (not app.has_downloads and app.confidence < 0.85)
    return _clone_app(app, review_needed=review_needed)


def apply_scoring(apps: list[AppRecord]) -> list[AppRecord]:
    return [classify_review_needed(calibrate_confidence(app)) for app in apps]


def apply_review_classification(apps: list[AppRecord]) -> list[AppRecord]:
    return apply_scoring(apps)
