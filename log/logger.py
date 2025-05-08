import logging
import sys
from typing import Optional


class Logger:

    def __init__(self, logger_name: str):
        self._initialize_logger(logger_name)

    def _initialize_logger(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            # formatter = logging.Formatter(
            #     '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            # )
            # console_handler.setFormatter(formatter)

            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            self.logger.addHandler(console_handler)

            # can add file handler here if needed
            # file_handler = logging.FileHandler('fault_localization.log')
            # file_handler.setFormatter(formatter)
            # self.logger.addHandler(file_handler)

    def configure(self,
                  *,
                  level: int = logging.DEBUG,
                  logging_formatter: Optional[logging.Formatter] = None,
                  file_path: Optional[str] = None,
                  stdout: bool = True,
                  ) -> "Logger":
        self.logger.setLevel(level)

        # Clear existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Add console handler
        if stdout:
            console_handler = logging.StreamHandler(sys.stdout)
            if logging_formatter:
                console_handler.setFormatter(logging_formatter)
            self.logger.addHandler(console_handler)

        # Add file handler if path provided
        if file_path:
            file_handler = logging.FileHandler(file_path)
            self.logger.addHandler(file_handler)
        return self

    def get_logger(self) -> logging.Logger:
        """Get the logger instance"""
        return self.logger
