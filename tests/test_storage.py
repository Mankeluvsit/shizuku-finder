from pathlib import Path

from shizuku_finder.models import AppRecord
from shizuku_finder.storage import SQLiteCache


def test_sqlite_cache_roundtrip_preserves_review_needed(tmp_path: Path) -> None:
    db_path = tmp_path / 'cache.sqlite3'
    cache = SQLiteCache(db_path)
    apps = [
        AppRecord(canonical_id='1', name='One', primary_url='https://one', source='x', confidence=0.9, review_needed=False),
        AppRecord(canonical_id='2', name='Two', primary_url='https://two', source='x', confidence=0.4, review_needed=True),
    ]
    cache.replace_all(apps)
    loaded = cache.load_all()
    assert [(app.canonical_id, app.review_needed) for app in loaded] == [('1', False), ('2', True)]
