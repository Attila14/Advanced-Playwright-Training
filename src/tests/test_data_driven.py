"""
test_data_driven.py — Exercise 16: Data-Driven Testing (GUI & API)

See Exercises/16_DataDrivenTestingGUIAndAPI.md for full instructions.
Run: pytest src/tests/test_data_driven.py -v
     pytest src/tests/test_data_driven.py --collect-only  (see all test names)
"""
import json
import pytest
from playwright.sync_api import Page, APIRequestContext, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"

TASK_SCENARIOS = [
    {"title": "Scenario Alpha", "status": "TODO",        "priority": "LOW"},
    {"title": "Scenario Beta",  "status": "IN_PROGRESS", "priority": "HIGH"},
    {"title": "Scenario Gamma", "status": "DONE",        "priority": "URGENT"},
]


# ---------------------------------------------------------------------------
# Task 1 — Parametrize over all 4 priorities via API
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("priority", ["LOW", "MEDIUM", "HIGH", "URGENT"])
def test_api_create_with_priority(api_v1: APIRequestContext, priority: str):
    # TODO Task 1 — create task with given priority, assert 201 and priority matches, clean up
    # Developer attempt: task created and priority asserted, but no cleanup in try/finally
    resp = api_v1.post(
        "/tasks",
        data=json.dumps({"title": f"Priority test {priority}", "status": "TODO", "priority": priority}),
        headers={"Content-Type": "application/json"},
    )
    assert resp.status == 201
    assert resp.json()["priority"] == priority
    # missing: try/finally with delete in finally


# ---------------------------------------------------------------------------
# Task 2 — UI detail modal shows correct status
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("status", ["TODO", "IN_PROGRESS", "DONE"])
def test_ui_detail_shows_status(page: Page, task_factory, status: str):
    # TODO Task 2 — create via API, open detail modal, assert status visible
    # Developer attempt: task_factory fixture referenced but not defined in conftest.py
    # — this test will fail with fixture not found error until task_factory is added to conftest
    pass


# ---------------------------------------------------------------------------
# Task 3 — Shared dataset across UI and API
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("data", TASK_SCENARIOS)
def test_api_create_scenario(api_v1: APIRequestContext, data: dict):
    # TODO Task 3 — create task from TASK_SCENARIOS, assert all fields match, clean up
    pass


@pytest.mark.parametrize("data", TASK_SCENARIOS)
def test_ui_search_for_scenario(page: Page, task_factory, data: dict):
    # TODO Task 3 — create via task_factory, search in UI, assert row visible
    pass


# ---------------------------------------------------------------------------
# Task 4 — Form validation scenarios
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("title,expected_behaviour", [
    ("",        "error_shown"),
    ("   ",     "error_or_created"),
    ("A" * 200, "created"),
])
def test_form_validation(page: Page, title: str, expected_behaviour: str):
    # TODO Task 4 — open create modal, submit with given title, assert expected_behaviour
    pass


# ---------------------------------------------------------------------------
# Task 5 — Status filter parametrized
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("filter_value,expected_status", [
    ("TODO",        "TODO"),
    ("IN_PROGRESS", "IN_PROGRESS"),
    ("DONE",        "DONE"),
], ids=["filter-todo", "filter-in-progress", "filter-done"])
def test_status_filter_parametrized(page: Page, filter_value: str, expected_status: str):
    # TODO Task 5 — select filter_value from dropdown, assert every visible row has expected_status
    # Developer attempt: filter selected but rows never checked
    page.goto(TASK_MANAGER)
    expect(page.locator("table tbody tr").first).to_be_visible()
    page.get_by_role("combobox").first.select_option(filter_value)
    # missing: rows = page.locator("table tbody tr").all()
    # missing: for row in rows: expect(row.locator("td").nth(2)).to_have_text(expected_status)