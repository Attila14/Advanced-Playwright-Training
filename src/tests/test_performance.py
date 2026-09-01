"""
test_performance.py — Exercise 04: Performance & Tracing

See Exercises/04_PerformanceAndTracing.md for full instructions.
Run: pytest src/tests/test_performance.py -v -s
     playwright show-trace traces/task-create.zip
"""
import json
import os
import pytest
from playwright.sync_api import Browser, Page, APIRequestContext

TASK_MANAGER = "https://testauto.app/task-manager-spa"
os.makedirs("traces", exist_ok=True)


# ---------------------------------------------------------------------------
# Task 1 — Record a trace of a full create-task flow
# ---------------------------------------------------------------------------

def test_trace_capture(browser: Browser, api_v1: APIRequestContext):
    """
    Start tracing with screenshots=True, snapshots=True, sources=True.
    Navigate, click Add New Task, fill title, submit.
    Wait for task to appear. Stop trace to traces/task-create.zip.
    Assert the file exists. Clean up the created task via api_v1 in finally.
    """
    # TODO:
    # 1. ctx = browser.new_context()
    # 2. ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    # 3. page = ctx.new_page(); page.goto(TASK_MANAGER)
    # 4. Click Add New Task, fill unique title, submit
    # 5. expect(rows.filter(has_text=title)).to_be_visible()
    # 6. ctx.tracing.stop(path="traces/task-create.zip")
    # 7. assert os.path.exists("traces/task-create.zip")
    # 8. ctx.close(); delete task in finally

    # Developer attempt: tracing.start called but tracing.stop never called — no zip file written
    ctx = browser.new_context()
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = ctx.new_page()
    page.goto(TASK_MANAGER)
    page.locator("table tbody tr").first.wait_for()
    # missing: fill create form with unique title and submit
    # missing: ctx.tracing.stop(path="traces/task-create.zip")
    # missing: assert os.path.exists("traces/task-create.zip")
    ctx.close()


# ---------------------------------------------------------------------------
# Task 2 — HAR capture and analysis
# ---------------------------------------------------------------------------

def test_har_capture(browser: Browser, tmp_path):
    """
    Create context with record_har_path. Navigate. Close context (HAR written on close).
    Load and parse the HAR JSON.
    Assert: at least one entry URL contains api.testauto.app,
            all response statuses < 400, at least one URL contains /api/v1/tasks.
    """
    # TODO:
    # 1. har_path = str(tmp_path / "network.har")
    # 2. ctx = browser.new_context(record_har_path=har_path)
    # 3. page = ctx.new_page(); page.goto(TASK_MANAGER); page.wait_for_load_state("networkidle")
    # 4. ctx.close()  — HAR is flushed here
    # 5. import json; har = json.loads(open(har_path).read())
    # 6. entries = har["log"]["entries"]
    # 7. assert any("api.testauto.app" in e["request"]["url"] for e in entries)
    # 8. assert all(e["response"]["status"] < 400 for e in entries)
    # 9. assert any("/api/v1/tasks" in e["request"]["url"] for e in entries)

    # Developer attempt: context created WITHOUT record_har_path — no HAR recorded
    ctx = browser.new_context()  # wrong: missing record_har_path=har_path
    page = ctx.new_page()
    page.goto(TASK_MANAGER)
    ctx.close()
    # missing: all HAR assertions


# ---------------------------------------------------------------------------
# Task 3 — Page timing assertions
# ---------------------------------------------------------------------------

def test_page_performance_metrics(page: Page):
    """
    Navigate and wait for networkidle.
    Read window.performance.timing via page.evaluate().
    Assert domContentLoaded < 5000ms and fullLoad < 10000ms.
    Print both values.
    """
    # TODO:
    # 1. page.goto(TASK_MANAGER); page.wait_for_load_state("networkidle")
    # 2. timing = page.evaluate("() => JSON.parse(JSON.stringify(window.performance.timing))")
    # 3. dom_ready = timing["domContentLoadedEventEnd"] - timing["navigationStart"]
    # 4. full_load = timing["loadEventEnd"] - timing["navigationStart"]
    # 5. print(f"DOM ready: {dom_ready}ms, Full load: {full_load}ms")
    # 6. assert dom_ready < 5000
    # 7. assert full_load < 10000

    # Developer attempt: metrics fetched but never parsed or asserted
    page.goto(TASK_MANAGER)
    page.wait_for_load_state("networkidle")
    metrics = page.evaluate("JSON.stringify(window.performance.timing)")
    # missing: parse json, compute dom_ready and full_load, print, assert


# ---------------------------------------------------------------------------
# Task 4 — Console error detection
# ---------------------------------------------------------------------------

def test_console_error_monitoring(page: Page):
    """
    Attach page.on("console") listener before navigating.
    Collect messages where msg.type == "error".
    Filter for "Uncaught", "TypeError", "SyntaxError".
    Assert none were found.
    """
    # TODO:
    # 1. errors = []
    # 2. page.on("console", lambda msg: errors.append(msg) if msg.type == "error" else None)
    # 3. page.goto(TASK_MANAGER); page.locator("table tbody tr").first.wait_for()
    # 4. critical = [m.text for m in errors if any(k in m.text for k in ("Uncaught","TypeError","SyntaxError"))]
    # 5. assert critical == [], f"JS errors found: {critical}"

    # Developer attempt: listener collects all messages but never filters by type or asserts
    all_messages = []
    page.on("console", lambda msg: all_messages.append(msg))  # wrong: should filter msg.type=="error"
    page.goto(TASK_MANAGER)
    page.locator("table tbody tr").first.wait_for()
    # missing: filter and assert no critical errors


# ---------------------------------------------------------------------------
# Task 5 — Auto-save trace on test failure
# ---------------------------------------------------------------------------

@pytest.fixture
def traced_page(browser, request):
    # TODO Task 5 — fixture that starts tracing, saves zip on failure only
    # 1. ctx = browser.new_context()
    # 2. ctx.tracing.start(screenshots=True, snapshots=True)
    # 3. page = ctx.new_page(); yield page
    # 4. rep = getattr(request.node, "rep_call", None)
    # 5. if rep and rep.failed: ctx.tracing.stop(path=f"traces/{request.node.name}.zip")
    # 6. else: ctx.tracing.stop()
    # 7. ctx.close()
    pass


def test_intentional_failure_with_trace(traced_page):
    # TODO Task 5 — use traced_page fixture, intentionally fail, verify traces/<name>.zip appears
    pass