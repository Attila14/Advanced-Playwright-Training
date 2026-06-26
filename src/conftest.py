"""
conftest.py — Shared fixtures for all exercises.

Do not modify the fixture signatures — your exercise code depends on them.
You CAN add new fixtures at the bottom.
"""

import os
import pytest
from playwright.sync_api import Page, APIRequestContext, Playwright  # Page used by task_manager_page fixture

# ---------------------------------------------------------------------------
# Base URLs
# ---------------------------------------------------------------------------
TASK_MANAGER_URL = "https://testauto.app/task-manager-spa"
API_V1_BASE      = "https://api.testauto.app/api/v1"
API_V2_BASE      = "https://api.testauto.app/api/v2"
API_BUGGY_BASE   = "https://api.testauto.app/api/buggy"


# ---------------------------------------------------------------------------
# URL fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def task_manager_url() -> str:
    return TASK_MANAGER_URL

@pytest.fixture(scope="session")
def api_v1_url() -> str:
    return API_V1_BASE

@pytest.fixture(scope="session")
def api_v2_url() -> str:
    return API_V2_BASE


# ---------------------------------------------------------------------------
# API V1 — unauthenticated request context
# ---------------------------------------------------------------------------

@pytest.fixture
def api_v1(playwright: Playwright) -> APIRequestContext:
    """Unauthenticated APIRequestContext pointed at V1."""
    ctx = playwright.request.new_context(base_url=API_V1_BASE)
    yield ctx
    ctx.dispose()


# ---------------------------------------------------------------------------
# API V2 — JWT-authenticated request context
# Logs in as 'user/user123' automatically.
# ---------------------------------------------------------------------------

@pytest.fixture
def api_v2(playwright: Playwright) -> APIRequestContext:
    """JWT-authenticated APIRequestContext for V2. Pre-logged in as 'user'."""
    import json
    # Step 1: get token
    auth = playwright.request.new_context(base_url=API_V2_BASE)
    resp = auth.post(
        "/auth/login",
        data=json.dumps({"username": "user", "password": "user123"}),
        headers={"Content-Type": "application/json"},
    )
    assert resp.ok, f"V2 login failed: {resp.status} — {resp.text()}"
    token = resp.json()["token"]
    auth.dispose()

    # Step 2: context with token pre-set
    ctx = playwright.request.new_context(
        base_url=API_V2_BASE,
        extra_http_headers={"Authorization": f"Bearer {token}"},
    )
    yield ctx
    ctx.dispose()


# ---------------------------------------------------------------------------
# Page pre-navigated to the task manager
# ---------------------------------------------------------------------------

@pytest.fixture
def task_manager_page(page: Page) -> Page:
    """Page already navigated to /task-manager."""
    page.goto(TASK_MANAGER_URL)
    return page


# ---------------------------------------------------------------------------
# Screenshot on failure (autouse — applies to every test automatically)
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def screenshot_on_failure(request):
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed and "page" in request.fixturenames:
        page = request.getfixturevalue("page")
        os.makedirs("screenshots", exist_ok=True)
        safe_name = request.node.name.replace("/", "_").replace(" ", "_")
        page.screenshot(path=f"screenshots/{safe_name}.png", full_page=True)


# Make rep_call available to fixtures above
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


# ---------------------------------------------------------------------------
# Add your own fixtures below this line
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Worker ID — used in parallel execution exercises (Ex08)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def worker_id(request) -> str:
    """Returns xdist worker id ('gw0', 'gw1' ...) or 'master' for single-worker runs."""
    return getattr(request.config, "workerinput", {}).get("workerid", "master")


# ---------------------------------------------------------------------------
# authenticated_page — session-scoped; logs in via the SPA V2 modal once
# and persists browser storage state so subsequent tests skip the login flow.
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def authenticated_page(browser, tmp_path_factory):
    """
    Session-scoped page that is already logged in via the SPA V2 login modal.
    Storage state is saved once and reused — login UI is only hit once per run.

    Usage:
        def test_something(authenticated_page):
            authenticated_page.goto(TASK_MANAGER_URL)
            # already authenticated
    """
    from playwright.sync_api import expect as pw_expect
    state_path = str(tmp_path_factory.mktemp("auth") / "storage_state.json")

    # Step 1: log in once and save storage state
    setup_ctx  = browser.new_context()
    setup_page = setup_ctx.new_page()
    setup_page.goto(TASK_MANAGER_URL)

    # Open Login modal
    setup_page.get_by_role("button", name="Login").first.click()
    pw_expect(setup_page.get_by_role("dialog")).to_be_visible()

    # Select V2 in the modal API selector
    setup_page.get_by_role("combobox").select_option(label="V2")

    # Use quick-fill if available; otherwise fill manually
    fill_btn = setup_page.get_by_role("button", name="test-user-fill")
    if fill_btn.is_visible():
        fill_btn.click()
    else:
        setup_page.get_by_label("Username").fill("user")
        setup_page.get_by_label("Password").fill("user123")

    setup_page.get_by_role("button", name="Login").last.click()
    pw_expect(setup_page.get_by_role("dialog")).not_to_be_visible()

    setup_ctx.storage_state(path=state_path)
    setup_ctx.close()

    # Step 2: restore state in a fresh context — all tests share this page
    auth_ctx  = browser.new_context(storage_state=state_path)
    auth_page = auth_ctx.new_page()
    yield auth_page
    auth_ctx.close()
