import sqlite3
from datetime import UTC, datetime
from pathlib import Path


class TestRunRepository:
    def __init__(self, database_path: Path):
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _initialize(self) -> None:
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS test_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    browser TEXT NOT NULL,
                    recorded_at TEXT NOT NULL
                )"""
            )

    def record(self, test_name: str, status: str, browser: str) -> None:
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                "INSERT INTO test_runs(test_name, status, browser, recorded_at) VALUES (?, ?, ?, ?)",
                (test_name, status, browser, datetime.now(UTC).isoformat()),
            )
