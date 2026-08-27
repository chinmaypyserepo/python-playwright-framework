import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from config.settings import settings
from test_framework.database import TestRunRepository
from test_framework.logging_config import configure_logging

logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parent


def pytest_configure() -> None:
    configure_logging()


@pytest.fixture(scope="session")
def test_data() -> dict[str, Any]:
    with (ROOT / "data" / "contact.json").open(encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture(scope="session")
def rooms_data() -> dict[str, Any]:
    with (ROOT / "data" / "rooms.json").open(encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def runtime_contact_data() -> dict[str, str]:
    runtime_data = {
        "name": "Runtime Playwright Test",
        "email": f"playwright-{uuid4().hex[:8]}@example.com",
        "phone": "01234567890",
        "subject": f"Runtime capture {datetime.now(timezone.utc):%Y%m%d%H%M%S}",
        "message": "Captured during the test run and used in the contact form.",
    }
    allure.attach(
        json.dumps(runtime_data, indent=2),
        name="runtime-contact-data.json",
        attachment_type=allure.attachment_type.JSON,
    )
    return runtime_data


@pytest.fixture(scope="session")
def run_repository() -> TestRunRepository:
    return TestRunRepository(settings.db_path)


@pytest.fixture
def context(browser: Browser) -> BrowserContext:
    return browser.new_context(
        record_video_dir="test-results/videos",
        viewport={"width": 1440, "height": 900},
    )


@pytest.fixture
def page(context: BrowserContext, request: pytest.FixtureRequest) -> Page:
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    current_page = context.new_page()
    current_page.set_default_timeout(settings.action_timeout_ms)
    current_page.set_default_navigation_timeout(settings.navigation_timeout_ms)
    yield current_page

    screenshot = current_page.screenshot(full_page=True)
    allure.attach(screenshot, "screenshot.png", allure.attachment_type.PNG)
    trace_path = ROOT / "test-results" / "traces" / f"{request.node.name}.zip"
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    context.tracing.stop(path=str(trace_path))
    allure.attach.file(str(trace_path), name="trace.zip", attachment_type=allure.attachment_type.ZIP)
    current_page.close()
    context.close()
    if current_page.video:
        allure.attach.file(
            current_page.video.path(),
            name="video.webm",
            attachment_type=allure.attachment_type.WEBM,
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[Any]):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
    if report.when == "call":
        browser = item.config.getoption("--browser") or settings.browser
        repository = item.funcargs.get("run_repository")
        if repository:
            repository.record(item.nodeid, report.outcome, browser)


@pytest.fixture(scope="session")
def browser_type_launch_args() -> dict[str, Any]:
    return {"headless": settings.headless, "slow_mo": settings.slow_mo}
