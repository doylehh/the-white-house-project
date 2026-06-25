from tests.ui.base_page import BasePage
from ui.locators.footer_locators import FooterLocators

class FooterPage(BasePage):

    def get_footer_links(self):
        elements = self.find_all(FooterLocators.FOOTER_LINKS)
        return [el.text.strip() for el in elements if el.text.strip() != ""]

    def click_footer_link(self, name):
        links = self.find_all(FooterLocators.FOOTER_LINKS)
        for link in links:
            if link.text.strip().lower() == name.lower():
                link.click()
                return True
        return False

    def get_copyright(self):
        return self.get_text(FooterLocators.COPYRIGHT)
