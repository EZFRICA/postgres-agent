"""
Enhanced logging configuration with centralized settings.
"""

import logging
import sys
import os
from typing import Optional


class LoggingConfig:
    """Centralized logging configuration for PostgreSQL DBA Multi-Agent"""

    # Log levels mapping
    LOG_LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    # Default configuration
    DEFAULT_LEVEL = "INFO"
    DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @classmethod
    def get_log_level(cls, level_name: Optional[str] = None) -> int:
        """
        Get log level from environment or parameter.

        Args:
            level_name: Optional log level name override

        Returns:
            Log level integer
        """
        if level_name is None:
            level_name = os.getenv("LOG_LEVEL", cls.DEFAULT_LEVEL)

        return cls.LOG_LEVELS.get(level_name.upper(), logging.INFO)

    @classmethod
    def get_log_format(cls) -> str:
        """
        Get log format from environment or default.

        Returns:
            Log format string
        """
        return os.getenv("LOG_FORMAT", cls.DEFAULT_FORMAT)


def initialize_logging(level: Optional[str] = None, logger_name: Optional[str] = None):
    """
    Initialize logging with configuration from settings.

    Args:
        level: Optional log level override
        logger_name: Optional logger name (defaults to __name__)

    Returns:
        Logger instance
    """
    # Get log level
    log_level = LoggingConfig.get_log_level(level)

    # Configure logging format
    formatter = logging.Formatter(LoggingConfig.get_log_format())

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Add handler to root logger
    root_logger.addHandler(console_handler)

    # Configure specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("toolbox_core").setLevel(logging.INFO)

    # Return specific logger or root logger
    if logger_name:
        return logging.getLogger(logger_name)
    return logging.getLogger(__name__)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Initialize default logger
logger = initialize_logging()
