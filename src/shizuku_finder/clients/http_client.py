from __future__ import annotations

from collections.abc import Iterable

import httpx


class HttpJsonClient:
    def __init__(self, timeout: float = 30.0) -> None:
        self.timeout = timeout

    def get_json(self, url: str, params: dict | None = None):
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    def get_json_pages(self, url: str, base_params: dict | None = None, page_param: str = "page", max_pages: int = 3) -> list:
        items: list = []
        params = dict(base_params or {})
        with httpx.Client(timeout=self.timeout) as client:
            for page in range(1, max_pages + 1):
                page_params = dict(params)
                page_params[page_param] = page
                try:
                    response = client.get(url, params=page_params)
                    response.raise_for_status()
                except httpx.HTTPError:
                    break
                payload = response.json()
                batch = self._coerce_batch(payload)
                if not batch:
                    break
                items.extend(batch)
        return items

    @staticmethod
    def _coerce_batch(payload) -> list:
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            for key in ("data", "repos", "items", "projects"):
                value = payload.get(key)
                if isinstance(value, list):
                    return value
        return []
