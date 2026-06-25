import pytest
import os
from utils.helpers import create_dir, get_timestamp, get_screenshot_path


class TestHelpers:

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        self.test_dir = tmp_path

    def test_create_dir_creates_directory(self):
        path = os.path.join(str(self.test_dir), "new_dir")
        result = create_dir(path)
        assert os.path.isdir(result)

    def test_create_dir_existing_directory(self):
        path = os.path.join(str(self.test_dir), "existing")
        os.makedirs(path)
        result = create_dir(path)
        assert os.path.isdir(result)

    def test_create_dir_nested(self):
        path = os.path.join(str(self.test_dir), "a", "b", "c")
        result = create_dir(path)
        assert os.path.isdir(result)

    def test_get_timestamp_format(self):
        ts = get_timestamp()
        assert len(ts) == 19
        assert ts[4] == "-"
        assert ts[7] == "-"
        assert ts[10] == "_"
        assert ts[13] == "-"

    def test_get_screenshot_path_contains_name(self):
        path = get_screenshot_path("my_test")
        assert "my_test" in path
        assert path.startswith("screenshots/")

    def test_get_screenshot_path_default_name(self):
        path = get_screenshot_path()
        assert "screenshot" in path
