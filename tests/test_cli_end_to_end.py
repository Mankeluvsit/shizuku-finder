from pathlib import Path

from shizuku_finder import cli
from shizuku_finder.config import AppConfig
from shizuku_finder.models import AppRecord


class FakeScanner:
    def __init__(self, apps):
        self._apps = apps

    def scan(self):
        return self._apps


def test_run_scan_end_to_end_with_monkeypatched_scanners(tmp_path: Path, monkeypatch) -> None:
    apps = [
        AppRecord(canonical_id='1', name='ExistingApp', primary_url='https://github.com/example/existing-app', source='github_code', confidence=0.9, has_downloads=True),
        AppRecord(canonical_id='2', name='FreshApp', primary_url='https://github.com/example/fresh-app', source='github_code', confidence=0.9, has_downloads=True),
        AppRecord(canonical_id='3', name='ReviewApp', primary_url='https://github.com/example/review-app', source='gitlab', confidence=0.4, has_downloads=False),
    ]
    docs = tmp_path / 'list'
    docs.mkdir()
    (docs / 'README.md').write_text('* [ExistingApp](https://github.com/example/existing-app)\n', encoding='utf-8')

    monkeypatch.setattr(cli, 'FDroidScanner', lambda *args, **kwargs: FakeScanner([]))
    monkeypatch.setattr(cli, 'GitHubCodeScanner', lambda *args, **kwargs: FakeScanner(apps))
    monkeypatch.setattr(cli, 'GitHubMetaScanner', lambda *args, **kwargs: FakeScanner([]))
    monkeypatch.setattr(cli, 'GitLabScanner', lambda *args, **kwargs: FakeScanner([]))
    monkeypatch.setattr(cli, 'CodebergScanner', lambda *args, **kwargs: FakeScanner([]))

    config = AppConfig(
        github_auth=None,
        target_list_path=docs,
        summary_file=tmp_path / 'SUMMARY.md',
        json_file=tmp_path / 'summary.json',
        csv_file=tmp_path / 'summary.csv',
        review_file=tmp_path / 'REVIEW_NEEDED.md',
        diff_file=tmp_path / 'DIFF.md',
        database_path=tmp_path / 'cache.sqlite3',
    )
    cli.run_scan(config)

    summary = config.summary_file.read_text(encoding='utf-8')
    review = config.review_file.read_text(encoding='utf-8')
    diff_text = config.diff_file.read_text(encoding='utf-8')
    assert 'FreshApp' in summary
    assert 'ExistingApp' not in summary
    assert 'ReviewApp' in review
    assert 'Added:' in diff_text
