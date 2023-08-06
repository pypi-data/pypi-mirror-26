# coding: utf-8


import unittest


class TestConfigLogger(unittest.TestCase):
    def setUp(self):
        import mte.logger
        self.AXUI_logger = mte.logger

    def test_valid_config(self):
        valid_configs = {"logger_name": "TestConfigLogger",
                         "logging_level_file": "DEBUG",
                         "logging_level_stream": "DEBUG",
                         "logging_stream": "stdout",
                         "logging_file": "test_config_logger.log",
                         "file_logging_mode": "a",
                         "formatter": "%(message)s",
                         "color_enable": "True"}

        self.AXUI_logger.config(valid_configs)
        logger = self.AXUI_logger.LOGGER()
        self.assertTrue(logger)
        self.assertEqual(logger.name, valid_configs["logger_name"])


class TestLogger(unittest.TestCase):
    def setUp(self):
        import AXUI.logger
        self.AXUI_logger = AXUI.logger
        valid_configs = {"logger_name": "TestLogger",
                         "logging_level_file": "DEBUG",
                         "logging_level_stream": "DEBUG",
                         "logging_stream": "stdout",
                         "logging_file": "test_logger.log",
                         "file_logging_mode": "a",
                         "formatter": "%(message)s",
                         "color_enable": "True"}

        self.AXUI_logger.config(valid_configs)
        self.logger = self.AXUI_logger.LOGGER()

    def test_logger(self):
        self.logger.debug("test debug")
        self.logger.info("test info")
        self.logger.warn("test warn")
        self.logger.error("test error")
        self.logger.critical("test critical")



