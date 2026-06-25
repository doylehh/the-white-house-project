import allure
import pytest

from ui.pages.navigation_page import NavigationPage
from urls import BASE_URL


@allure.feature("Navigation")
@allure.story("Page navigation tests")
class TestNavigation:

    @allure.title("Home page has correct title")
    def test_home_page_title(self, driver):
        page = NavigationPage(driver)
        page.open(BASE_URL)

        with allure.step("Check page title"):
            title = page.get_title()
            assert title, "Page title is empty"
            allure.attach(title, name="page_title", attachment_type=allure.attachment_type.TEXT)

    @allure.title("Home page has content")
    def test_home_page_has_content(self, driver):
        page = NavigationPage(driver)
        page.open(BASE_URL)

        with allure.step("Check page has text content"):
            source = driver.page_source
            assert "White House" in source or "whitehouse" in source, "Home page missing White House content"

    @allure.title("Navigation links are present")
    def test_nav_links_present(self, driver):
        page = NavigationPage(driver)
        page.open(BASE_URL)

        with allure.step("Check nav links count"):
            count = page.get_nav_links_count()
            assert count > 0, "No navigation links found"

    @allure.title("Logo links to home page")
    def test_logo_click(self, driver):
        page = NavigationPage(driver)
        page.open(BASE_URL + "/news/")

        with allure.step("Click logo"):
            page.click_logo()

        with allure.step("Verify home page"):
            assert driver.current_url.rstrip("/") == BASE_URL.rstrip("/"), \
                f"Not on home page: {driver.current_url}"

    @allure.title("News page navigation")
    def test_news_navigation(self, driver):
        page = NavigationPage(driver)
        page.open(BASE_URL)

        with allure.step("Click News link"):
            clicked = page.click_nav_link("News")
            assert clicked, "News link not found"

        with allure.step("Verify navigation"):
            assert "news" in driver.current_url.lower(), f"Not on news page: {driver.current_url}"

    @allure.title("Contact page navigation")
    def test_contact_navigation(self, driver):
        page = NavigationPage(driver)
        page.open(BASE_URL)

        with allure.step("Click Contact link"):
            clicked = page.click_nav_link("Contact")
            assert clicked, "Contact link not found"

        with allure.step("Verify navigation"):
            assert "contact" in driver.current_url.lower(), f"Not on contact page: {driver.current_url}"

    @allure.title("Gallery page navigation")
    def test_gallery_navigation(self, driver):
        page = NavigationPage(driver)
        page.open(BASE_URL)

        with allure.step("Click Gallery link"):
            clicked = page.click_nav_link("Gallery")
            assert clicked, "Gallery link not found"

        with allure.step("Verify navigation"):
            assert "gallery" in driver.current_url.lower(), f"Not on gallery page: {driver.current_url}"

    @allure.title("Skip to content link exists")
    def test_skip_link(self, driver):
        page = NavigationPage(driver)
        page.open(BASE_URL)

        with allure.step("Check skip link"):
            links = page.find_all((("css selector", "a[href='#wp--skip-link--target']")))
            assert len(links) > 0, "Skip to content link not found"
