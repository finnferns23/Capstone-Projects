"""Central logging configuration for the Content Assistant project."""
from __future__ import annotations

import logging
import os


def configure_logging() -> None:
    """Configure application-wide logging once, with environment override support."""
    level_name = os.getenv("CONTENT_ASSISTANT_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger for a module."""
    configure_logging()
    return logging.getLogger(name)
