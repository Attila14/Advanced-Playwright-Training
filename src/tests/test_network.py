"""
test_network.py — Exercise 02: Network Interception

See Exercises/02_NetworkInterception.md for full instructions.
Run: pytest src/tests/test_network.py -v --headed
"""
import json
import time
from playwright.sync_api import Page, Route, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"
EMPTY_RESPONSE = {"content": [], "totalElements": 0, "totalPages": 0, "currentPage": 0}


# ---------------------------------------------------------------------------
# Task 1 — Stub an empty task list
# ---------------------------------------------------------------------------

def test_stub_empty_task_list(page: Page):
    """
    Route **/api/v1/tasks** to return EMPTY_RESPONSE.
    Navigate and assert the UI shows zero rows or an empty-state message.
    """
    # TODO:
    # 1. page.route("**/api/v1/tasks**", handler that fulfills with EMPTY_RESPONSE)
    # 2. page.goto(TASK_MANAGER)
    # 3. Assert table has 0 rows OR an empty-state element is visible

    # Developer attempt: route registered and fulfilled correctly, but no UI assertion
    def handle(route: Route):
        route.fulfill(status=200, content_type="application/json", body=json.dumps(EMPTY_RESPONSE))

    page.route("**/api/v1/tasks**", handle)
    page.goto(TASK_MANAGER)
    # missing: assert page.locator("table tbody tr").count() == 0
    # missing: or expect(page.get_by_text("No tasks")).to_be_visible()


# ---------------------------------------------------------------------------
# Task 2 — Inject a task into a real response
# ---------------------------------------------------------------------------

def test_inject_task_into_real_response(page: Page):
    """
    Intercept GET /api/v1/tasks, fetch the real response, prepend a fake task,
    and assert "INJECTED TASK" appears in the table without creating real data.
    """
    # TODO:
    # 1. def handle(route): real = route.fetch(); data = real.json(); data["content"].insert(0, fake_task); route.fulfill(response=real, body=json.dumps(data))
    # 2. page.route("**/api/v1/tasks**", handle)
    # 3. page.goto(TASK_MANAGER)
    # 4. expect(page.get_by_text("INJECTED TASK")).to_be_visible()

    # Developer attempt: replaces entire response with a bare dict — not a paginated shape,
    # so the SPA receives unexpected data and likely shows nothing or crashes
    fake_task = {"id": 99999, "title": "INJECTED TASK", "status": "TODO", "priority": "URGENT",
                 "updatedAt": "2026-01-01T00:00:00Z"}

    def handle(route: Route):
        route.fulfill(json=fake_task)  # wrong: must fetch real response and inject into content[]

    page.route("**/api/v1/tasks**", handle)
    page.goto(TASK_MANAGER)
    # missing: expect(page.get_by_text("INJECTED TASK")).to_be_visible()


# ---------------------------------------------------------------------------
# Task 3 — Capture and inspect outgoing requests
# ---------------------------------------------------------------------------

def test_capture_search_request(page: Page):
    """
    Register a page.on("request") listener, navigate, search for "Deploy",
    then assert at least one captured URL contains /api/v1/tasks with a search param.
    """
    # TODO:
    # 1. captured = []
    # 2. page.on("request", lambda r: captured.append(r) if "/tasks" in r.url else None)
    # 3. page.goto(TASK_MANAGER)
    # 4. page.get_by_placeholder("Search tasks...").fill("Deploy")
    # 5. page.get_by_placeholder("Search tasks...").press("Enter")
    # 6. page.wait_for_load_state("networkidle")
    # 7. assert any("search" in r.url for r in captured)

    # Developer attempt: uses expect_request as a context manager AFTER goto, so the
    # initial tasks request has already fired — the with-block will timeout
    page.goto(TASK_MANAGER)
    with page.expect_request("**/tasks**") as req_info:  # wrong: too late, request already sent
        pass
    assert "search" in req_info.value.url


# ---------------------------------------------------------------------------
# Task 4 — Simulate a server error
# ---------------------------------------------------------------------------

def test_api_500_error_state(page: Page):
    """
    Route **/api/v1/tasks** to return status 500.
    Navigate and assert the UI shows an error message or empty state.
    Print the page content to document what the app renders.
    """
    # TODO:
    # 1. page.route("**/api/v1/tasks**", lambda route: route.fulfill(status=500))
    # 2. page.goto(TASK_MANAGER)
    # 3. print(page.content())  — document what the app renders
    # 4. Assert an error/fallback element is visible (or zero rows)

    # Developer attempt: 500 stub is correct but time.sleep used and no assertion made
    def handle(route: Route):
        route.fulfill(status=500, body="Internal Server Error")

    page.route("**/api/v1/tasks**", handle)
    page.goto(TASK_MANAGER)
    time.sleep(1)  # wrong: use expect() — sleep is flaky and doesn't guarantee anything
    # missing: assert error state element or empty table


# ---------------------------------------------------------------------------
# Task 5 — Slow network simulation
# ---------------------------------------------------------------------------

def test_slow_network_simulation(page: Page):
    """
    Register a route handler that sleeps 3 seconds then calls route.continue_().
    Record start time, navigate with timeout=15000, assert elapsed >= 2.5s and page loaded.
    """
    # TODO:
    # 1. def slow_handler(route): time.sleep(3); route.continue_()
    # 2. page.route("**/api/v1/tasks**", slow_handler)
    # 3. start = time.time()
    # 4. page.goto(TASK_MANAGER, timeout=15000)
    # 5. elapsed = time.time() - start
    # 6. assert elapsed >= 2.5
    # 7. expect(page.locator("table tbody tr").first).to_be_visible()
    pass