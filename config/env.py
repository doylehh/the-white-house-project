import os


class Env:
    ENV = os.getenv("TEST_ENV", "prod")

    CHROME_OPTIONS = {
        "headless": os.getenv("HEADLESS", "false").lower() == "true",
        "window_size": os.getenv("WINDOW_SIZE", "1920,1080"),
    }

    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))


env = Env()
