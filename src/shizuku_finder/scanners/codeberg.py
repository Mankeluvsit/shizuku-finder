from __future__ import annotations

from hashlib import sha1
from pathlib import Path

from shizuku_finder.clients import HttpJsonClient
from shizuku_finder.models import AppRecord, Evidence
from shizuku_finder.repo_cache import RepoCache
from shizuku_finder.scanners.base import BaseScanner


class CodebergScanner(BaseScanner):
    name = "codeberg"

    def __init__(self, cache_root: Path, base_url: str = "https://codeberg.org/api/v1") -> None:
        self.cache = RepoCache(cache_root)
        self.base_url = base_url.rstrip("/")
        self.http = HttpJsonClient()

    def _fetch_repos(self) -> list[dict]:
        return self.http.get_json_pages(
            f"{self.base_url}/repos/search",
            base_params={"q": "shizuku", "limit": 50},
            max_pages=3,
        )

    def scan(self) -> list[AppRecord]:
        apps: list[AppRecord] = []
        for repo in self._fetch_repos():
            clone_url = repo.get("clone_url") or repo.get("ssh_url") or repo.get("html_url")
            web_url = repo.get("html_url") or repo.get("website")
            full_name = repo.get("full_name") or f"{repo.get('owner', {}).get('username', '')}/{repo.get('name', '')}".strip("/")
            if not clone_url or not web_url or not full_name:
                continue

            repo_id = sha1(web_url.encode("utf-8")).hexdigest()
            try:
                repo_path = self.cache.ensure_clone(clone_url, repo_id)
            except Exception:
                continue

            matched = self.cache.contains_any_text(
                repo_path,
                (
                    "import rikka.shizuku.Shizuku",
                    "rikka.shizuku.ShizukuProvider",
                    "moe.shizuku.manager.permission.API_V23",
                ),
            )
            if not matched:
                continue

            apps.append(
                AppRecord(
                    canonical_id=sha1(f"codeberg:{full_name}".encode("utf-8")).hexdigest(),
                    name=repo.get("name") or full_name.split("/")[-1],
                    primary_url=web_url,
                    source=self.name,
                    description=repo.get("description"),
                    has_downloads=False,
                    confidence=0.7,
                    evidence=(
                        Evidence(
                            source=self.name,
                            kind="repo_content",
                            detail="Matched Shizuku signature in cloned Codeberg repository contents",
                            confidence_delta=0.7,
                        ),
                    ),
                    review_needed=False,
                )
            )
        return apps
