from selenium.webdriver.common.by import By

class HeaderLocators:
    MENU_BUTTON = (By.XPATH, "//div[@class='wp-block-whitehouse-header__menu-toggle']//button")
    LOGO = (By.XPATH, "//a[@class='wp-block-whitehouse-header__logo']")
    SEARCH_BUTTON = (By.XPATH, "//div[@class='wp-block-whitehouse-header__search-toggle']//button")

    NEWS = (By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'News')]")
    GALLERY = (By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'Gallery')]")
    LIVESTREAM = (By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'Livestream')]")
    TRUMP_ACCOUNTS = (By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'Trump Accounts')]")
    SAVE_AMERICA = (By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'SAVE America')]")
    INVESTMENTS = (By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'Investments')]")
    CONTACT = (By.XPATH, "//ul[@id='menu-primary-navigation']//a[contains(text(), 'Contact')]")
