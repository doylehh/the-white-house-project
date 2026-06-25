from tests.ui.base_page import BasePage
from ui.locators.header_locators import HeaderLocators
from utils.logger import logger


class HeaderPage(BasePage):

    def get_all_header_elements(self):
        logger.info("Collecting all header elements")
        return [
            (HeaderLocators.MENU_BUTTON, "Menu"),
            (HeaderLocators.LOGO, "Logo"),
            (HeaderLocators.SEARCH_BUTTON, "Search"),
            (HeaderLocators.NEWS, "News"),
            (HeaderLocators.GALLERY, "Gallery"),
            (HeaderLocators.LIVESTREAM, "Livestream"),
            (HeaderLocators.TRUMP_ACCOUNTS, "Trump Accounts"),
            (HeaderLocators.SAVE_AMERICA, "Save America"),
            (HeaderLocators.INVESTMENTS, "Investments"),
            (HeaderLocators.CONTACT, "Contact"),
        ]

    def click_header_element(self, name):
        logger.info(f"Clicking header element: {name}")
        for locator, text in self.get_all_header_elements():
            if text.lower() == name.lower():
                element = self.find(locator)
                element.click()
                logger.info(f"Clicked header element: {name}")
                return True
        logger.warning(f"Header element not found: {name}")
        return False
