from pathlib import Path
import json

from shizuku_finder.diffing import DiffResult
from shizuku_finder.models import AppRecord
from shizuku_finder.run_summary import ScannerFailure, write_run_summary


def test_write_run_summary_includes_counts_and_failures(tmp_path: Path) -> None:
    path = tmp_path / 'RUN_SUMMARY.json'
    apps = [
        AppRecord(canonical_id='1', name='A', primary_url='https://a', source='fdroid', confidence=0.9, review_needed=False),
        AppRecord(canonical_id='2', name='B', primary_url='https://b', source='gitlab', confidence=0.4, review_needed=True),
    ]
    diff = DiffResult(added=apps[:1], removed=[], changed=apps[1:])
    failures = [ScannerFailure(scanner='BadScanner', error='boom')]
    write_run_summary(path, apps, diff, failures)
    payload = json.loads(path.read_text(encoding='utf-8'))
    assert payload['total_apps'] == 2
    assert payload['review_needed'] == 1
    assert payload['by_source']['fdroid'] == 1
    assert payload['failures'][0]['scanner'] == 'BadScanner'
