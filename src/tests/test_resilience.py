"""
test_resilience.py — Exercise 15: Resilience & Edge Cases

See Exercises/15_ResilienceAndEdgeCases.md for full instructions.
Run: pytest src/tests/test_resilience.py -v -s

Buggy endpoint: https://api.testauto.app/api/buggy (returns random 500s)
"""
import json
import threading
import time
import uuid
from playwright.sync_api import Browser, APIRequestContext, Playwright


BUGGY_BASE = "https://api.testauto.app/api/buggy"


# ---------------------------------------------------------------------------
# Helper — implement this (Task 1)
# ---------------------------------------------------------------------------

def call_with_retry(fn, max_attempts=5):
    """
    Call fn() up to max_attempts times with exponential backoff.
    Backoff: 0.5 * (2 ** (attempt - 1)) seconds between retries.
    Return the successful response. Raise the last exception if all attempts fail.
    """
    # TODO Task 1:
    # last_exc = None
    # for attempt in range(1, max_attempts + 1):
    #     try:
    #         return fn()
    #     except Exception as e:
    #         last_exc = e
    #         if attempt < max_attempts:
    #             time.sleep(0.5 * (2 ** (attempt - 1)))
    # raise last_exc
    raise NotImplementedError("call_with_retry not implemented — see Task 1")  # wrong


# ---------------------------------------------------------------------------
# Task 1 — Retry against the buggy endpoint
# ---------------------------------------------------------------------------

def test_retry_buggy_endpoint(playwright: Playwright):
    """
    Use call_with_retry to GET /tasks from the buggy endpoint.
    Assert the successful response has a "content" key.
    Assert the returned task schema matches the V1 schema (same keys).
    """
    # Developer attempt: calls the unimplemented helper — raises NotImplementedError
    ctx = playwright.request.new_context(base_url=BUGGY_BASE)
    try:
        resp = call_with_retry(lambda: ctx.get("/tasks"))  # wrong: raises NotImplementedError
        assert resp.status == 200
        assert "content" in resp.json()
    finally:
        ctx.dispose()


# ---------------------------------------------------------------------------
# Task 2 — Boundary: title length
# ---------------------------------------------------------------------------

def test_boundary_empty_title(playwright: Playwright):
    """POST task with title="" — assert 400 or 422 (empty title is invalid)."""
    # Developer attempt: asserts 201 instead of 400/422
    ctx = playwright.request.new_context(base_url="https://api.testauto.app/api/v1")
    try:
        resp = ctx.post(
            "/tasks",
            data=json.dumps({"title": "", "status": "TODO", "priority": "LOW"}),
            headers={"Content-Type": "application/json"},
        )
        assert resp.status == 201  # wrong: should be 400 or 422 — empty title must be rejected
    finally:
        ctx.dispose()


def test_boundary_single_char_title(playwright: Playwright):
    # TODO Task 2 — single char title → assert 201, cleanup in finally
    pass


def test_boundary_255_char_title(playwright: Playwright):
    # TODO Task 2 — 255-char title → assert 201, cleanup in finally
    pass


def test_boundary_long_title(playwright: Playwright):
    """POST task with 256-char title — document whether 400 or 201."""
    # Developer attempt: long title sent but no cleanup in finally
    ctx = playwright.request.new_context(base_url="https://api.testauto.app/api/v1")
    try:
        resp = ctx.post(
            "/tasks",
            data=json.dumps({"title": "A" * 256, "status": "TODO", "priority": "LOW"}),
            headers={"Content-Type": "application/json"},
        )
        print(f"256-char title status: {resp.status}")  # document behaviour
        task_id = resp.json().get("id") if resp.status == 201 else None
        # missing: cleanup — if task_id: ctx.delete(f"/tasks/{task_id}")
    finally:
        ctx.dispose()


# ---------------------------------------------------------------------------
# Task 3 — Invalid enum values
# ---------------------------------------------------------------------------

def test_invalid_status_pending(playwright: Playwright):
    """POST with status="PENDING" — assert 400 or 422."""
    ctx = playwright.request.new_context(base_url="https://api.testauto.app/api/v1")
    try:
        resp = ctx.post(
            "/tasks",
            data=json.dumps({"title": f"Bad Status {uuid.uuid4()}", "status": "PENDING", "priority": "LOW"}),
            headers={"Content-Type": "application/json"},
        )
        assert resp.status in (400, 422)
    finally:
        ctx.dispose()


def test_invalid_priority_extreme(playwright: Playwright):
    # TODO Task 3 — priority="EXTREME" → assert 400 or 422
    pass


# ---------------------------------------------------------------------------
# Task 4 — Missing / null fields
# ---------------------------------------------------------------------------

def test_empty_body(playwright: Playwright):
    # TODO Task 4 — POST {} → assert 400 or 422, never 500
    pass


def test_no_title_field(playwright: Playwright):
    # TODO Task 4 — POST {status,priority} without title → assert 400 or 422
    pass


# ---------------------------------------------------------------------------
# Task 5 — Concurrent requests (threading)
# ---------------------------------------------------------------------------

def test_concurrent_requests(playwright: Playwright):
    """
    Launch 5 threads, each using a new browser context and APIRequestContext.
    Each thread creates one uuid-titled task.
    All must succeed (200/201), no 500s.
    Assert 5 unique task IDs returned.
    Clean up all tasks in finally.
    """
    # Developer attempt: sequential for loop — not actually concurrent
    created = []
    for i in range(5):
        ctx = playwright.request.new_context(base_url="https://api.testauto.app/api/v1")
        try:
            resp = ctx.post(
                "/tasks",
                data=json.dumps({"title": f"Concurrent {i}", "status": "TODO", "priority": "LOW"}),
                headers={"Content-Type": "application/json"},
            )
            # wrong: hardcoded title "Concurrent {i}" — parallel runs would collide
            assert resp.status in (200, 201)
            created.append(resp.json()["id"])
        finally:
            ctx.dispose()

    assert len(set(created)) == 5  # IDs may happen to differ but approach is wrong

    # wrong: should use threading.Thread; each thread should create its own new_context;
    # missing: cleanup all created tasks