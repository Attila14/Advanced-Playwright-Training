"""
test_performance.py — Exercise 04: Performance & Tracing

See Exercises/04_PerformanceAndTracing.md for full instructions.
Run: pytest src/tests/test_performance.py -v -s
"""
import os
import json
import pytest
from playwright.sync_api import Page, Browser, APIRequestContext

TASK_MANAGER = "https://testauto.app/task-manager-spa"
os.makedirs("traces", exist_ok=True)


def test_record_create_task_trace(browser: Browser, api_v1: APIRequestContext):
    # TODO Task 1 — trace a full create flow, save to traces/task-create.zip
    pass


def test_har_captures_api_calls(browser: Browser, tmp_path):
    # TODO Task 2 — capture HAR, assert api.testauto.app calls present, no 4xx
    pass


def test_page_timing_is_acceptable(page: Page):
    # TODO Task 3 — domContentLoaded < 5000ms, load < 10000ms
    pass


def test_no_uncaught_console_errors(page: Page):
    # TODO Task 4 — assert no Uncaught/TypeError/SyntaxError in console
    pass


@pytest.fixture
def traced_page(browser: Browser, request):
    # TODO Task 5 — start tracing, yield page, save trace only on failure
    yield None   # replace with real implementation


def test_traced_page_on_failure(traced_page):
    # Intentional failure — verify trace file appears
    assert False, "Intentional failure — check traces/ for the zip"
