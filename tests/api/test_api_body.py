import pytest
import allure

from tests.api.client import ApiClient


@allure.feature("API Body Content")
@allure.story("Response body validation")
class TestApiBody:
    @allure.title("Home page contains expected content")
    def test_home_page_content(self):
        client = ApiClient()
        response = client.get()

        with allure.step("Check body contains key elements"):
            body = response.text.lower()
            assert "white house" in body or "the white house" in body, "Home page missing White House reference"

    @allure.title("News page contains articles")
    def test_news_page_content(self):
        client = ApiClient()
        response = client.get("/news/")

        with allure.step("Check page loaded"):
            assert response.status_code == 200
            assert len(response.text) > 1000, "News page body too short"

    @allure.title("Contact page has form elements")
    def test_contact_page_content(self):
        client = ApiClient()
        response = client.get("/contact/")

        with allure.step("Check contact page"):
            assert response.status_code == 200
            body = response.text.lower()
            assert "contact" in body, "Contact page missing contact reference"

    @allure.title("Page does not contain error messages: {url}")
    @pytest.mark.parametrize("url", [
        "/news/",
        "/contact/",
        "/gallery/",
    ])
    def test_no_error_in_body(self, url):
        client = ApiClient()
        response = client.get(url)

        with allure.step("Check no error in body"):
            body_lower = response.text.lower()
            assert "fatal error" not in body_lower, "Page contains fatal error"
            assert "database error" not in body_lower, "Page contains database error"
