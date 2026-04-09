from pathlib import Path

from shizuku_finder.repo_cache import RepoCache


def test_repo_cache_contains_any_text(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "Main.kt").write_text("import rikka.shizuku.Shizuku\n", encoding="utf-8")
    cache = RepoCache(tmp_path / "cache")
    assert cache.contains_any_text(repo, ("import rikka.shizuku.Shizuku",)) is True
