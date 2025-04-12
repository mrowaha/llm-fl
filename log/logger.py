import logging
import sys
from typing import Optional


class Logger:
    _instance = None

    def __init__(self, logger_name: str):
        self._initialize_logger(logger_name)

    def _initialize_logger(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )

            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            # can add file handler here if needed
            # file_handler = logging.FileHandler('application.log')
            # file_handler.setFormatter(formatter)
            # self.logger.addHandler(file_handler)

    def configure(self,
                  *,
                  level: int = logging.DEBUG,
                  logging_formatter: Optional[logging.Formatter] = None,
                  file_path: Optional[str] = None) -> "Logger":
        self.logger.setLevel(level)
        formatter = logging_formatter or logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Clear existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Add console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Add file handler if path provided
        if file_path:
            file_handler = logging.FileHandler(file_path)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        return self

    def get_logger(self) -> logging.Logger:
        """Get the logger instance"""
        return self.logger
