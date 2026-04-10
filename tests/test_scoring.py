from shizuku_finder.models import AppRecord
from shizuku_finder.scoring import apply_scoring, calibrate_confidence


def test_apply_scoring_marks_low_confidence_or_no_downloads() -> None:
    apps = [
        AppRecord(canonical_id="1", name="A", primary_url="https://a", source="fdroid", confidence=0.9, has_downloads=True),
        AppRecord(canonical_id="2", name="B", primary_url="https://b", source="gitlab", confidence=0.5, has_downloads=True),
        AppRecord(canonical_id="3", name="C", primary_url="https://c", source="gitlab", confidence=0.8, has_downloads=False),
    ]
    classified = apply_scoring(apps)
    assert [app.review_needed for app in classified] == [False, True, True]


def test_calibrate_confidence_applies_source_floor_and_bonuses() -> None:
    app = AppRecord(canonical_id="1", name="A", primary_url="https://a", source="github_code", confidence=0.3, has_downloads=True, description="desc")
    calibrated = calibrate_confidence(app)
    assert calibrated.confidence >= 0.85
