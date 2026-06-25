import pytest
from config.settings import Settings, settings
from config.env import Env, env


class TestSettings:

    def test_settings_exists(self):
        assert settings is not None

    def test_base_url_default(self):
        s = Settings()
        assert s.BASE_URL.startswith("https://")

    def test_implicit_wait_is_int(self):
        s = Settings()
        assert isinstance(s.IMPLICIT_WAIT, int)

    def test_page_load_timeout_is_int(self):
        s = Settings()
        assert isinstance(s.PAGE_LOAD_TIMEOUT, int)

    def test_allure_results_dir(self):
        s = Settings()
        assert s.ALLURE_RESULTS_DIR


class TestEnv:

    def test_env_exists(self):
        assert env is not None

    def test_env_value(self):
        e = Env()
        assert e.ENV in ["prod", "staging", "dev", "test"]

    def test_chrome_options_is_dict(self):
        e = Env()
        assert isinstance(e.CHROME_OPTIONS, dict)

    def test_api_timeout_is_int(self):
        e = Env()
        assert isinstance(e.API_TIMEOUT, int)
