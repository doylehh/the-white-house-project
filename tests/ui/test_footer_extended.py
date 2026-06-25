import allure

from ui.pages.footer_page import FooterPage
from urls import BASE_URL


@allure.feature("Footer Extended")
@allure.story("Footer content and links")
class TestFooterExtended:

    @allure.title("Footer has multiple link sections")
    def test_footer_has_links(self, driver):
        page = FooterPage(driver)
        page.open(BASE_URL)

        with allure.step("Check footer links"):
            links = page.get_footer_links()
            assert len(links) > 5, f"Expected >5 footer links, got {len(links)}"

    @allure.title("Footer links are not empty strings")
    def test_footer_links_not_empty(self, driver):
        page = FooterPage(driver)
        page.open(BASE_URL)

        with allure.step("Check each link text"):
            links = page.get_footer_links()
            for link in links:
                assert link.strip(), f"Empty footer link found"

    @allure.title("Footer has navigation content")
    def test_footer_navigation_content(self, driver):
        page = FooterPage(driver)
        page.open(BASE_URL)

        with allure.step("Check footer has content"):
            links = page.get_footer_links()
            assert len(links) > 3, f"Expected >3 footer links, got {len(links)}"

    @allure.title("Footer visible on page")
    def test_footer_visible(self, driver):
        page = FooterPage(driver)
        page.open(BASE_URL)

        with allure.step("Scroll to footer"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        with allure.step("Check footer elements"):
            links = page.get_footer_links()
            assert len(links) > 0, "Footer not visible or empty"
