"""
test_multi_user.py — Exercise 14: Multi-User & Role-Based Testing

See Exercises/14_MultiUserAndRoleBasedTesting.md for full instructions.
Run: pytest src/tests/test_multi_user.py -v -s
"""
import json
from playwright.sync_api import Playwright, Browser

API_V2 = "https://api.testauto.app/api/v2"


def test_document_access_permissions(playwright: Playwright):
    # TODO Task 1 — table of what admin and user can do
    pass


def test_admin_creates_user_reads(playwright: Playwright):
    # TODO Task 2
    pass


def test_concurrent_creation(playwright: Playwright):
    # TODO Task 3
    pass


def test_permission_boundary(playwright: Playwright):
    # TODO Task 4
    pass


def test_two_browser_sessions(browser: Browser):
    # TODO Task 5 — two contexts, two screenshots
    pass
