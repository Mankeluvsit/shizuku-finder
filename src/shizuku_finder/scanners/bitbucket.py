from __future__ import annotations

from hashlib import sha1
from pathlib import Path

from shizuku_finder.clients import HttpJsonClient
from shizuku_finder.models import AppRecord, Evidence
from shizuku_finder.repo_cache import RepoCache
from shizuku_finder.scanners.base import BaseScanner


class BitbucketScanner(BaseScanner):
    name = "bitbucket"

    def __init__(self, cache_root: Path, base_url: str = "https://api.bitbucket.org/2.0") -> None:
        self.cache = RepoCache(cache_root)
        self.base_url = base_url.rstrip("/")
        self.http = HttpJsonClient()

    def _fetch_repos(self) -> list[dict]:
        return self.http.get_json_pages(
            f"{self.base_url}/repositories",
            base_params={"q": 'name ~ "shizuku" OR description ~ "shizuku"', "sort": "-updated_on", "pagelen": 50},
            max_pages=3,
        )

    def _clone_url(self, repo: dict) -> str | None:
        clones = repo.get("links", {}).get("clone", [])
        for clone in clones:
            if clone.get("name") == "https":
                return clone.get("href")
        for clone in clones:
            href = clone.get("href")
            if href:
                return href
        return None

    def _html_url(self, repo: dict) -> str | None:
        return repo.get("links", {}).get("html", {}).get("href")

    def _has_downloads(self, repo: dict) -> bool:
        full_name = repo.get("full_name", "")
        if "/" not in full_name:
            return False
        workspace, repo_slug = full_name.split("/", 1)
        payload = self.http.get_json(f"{self.base_url}/repositories/{workspace}/{repo_slug}/downloads")
        values = payload.get("values", []) if isinstance(payload, dict) else []
        return bool(values)

    def scan(self) -> list[AppRecord]:
        apps: list[AppRecord] = []
        for repo in self._fetch_repos():
            clone_url = self._clone_url(repo)
            web_url = self._html_url(repo)
            full_name = repo.get("full_name")
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

            try:
                has_downloads = self._has_downloads(repo)
            except Exception:
                has_downloads = False

            apps.append(
                AppRecord(
                    canonical_id=sha1(f"bitbucket:{full_name}".encode("utf-8")).hexdigest(),
                    name=repo.get("name") or full_name.split("/")[-1],
                    primary_url=web_url,
                    source=self.name,
                    description=repo.get("description"),
                    has_downloads=has_downloads,
                    confidence=0.69,
                    evidence=(
                        Evidence(
                            source=self.name,
                            kind="repo_content",
                            detail="Matched Shizuku signature in cloned Bitbucket repository contents",
                            confidence_delta=0.69,
                        ),
                    ),
                    review_needed=False,
                )
            )
        return apps
