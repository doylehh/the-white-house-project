import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.settings import settings
from config.env import env


@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()

    if env.CHROME_OPTIONS["headless"]:
        chrome_options.add_argument("--headless=new")

    window_size = env.CHROME_OPTIONS["window_size"]
    chrome_options.add_argument(f"--window-size={window_size}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(settings.IMPLICIT_WAIT)

    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )
