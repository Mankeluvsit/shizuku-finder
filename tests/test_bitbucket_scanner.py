from pathlib import Path
import json

from shizuku_finder.scanners.bitbucket import BitbucketScanner


def test_bitbucket_scanner_filters_by_content(monkeypatch) -> None:
    fixture = json.loads(Path('tests/fixtures/bitbucket_repos.json').read_text(encoding='utf-8'))
    scanner = BitbucketScanner(Path('cache'))
    monkeypatch.setattr(scanner, '_fetch_repos', lambda: fixture['values'])
    monkeypatch.setattr(scanner, '_has_downloads', lambda repo: repo.get('name') == 'BitbucketShizuku')

    def fake_ensure_clone(url: str, repo_id: str):
        return Path(url)

    def fake_contains(repo_path: Path, needles):
        return 'bitbucketshizuku' in str(repo_path).lower()

    scanner.cache.ensure_clone = fake_ensure_clone
    scanner.cache.contains_any_text = fake_contains
    apps = scanner.scan()
    assert len(apps) == 1
    assert apps[0].name == 'BitbucketShizuku'
    assert apps[0].source == 'bitbucket'
    assert apps[0].has_downloads is True
