from django.test import TestCase
from core.utils.logger import get_logger
from pythonjsonlogger import jsonlogger
import logging


class LoggerUtilityTests(TestCase):

    def test_logger_configuration(self):
        logger_name = "TestLogger"
        logger = get_logger(logger_name)

        # ✅ Check logger is returned with correct name
        self.assertEqual(logger.name, logger_name)

        # ✅ Ensure logger has one handler
        self.assertEqual(len(logger.handlers), 1)

        # ✅ Handler should be a StreamHandler
        handler = logger.handlers[0]
        self.assertIsInstance(handler, logging.StreamHandler)

        # ✅ Formatter should be an instance of jsonlogger.JsonFormatter
        formatter = handler.formatter
        self.assertIsInstance(formatter, jsonlogger.JsonFormatter)

        # ✅ Check emoji/unicode support
        log_output = formatter.format(logging.LogRecord(
            name=logger_name,
            level=logging.INFO,
            pathname="test_logger.py",
            lineno=42,
            msg="Test 🧪 emoji",
            args=(),
            exc_info=None
        ))
        self.assertIn("🧪", log_output)
