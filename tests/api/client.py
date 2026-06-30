import requests

from config.settings import settings


class ApiClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or settings.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })

    def request(self, method, endpoint="", **kwargs):
        url = f"{self.base_url}{endpoint}"
        return self.session.request(method, url, timeout=kwargs.pop("timeout", 30), **kwargs)

    def get(self, endpoint="", **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint="", **kwargs):
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint="", **kwargs):
        return self.request("PUT", endpoint, **kwargs)

    def patch(self, endpoint="", **kwargs):
        return self.request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint="", **kwargs):
        return self.request("DELETE", endpoint, **kwargs)

    def head(self, endpoint="", **kwargs):
        return self.request("HEAD", endpoint, **kwargs)

    def options(self, endpoint="", **kwargs):
        return self.request("OPTIONS", endpoint, **kwargs)

    def close(self):
        self.session.close()
