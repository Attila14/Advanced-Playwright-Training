"""
test_auto_waiting.py — Exercise 17: Auto-Waiting & Flakiness Prevention

See Exercises/17_AutoWaitingAndFlakiness.md for full instructions.
Run: pytest src/tests/test_auto_waiting.py -v --headed

Key rule: NEVER use time.sleep(), wait_for_load_state("networkidle"), or bare assert.
          ALWAYS use expect(locator).to_be_visible() / to_have_count() / to_have_text().
"""
import json
import time
import uuid
from playwright.sync_api import Page, APIRequestContext, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"


# ---------------------------------------------------------------------------
# Task 1 — Replace networkidle + bare assert with expect()
# ---------------------------------------------------------------------------

def test_task_list_loads(page: Page):
    """
    Navigate to the Task Manager and assert at least one task row is visible.
    Do NOT use wait_for_load_state("networkidle") or bare assert.
    Do NOT use time.sleep().
    Use expect(rows.first).to_be_visible() instead.
    """
    # TODO:
    # page.goto(TASK_MANAGER)
    # rows = page.locator("table tbody tr")
    # expect(rows.first).to_be_visible()

    # Developer attempt: networkidle + bare assert — fragile and flaky
    page.goto(TASK_MANAGER)
    page.wait_for_load_state("networkidle")      # wrong: slow and unreliable
    count = page.locator("table tbody tr").count()
    assert count > 0                             # wrong: use expect().to_be_visible()


# ---------------------------------------------------------------------------
# Task 2 — Modal open and close — no time.sleep()
# ---------------------------------------------------------------------------

def test_login_modal_open_close(page: Page):
    """
    1. Navigate to Task Manager.
    2. Click the Login button to open the modal — expect modal to be visible.
    3. Press Escape to close the modal — expect modal to NOT be visible.
    NO time.sleep() allowed.
    """
    # TODO:
    # page.goto(TASK_MANAGER)
    # page.get_by_role("button", name="Login").click()
    # dialog = page.get_by_role("dialog")
    # expect(dialog).to_be_visible()
    # page.keyboard.press("Escape")
    # expect(dialog).not_to_be_visible()

    # Developer attempt: two time.sleep() calls — flaky and slow
    page.goto(TASK_MANAGER)
    page.get_by_role("button", name="Login").click()
    time.sleep(1)                                    # wrong: use expect(dialog).to_be_visible()
    page.keyboard.press("Escape")
    time.sleep(1)                                    # wrong: use expect(dialog).not_to_be_visible()


# ---------------------------------------------------------------------------
# Task 3 — Status filter and row verification
# ---------------------------------------------------------------------------

def test_filter_todo_tasks_only(page: Page):
    """
    Navigate. Select "TODO" from the status filter dropdown.
    Wait using expect(). Assert every visible row's status cell contains "TODO".
    """
    # TODO:
    # page.goto(TASK_MANAGER)
    # page.get_by_role("combobox").first.select_option("TODO")
    # expect(page.locator("table tbody tr").first).to_be_visible()
    # rows = page.locator("table tbody tr").all()
    # for row in rows:
    #     expect(row.locator("td").nth(2)).to_contain_text("TODO")
    pass


# ---------------------------------------------------------------------------
# Task 4 — Row count increments after second API create
# ---------------------------------------------------------------------------

def test_row_count_updates_after_api_create(page: Page, api_v1: APIRequestContext):
    """
    1. Create task 1 via API ("Count Task 1 <uuid>").
    2. Navigate to Task Manager — record count_before (rows visible after load).
    3. Create task 2 via API ("Count Task 2 <uuid>") while on the page.
    4. Reload the page.
    5. expect(rows).to_have_count(count_before + 1, timeout=8000).
    6. Delete both tasks in finally.
    """
    # TODO:
    # title1 = f"Count Task 1 {uuid.uuid4()}"
    # title2 = f"Count Task 2 {uuid.uuid4()}"
    # id1 = id2 = None
    # try:
    #     resp1 = api_v1.post("/tasks", ...); id1 = resp1.json()["id"]
    #     page.goto(TASK_MANAGER)
    #     rows = page.locator("table tbody tr")
    #     expect(rows.first).to_be_visible()
    #     count_before = rows.count()
    #     resp2 = api_v1.post("/tasks", ...); id2 = resp2.json()["id"]
    #     page.reload()
    #     expect(rows).to_have_count(count_before + 1, timeout=8000)
    # finally:
    #     for id_ in [id1, id2]:
    #         if id_: api_v1.delete(f"/tasks/{id_}")

    # Developer attempt: only one task created (misses count_before step);
    # time.sleep after reload instead of expect()
    title = f"Count Task {uuid.uuid4()}"
    task_id = None
    try:
        resp = api_v1.post(
            "/tasks",
            data=json.dumps({"title": title, "status": "TODO", "priority": "LOW"}),
            headers={"Content-Type": "application/json"},
        )
        task_id = resp.json()["id"]
        page.goto(TASK_MANAGER)
        # wrong: count_before never recorded — can't assert +1
        page.reload()
        time.sleep(2)                                    # wrong: use expect()
        count = page.locator("table tbody tr").count()
        assert count > 0                                 # wrong: should be count_before + 1
    finally:
        if task_id:
            api_v1.delete(f"/tasks/{task_id}")


# ---------------------------------------------------------------------------
# Task 5 — Authenticated page with storage state
# ---------------------------------------------------------------------------

def test_authenticated_task_list(browser, tmp_path):
    """
    Reuse the storage state saved from a prior login.
    Create a context with storage_state, navigate to Task Manager.
    Assert the task table is visible and NO login button is shown.
    (Uses the authenticated_page fixture if defined in conftest.py.)
    """
    # TODO Task 5 — use saved auth state, assert table visible, assert no login button
    pass