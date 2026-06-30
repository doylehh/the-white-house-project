import pytest
import allure

from tests.api.client import ApiClient
from urls import links


@allure.feature("API Headers")
@allure.story("Security and content headers")
class TestApiHeaders:
    @allure.title("Content-Type header present for {url}")
    @pytest.mark.parametrize("url", links[:5])
    def test_content_type_header(self, url):
        client = ApiClient()
        response = client.get(endpoint=url.replace("https://www.whitehouse.gov", ""))

        with allure.step("Check Content-Type header"):
            assert "Content-Type" in response.headers, "Content-Type header missing"

    @allure.title("Security headers present for {url}")
    @pytest.mark.parametrize("url", links[:5])
    def test_security_headers(self, url):
        client = ApiClient()
        response = client.get(endpoint=url.replace("https://www.whitehouse.gov", ""))

        security_headers = ["X-Content-Type-Options", "X-Frame-Options"]
        with allure.step("Check security headers"):
            for header in security_headers:
                value = response.headers.get(header)
                allure.attach(f"{header}: {value or 'MISSING'}", name=header)
                assert value is not None, f"Security header {header} missing"

    @allure.title("Server header does not expose version")
    @pytest.mark.parametrize("url", links[:3])
    def test_server_header_no_version(self, url):
        client = ApiClient()
        response = client.get(endpoint=url.replace("https://www.whitehouse.gov", ""))

        with allure.step("Check Server header"):
            server = response.headers.get("Server", "")
            assert "Apache/" not in server and "nginx/" not in server, f"Server header exposes version: {server}"
