from pathlib import Path
import json

from shizuku_finder.scanners.codeberg import CodebergScanner


def test_codeberg_scanner_filters_by_content(monkeypatch) -> None:
    fixture = json.loads(Path('tests/fixtures/codeberg_repos.json').read_text(encoding='utf-8'))
    scanner = CodebergScanner(Path('cache'))
    monkeypatch.setattr(scanner, '_fetch_repos', lambda: fixture['data'])

    def fake_ensure_clone(url: str, repo_id: str):
        return Path(url)
    def fake_contains(repo_path: Path, needles):
        return 'CodebergShizuku' in str(repo_path)

    scanner.cache.ensure_clone = fake_ensure_clone
    scanner.cache.contains_any_text = fake_contains
    apps = scanner.scan()
    assert len(apps) == 1
    assert apps[0].name == 'CodebergShizuku'
    assert apps[0].source == 'codeberg'
