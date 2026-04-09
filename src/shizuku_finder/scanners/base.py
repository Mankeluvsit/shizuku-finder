from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from shizuku_finder.models import AppRecord


class BaseScanner(ABC):
    name: str

    @abstractmethod
    def scan(self) -> Iterable[AppRecord]:
        raise NotImplementedError
