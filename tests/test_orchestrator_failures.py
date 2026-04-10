from pathlib import Path

from shizuku_finder.models import AppRecord
from shizuku_finder.orchestrator import ScanOrchestrator
from shizuku_finder.scanners.base import BaseScanner


class GoodScanner(BaseScanner):
    name = 'good'

    def scan(self):
        return [AppRecord(canonical_id='1', name='App', primary_url='https://a', source='good', confidence=0.8)]


class BadScanner(BaseScanner):
    name = 'bad'

    def scan(self):
        raise RuntimeError('boom')


def test_orchestrator_captures_failures_and_keeps_successful_results(tmp_path: Path) -> None:
    result = ScanOrchestrator([BadScanner(), GoodScanner()], None).run_detailed()
    assert [app.name for app in result.apps] == ['App']
    assert len(result.failures) == 1
    assert result.failures[0].scanner == 'BadScanner'
