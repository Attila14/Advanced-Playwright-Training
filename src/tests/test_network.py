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
    def handle(route: Route):
        route.fulfill(status=200, content_type="application/json", body=json.dumps(EMPTY_RESPONSE))

    page.route("**/api/v1/tasks**", handle)
    page.goto(TASK_MANAGER)
    expect(page.locator("table tbody tr")).to_have_count(0)


# ---------------------------------------------------------------------------
# Task 2 — Inject a task into a real response
# ---------------------------------------------------------------------------

def test_inject_task_into_real_response(page: Page):
    """
    Intercept GET /api/v1/tasks, fetch the real response, prepend a fake task,
    and assert "INJECTED TASK" appears in the table without creating real data.
    """
    fake_task = {"id": 99999, "title": "INJECTED TASK", "status": "TODO", "priority": "URGENT",
                 "updatedAt": "2026-01-01T00:00:00Z"}

    def handle(route: Route):
        real = route.fetch()
        data = real.json()
        if "content" in data:
            data["content"].insert(0, fake_task)
            route.fulfill(response=real, body=json.dumps(data))
        else:
            route.fulfill(response=real)

    page.route("**/api/v1/tasks**", handle)
    page.goto(TASK_MANAGER)
    expect(page.locator("table").get_by_text("INJECTED TASK")).to_be_visible()


# ---------------------------------------------------------------------------
# Task 3 — Capture and inspect outgoing requests
# ---------------------------------------------------------------------------

def test_capture_search_request(page: Page):
    """
    Register a page.on("request") listener, navigate, search for "Deploy",
    then assert at least one captured URL contains /api/v1/tasks with a search param.
    """
    captured = []
    page.on("request", lambda r: captured.append(r) if "/api/v1/tasks" in r.url and "summary" not in r.url else None)
    page.goto(TASK_MANAGER)
    page.get_by_placeholder("Search tasks...").fill("Deploy")
    page.get_by_placeholder("Search tasks...").press("Enter")
    page.wait_for_load_state("networkidle")
    assert any("Deploy" in r.url or "search" in r.url.lower() for r in captured)


# ---------------------------------------------------------------------------
# Task 4 — Simulate a server error
# ---------------------------------------------------------------------------

def test_api_500_error_state(page: Page):
    """
    Route **/api/v1/tasks** to return status 500.
    Navigate and assert the UI shows an error message or empty state.
    Print the page content to document what the app renders.
    """
    def handle(route: Route):
        route.fulfill(status=500, body="Internal Server Error")

    page.route("**/api/v1/tasks**", handle)
    page.goto(TASK_MANAGER)
    print(page.content())
    expect(page.locator("table tbody tr")).to_have_count(0)


# ---------------------------------------------------------------------------
# Task 5 — Slow network simulation
# ---------------------------------------------------------------------------

def test_slow_network_simulation(page: Page):
    """
    Register a route handler that sleeps 3 seconds then calls route.continue_().
    Record start time, navigate with timeout=15000, assert elapsed >= 2.5s and page loaded.
    """
    def slow_handler(route: Route):
        time.sleep(3)
        route.continue_()

    page.route("**/api/v1/tasks**", slow_handler)
    start = time.time()
    page.goto(TASK_MANAGER, timeout=15000)
    # Wait for the table — this blocks until the slow handler has responded
    expect(page.locator("table tbody tr").first).to_be_visible(timeout=12000)
    elapsed = time.time() - start
    assert elapsed >= 2.5