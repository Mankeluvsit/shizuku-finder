from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

from .models import AppRecord


class SQLiteCache:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                create table if not exists app_runs (
                    canonical_id text not null,
                    name text not null,
                    source text not null,
                    primary_url text not null,
                    description text,
                    has_downloads integer not null,
                    confidence real not null,
                    review_needed integer not null
                )
                """
            )
            columns = [row[1] for row in conn.execute("pragma table_info(app_runs)")]
            if "review_needed" not in columns:
                conn.execute("alter table app_runs add column review_needed integer not null default 0")

    def load_all(self) -> list[AppRecord]:
        with self._connect() as conn:
            rows = conn.execute(
                "select canonical_id, name, source, primary_url, description, has_downloads, confidence, review_needed from app_runs"
            ).fetchall()
        return [
            AppRecord(
                canonical_id=row[0],
                name=row[1],
                source=row[2],
                primary_url=row[3],
                description=row[4],
                has_downloads=bool(row[5]),
                confidence=float(row[6]),
                review_needed=bool(row[7]),
            )
            for row in rows
        ]

    def replace_all(self, apps: Iterable[AppRecord]) -> None:
        with self._connect() as conn:
            conn.execute("delete from app_runs")
            conn.executemany(
                "insert into app_runs (canonical_id, name, source, primary_url, description, has_downloads, confidence, review_needed) values (?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        app.canonical_id,
                        app.name,
                        app.source,
                        app.primary_url,
                        app.description,
                        int(app.has_downloads),
                        app.confidence,
                        int(app.review_needed),
                    )
                    for app in apps
                ],
            )
