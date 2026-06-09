import allure
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from urls import BASE_URL


def test_header_clickable(driver):
    driver.get(BASE_URL)

    elements = [
        (driver.find_element(By.XPATH, "//div[@class='wp-block-whitehouse-header__menu-toggle']//button"), "Menu"),
        (driver.find_element(By.XPATH, "//a[@class='wp-block-whitehouse-header__logo']"), "Logo"),
        (driver.find_element(By.XPATH, "//div[@class='wp-block-whitehouse-header__search-toggle']//button"), "Search"),
        (driver.find_element(By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'News')]"), "News"),
        (driver.find_element(By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'Gallery')]"), "Gallery"),
        (driver.find_element(By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'Livestream')]"), "Livestream"),
        (driver.find_element(By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'Trump Accounts')]"), "Trump Accounts"),
        (driver.find_element(By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'SAVE America')]"), "Save America"),
        (driver.find_element(By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'Investments')]"), "Investments"),
        (driver.find_element(By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'Contact')]"), "Contact"),
    ]

    for element, name in elements:
        with allure.step(f"Проверка кликабельности: {name}"):
            assert element.is_displayed(), f"{name} не отображается"
            assert element.is_enabled(), f"{name} не кликабелен"
