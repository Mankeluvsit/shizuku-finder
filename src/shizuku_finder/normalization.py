from __future__ import annotations

import re
from urllib.parse import urlparse


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower()).strip()


def normalize_url(value: str) -> str:
    parsed = urlparse(value)
    scheme = parsed.scheme.lower() or "https"
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    return f"{scheme}://{netloc}{path}"
