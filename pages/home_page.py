from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.book_now_link = page.get_by_role("link", name="Book Now")
        self.contact_name = page.locator("#name")
        self.contact_email = page.locator("#email")
        self.contact_phone = page.locator("#phone")
        self.contact_subject = page.locator("#subject")
        self.contact_message = page.locator("#description")
        self.submit_button = page.get_by_role("button", name="Submit")
        self.check_in = page.locator("form").first.locator("input").nth(0)
        self.check_out = page.locator("form").first.locator("input").nth(1)
        self.check_availability_button = page.get_by_role("button", name="Check Availability")
        self.date_picker = page.locator(".react-datepicker")

    def submit_contact_form(self, name: str, email: str, phone: str, subject: str, message: str) -> None:
        self.contact_name.fill(name)
        self.contact_email.fill(email)
        self.contact_phone.fill(phone)
        self.contact_subject.fill(subject)
        self.contact_message.fill(message)
        self.submit_button.click()

    def open_check_in_date_picker(self) -> None:
        self.check_in.click()

    def move_to_next_month(self) -> None:
        self.date_picker.get_by_role("button", name="Next Month").click()

    def check_availability(self) -> None:
        self.check_availability_button.click()
