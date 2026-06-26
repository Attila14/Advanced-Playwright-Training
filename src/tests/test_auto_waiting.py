"""
test_auto_waiting.py — Exercise 17: Auto-waiting & Flakiness Prevention

Replaces networkidle / time.sleep() with web-first expect() assertions.

See Exercises/17_AutoWaitingAndFlakiness.md for full instructions.
Run: pytest src/tests/test_auto_waiting.py -v --headed
"""

import pytest
from playwright.sync_api import Page, APIRequestContext, expect

SPA_URL = "https://testauto.app/task-manager-spa"


# ---------------------------------------------------------------------------
# Task 1 — Replace networkidle with web-first assertions
# ---------------------------------------------------------------------------

def test_task_list_loads(page: Page):
    """
    Navigate to the SPA and assert the task table loads.
    No networkidle, no time.sleep() — only expect().
    """
    # TODO:
    # 1. page.goto(SPA_URL)
    # 2. expect(page.locator("table tbody tr").first).to_be_visible()
    # 3. assert page.locator("table tbody tr").count() > 0
    pass


# ---------------------------------------------------------------------------
# Task 2 — Wait for modal open and close
# ---------------------------------------------------------------------------

def test_login_modal_open_close(page: Page):
    """
    Open the Login modal, assert it is visible, cancel, assert it is gone.
    No sleep or networkidle.
    """
    # TODO:
    # 1. page.goto(SPA_URL)
    # 2. Click the Login button (first in navbar)
    # 3. expect(page.get_by_role("dialog")).to_be_visible()
    # 4. Click Cancel
    # 5. expect(page.get_by_role("dialog")).not_to_be_visible()
    pass


# ---------------------------------------------------------------------------
# Task 3 — Wait for dynamic content after filtering
# ---------------------------------------------------------------------------

def test_filter_todo_with_web_first_wait(page: Page):
    """
    Filter by TODO status and wait for the table to reflect the filter.
    No sleep or networkidle.
    """
    # TODO:
    # 1. page.goto(SPA_URL)
    # 2. expect(page.locator("table tbody tr").first).to_be_visible()
    # 3. Select "TODO" from the status filter (get_by_role("combobox"))
    # 4. expect(page.locator("table tbody tr").first).to_be_visible()
    # 5. rows = page.locator("table tbody tr").all()
    # 6. For each row, assert its status cell contains "TODO"
    pass


# ---------------------------------------------------------------------------
# Task 4 — Wait for count change after API creation
# ---------------------------------------------------------------------------

def test_row_count_updates_after_api_create(page: Page, api_v1: APIRequestContext):
    """
    Create a task via API, reload, assert the row count increased.
    """
    import json
    task_id_1 = task_id_2 = None
    try:
        # TODO:
        # 1. page.goto(SPA_URL)
        # 2. expect first row to_be_visible()
        # 3. count_before = page.locator("table tbody tr").count()
        # 4. Create a task via api_v1
        # 5. page.reload() — no sleep
        # 6. expect(page.locator("table tbody tr")).to_have_count(count_before + 1, timeout=8000)
        pass
    finally:
        for tid in [task_id_1, task_id_2]:
            if tid:
                api_v1.delete(f"/tasks/{tid}")


# ---------------------------------------------------------------------------
# Task 5 — Authenticated SPA flow with storage_state reuse
# ---------------------------------------------------------------------------

def test_authenticated_session_reused(authenticated_page):
    """
    Uses the session-scoped authenticated_page fixture.
    Storage state is reused — login modal is not shown again.
    """
    # TODO:
    # 1. authenticated_page.goto(SPA_URL)
    # 2. expect(authenticated_page.locator("table tbody tr").first).to_be_visible()
    # 3. Assert login button is not visible (already authenticated)
    #    OR assert a logout / user indicator IS visible
    pass
