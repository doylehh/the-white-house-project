import allure
from ui.pages.header_page import HeaderPage
from urls import BASE_URL

def test_header_clickable(driver):
    page = HeaderPage(driver)
    page.open(BASE_URL)

    for locator, name in page.get_all_header_elements():
        with allure.step(f"Проверка кликабельности: {name}"):
            element = page.find(locator)
            assert element.is_displayed(), f"{name} не отображается"
            assert element.is_enabled(), f"{name} не кликабелен"
