from conftest import driver
from locators.main_locators import MainPage


def test_whitehouse(driver):
    page = MainPage(driver)
    page.btn_news.click()

