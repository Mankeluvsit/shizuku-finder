from __future__ import annotations

import argparse
from pathlib import Path

from .config import AppConfig
from .filtering import filter_known_apps
from .orchestrator import ScanOrchestrator
from .readme_index import ReadmeIndex
from .reporting import write_csv, write_json, write_markdown, write_review_markdown
from .scanners import FDroidScanner, GitHubCodeScanner
from .storage import SQLiteCache


def _default_ignore_rules_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "ignore_rules.yaml"


def run_scan(config: AppConfig) -> None:
    scanners = [
        FDroidScanner("https://f-droid.org/repo/index.xml"),
        FDroidScanner("https://apt.izzysoft.de/fdroid/repo/index.xml"),
        GitHubCodeScanner(config.github_auth),
    ]
    orchestrator = ScanOrchestrator(scanners, _default_ignore_rules_path())
    apps = orchestrator.run()
    apps = filter_known_apps(apps, ReadmeIndex.from_directory(config.target_list_path))

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
