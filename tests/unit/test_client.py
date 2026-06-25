import pytest
from tests.api.client import ApiClient


class TestApiClient:

    def test_client_creation(self):
        client = ApiClient()
        assert client is not None

    def test_client_has_session(self):
        client = ApiClient()
        assert client.session is not None

    def test_client_default_base_url(self):
        client = ApiClient()
        assert client.base_url.startswith("https://")

    def test_client_custom_base_url(self):
        client = ApiClient("https://example.com")
        assert client.base_url == "https://example.com"

    def test_client_get_returns_response(self):
        client = ApiClient()
        response = client.get("/")
        assert response is not None
        assert hasattr(response, "status_code")

    def test_client_close(self):
        client = ApiClient()
        client.close()
