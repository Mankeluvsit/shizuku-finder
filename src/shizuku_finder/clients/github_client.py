from __future__ import annotations

from github import Auth, Github


class GitHubSearchClient:
    def __init__(self, auth_token: str | None) -> None:
        self.auth_token = auth_token

    def is_enabled(self) -> bool:
        return bool(self.auth_token)

    def search_code(self, query: str):
        if not self.auth_token:
            return []
        client = Github(auth=Auth.Token(self.auth_token))
        return client.search_code(query)

    def search_repositories(self, query: str, sort: str = "stars", order: str = "desc"):
        if not self.auth_token:
            return []
        client = Github(auth=Auth.Token(self.auth_token))
        return client.search_repositories(query, sort, order)
