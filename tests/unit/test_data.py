import pytest
from data.test_data import TestData


class TestTestData:

    def test_header_locators_exist(self):
        assert TestData.HEADER_LOCATORS is not None

    def test_header_locators_has_news(self):
        assert "news" in TestData.HEADER_LOCATORS

    def test_header_locators_has_gallery(self):
        assert "gallery" in TestData.HEADER_LOCATORS

    def test_header_locators_has_contact(self):
        assert "contact" in TestData.HEADER_LOCATORS

    def test_footer_links_selector(self):
        assert TestData.FOOTER_LINKS_SELECTOR

    def test_copyright_selector(self):
        assert TestData.COPYRIGHT_SELECTOR

    def test_expected_status_code(self):
        assert TestData.EXPECTED_STATUS_CODE == 200
