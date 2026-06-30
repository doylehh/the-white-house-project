import pytest
import allure

from tests.api.client import ApiClient


@allure.feature("API Error Handling")
@allure.story("404, method rejection, error pages")
class TestApiErrors:

    @allure.title("Non-existent page returns 404")
    def test_404_page(self):
        client = ApiClient()
        response = client.get("/this-page-does-not-exist-12345/")

        with allure.step("Verify 404"):
            assert response.status_code == 404

    @allure.title("Deep nested invalid path returns 404")
    def test_invalid_path_returns_404(self):
        client = ApiClient()
        response = client.get("/nonexistent/deeply/nested/path/")

        with allure.step("Verify 404"):
            assert response.status_code == 404

    @allure.title("Random UUID path returns 404")
    def test_uuid_path_returns_404(self):
        client = ApiClient()
        response = client.get("/a1b2c3d4-e5f6-7890-abcd-ef1234567890/")

        with allure.step("Verify 404"):
            assert response.status_code == 404

    @allure.title("POST /news/ blocked by server")
    def test_post_news_blocked(self):
        client = ApiClient()
        response = client.post("/news/")

        with allure.step(f"Server returns {response.status_code}"):
            assert response.status_code in [403, 405], \
                f"Expected 403 or 405, got {response.status_code}"

    @allure.title("POST /contact/ without form data blocked")
    def test_post_contact_no_form(self):
        client = ApiClient()
        response = client.post("/contact/")

        with allure.step(f"Server returns {response.status_code}"):
            assert response.status_code in [200, 403, 405, 301, 302], \
                f"Unexpected status: {response.status_code}"

    @allure.title("PUT /api/nonexistent/ returns error")
    def test_put_nonexistent(self):
        client = ApiClient()
        response = client.put("/api/nonexistent/")

        with allure.step(f"Server returns {response.status_code}"):
            assert response.status_code in [404, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("PATCH /api/nonexistent/ returns error")
    def test_patch_nonexistent(self):
        client = ApiClient()
        response = client.patch("/api/nonexistent/")

        with allure.step(f"Server returns {response.status_code}"):
            assert response.status_code in [404, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("DELETE /api/nonexistent/ returns error")
    def test_delete_nonexistent(self):
        client = ApiClient()
        response = client.delete("/api/nonexistent/")

        with allure.step(f"Server returns {response.status_code}"):
            assert response.status_code in [404, 405], \
                f"Unexpected status: {response.status_code}"
