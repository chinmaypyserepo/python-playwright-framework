import allure
import pytest
from playwright.sync_api import expect

from config.settings import settings
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.smoke
@allure.title("Home page is reachable")
def test_home_page_loads(page):
    page.goto(settings.base_url, wait_until="domcontentloaded")
    assert "restful-booker-platform" in page.title().lower()


@pytest.mark.ui
@allure.title("User can submit the contact form")
def test_contact_form_submission(page, test_data):
    page.goto(settings.base_url, wait_until="domcontentloaded")
    HomePage(page).submit_contact_form(**test_data["valid"])
    expect(page.locator("body")).to_contain_text("Thanks for getting in touch", timeout=10000)


@pytest.mark.ui
@allure.title("Guest can navigate the availability date picker")
def test_availability_date_picker_supports_month_navigation(page):
    page.goto(settings.base_url, wait_until="domcontentloaded")
    home = HomePage(page)
    home.open_check_in_date_picker()
    expect(home.date_picker).to_be_visible()
    current_month = home.date_picker.get_by_role("heading", level=2)
    original_month = current_month.inner_text()
    home.move_to_next_month()
    expect(current_month).not_to_have_text(original_month)


@pytest.mark.ui
@allure.title("Contact form displays server-side validation errors")
def test_contact_form_validation(page):
    page.goto(settings.base_url, wait_until="domcontentloaded")
    HomePage(page).submit_button.click()
    expect(page.locator("body")).to_contain_text("Email may not be blank", timeout=10000)
