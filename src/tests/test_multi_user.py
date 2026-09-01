"""
test_multi_user.py — Exercise 14: Multi-User Scenarios

See Exercises/14_MultiUserScenarios.md for full instructions.
Run: pytest src/tests/test_multi_user.py -v --headed

V2 credentials:
  admin  / admin123
  user   / user123
"""
import json
import uuid
import pytest
from playwright.sync_api import Browser, Playwright, APIRequestContext, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"
BASE_V2 = "https://api.testauto.app/api/v2"


def _login_ctx(playwright: Playwright, username: str, password: str) -> APIRequestContext:
    ctx = playwright.request.new_context(base_url=BASE_V2)
    resp = ctx.post(
        "/auth/login",
        data=json.dumps({"username": username, "password": password}),
        headers={"Content-Type": "application/json"},
    )
    token = resp.json()["token"]
    ctx.dispose()
    return playwright.request.new_context(
        base_url=BASE_V2,
        extra_http_headers={"Authorization": f"Bearer {token}"},
    )


# ---------------------------------------------------------------------------
# Task 1 — Document access permissions (print table)
# ---------------------------------------------------------------------------

def test_document_access_permissions(playwright: Playwright):
    """
    For admin and user: test GET /tasks, POST /tasks, DELETE /tasks/{id} (own + other's task).
    Print a markdown table documenting the HTTP status for each combination.
    No assertions required — this is a documentation / exploratory test.
    """
    # TODO Task 1:
    # admin_ctx = _login_ctx(playwright, "admin", "admin123")
    # user_ctx  = _login_ctx(playwright, "user",  "user123")
    # ... POST tasks as each role, try DELETE cross-user, print table
    # finally: dispose both contexts, delete any created tasks
    pass


# ---------------------------------------------------------------------------
# Task 2 — Admin creates, user reads
# ---------------------------------------------------------------------------

def test_admin_creates_user_reads(playwright: Playwright):
    """
    1. Admin creates "Admin Task <uuid>" via V2.
    2. User searches GET /tasks?search=<uuid> via V2 — assert task in results.
    3. Admin deletes the task in finally.
    Both roles use separate APIRequestContext instances (separate JWT tokens).
    """
    # Developer attempt: single context used for both roles — user role never actually tested;
    # no cleanup at all
    title = f"Admin Task {uuid.uuid4()}"
    admin_ctx = _login_ctx(playwright, "admin", "admin123")

    try:
        resp = admin_ctx.post(
            "/tasks",
            data=json.dumps({"title": title, "status": "TODO", "priority": "LOW"}),
            headers={"Content-Type": "application/json"},
        )
        assert resp.status == 201
        task_id = resp.json()["id"]

        # wrong: uses admin_ctx to verify — should be a separate user context
        user_search = admin_ctx.get("/tasks", params={"search": title})
        assert user_search.status == 200
        titles = [t["title"] for t in user_search.json()["content"]]
        assert title in titles

        # missing: admin_ctx.delete(f"/tasks/{task_id}") in finally
    finally:
        admin_ctx.dispose()


# ---------------------------------------------------------------------------
# Task 3 — Concurrent creation by two users
# ---------------------------------------------------------------------------

def test_concurrent_user_creation(playwright: Playwright):
    """
    Admin creates "Admin Concurrent <uuid>". User creates "User Concurrent <uuid>".
    Each verifies their own task exists via GET.
    Clean up both tasks in finally.
    """
    # TODO Task 3 — two separate authenticated contexts, each creates and reads own task
    pass


# ---------------------------------------------------------------------------
# Task 4 — Cross-user delete attempt
# ---------------------------------------------------------------------------

def test_user_cannot_delete_admin_task(playwright: Playwright):
    """
    Admin creates a task. User attempts DELETE /tasks/{id}.
    Capture status (may be 403 or 200 — document the behaviour).
    If 403: assert task still exists via admin GET.
    Admin cleans up in finally.
    """
    # TODO Task 4 — document cross-role delete behaviour
    pass


# ---------------------------------------------------------------------------
# Task 5 — Two browser contexts side by side
# ---------------------------------------------------------------------------

def test_two_browser_sessions(browser: Browser, tmp_path):
    """
    Open two browser contexts (admin session and user session).
    Navigate both to the Task Manager.
    Take a screenshot of each and save as admin-session.png and user-session.png.
    Assert the task table is visible in both.
    """
    # TODO Task 5 — browser context per role, screenshot both
    pass