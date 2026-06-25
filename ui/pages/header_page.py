from tests.ui.base_page import BasePage
from ui.locators.header_locators import HeaderLocators

class HeaderPage(BasePage):

    def get_all_header_elements(self):
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
