from pathlib import Path
import json

from shizuku_finder.scanners.gitlab import GitLabScanner


def test_gitlab_scanner_filters_by_content(monkeypatch) -> None:
    fixture = json.loads(Path('tests/fixtures/gitlab_projects.json').read_text(encoding='utf-8'))
    scanner = GitLabScanner(Path('cache'))
    monkeypatch.setattr(scanner, '_fetch_projects', lambda: fixture)

    def fake_ensure_clone(url: str, repo_id: str):
        return Path(url)
    def fake_contains(repo_path: Path, needles):
        return 'gitlabshizuku' in str(repo_path)

    scanner.cache.ensure_clone = fake_ensure_clone
    scanner.cache.contains_any_text = fake_contains
    apps = scanner.scan()
    assert len(apps) == 1
    assert apps[0].name == 'GitLabShizuku'
    assert apps[0].source == 'gitlab'
