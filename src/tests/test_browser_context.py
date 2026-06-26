"""
test_browser_context.py — Exercise 01: Browser & Context Management

See Exercises/01_BrowserContextManagement.md for full instructions.
Run: pytest src/tests/test_browser_context.py -v --headed
"""
import pytest
from playwright.sync_api import Browser, Page, expect


def test_two_contexts_are_independent(browser: Browser):
    # TODO Task 1: create two contexts, navigate both, assert independence
    pass


def test_save_and_restore_auth_state(browser: Browser, tmp_path):
    # TODO Task 2: save storage state, restore in new context, assert task manager loads
    pass


def test_multiple_viewport_screenshots(browser: Browser):
    # TODO Task 3: desktop 1440x900, tablet 768x1024, mobile 390x844 screenshots
    pass


def test_two_users_simultaneously(browser: Browser, api_v1):
    # TODO Task 4: user A creates via API, user B finds it in the browser
    pass


def test_context_with_custom_headers(browser: Browser):
    # TODO Task 5: locale, timezone, extra_http_headers — assert page loads without error
    pass
