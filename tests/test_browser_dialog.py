import allure
import pytest

from pages.base_page import BasePage


@pytest.mark.ui
@allure.title("Framework can accept a native browser alert")
def test_native_alert_handler(page):
    base_page = BasePage(page)
    with base_page.handle_dialog():
        page.evaluate("alert('Playwright handled this alert')")
