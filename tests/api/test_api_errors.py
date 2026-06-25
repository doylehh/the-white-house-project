import pytest
import allure

from tests.api.client import ApiClient


@allure.feature("API Error Handling")
@allure.story("404 and error pages")
class TestApiErrors:
    @allure.title("Non-existent page returns 404")
    def test_404_page(self):
        client = ApiClient()
        response = client.get("/this-page-does-not-exist-12345/")

        with allure.step("Check 404 status"):
            assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    @allure.title("Invalid path returns proper error")
    def test_invalid_path(self):
        client = ApiClient()
        response = client.get("/nonexistent/deeply/nested/path/")

        with allure.step("Check response"):
            assert response.status_code in [404, 403, 301, 302], f"Unexpected status: {response.status_code}"

    @allure.title("Method not allowed handled gracefully")
    def test_post_on_get_page(self):
        client = ApiClient()
        response = client.post("/news/")

        with allure.step("Check POST response"):
            assert response.status_code in [404, 403, 405, 301, 302], f"Unexpected status: {response.status_code}"
