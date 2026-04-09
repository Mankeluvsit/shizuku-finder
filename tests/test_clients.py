from shizuku_finder.clients import GitHubSearchClient, HttpJsonClient


def test_http_json_client_coerce_batch_handles_supported_shapes() -> None:
    assert HttpJsonClient._coerce_batch([{"a": 1}]) == [{"a": 1}]
    assert HttpJsonClient._coerce_batch({"data": [{"a": 1}]}) == [{"a": 1}]
    assert HttpJsonClient._coerce_batch({"repos": [{"a": 1}]}) == [{"a": 1}]
    assert HttpJsonClient._coerce_batch({"items": [{"a": 1}]}) == [{"a": 1}]
    assert HttpJsonClient._coerce_batch({"projects": [{"a": 1}]}) == [{"a": 1}]


def test_github_search_client_disabled_without_token() -> None:
    client = GitHubSearchClient(None)
    assert client.is_enabled() is False
    assert client.search_code("test") == []
    assert client.search_repositories("test") == []
