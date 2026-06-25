import pytest
from urls import BASE_URL, links


class TestUrls:

    def test_base_url_is_string(self):
        assert isinstance(BASE_URL, str)

    def test_base_url_starts_with_https(self):
        assert BASE_URL.startswith("https://")

    def test_base_url_ends_without_slash(self):
        assert not BASE_URL.endswith("/")

    def test_links_is_list(self):
        assert isinstance(links, list)

    def test_links_not_empty(self):
        assert len(links) > 0

    def test_all_links_are_strings(self):
        for link in links:
            assert isinstance(link, str), f"Link is not a string: {link}"

    def test_all_links_start_with_base_url(self):
        for link in links:
            assert link.startswith(BASE_URL), f"Link doesn't start with BASE_URL: {link}"

    def test_all_links_are_https(self):
        for link in links:
            assert link.startswith("https://"), f"Link is not HTTPS: {link}"

    def test_no_duplicate_links(self):
        assert len(links) == len(set(links)), "Duplicate links found in urls.py"

    def test_home_page_in_links(self):
        assert BASE_URL + "/" in links
