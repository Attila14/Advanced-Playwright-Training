"""
test_selectors.py — Exercise 03: Advanced Locator Strategies

See Exercises/03_AdvancedLocatorStrategies.md for full instructions.
Run: pytest src/tests/test_selectors.py -v --headed
"""
import json
import re
import uuid
from playwright.sync_api import Page, APIRequestContext, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"


# ---------------------------------------------------------------------------
# Task 1 — Rewrite brittle selectors with semantic alternatives
# ---------------------------------------------------------------------------

def test_semantic_selectors_only(page: Page):
    """
    Fill search with "deploy" using get_by_placeholder.
    Click Add New Task using get_by_role("link").
    Assert URL contains taskModal=create using expect(page).to_have_url().
    No page.locator("css") allowed anywhere.
    """
    # TODO:
    # 1. page.goto(TASK_MANAGER)
    # 2. page.get_by_placeholder("Search tasks...").fill("deploy")
    # 3. page.get_by_role("link", name="Add New Task").click()
    # 4. expect(page).to_have_url(re.compile("taskModal=create"))

    page.goto(TASK_MANAGER)
    page.get_by_placeholder("Search tasks...").fill("deploy")
    page.get_by_role("button", name="Add New Task").click()
    expect(page).to_have_url(re.compile("taskModal=create"))


# ---------------------------------------------------------------------------
# Task 2 — filter() to act on a specific row
# ---------------------------------------------------------------------------

def test_filter_specific_row(page: Page):
    """
    Find the "Deploy to Railway.app" row using .filter(has_text=...).
    Read the priority cell from within that row only.
    Assert it contains "High". Assert no other row was accidentally matched.
    """
    # TODO:
    # 1. page.goto(TASK_MANAGER)
    # 2. expect(page.locator("table tbody tr").first).to_be_visible()
    # 3. row = page.locator("table tbody tr").filter(has_text="Deploy to Railway.app")
    # 4. expect(row).to_have_count(1)  — assert exactly one row matched
    # 5. Read priority cell from within row using get_by_text or column header scope
    # 6. assert priority contains "High"

    page.goto(TASK_MANAGER)
    expect(page.locator("table tbody tr").first).to_be_visible()

    row = page.locator("table tbody tr").filter(has_text="Deploy to Railway.app")
    expect(row).to_have_count(1)
    expect(row).to_contain_text("High")


# ---------------------------------------------------------------------------
# Task 3 — nth(), first, last and counting
# ---------------------------------------------------------------------------

def test_nth_first_last(page: Page):
    """
    1. Navigate to the task manager
    2. Change items-per-page dropdown to 10
    3. Assert row_count <= 10
    4. Read first row title — assert not empty string
    5. Read last row title — assert differs from first
    """
    page.goto(TASK_MANAGER)
    page.get_by_label("Items per page:").select_option("10")
    rows = page.locator("table tbody tr")
    # Wait until the table actually refreshes to 10 rows
    expect(rows).to_have_count(10)
    assert rows.count() <= 10
    first_title = rows.first.locator("td").nth(1).inner_text()
    last_title = rows.last.locator("td").nth(1).inner_text()
    assert first_title != "" and last_title != "" and first_title != last_title


# ---------------------------------------------------------------------------
# Task 4 — Board view column scoping
# ---------------------------------------------------------------------------

def test_board_view_column_scoping(page: Page):
    """
    Navigate to board view (?view=board).
    For each column (TODO, In Progress, Done): scope a locator to that column container
    and count the task cards inside it.
    Assert the sum of all three column counts is > 0.
    """
    page.goto(TASK_MANAGER)
    page.get_by_role("button", name="Board view").click()
    expect(page.locator(".task-board").first).to_be_visible()
    total = 0
    for status in ["TODO", "In Progress", "Done"]:
        col = page.locator(".board-column").filter(
            has=page.locator(".board-column-title", has_text=status)
        )
        total += col.locator(".board-task-card").count()
    assert total > 0


# ---------------------------------------------------------------------------
# Task 5 — Dynamic filter loop
# ---------------------------------------------------------------------------

def test_dynamic_filter_loop(page: Page, api_v1: APIRequestContext):
    """
    Create 3 tasks: "Selector Alpha" (LOW), "Selector Beta" (MEDIUM), "Selector Gamma" (HIGH).
    Navigate to task manager, search for "Selector".
    For each title, use .filter(has_text=title) and assert the row is visible.
    Clean up all 3 tasks in finally.
    """
    # TODO:
    # titles = ["Selector Alpha", "Selector Beta", "Selector Gamma"]
    # priorities = ["LOW", "MEDIUM", "HIGH"]
    # task_ids = []
    # try:
    #     for title, priority in zip(titles, priorities):
    #         resp = api_v1.post("/tasks", data=json.dumps({...}), headers={...})
    #         task_ids.append(resp.json()["id"])
    #     page.goto(TASK_MANAGER)
    #     page.get_by_placeholder("Search tasks...").fill("Selector")
    #     for title in titles:
    #         expect(page.locator("table tbody tr").filter(has_text=title)).to_be_visible()
    # finally:
    #     for task_id in task_ids:
    #         api_v1.delete(f"/tasks/{task_id}")

    uid = str(uuid.uuid4())[:8]
    titles = [f"Selector Alpha {uid}", f"Selector Beta {uid}", f"Selector Gamma {uid}"]
    priorities = ["LOW", "MEDIUM", "HIGH"]
    task_ids = []
    try:
        for title, priority in zip(titles, priorities):
            resp = api_v1.post(
                "/api/v1/tasks",
                data=json.dumps({"title": title, "status": "TODO", "priority": priority}),
                headers={"Content-Type": "application/json"},
            )
            assert resp.ok, f"POST failed: {resp.status}"
            task_ids.append(resp.json()["id"])
        page.goto(TASK_MANAGER)
        search = page.get_by_placeholder("Search tasks...")
        search.fill(uid)
        with page.expect_response(
            lambda r: "/api/v1/tasks" in r.url and "summary" not in r.url and r.request.method == "GET"
        ):
            search.press("Enter")
        for title in titles:
            expect(page.locator("table tbody tr").filter(has_text=title)).to_be_visible()
    finally:
        for task_id in task_ids:
            api_v1.delete(f"/api/v1/tasks/{task_id}")