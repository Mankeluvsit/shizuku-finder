from pathlib import Path

from shizuku_finder.cli import run_scan
from shizuku_finder.config import AppConfig


def test_run_scan_writes_outputs(tmp_path: Path) -> None:
    config = AppConfig(
        github_auth=None,
        target_list_path=tmp_path / "list",
        summary_file=tmp_path / "SUMMARY.md",
        json_file=tmp_path / "summary.json",
        csv_file=tmp_path / "summary.csv",
        review_file=tmp_path / "REVIEW_NEEDED.md",
        database_path=tmp_path / "cache" / "db.sqlite3",
    )

    run_scan(config)

    assert config.summary_file.exists()
    assert config.json_file.exists()
    assert config.csv_file.exists()
    assert config.review_file.exists()
    assert config.database_path.exists()
