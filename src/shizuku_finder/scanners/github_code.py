from __future__ import annotations

from hashlib import sha1

from github import Auth, Github

from shizuku_finder.models import AppRecord, Evidence
from shizuku_finder.scanners.base import BaseScanner


class GitHubCodeScanner(BaseScanner):
    name = "github_code"

    def __init__(self, auth_token: str | None) -> None:
        self.auth_token = auth_token

    def scan(self) -> list[AppRecord]:
        if not self.auth_token:
            return []

        client = Github(auth=Auth.Token(self.auth_token))
        results = client.search_code("rikka.shizuku.ShizukuProvider language:XML NOT is:fork")

        apps: list[AppRecord] = []
        seen: set[str] = set()
        for file in results:
            repo = file.repository
            if repo.html_url in seen:
                continue
            seen.add(repo.html_url)
            has_downloads = len(repo.get_releases().get_page(0)) > 0
            evidence = (
                Evidence(
                    source=self.name,
                    kind="code_search",
                    detail="Matched rikka.shizuku.ShizukuProvider in GitHub code search",
                    confidence_delta=0.8,
                ),
            )
            apps.append(
                AppRecord(
                    canonical_id=sha1(f"github:{repo.full_name}".encode("utf-8")).hexdigest(),
                    name=repo.name,
                    primary_url=repo.html_url,
                    source=self.name,
                    description=repo.description,
                    has_downloads=has_downloads,
                    last_updated=repo.pushed_at,
                    confidence=0.8,
                    evidence=evidence,
                    review_needed=False,
                )
            )
        return apps
