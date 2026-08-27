import json
import logging
from pathlib import Path
from typing import Any

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from config.settings import settings
from test_framework.database import TestRunRepository
from test_framework.logging_config import configure_logging

logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]


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
    video = current_page.video
    current_page.set_default_timeout(settings.action_timeout_ms)
    current_page.set_default_navigation_timeout(settings.navigation_timeout_ms)
    yield current_page
    report = getattr(request.node, "rep_call", None)
    screenshot = current_page.screenshot(full_page=True)
    allure.attach(screenshot, "screenshot.png", allure.attachment_type.PNG)
    trace_path = ROOT / "test-results" / "traces" / f"{request.node.name}.zip"
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    context.tracing.stop(path=str(trace_path))
    allure.attach.file(str(trace_path), name="trace.zip", attachment_type=allure.attachment_type.ZIP)
    current_page.close()
    context.close()
    if video:
        allure.attach.file(video.path(), name="video.webm", attachment_type=allure.attachment_type.WEBM)


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
