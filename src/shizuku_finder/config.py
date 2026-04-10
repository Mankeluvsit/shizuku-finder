from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(slots=True)
class AppConfig:
    github_auth: str | None
    target_list_path: Path
    summary_file: Path
    json_file: Path
    csv_file: Path
    review_file: Path
    diff_file: Path
    run_summary_file: Path
    database_path: Path

    @classmethod
    def from_env(
        cls,
        target_list_path: str | None = None,
        summary_file: str | None = None,
        json_file: str | None = None,
        csv_file: str | None = None,
        review_file: str | None = None,
        diff_file: str | None = None,
        run_summary_file: str | None = None,
        database_path: str | None = None,
    ) -> "AppConfig":
        return cls(
            github_auth=os.getenv("GITHUB_AUTH"),
            target_list_path=Path(target_list_path or os.getenv("TARGET_LIST_PATH", "./list")),
            summary_file=Path(summary_file or os.getenv("SUMMARY_FILE", "SUMMARY.md")),
            json_file=Path(json_file or os.getenv("JSON_FILE", "summary.json")),
            csv_file=Path(csv_file or os.getenv("CSV_FILE", "summary.csv")),
            review_file=Path(review_file or os.getenv("REVIEW_FILE", "REVIEW_NEEDED.md")),
            diff_file=Path(diff_file or os.getenv("DIFF_FILE", "DIFF.md")),
            run_summary_file=Path(run_summary_file or os.getenv("RUN_SUMMARY_FILE", "RUN_SUMMARY.json")),
            database_path=Path(database_path or os.getenv("DATABASE_PATH", "./cache/shizuku_finder.sqlite3")),
        )
