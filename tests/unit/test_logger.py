import pytest
import logging
from utils.logger import logger


class TestLogger:

    def test_logger_exists(self):
        assert logger is not None

    def test_logger_has_handlers_or_level(self):
        root = logging.getLogger()
        assert len(root.handlers) > 0 or logger.level >= logging.INFO

    def test_logger_name(self):
        assert logger.name is not None

    def test_logger_info_does_not_raise(self):
        try:
            logger.info("Test message")
        except Exception as e:
            pytest.fail(f"logger.info raised {e}")

    def test_logger_warning_does_not_raise(self):
        try:
            logger.warning("Test warning")
        except Exception as e:
            pytest.fail(f"logger.warning raised {e}")

    def test_logger_error_does_not_raise(self):
        try:
            logger.error("Test error")
        except Exception as e:
            pytest.fail(f"logger.error raised {e}")
