"""
Smoke Test — Run this first to verify your setup is working correctly.

    pytest src/tests/smoke_test.py -v

All 5 tests should pass before starting the exercises.
"""

import pytest
from playwright.sync_api import Page, APIRequestContext, expect


@pytest.mark.smoke
def test_task_manager_page_loads(page: Page):
    """The task manager page should load and show the correct title."""
    page.goto("https://testauto.app/task-manager-spa-spa")
    expect(page).to_have_title("Task Manager (SSR) - TestAuto.app")


@pytest.mark.smoke
def test_task_table_is_visible(page: Page):
    """The task list table should be visible on page load."""
    page.goto("https://testauto.app/task-manager-spa-spa")
    expect(page.locator("table")).to_be_visible()


@pytest.mark.smoke
def test_api_v1_returns_tasks(api_v1: APIRequestContext):
    """API V1 should return a paginated list of tasks without authentication."""
    resp = api_v1.get("/tasks")
    assert resp.status == 200, f"Expected 200, got {resp.status}"
    body = resp.json()
    assert "content" in body, "Response missing 'content' key"
    assert isinstance(body["content"], list), "'content' should be a list"


@pytest.mark.smoke
def test_api_v2_login_works(playwright):
    """API V2 login should return a valid JWT token."""
    import json
    ctx = playwright.request.new_context(base_url="https://api.testauto.app/api/v2")
    resp = ctx.post(
        "/auth/login",
        data=json.dumps({"username": "user", "password": "user123"}),
        headers={"Content-Type": "application/json"},
    )
    assert resp.status == 200, f"Login failed: {resp.status}"
    data = resp.json()
    assert "token" in data, "Response missing 'token'"
    assert len(data["token"]) > 20, "Token seems too short"
    ctx.dispose()


@pytest.mark.smoke
def test_board_view_loads(page: Page):
    """Switching to board view should show the three status columns."""
    page.goto("https://testauto.app/task-manager-spa-spa?view=board")
    expect(page).to_have_url(lambda url: "view=board" in url)
    expect(page.get_by_text("TODO").first).to_be_visible()
