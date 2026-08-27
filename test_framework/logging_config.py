import logging
from pathlib import Path

from config.settings import settings


def configure_logging() -> None:
    Path("test-results").mkdir(exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, settings.log_level, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("test-results/test.log", encoding="utf-8"),
        ],
        force=True,
    )

