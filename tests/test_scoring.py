from shizuku_finder.models import AppRecord
from shizuku_finder.scoring import apply_review_classification


def test_apply_review_classification_marks_low_confidence_or_no_downloads() -> None:
    apps = [
        AppRecord(canonical_id="1", name="A", primary_url="https://a", source="x", confidence=0.9, has_downloads=True),
        AppRecord(canonical_id="2", name="B", primary_url="https://b", source="x", confidence=0.5, has_downloads=True),
        AppRecord(canonical_id="3", name="C", primary_url="https://c", source="x", confidence=0.8, has_downloads=False),
    ]
    classified = apply_review_classification(apps)
    assert [app.review_needed for app in classified] == [False, True, True]
