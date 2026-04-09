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
                    confidence real not null
                )
                """
            )

    def replace_all(self, apps: Iterable[AppRecord]) -> None:
        with self._connect() as conn:
            conn.execute("delete from app_runs")
            conn.executemany(
                "insert into app_runs (canonical_id, name, source, primary_url, description, has_downloads, confidence) values (?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        app.canonical_id,
                        app.name,
                        app.source,
                        app.primary_url,
                        app.description,
                        int(app.has_downloads),
                        app.confidence,
                    )
                    for app in apps
                ],
            )
