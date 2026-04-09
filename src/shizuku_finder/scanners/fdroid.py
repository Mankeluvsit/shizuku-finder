from __future__ import annotations

from datetime import datetime, UTC
from hashlib import sha1
from xml.dom import minidom

import httpx

from shizuku_finder.models import AppRecord, Evidence
from shizuku_finder.scanners.base import BaseScanner


class FDroidScanner(BaseScanner):
    name = "fdroid"

    def __init__(self, repo_xml_url: str) -> None:
        self.repo_xml_url = repo_xml_url

    def scan(self) -> list[AppRecord]:
        response = httpx.get(self.repo_xml_url, follow_redirects=True, timeout=30.0)
        response.raise_for_status()
        document = minidom.parseString(response.content)
        apps: list[AppRecord] = []

        for application in document.getElementsByTagName("application"):
            package_id = self._text(application, "id")
            if not package_id:
                continue

            if not self._has_shizuku_permission(application):
                continue

            source_url = self._text(application, "source")
            web_url = self._text(application, "web")
            primary_url = source_url or web_url or f"https://f-droid.org/packages/{package_id}"
            alternate_urls = tuple(
                url
                for url in [
                    source_url,
                    web_url,
                    f"https://f-droid.org/packages/{package_id}",
                    f"https://f-droid.org/en/packages/{package_id}",
                ]
                if url and url != primary_url
            )
            updated = self._parse_date(self._text(application, "lastupdated"))
            evidence = (
                Evidence(
                    source=self.name,
                    kind="permission",
                    detail="Matched moe.shizuku.manager.permission.API_V23 in F-Droid package metadata",
                    confidence_delta=0.9,
                ),
            )
            canonical_id = sha1(f"fdroid:{package_id}:{primary_url}".encode("utf-8")).hexdigest()
            apps.append(
                AppRecord(
                    canonical_id=canonical_id,
                    name=self._text(application, "name") or package_id,
                    primary_url=primary_url,
                    source=self.name,
                    description=self._text(application, "summary"),
                    alternate_urls=alternate_urls,
                    has_downloads=True,
                    last_updated=updated,
                    confidence=0.9,
                    evidence=evidence,
                    review_needed=False,
                )
            )

        return apps

    def _has_shizuku_permission(self, application) -> bool:
        for package in application.getElementsByTagName("package"):
            permissions_nodes = package.getElementsByTagName("permissions")
            if not permissions_nodes:
                continue
            value = permissions_nodes[0].firstChild.nodeValue if permissions_nodes[0].firstChild else ""
            if value and "moe.shizuku.manager.permission.API_V23" in value:
                return True
        return False

    @staticmethod
    def _text(parent, tag_name: str) -> str | None:
        nodes = parent.getElementsByTagName(tag_name)
        if not nodes:
            return None
        first = nodes[0].firstChild
        if first is None:
            return None
        return first.nodeValue.strip()

    @staticmethod
    def _parse_date(value: str | None) -> datetime | None:
        if not value:
            return None
        parsed = datetime.strptime(value, "%Y-%m-%d")
        return parsed.replace(tzinfo=UTC)
