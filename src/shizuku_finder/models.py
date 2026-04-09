from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Evidence:
    source: str
    kind: str
    detail: str
    confidence_delta: float = 0.0


@dataclass(frozen=True, slots=True)
class AppRecord:
    canonical_id: str
    name: str
    primary_url: str
    source: str
    description: str | None = None
    alternate_urls: tuple[str, ...] = field(default_factory=tuple)
    has_downloads: bool = False
    last_updated: datetime | None = None
    confidence: float = 0.0
    evidence: tuple[Evidence, ...] = field(default_factory=tuple)
    review_needed: bool = False

    def with_evidence(self, items: Iterable[Evidence], confidence: float | None = None) -> "AppRecord":
        merged = self.evidence + tuple(items)
        next_confidence = self.confidence if confidence is None else confidence
        return AppRecord(
            canonical_id=self.canonical_id,
            name=self.name,
            primary_url=self.primary_url,
            source=self.source,
            description=self.description,
            alternate_urls=self.alternate_urls,
            has_downloads=self.has_downloads,
            last_updated=self.last_updated,
            confidence=next_confidence,
            evidence=merged,
            review_needed=self.review_needed,
        )
