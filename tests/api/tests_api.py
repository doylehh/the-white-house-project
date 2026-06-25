import pytest
import allure

from tests.api.client import ApiClient
from tests.api.endpoints import Endpoints


@allure.feature("API Tests")
@allure.story("GET requests")
class TestApi:
    @allure.title("Home page returns 200")
    def test_home_page(self):
        client = ApiClient()
        response = client.get()
        assert response.status_code == 200

    @allure.title("News page returns 200")
    def test_news_page(self):
        client = ApiClient()
        response = client.get("/news/")
        assert response.status_code == 200

    @allure.title("Contact page returns 200")
    def test_contact_page(self):
        client = ApiClient()
        response = client.get("/contact/")
        assert response.status_code == 200

    @allure.title("Gallery page returns 200")
    def test_gallery_page(self):
        client = ApiClient()
        response = client.get("/gallery/")
        assert response.status_code == 200
