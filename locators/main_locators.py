import os
from pages.elements import WebElement, ManyWebElements
from pages.base_page import WebPage


class MainPage(WebPage):
    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("MAIN_PAGE") or 'https://www.whitehouse.gov/'

        super().__init__(web_driver, url)

    btn_news = WebElement(xpath='(//*[@class="menu-item menu-item-type-post_type menu-item-object-page menu-item-37"])')
