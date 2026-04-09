from __future__ import annotations

from shizuku_finder.models import AppRecord
from shizuku_finder.readme_index import ReadmeIndex


def filter_known_apps(apps: list[AppRecord], index: ReadmeIndex) -> list[AppRecord]:
    filtered: list[AppRecord] = []
    for app in apps:
        urls = (app.primary_url, *app.alternate_urls)
        if index.contains_name(app.name) or index.contains_any_url(urls):
            continue
        filtered.append(app)
    return filtered
