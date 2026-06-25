import pytest
from tests.api.endpoints import Endpoints
from urls import BASE_URL


class TestEndpoints:

    def test_home_endpoint(self):
        assert Endpoints.HOME == BASE_URL

    def test_all_endpoints_start_with_base(self):
        endpoints = [
            Endpoints.HOME, Endpoints.NEWS, Endpoints.LIVE,
            Endpoints.CONTACT, Endpoints.INVESTMENTS, Endpoints.GALLERY,
            Endpoints.SAVE_AMERICA, Endpoints.RELEASES, Endpoints.FACT_SHEETS,
            Endpoints.PRESIDENTIAL_ACTIONS, Endpoints.EXECUTIVE_ORDERS,
            Endpoints.PROCLAMATIONS, Endpoints.ADMINISTRATION,
            Endpoints.REMARKS, Endpoints.BRIEFINGS, Endpoints.VIDEOS,
            Endpoints.WIRE, Endpoints.CRYPTO
        ]
        for ep in endpoints:
            assert ep.startswith(BASE_URL), f"Endpoint {ep} doesn't start with BASE_URL"

    def test_news_endpoint(self):
        assert "/news/" in Endpoints.NEWS

    def test_contact_endpoint(self):
        assert "/contact/" in Endpoints.CONTACT

    def test_gallery_endpoint(self):
        assert "/gallery/" in Endpoints.GALLERY
