from __future__ import annotations

import argparse
import hashlib

from .config import AppConfig
from .models import AppRecord, Evidence
from .reporting import write_csv, write_json, write_markdown, write_review_markdown
from .storage import SQLiteCache


def _seed_records() -> list[AppRecord]:
    examples = [
        ("AppDualZuku", "https://github.com/nathanatgit/AppDualZuku", "GitHub", "Manage app multiple instances in workspaces with Shizuku privilege.", 0.91, False),
        ("DarkSwitch", "https://github.com/mahmutaunal/DarkSwitch", "GitHub", "System-level dark mode attempts for Android apps without native dark theme.", 0.84, False),
        ("Potential Match", "https://example.com/potential-match", "Seed", "Needs additional validation before publication.", 0.35, True),
    ]
    records: list[AppRecord] = []
    for name, url, source, desc, confidence, review_needed in examples:
        canonical_id = hashlib.sha1(f"{source}:{url}".encode("utf-8")).hexdigest()
        evidence = (Evidence(source=source, kind="seed", detail="Initial refactor placeholder dataset", confidence_delta=confidence),)
        records.append(
            AppRecord(
                canonical_id=canonical_id,
                name=name,
                primary_url=url,
                source=source,
                description=desc,
                has_downloads=True,
                confidence=confidence,
                evidence=evidence,
                review_needed=review_needed,
            )
        )
    return records


def run_scan(config: AppConfig) -> None:
    apps = _seed_records()
    config.summary_file.parent.mkdir(parents=True, exist_ok=True)
    config.json_file.parent.mkdir(parents=True, exist_ok=True)
    config.csv_file.parent.mkdir(parents=True, exist_ok=True)
    config.review_file.parent.mkdir(parents=True, exist_ok=True)
    write_markdown(config.summary_file, apps)
    write_json(config.json_file, apps)
    write_csv(config.csv_file, apps)
    write_review_markdown(config.review_file, apps)
    SQLiteCache(config.database_path).replace_all(apps)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shizuku-finder")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Run the crawler pipeline")
    scan.add_argument("--target-list-path", default=None)
    scan.add_argument("--summary-file", default=None)
    scan.add_argument("--json-file", default=None)
    scan.add_argument("--csv-file", default=None)
    scan.add_argument("--review-file", default=None)
    scan.add_argument("--database-path", default=None)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "scan":
        config = AppConfig.from_env(
            target_list_path=args.target_list_path,
            summary_file=args.summary_file,
            json_file=args.json_file,
            csv_file=args.csv_file,
            review_file=args.review_file,
            database_path=args.database_path,
        )
        run_scan(config)


if __name__ == "__main__":
    main()
