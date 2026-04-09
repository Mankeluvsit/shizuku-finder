from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from shizuku_finder.models import AppRecord


@dataclass(frozen=True, slots=True)
class IgnoreRule:
    type: str
    value: str
    category: str
    reason: str


class IgnoreRules:
    def __init__(self, rules: list[IgnoreRule]) -> None:
        self.rules = rules

    @classmethod
    def load(cls, path: Path) -> "IgnoreRules":
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        rules = [IgnoreRule(**item) for item in payload.get("rules", [])]
        return cls(rules)

    def should_ignore(self, app: AppRecord) -> bool:
        for rule in self.rules:
            if rule.type == "name" and app.name == rule.value:
                return True
            if rule.type == "url" and (app.primary_url == rule.value or rule.value in app.alternate_urls):
                return True
        return False
