class TestData:
    HEADER_LOCATORS = {
        "news": ("xpath", "//a[contains(text(), 'News')]"),
        "gallery": ("xpath", "//a[contains(text(), 'Gallery')]"),
        "contact": ("xpath", "//a[contains(text(), 'Contact')]"),
    }

    FOOTER_LINKS_SELECTOR = "footer a"
    COPYRIGHT_SELECTOR = "footer .copyright"

    EXPECTED_STATUS_CODE = 200
