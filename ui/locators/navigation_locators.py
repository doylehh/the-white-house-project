from selenium.webdriver.common.by import By


class NavigationLocators:
    LOGO = (By.CSS_SELECTOR, "a.wp-block-whitehouse-header__logo, .site-logo a, header a[href='/']")
    MENU_TOGGLE = (By.CSS_SELECTOR, ".wp-block-whitehouse-header__menu-toggle button, button[aria-label='Menu']")
    SEARCH_TOGGLE = (By.CSS_SELECTOR, ".wp-block-whitehouse-header__search-toggle button, button[aria-label='Search']")
    NAV_LINKS = (By.CSS_SELECTOR, "#menu-primary-navigation a, nav a")
    PAGE_TITLE = (By.TAG_NAME, "title")
    H1 = (By.TAG_NAME, "h1")
    SKIP_LINK = (By.CSS_SELECTOR, "a[href='#wp--skip-link--target']")
