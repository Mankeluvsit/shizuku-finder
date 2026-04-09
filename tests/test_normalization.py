from shizuku_finder.normalization import normalize_name, normalize_url


def test_normalization_normalizes_name_and_url() -> None:
    assert normalize_name("My App++") == "myapp"
    assert normalize_url("HTTPS://GitHub.com/Example/Repo/") == "https://github.com/Example/Repo"
