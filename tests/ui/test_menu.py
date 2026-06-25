import allure

from ui.pages.navigation_page import NavigationPage
from urls import BASE_URL


@allure.feature("Menu")
@allure.story("Menu toggle and navigation")
class TestMenu:

    @allure.title("Menu toggle is visible")
    def test_menu_toggle_visible(self, driver):
        page = NavigationPage(driver)
        page.open(BASE_URL)

        with allure.step("Check menu toggle"):
            visible = page.is_menu_toggle_visible()
            assert visible, "Menu toggle button not visible"

    @allure.title("Menu toggle opens menu")
    def test_menu_toggle_click(self, driver):
        page = NavigationPage(driver)
        page.open(BASE_URL)

        with allure.step("Click menu toggle"):
            page.click_menu_toggle()

    @allure.title("Search toggle is visible")
    def test_search_toggle_visible(self, driver):
        page = NavigationPage(driver)
        page.open(BASE_URL)

        with allure.step("Check search toggle"):
            visible = page.is_search_toggle_visible()
            assert visible, "Search toggle button not visible"

    @allure.title("Search toggle opens search")
    def test_search_toggle_click(self, driver):
        page = NavigationPage(driver)
        page.open(BASE_URL)

        with allure.step("Click search toggle"):
            page.click_search_toggle()
