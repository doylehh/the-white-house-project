import pytest
import allure
import time

from tests.api.client import ApiClient
from urls import links


@allure.feature("API Performance")
@allure.story("Response time checks")
class TestApiPerformance:
    MAX_RESPONSE_TIME = 5.0

    @allure.title("Response time for {url}")
    @pytest.mark.parametrize("url", links[:10])
    def test_response_time(self, url):
        client = ApiClient()
        start = time.time()
        response = client.get()
        elapsed = time.time() - start

        with allure.step(f"Response time: {elapsed:.2f}s"):
            allure.attach(f"{elapsed:.2f}s", name="response_time", attachment_type=allure.attachment_type.TEXT)

        assert elapsed < self.MAX_RESPONSE_TIME, f"Response time {elapsed:.2f}s exceeds {self.MAX_RESPONSE_TIME}s"
