from __future__ import annotations

from hashlib import sha1
from pathlib import Path

from github import Auth, Github

from shizuku_finder.models import AppRecord, Evidence
from shizuku_finder.repo_cache import RepoCache
from shizuku_finder.scanners.base import BaseScanner


class GitHubMetaScanner(BaseScanner):
    name = "github_meta"

    def __init__(self, auth_token: str | None, cache_root: Path) -> None:
        self.auth_token = auth_token
        self.cache = RepoCache(cache_root)

    def scan(self) -> list[AppRecord]:
        if not self.auth_token:
            return []

        client = Github(auth=Auth.Token(self.auth_token))
        results = client.search_repositories(
            "(shizuku AND NOT RepainterServicePriv) in:readme in:topics in:description language:Dart language:Kotlin language:Java",
            "stars",
            "desc",
        )

        apps: list[AppRecord] = []
        for repo in results:
            repo_id = sha1(repo.html_url.encode("utf-8")).hexdigest()
            try:
                repo_path = self.cache.ensure_clone(repo.clone_url, repo_id)
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

            evidence = (
                Evidence(
                    source=self.name,
                    kind="repo_content",
                    detail="Matched Shizuku signature in cloned repository contents",
                    confidence_delta=0.85,
                ),
            )
            apps.append(
                AppRecord(
                    canonical_id=sha1(f"github-meta:{repo.full_name}".encode("utf-8")).hexdigest(),
                    name=repo.name,
                    primary_url=repo.html_url,
                    source=self.name,
                    description=repo.description,
                    has_downloads=len(repo.get_releases().get_page(0)) > 0,
                    last_updated=repo.pushed_at,
                    confidence=0.85,
                    evidence=evidence,
                    review_needed=False,
                )
            )
        return apps
