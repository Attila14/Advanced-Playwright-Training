"""
test_browser_context.py — Exercise 01: Browser Contexts & Storage State

See Exercises/01_BrowserContexts.md for full instructions.
Run: pytest src/tests/test_browser_context.py -v --headed
"""
import json
import time
import uuid
from playwright.sync_api import Browser, BrowserContext, Page, APIRequestContext, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"
LOGIN_URL = "https://testauto.app/task-manager-spa#login"


# ---------------------------------------------------------------------------
# Task 1 — Two independent browser contexts
# ---------------------------------------------------------------------------

def test_two_contexts_are_independent(browser: Browser):
    """
    Create ctx1 and ctx2 from the same browser.
    Navigate ctx1 to the Task Manager, ctx2 to https://example.com.
    Assert ctx1.pages[0].url == TASK_MANAGER and ctx2.pages[0].url contains "example.com".
    Assert their URLs differ. Close BOTH contexts in finally.
    """
    # TODO:
    # 1. ctx1 = browser.new_context()
    # 2. ctx2 = browser.new_context()
    # 3. page1 = ctx1.new_page(); page1.goto(TASK_MANAGER)
    # 4. page2 = ctx2.new_page(); page2.goto("https://example.com")
    # 5. assert page1.url == TASK_MANAGER
    # 6. assert "example.com" in page2.url
    # 7. assert page1.url != page2.url
    # 8. ctx1.close(); ctx2.close()  — BOTH in finally

    # Developer attempt: ctx2 is never closed — resource leak
    ctx1 = browser.new_context()
    ctx2 = browser.new_context()
    page1 = ctx1.new_page()
    page2 = ctx2.new_page()
    page1.goto(TASK_MANAGER)
    page2.goto("https://example.com")
    assert page1.url == TASK_MANAGER
    ctx1.close()  # wrong: ctx2 is never closed — also missing independence assertion


# ---------------------------------------------------------------------------
# Task 2 — Save and restore authentication state
# ---------------------------------------------------------------------------

def test_save_and_restore_auth_state(browser: Browser, tmp_path):
    """
    1. Create ctx1, navigate to Task Manager, log in as admin/admin123.
    2. Save storage state to a JSON file: ctx1.storage_state(path=state_path).
    3. Create ctx2 using storage_state=state_path.
    4. Navigate ctx2 to Task Manager and assert the task table is visible without logging in again.
    Close both contexts in finally.
    """
    # TODO:
    # 1. state_path = str(tmp_path / "auth.json")
    # 2. ctx1 = browser.new_context(); page1 = ctx1.new_page(); page1.goto(TASK_MANAGER)
    # 3. Log in as admin/admin123 via UI
    # 4. ctx1.storage_state(path=state_path); ctx1.close()
    # 5. ctx2 = browser.new_context(storage_state=state_path)
    # 6. page2 = ctx2.new_page(); page2.goto(TASK_MANAGER)
    # 7. expect(page2.locator("table tbody tr").first).to_be_visible()
    # 8. ctx2.close()

    # Developer attempt: ctx2 created WITHOUT storage_state — still on login page; time.sleep used
    state_path = str(tmp_path / "auth.json")
    ctx1 = browser.new_context()
    page1 = ctx1.new_page()
    page1.goto(TASK_MANAGER)
    # (login steps omitted for brevity but should use expect())
    ctx1.storage_state(path=state_path)
    ctx1.close()

    ctx2 = browser.new_context()           # wrong: missing storage_state=state_path
    page2 = ctx2.new_page()
    page2.goto(TASK_MANAGER)
    time.sleep(2)                          # wrong: use expect(locator).to_be_visible()
    assert page2.locator("table").is_visible()  # wrong: use expect()
    ctx2.close()


# ---------------------------------------------------------------------------
# Task 3 — Multiple viewports and screenshots
# ---------------------------------------------------------------------------

def test_multiple_viewports(browser: Browser, tmp_path):
    """
    For each viewport (desktop 1280x720, tablet 768x1024, mobile 375x812):
    1. Create a context with that viewport size.
    2. Navigate to Task Manager.
    3. Take a screenshot and save it to tmp_path/<name>.png.
    4. Assert the file exists and is > 5 KB.
    Close each context after use.
    """
    # TODO:
    # viewports = [
    #   {"name": "desktop", "width": 1280, "height": 720},
    #   {"name": "tablet",  "width": 768,  "height": 1024},
    #   {"name": "mobile",  "width": 375,  "height": 812},
    # ]
    # for vp in viewports:
    #     ctx = browser.new_context(viewport={"width": vp["width"], "height": vp["height"]})
    #     page = ctx.new_page()
    #     page.goto(TASK_MANAGER)
    #     path = str(tmp_path / f"{vp['name']}.png")
    #     page.screenshot(path=path)
    #     import os; assert os.path.getsize(path) > 5000
    #     ctx.close()
    pass


# ---------------------------------------------------------------------------
# Task 4 — Cross-context data sharing via API
# ---------------------------------------------------------------------------

def test_user_a_creates_task_user_b_reads(browser: Browser, api_v1: APIRequestContext):
    """
    User A creates a task via the API with a unique uuid-based title.
    User B opens a new browser context, navigates to the Task Manager.
    User B asserts the task title is visible in the table.
    Clean up the task via api_v1 in finally.
    """
    # TODO:
    # title = f"Shared Task {uuid.uuid4()}"
    # task_id = None
    # try:
    #     resp = api_v1.post("/tasks", data=json.dumps({"title": title, "status": "TODO", "priority": "LOW"}), headers={...})
    #     task_id = resp.json()["id"]
    #     ctx_b = browser.new_context()
    #     page_b = ctx_b.new_page()
    #     page_b.goto(TASK_MANAGER)
    #     expect(page_b.locator("table tbody tr").filter(has_text=title)).to_be_visible()
    #     ctx_b.close()
    # finally:
    #     if task_id: api_v1.delete(f"/tasks/{task_id}")
    pass


# ---------------------------------------------------------------------------
# Task 5 — Context with locale and extra HTTP headers
# ---------------------------------------------------------------------------

def test_context_with_locale_and_headers(browser: Browser):
    """
    Create a context with:
    - locale="it-IT"
    - timezone_id="Europe/Rome"
    - extra_http_headers={"X-Test-Agent": "playwright-training"}
    Navigate to Task Manager and assert the page loads (table visible).
    """
    # TODO:
    # 1. ctx = browser.new_context(locale="it-IT", timezone_id="Europe/Rome",
    #         extra_http_headers={"X-Test-Agent": "playwright-training"})
    # 2. page = ctx.new_page(); page.goto(TASK_MANAGER)
    # 3. expect(page.locator("table tbody tr").first).to_be_visible()
    # 4. ctx.close()
    pass