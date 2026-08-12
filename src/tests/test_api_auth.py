"""
test_api_auth.py — Exercise 10: API Authentication (JWT / V2)

See Exercises/10_APIAuthentication.md for full instructions.
Run: pytest src/tests/test_api_auth.py -v -s

V2 login: POST https://api.testauto.app/api/v2/auth/login
           Body: {"username": "admin", "password": "admin123"}
           Returns: {"token": "...", "username": "admin", "expiresIn": 3600}
"""
import json
import uuid
import pytest
from playwright.sync_api import Playwright, APIRequestContext

BASE_V2 = "https://api.testauto.app/api/v2"


# ---------------------------------------------------------------------------
# Task 1 — Login scenarios
# ---------------------------------------------------------------------------

def test_valid_login(playwright: Playwright):
    """
    POST /auth/login with admin/admin123.
    Assert status 200.
    Assert response body has keys: token, username, expiresIn.
    Assert token is a string with length > 20.
    Assert username == "admin".
    Close the context in finally.
    """
    # TODO:
    # ctx = playwright.request.new_context(base_url=BASE_V2)
    # try:
    #     resp = ctx.post("/auth/login", data=json.dumps({"username":"admin","password":"admin123"}), headers={...})
    #     assert resp.status == 200
    #     body = resp.json()
    #     assert "token" in body and "username" in body and "expiresIn" in body
    #     assert isinstance(body["token"], str) and len(body["token"]) > 20
    #     assert body["username"] == "admin"
    # finally:
    #     ctx.dispose()

    # Developer attempt: assertions correct but context never disposed — resource leak
    ctx = playwright.request.new_context(base_url=BASE_V2)
    resp = ctx.post(
        "/auth/login",
        data=json.dumps({"username": "admin", "password": "admin123"}),
        headers={"Content-Type": "application/json"},
    )
    assert resp.status == 200
    body = resp.json()
    assert "token" in body and "username" in body and "expiresIn" in body
    assert isinstance(body["token"], str) and len(body["token"]) > 20
    assert body["username"] == "admin"
    # missing: ctx.dispose() in finally


def test_wrong_password(playwright: Playwright):
    """POST /auth/login with admin/wrongpassword — expect 401."""
    # TODO: assert resp.status == 401

    # Developer attempt: asserts 200 instead of 401
    ctx = playwright.request.new_context(base_url=BASE_V2)
    try:
        resp = ctx.post(
            "/auth/login",
            data=json.dumps({"username": "admin", "password": "wrongpassword"}),
            headers={"Content-Type": "application/json"},
        )
        assert resp.status == 200  # wrong: should be 401
    finally:
        ctx.dispose()


def test_unknown_user(playwright: Playwright):
    """POST /auth/login with nonexistent/any — expect 4xx."""
    # TODO: assert resp.status in (400, 401, 404)
    pass


# ---------------------------------------------------------------------------
# Task 2 — Authenticated CRUD via V2
# ---------------------------------------------------------------------------

@pytest.fixture
def api_v2(playwright: Playwright):
    """Logs in as admin, returns an authenticated APIRequestContext."""
    ctx = playwright.request.new_context(base_url=BASE_V2)
    login = ctx.post(
        "/auth/login",
        data=json.dumps({"username": "admin", "password": "admin123"}),
        headers={"Content-Type": "application/json"},
    )
    token = login.json()["token"]
    auth_ctx = playwright.request.new_context(
        base_url=BASE_V2,
        extra_http_headers={"Authorization": f"Bearer {token}"},
    )
    ctx.dispose()
    yield auth_ctx
    auth_ctx.dispose()


def test_create_task_authenticated(api_v2: APIRequestContext):
    """Create a task via V2, assert 201, clean up in finally."""
    # TODO: try/finally with uuid title
    # Developer attempt: hardcoded title, no try/finally cleanup
    resp = api_v2.post(
        "/tasks",
        data=json.dumps({"title": "my test task", "status": "TODO", "priority": "LOW"}),
        headers={"Content-Type": "application/json"},
    )
    assert resp.status == 201
    # missing: uuid title; missing: try/finally with delete in finally


def test_update_task_authenticated(api_v2: APIRequestContext):
    """Create task, PUT with new title, assert 200 and title changed. Delete in finally."""
    # TODO Task 2 — full create → update cycle
    pass


def test_delete_task_authenticated(api_v2: APIRequestContext):
    """Create task, DELETE it, assert 200/204, GET → assert 404. Cleanup in finally."""
    # TODO Task 2 — create → delete → verify 404
    pass


# ---------------------------------------------------------------------------
# Task 3 — Unauthenticated access returns 401
# ---------------------------------------------------------------------------

def test_unauthenticated_get_tasks(playwright: Playwright):
    """GET /tasks without token — assert 401."""
    # TODO Task 3 — also test POST and DELETE without token
    ctx = playwright.request.new_context(base_url=BASE_V2)
    try:
        resp = ctx.get("/tasks")
        assert resp.status == 401
    finally:
        ctx.dispose()


# ---------------------------------------------------------------------------
# Task 4 — Token refresh
# ---------------------------------------------------------------------------

def test_token_refresh(playwright: Playwright):
    """
    Login, POST /auth/refresh with old token, receive new token.
    Use new token on GET /tasks — assert 200.
    """
    # TODO Task 4
    pass


# ---------------------------------------------------------------------------
# Task 5 — Multi-user role separation
# ---------------------------------------------------------------------------

def test_admin_and_user_roles(playwright: Playwright):
    """
    Admin creates a task, user reads it (assert 200).
    User attempts to delete it (capture status — document whether 403 or 200).
    Admin cleans up in finally.
    """
    # TODO Task 5 — two authenticated contexts, role-based access test
    pass