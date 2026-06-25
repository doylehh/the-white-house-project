from tests.ui.base_page import BasePage
from ui.locators.footer_locators import FooterLocators
from utils.logger import logger


class FooterPage(BasePage):

    def get_footer_links(self):
        logger.info("Collecting footer links")
        elements = self.find_all(FooterLocators.FOOTER_LINKS)
        return [el.text.strip() for el in elements if el.text.strip() != ""]

    def click_footer_link(self, name):
        logger.info(f"Clicking footer link: {name}")
        links = self.find_all(FooterLocators.FOOTER_LINKS)
        for link in links:
            if link.text.strip().lower() == name.lower():
                link.click()
                logger.info(f"Clicked footer link: {name}")
                return True
        logger.warning(f"Footer link not found: {name}")
        return False

    def get_copyright(self):
        logger.info("Getting copyright text")
        return self.get_text(FooterLocators.COPYRIGHT)
