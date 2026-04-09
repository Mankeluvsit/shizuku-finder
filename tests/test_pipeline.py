from pathlib import Path

from shizuku_finder.filtering import filter_known_apps
from shizuku_finder.models import AppRecord
from shizuku_finder.pipeline import normalize_and_dedupe
from shizuku_finder.readme_index import ReadmeIndex


def test_normalize_and_dedupe_prefers_higher_priority_source_at_equal_confidence() -> None:
    apps = [
        AppRecord(canonical_id="1", name="Same App", primary_url="https://github.com/example/repo/", source="gitlab", confidence=0.8),
        AppRecord(canonical_id="2", name="Same App", primary_url="https://github.com/example/repo", source="github_code", confidence=0.8),
    ]
    result = normalize_and_dedupe(apps)
    assert len(result) == 1
    assert result[0].source == "github_code"


def test_filter_known_apps_removes_existing_target_list_entries(tmp_path: Path) -> None:
    docs = tmp_path / "list"
    docs.mkdir()
    (docs / "README.md").write_text("* [ExistingApp](https://github.com/example/existing-app)\n", encoding="utf-8")
    index = ReadmeIndex.from_directory(docs)
    apps = [
        AppRecord(canonical_id="1", name="ExistingApp", primary_url="https://github.com/example/existing-app", source="github_code", confidence=0.9),
        AppRecord(canonical_id="2", name="NewApp", primary_url="https://github.com/example/new-app", source="github_code", confidence=0.9),
    ]
    filtered = filter_known_apps(apps, index)
    assert [app.name for app in filtered] == ["NewApp"]
