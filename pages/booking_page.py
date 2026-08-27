from playwright.sync_api import Page

from pages.base_page import BasePage


class BookingPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name = page.locator("#firstname")
        self.last_name = page.locator("#lastname")
        self.email = page.locator("#email")
        self.phone = page.locator("#phone")
        self.reserve_button = page.get_by_role("button", name="Reserve Now")

    def fill_guest_details(self, first_name: str, last_name: str, email: str, phone: str) -> None:
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.email.fill(email)
        self.phone.fill(phone)

