import pytest
from pages.elements import WebElement, ManyWebElements


class TestWebElement:

    def test_element_creation(self):
        el = WebElement()
        assert el is not None

    def test_element_timeout_default(self):
        el = WebElement()
        assert el._timeout == 10

    def test_element_timeout_custom(self):
        el = WebElement(timeout=20)
        assert el._timeout == 20

    def test_element_locator_from_kwargs(self):
        el = WebElement(xpath="//div")
        assert el._locator == ("xpath", "//div")

    def test_element_locator_css(self):
        el = WebElement(css_selector=".btn")
        assert el._locator == ("css selector", ".btn")

    def test_element_wait_after_click_default(self):
        el = WebElement()
        assert el._wait_after_click is False


class TestManyWebElements:

    def test_many_elements_creation(self):
        el = ManyWebElements()
        assert el is not None

    def test_set_value_raises(self):
        el = ManyWebElements()
        with pytest.raises(NotImplementedError):
            el._set_value(None, "test")

    def test_click_raises(self):
        el = ManyWebElements()
        with pytest.raises(NotImplementedError):
            el.click()
