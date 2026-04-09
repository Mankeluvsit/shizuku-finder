from __future__ import annotations

from hashlib import sha1
from pathlib import Path

from shizuku_finder.clients import HttpJsonClient
from shizuku_finder.models import AppRecord, Evidence
from shizuku_finder.repo_cache import RepoCache
from shizuku_finder.scanners.base import BaseScanner


class GitLabScanner(BaseScanner):
    name = "gitlab"

    def __init__(self, cache_root: Path, base_url: str = "https://gitlab.com/api/v4") -> None:
        self.cache = RepoCache(cache_root)
        self.base_url = base_url.rstrip("/")
        self.http = HttpJsonClient()

    def _fetch_projects(self) -> list[dict]:
        return self.http.get_json_pages(
            f"{self.base_url}/projects",
            base_params={"search": "shizuku", "simple": True, "per_page": 50},
            max_pages=3,
        )

    def scan(self) -> list[AppRecord]:
        apps: list[AppRecord] = []
        for project in self._fetch_projects():
            clone_url = project.get("http_url_to_repo")
            web_url = project.get("web_url")
            if not clone_url or not web_url:
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
                    canonical_id=sha1(f"gitlab:{project.get('path_with_namespace', web_url)}".encode("utf-8")).hexdigest(),
                    name=project.get("name") or project.get("path") or "unknown",
                    primary_url=web_url,
                    source=self.name,
                    description=project.get("description"),
                    has_downloads=False,
                    confidence=0.72,
                    evidence=(
                        Evidence(
                            source=self.name,
                            kind="repo_content",
                            detail="Matched Shizuku signature in cloned GitLab repository contents",
                            confidence_delta=0.72,
                        ),
                    ),
                    review_needed=False,
                )
            )
        return apps
