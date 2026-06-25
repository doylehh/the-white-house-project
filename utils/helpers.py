import os
from datetime import datetime


def create_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def get_screenshot_path(name="screenshot"):
    return f"screenshots/{name}_{get_timestamp()}.png"
