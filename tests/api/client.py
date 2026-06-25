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

    def get(self, endpoint="", **kwargs):
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, timeout=kwargs.pop("timeout", 30), **kwargs)

    def post(self, endpoint="", **kwargs):
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, timeout=kwargs.pop("timeout", 30), **kwargs)

    def close(self):
        self.session.close()
