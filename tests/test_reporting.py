from pathlib import Path

from shizuku_finder.diffing import DiffResult
from shizuku_finder.models import AppRecord
from shizuku_finder.reporting import write_diff_json, write_diff_markdown, write_markdown, write_review_markdown


def test_reporting_outputs_group_confirmed_and_review(tmp_path: Path) -> None:
    apps = [
        AppRecord(canonical_id="1", name="Alpha", primary_url="https://a", source="fdroid", confidence=0.9, review_needed=False, has_downloads=True),
        AppRecord(canonical_id="2", name="Beta", primary_url="https://b", source="gitlab", confidence=0.4, review_needed=True, has_downloads=False),
    ]
    summary = tmp_path / "SUMMARY.md"
    review = tmp_path / "REVIEW_NEEDED.md"
    write_markdown(summary, apps)
    write_review_markdown(review, apps)
    summary_text = summary.read_text(encoding="utf-8")
    review_text = review.read_text(encoding="utf-8")
    assert "Confirmed / likely matches" in summary_text
    assert "Review-needed matches" in summary_text
    assert "Source breakdown" in summary_text
    assert "source `fdroid`" in summary_text
    assert "status `downloadable`" in summary_text
    assert "Alpha" in summary_text and "Beta" in summary_text
    assert "Review Needed" in review_text and "Beta" in review_text


def test_diff_outputs_write_sections_and_json(tmp_path: Path) -> None:
    diff_file = tmp_path / "DIFF.md"
    diff_json = tmp_path / "DIFF.json"
    diff = DiffResult(
        added=[AppRecord(canonical_id="1", name="Added", primary_url="https://a", source="x", confidence=0.8)],
        removed=[AppRecord(canonical_id="2", name="Removed", primary_url="https://b", source="x", confidence=0.8)],
        changed=[AppRecord(canonical_id="3", name="Changed", primary_url="https://c", source="x", confidence=0.9)],
    )
    write_diff_markdown(diff_file, diff)
    write_diff_json(diff_json, diff)
    text = diff_file.read_text(encoding="utf-8")
    payload = diff_json.read_text(encoding="utf-8")
    assert "### Added" in text
    assert "### Removed" in text
    assert "### Changed" in text
    assert '"counts"' in payload
    assert '"added": 1' in payload
