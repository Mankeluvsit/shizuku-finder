from pathlib import Path

from shizuku_finder.scanners.fdroid import FDroidScanner


def test_fdroid_scanner_parses_fixture_xml() -> None:
    fixture = Path('tests/fixtures/fdroid_index.xml').read_bytes()
    scanner = FDroidScanner('https://example.com/index.xml')
    apps = scanner.parse_xml(fixture)
    assert len(apps) == 1
    app = apps[0]
    assert app.name == 'ShizukuApp'
    assert app.primary_url == 'https://github.com/example/shizukuapp'
    assert app.has_downloads is True
    assert app.confidence == 0.9
    assert app.last_updated is not None
