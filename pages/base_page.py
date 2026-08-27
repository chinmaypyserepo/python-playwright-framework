import logging
from contextlib import contextmanager
from collections.abc import Iterator

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def click_if_visible(self, selector: str) -> bool:
        try:
            self.page.locator(selector).first.click(timeout=3000)
            return True
        except PlaywrightTimeoutError:
            logger.debug("Optional element not visible: %s", selector)
            return False

    @contextmanager
    def handle_dialog(self, accept: bool = True, prompt_text: str | None = None) -> Iterator[None]:
        def on_dialog(dialog) -> None:
            logger.info("Browser dialog: %s", dialog.message)
            if not accept:
                dialog.dismiss()
            elif prompt_text is not None:
                dialog.accept(prompt_text)
            else:
                dialog.accept()

        self.page.once("dialog", on_dialog)
        yield

    def select_option(self, selector: str, value: str) -> None:
        self.page.locator(selector).select_option(value)
