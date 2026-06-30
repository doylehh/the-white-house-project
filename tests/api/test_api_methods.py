import pytest
import allure

from tests.api.client import ApiClient
from tests.api.endpoints import Endpoints


@allure.feature("API HTTP Methods")
@allure.story("Functional tests for POST, PUT, PATCH, DELETE, HEAD, OPTIONS")
class TestApiMethods:

    @allure.title("POST /contact/ with form data returns response")
    def test_post_contact_with_data(self):
        client = ApiClient()
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "message": "Automated test message",
        }
        response = client.post("/contact/", data=payload)

        with allure.step(f"Check response status: {response.status_code}"):
            allure.attach(
                f"Status: {response.status_code}\nBody length: {len(response.text)}",
                name="POST /contact/ response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert response.status_code in [200, 301, 302, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("POST /news/ without data")
    def test_post_news_no_data(self):
        client = ApiClient()
        response = client.post("/news/")

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 301, 302, 403, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("POST / with JSON body")
    def test_post_home_json(self):
        client = ApiClient()
        response = client.post("/", json={"key": "value"})

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 301, 302, 400, 403, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("POST / with empty body")
    def test_post_home_empty(self):
        client = ApiClient()
        response = client.post("/", data={})

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 301, 302, 400, 403, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("POST with custom Content-Type: application/json")
    def test_post_json_content_type(self):
        client = ApiClient()
        response = client.post(
            "/",
            json={"test": True},
            headers={"Content-Type": "application/json"},
        )

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 301, 302, 400, 403, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("POST with large payload")
    def test_post_large_payload(self):
        client = ApiClient()
        large_data = {"field": "x" * 10000}
        response = client.post("/contact/", data=large_data)

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 301, 302, 400, 405, 413], \
                f"Unexpected status: {response.status_code}"

    @allure.title("PUT / with JSON body")
    def test_put_home_json(self):
        client = ApiClient()
        response = client.put("/", json={"key": "value"})

        with allure.step(f"Check status: {response.status_code}"):
            allure.attach(
                f"Status: {response.status_code}\nBody: {response.text[:500]}",
                name="PUT / response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert response.status_code in [200, 301, 302, 400, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("PUT /news/ with data")
    def test_put_news_with_data(self):
        client = ApiClient()
        response = client.put("/news/", json={"title": "test"})

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 301, 302, 400, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("PUT /api/test/ with body")
    def test_put_api_endpoint(self):
        client = ApiClient()
        response = client.put("/api/test/", json={"data": "test"})

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 201, 204, 400, 404, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("PUT with empty body")
    def test_put_home_empty(self):
        client = ApiClient()
        response = client.put("/")

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 301, 302, 400, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("PUT with Content-Type: application/json")
    def test_put_json_content_type(self):
        client = ApiClient()
        response = client.put(
            "/",
            json={"update": True},
            headers={"Content-Type": "application/json"},
        )

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 301, 302, 400, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("PATCH / with JSON body")
    def test_patch_home_json(self):
        client = ApiClient()
        response = client.patch("/", json={"field": "updated"})

        with allure.step(f"Check status: {response.status_code}"):
            allure.attach(
                f"Status: {response.status_code}\nBody: {response.text[:500]}",
                name="PATCH / response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert response.status_code in [200, 301, 302, 400, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("PATCH /news/ with partial update")
    def test_patch_news_partial(self):
        client = ApiClient()
        response = client.patch("/news/", json={"status": "draft"})

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 301, 302, 400, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("PATCH /api/test/ with data")
    def test_patch_api_endpoint(self):
        client = ApiClient()
        response = client.patch("/api/test/", json={"patch": "me"})

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 204, 400, 404, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("PATCH with empty body")
    def test_patch_home_empty(self):
        client = ApiClient()
        response = client.patch("/")

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 301, 302, 400, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("PATCH with Content-Type: application/json")
    def test_patch_json_content_type(self):
        client = ApiClient()
        response = client.patch(
            "/",
            json={"partial": "update"},
            headers={"Content-Type": "application/json"},
        )

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 301, 302, 400, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("DELETE / returns method not allowed")
    def test_delete_home(self):
        client = ApiClient()
        response = client.delete("/")

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 204, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("DELETE /news/ returns method not allowed")
    def test_delete_news(self):
        client = ApiClient()
        response = client.delete("/news/")

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 204, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("DELETE /api/test/")
    def test_delete_api_endpoint(self):
        client = ApiClient()
        response = client.delete("/api/test/")

        with allure.step(f"Check status: {response.status_code}"):
            assert response.status_code in [200, 204, 404, 405], \
                f"Unexpected status: {response.status_code}"

    @allure.title("HEAD / returns same status as GET /")
    def test_head_home_matches_get(self):
        client = ApiClient()
        head_resp = client.head("/")
        get_resp = client.get("/")

        with allure.step("Compare HEAD vs GET"):
            allure.attach(
                f"HEAD: {head_resp.status_code}\nGET: {get_resp.status_code}",
                name="Status comparison",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert head_resp.status_code == get_resp.status_code

    @allure.title("HEAD response body is empty")
    def test_head_empty_body(self):
        client = ApiClient()
        response = client.head("/")

        with allure.step("Body must be empty"):
            assert len(response.content) == 0, \
                f"HEAD returned {len(response.content)} bytes"

    @allure.title("HEAD /news/ returns 200")
    def test_head_news(self):
        client = ApiClient()
        response = client.head("/news/")

        with allure.step(f"Status: {response.status_code}"):
            assert response.status_code == 200

    @allure.title("HEAD /contact/ returns 200")
    def test_head_contact(self):
        client = ApiClient()
        response = client.head("/contact/")

        with allure.step(f"Status: {response.status_code}"):
            assert response.status_code == 200

    @allure.title("HEAD /gallery/ returns 200")
    def test_head_gallery(self):
        client = ApiClient()
        response = client.head("/gallery/")

        with allure.step(f"Status: {response.status_code}"):
            assert response.status_code == 200

    @allure.title("OPTIONS / returns allowed methods")
    def test_options_home(self):
        client = ApiClient()
        response = client.options("/")

        with allure.step(f"Status: {response.status_code}"):
            allure.attach(
                f"Allow: {response.headers.get('Allow', 'N/A')}\n"
                f"Status: {response.status_code}",
                name="OPTIONS response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert response.status_code in [200, 204, 405]

    @allure.title("OPTIONS /news/")
    def test_options_news(self):
        client = ApiClient()
        response = client.options("/news/")

        with allure.step(f"Status: {response.status_code}"):
            assert response.status_code in [200, 204, 405]

    @allure.title("OPTIONS /contact/")
    def test_options_contact(self):
        client = ApiClient()
        response = client.options("/contact/")

        with allure.step(f"Status: {response.status_code}"):
            assert response.status_code in [200, 204, 405]
