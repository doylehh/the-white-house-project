import allure
import pytest

from tests.ui.base_page import BasePage
from urls import links


@allure.feature("Page Load")
@allure.story("Page loading and response checks")
class TestPageLoad:

    @allure.title("Page loads successfully: {url}")
    @pytest.mark.parametrize("url", [
        "https://www.whitehouse.gov/",
        "https://www.whitehouse.gov/news/",
        "https://www.whitehouse.gov/contact/",
        "https://www.whitehouse.gov/gallery/",
        "https://www.whitehouse.gov/live/",
    ])
    def test_page_loads(self, driver, url):
        page = BasePage(driver)
        page.open(url)

        with allure.step("Check page loaded"):
            title = driver.title
            assert title, f"Page title empty for {url}"
            allure.attach(title, name="title", attachment_type=allure.attachment_type.TEXT)

    @allure.title("Page has no console errors")
    @pytest.mark.parametrize("url", [
        "https://www.whitehouse.gov/",
        "https://www.whitehouse.gov/news/",
    ])
    def test_no_console_errors(self, driver, url):
        page = BasePage(driver)
        page.open(url)

        with allure.step("Check console"):
            logs = driver.get_log("browser")
            errors = [l for l in logs if l["level"] == "SEVERE"]
            assert len(errors) == 0, f"Console errors found: {errors}"

    @allure.title("Page source not empty")
    @pytest.mark.parametrize("url", [
        "https://www.whitehouse.gov/",
        "https://www.whitehouse.gov/news/",
    ])
    def test_page_source_not_empty(self, driver, url):
        page = BasePage(driver)
        page.open(url)

        with allure.step("Check page source"):
            source = driver.page_source
            assert len(source) > 1000, f"Page source too short for {url}"
