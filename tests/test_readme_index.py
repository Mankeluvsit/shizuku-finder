from pathlib import Path

from shizuku_finder.readme_index import ReadmeIndex


def test_readme_index_matches_name_and_url(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "README.md").write_text(
        "* [KeepMe](https://github.com/example/keepme)\n",
        encoding="utf-8",
    )
    index = ReadmeIndex.from_directory(docs)
    assert index.contains_name("KeepMe") is True
    assert index.contains_url("https://github.com/example/keepme") is True
