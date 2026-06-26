"""
login_modal.py — Page Object for the SPA Login modal.

The SPA at https://testauto.app/task-manager-spa has a Login button
that opens a modal with:
  - API selector (V1 / V2 / Buggy)
  - Username input
  - Password input
  - "test-user-fill" quick-fill button
  - Cancel button
  - Login button

Exercise 06 — Task 1 / Exercise 17:
See Exercises/06_AdvancedPOMPatterns.md and Exercises/17_AutoWaitingAndFlakiness.md
"""

from playwright.sync_api import Page, expect


class LoginModal:
    """Wraps the SPA login modal — opened by clicking the Login button in the navbar."""

    def __init__(self, page: Page):
        self.page  = page
        # Modal container — wait for it with expect() before interacting
        self._modal    = page.get_by_role("dialog")
        self._username = page.get_by_label("Username")
        self._password = page.get_by_label("Password")
        self._login_btn  = page.get_by_role("button", name="Login").last
        self._cancel_btn = page.get_by_role("button", name="Cancel")
        self._test_fill  = page.get_by_role("button", name="test-user-fill")
        self._api_select = page.get_by_role("combobox")   # V1 / V2 / Buggy selector

    def open(self):
        """Click the navbar Login button to open the modal."""
        self.page.get_by_role("button", name="Login").first.click()
        expect(self._modal).to_be_visible()

    def select_api(self, api: str):
        """
        Select which API backend to authenticate against.
        api: "V1" | "V2" | "Buggy"
        """
        self._api_select.select_option(label=api)

    def fill_credentials(self, username: str, password: str):
        """Fill username and password fields."""
        self._username.fill(username)
        self._password.fill(password)

    def fill_test_user(self):
        """Click the quick-fill button to populate default test credentials."""
        self._test_fill.click()

    def submit(self):
        """Click Login and wait for modal to close."""
        self._login_btn.click()
        expect(self._modal).not_to_be_visible()

    def cancel(self):
        """Dismiss the modal without logging in."""
        self._cancel_btn.click()
        expect(self._modal).not_to_be_visible()

    def login_as(self, username: str, password: str, api: str = "V2"):
        """Convenience: open modal, select API, fill creds, submit."""
        self.open()
        self.select_api(api)
        self.fill_credentials(username, password)
        self.submit()

    def login_as_test_user(self, api: str = "V2"):
        """Convenience: open modal, select API, use quick-fill, submit."""
        self.open()
        self.select_api(api)
        self.fill_test_user()
        self.submit()
