import os


class Settings:
    BASE_URL = os.getenv("BASE_URL", "https://www.whitehouse.gov")
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    ALLURE_RESULTS_DIR = os.getenv("ALLURE_RESULTS_DIR", "allure-results")
    SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "screenshots")


settings = Settings()
