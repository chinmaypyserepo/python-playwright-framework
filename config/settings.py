from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://automationintesting.online").rstrip("/")
    api_url: str = os.getenv("API_URL", os.getenv("BASE_URL", "https://automationintesting.online")).rstrip("/")
    headless: bool = _as_bool(os.getenv("HEADLESS", "true"))
    browser: str = os.getenv("BROWSER", "chromium").lower()
    slow_mo: int = int(os.getenv("SLOW_MO", "0"))
    action_timeout_ms: int = int(os.getenv("ACTION_TIMEOUT_MS", "15000"))
    navigation_timeout_ms: int = int(os.getenv("NAVIGATION_TIMEOUT_MS", "30000"))
    retries: int = int(os.getenv("RETRIES", "2"))
    db_path: Path = ROOT_DIR / os.getenv("DB_PATH", "test-results/test_runs.sqlite3")
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()

    def validate(self) -> None:
        if self.browser not in {"chromium", "firefox", "webkit"}:
            raise ValueError("BROWSER must be chromium, firefox, or webkit")
        if self.retries < 0:
            raise ValueError("RETRIES cannot be negative")


settings = Settings()
settings.validate()
