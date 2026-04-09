from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


@dataclass(slots=True)
class ReadmeIndex:
    text: str

    @classmethod
    def from_directory(cls, directory: Path) -> "ReadmeIndex":
        if not directory.exists():
            return cls(text="")
        parts: list[str] = []
        for path in sorted(directory.rglob("*.md")):
            try:
                parts.append(path.read_text(encoding="utf-8", errors="ignore").lower())
            except OSError:
                continue
        return cls(text="\n".join(parts))

    def contains_name(self, name: str) -> bool:
        return f"[{name.lower()}]" in self.text

    def contains_url(self, url: str) -> bool:
        normalized = url.replace("https://", "").replace("http://", "").lower()
        return normalized in self.text

    def contains_any_url(self, urls: tuple[str, ...] | list[str]) -> bool:
        return any(self.contains_url(url) for url in urls)
