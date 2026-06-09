# from selenium.webdriver.common.by import By
#
#
# class HeaderPage:
#     MENU_BUTTON = (By.XPATH, "//div[@class='wp-block-whitehouse-header__menu-toggle']//button")
#
#     LOGO = (By.XPATH, "//a[@class='wp-block-whitehouse-header__logo']")
#
#     SEARCH_BUTTON = (By.XPATH, "//div[@class='wp-block-whitehouse-header__search-toggle']//button")
#
#     NEWS = (By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'News')]")
#     GALLERY = (By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'Gallery')]")
#     LIVESTREAM = (By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'Livestream')]")
#     TRUMP_ACCOUNTS = (By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'Trump Accounts')]")
#     SAVE_AMERICA = (By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'SAVE America')]")
#     INVESTMENTS = (By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'Investments')]")
#     CONTACT = (By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'Contact')]")
#
#     def __init__(self, driver):
#         self.driver = driver
#
#     def get_header_elements(self):
#         return [
#             self.driver.find_element(*self.MENU_BUTTON),
#             self.driver.find_element(*self.LOGO),
#             self.driver.find_element(*self.SEARCH_BUTTON),
#             self.driver.find_element(*self.NEWS),
#             self.driver.find_element(*self.GALLERY),
#             self.driver.find_element(*self.LIVESTREAM),
#             self.driver.find_element(*self.TRUMP_ACCOUNTS),
#             self.driver.find_element(*self.SAVE_AMERICA),
#             self.driver.find_element(*self.INVESTMENTS),
#             self.driver.find_element(*self.CONTACT),
#         ]
