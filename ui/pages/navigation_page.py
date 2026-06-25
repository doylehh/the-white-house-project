from tests.ui.base_page import BasePage
from ui.locators.navigation_locators import NavigationLocators
from utils.logger import logger


class NavigationPage(BasePage):

    def get_title(self):
        logger.info("Getting page title")
        return self.driver.title

    def get_h1_text(self):
        logger.info("Getting H1 text")
        try:
            return self.find(NavigationLocators.H1).text
        except Exception:
            return ""

    def click_logo(self):
        logger.info("Clicking logo")
        logo = self.find(NavigationLocators.LOGO)
        logo.click()

    def get_nav_links_count(self):
        logger.info("Counting navigation links")
        return len(self.find_all(NavigationLocators.NAV_LINKS))

    def get_nav_links_text(self):
        logger.info("Getting navigation links text")
        links = self.find_all(NavigationLocators.NAV_LINKS)
        return [link.text.strip() for link in links if link.text.strip()]

    def click_nav_link(self, text):
        logger.info(f"Clicking nav link: {text}")
        links = self.find_all(NavigationLocators.NAV_LINKS)
        for link in links:
            if link.text.strip().lower() == text.lower():
                link.click()
                return True
        return False

    def is_menu_toggle_visible(self):
        logger.info("Checking menu toggle visibility")
        try:
            el = self.find(NavigationLocators.MENU_TOGGLE)
            return el.is_displayed()
        except Exception:
            return False

    def click_menu_toggle(self):
        logger.info("Clicking menu toggle")
        el = self.find(NavigationLocators.MENU_TOGGLE)
        el.click()

    def is_search_toggle_visible(self):
        logger.info("Checking search toggle visibility")
        try:
            el = self.find(NavigationLocators.SEARCH_TOGGLE)
            return el.is_displayed()
        except Exception:
            return False

    def click_search_toggle(self):
        logger.info("Clicking search toggle")
        el = self.find(NavigationLocators.SEARCH_TOGGLE)
        el.click()
