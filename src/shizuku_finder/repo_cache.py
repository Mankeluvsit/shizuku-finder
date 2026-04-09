from __future__ import annotations

from pathlib import Path
import shutil

from git import Repo


class RepoCache:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def ensure_clone(self, url: str, repo_id: str) -> Path:
        path = self.root / repo_id
        if path.exists():
            try:
                repo = Repo(path)
                repo.remote().fetch(prune=True)
                return path
            except Exception:
                shutil.rmtree(path, ignore_errors=True)

        Repo.clone_from(url, path, depth=1)
        return path

    def contains_any_text(self, repo_path: Path, needles: tuple[str, ...]) -> bool:
        for path in repo_path.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".kt", ".java", ".xml", ".gradle", ".kts"}:
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if any(needle in content for needle in needles):
                return True
        return False
