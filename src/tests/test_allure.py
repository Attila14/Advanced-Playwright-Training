"""
test_allure.py — Exercise 09: Allure Reporting

See Exercises/09_AllureReporting.md for full instructions.
Run: pytest src/tests/test_allure.py --alluredir=allure-results
     allure serve allure-results
"""
import json
import uuid
import allure
import pytest
from playwright.sync_api import Page, APIRequestContext, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"


# ---------------------------------------------------------------------------
# Task 1 — epic / feature / story hierarchy
# ---------------------------------------------------------------------------

# Developer attempt: missing @allure.epic / @allure.feature / @allure.story decorators
class TestTaskListUI:
    # wrong: no @allure.epic("Task Manager"), @allure.feature("Task List"), @allure.story("UI")

    def test_task_table_visible(self, page: Page):
        # TODO Task 1 — add epic/feature/story decorators above the class
        page.goto(TASK_MANAGER)
        expect(page.locator("table tbody tr").first).to_be_visible()

    def test_search_filters_rows(self, page: Page, api_v1: APIRequestContext):
        # TODO Task 1 — table filters by search term
        pass


# Developer attempt: missing @allure.epic / @allure.feature / @allure.story decorators
class TestAPIV1:
    # wrong: no @allure.epic("Task Manager"), @allure.feature("Task API"), @allure.story("v1")

    def test_get_tasks_returns_list(self, api_v1: APIRequestContext):
        # TODO Task 1 — GET /tasks returns content list
        resp = api_v1.get("/tasks")
        assert resp.status == 200
        assert "content" in resp.json()

    def test_create_task_returns_201(self, api_v1: APIRequestContext):
        # TODO Task 1 — POST /tasks, cleanup
        pass


# ---------------------------------------------------------------------------
# Task 2 — allure.step() blocks for a UI workflow
# ---------------------------------------------------------------------------

@allure.epic("Task Manager")
@allure.feature("Task Creation")
@allure.story("UI Workflow")
def test_create_task_via_ui_with_steps(page: Page, api_v1: APIRequestContext):
    """
    Exercise 09, Task 2: use 6+ allure.step() context managers wrapping each action.
    Steps: open app, wait for load, open modal, fill title, fill description, submit,
           wait for task in table, clean up.
    """
    # TODO Task 2:
    # with allure.step("Open Task Manager"):
    #     page.goto(TASK_MANAGER)
    # with allure.step("Wait for task list to load"):
    #     expect(page.locator("table tbody tr").first).to_be_visible()
    # with allure.step("Open Add New Task modal"):
    #     page.get_by_role("link", name="Add New Task").click()
    # ... etc.

    # Developer attempt: has decorators but no allure.step() blocks — all code runs unlabeled
    title = f"Allure Task {uuid.uuid4()}"
    task_id = None
    try:
        page.goto(TASK_MANAGER)                                           # step missing
        expect(page.locator("table tbody tr").first).to_be_visible()      # step missing
        page.get_by_role("link", name="Add New Task").click()             # step missing
        page.get_by_label("Title").fill(title)                            # step missing
        page.get_by_role("button", name="Create Task").click()            # step missing
        expect(page.locator("table tbody tr").filter(has_text=title)      # step missing
               ).to_be_visible()
    finally:
        if task_id:
            api_v1.delete(f"/tasks/{task_id}")


# ---------------------------------------------------------------------------
# Task 3 — Attach screenshot and API response body
# ---------------------------------------------------------------------------

@allure.epic("Task Manager")
@allure.feature("Attachments")
@allure.story("API + UI")
def test_attach_screenshot_and_api_data(page: Page, api_v1: APIRequestContext):
    """
    Navigate to Task Manager.
    Attach a full-page screenshot as PNG.
    Call GET /tasks?size=5 and attach the JSON response body.
    """
    # TODO Task 3:
    # page.goto(TASK_MANAGER); expect(rows.first).to_be_visible()
    # screenshot_bytes = page.screenshot(full_page=True)
    # allure.attach(screenshot_bytes, name="Task Manager", attachment_type=allure.attachment_type.PNG)
    # resp = api_v1.get("/tasks", params={"size": 5})
    # allure.attach(resp.text(), name="GET /tasks response", attachment_type=allure.attachment_type.JSON)

    # Developer attempt: screenshot taken but never attached; API response also never attached
    page.goto(TASK_MANAGER)
    expect(page.locator("table tbody tr").first).to_be_visible()
    screenshot_bytes = page.screenshot(full_page=True)   # taken but not attached
    # missing: allure.attach(screenshot_bytes, ...)
    resp = api_v1.get("/tasks", params={"size": 5})
    assert resp.status == 200
    # missing: allure.attach(resp.text(), ...)


# ---------------------------------------------------------------------------
# Task 4 — Autouse screenshot-on-failure fixture (should be in conftest.py)
# ---------------------------------------------------------------------------

# TODO Task 4 — add to conftest.py:
# @pytest.fixture(autouse=True)
# def screenshot_on_failure(page, request):
#     yield
#     if request.node.rep_call.failed:
#         allure.attach(page.screenshot(), name="failure", attachment_type=allure.attachment_type.PNG)


# ---------------------------------------------------------------------------
# Task 5 — Severity labels
# ---------------------------------------------------------------------------

@allure.severity(allure.severity_level.CRITICAL)
def test_task_list_loads_critical(page: Page):
    # TODO Task 5 — CRITICAL: task list must always be accessible
    page.goto(TASK_MANAGER)
    expect(page.locator("table tbody tr").first).to_be_visible()


@allure.severity(allure.severity_level.NORMAL)
def test_search_works_normal(page: Page):
    # TODO Task 5 — NORMAL: search is important but not critical
    pass


@allure.severity(allure.severity_level.MINOR)
def test_pagination_minor(page: Page):
    # TODO Task 5 — MINOR: cosmetic pagination behaviour
    pass