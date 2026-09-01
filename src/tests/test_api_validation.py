"""
test_api_validation.py — Exercise 11: Advanced Response Validation

See Exercises/11_AdvancedResponseValidation.md for full instructions.
Run: pytest src/tests/test_api_validation.py -v -s
"""
import math
import time
import json
import uuid
from playwright.sync_api import APIRequestContext

BASE_V1 = "https://api.testauto.app/api/v1"


# ---------------------------------------------------------------------------
# Helper — implement this (Task 1)
# ---------------------------------------------------------------------------

def validate_task_schema(task: dict) -> None:
    """
    Assert all required fields are present and correctly typed:
    - id        : int or str, non-empty
    - title     : str, len > 0
    - status    : str, one of TODO / IN_PROGRESS / DONE
    - priority  : str, one of LOW / MEDIUM / HIGH / URGENT
    - updatedAt : str, contains "T" and "-"   (ISO 8601)
    Raise AssertionError with a clear message on any failure.
    """
    # TODO Task 1 — implement the schema assertions
    # valid_statuses = {"TODO", "IN_PROGRESS", "DONE"}
    # valid_priorities = {"LOW", "MEDIUM", "HIGH", "URGENT"}
    # assert "id" in task, "missing id"
    # assert "title" in task and len(task["title"]) > 0, "title missing or empty"
    # assert task["status"] in valid_statuses, f"invalid status: {task['status']}"
    # assert task["priority"] in valid_priorities, f"invalid priority: {task['priority']}"
    # assert "updatedAt" in task and "T" in task["updatedAt"] and "-" in task["updatedAt"]
    raise NotImplementedError("validate_task_schema not implemented — see Task 1")  # wrong


# ---------------------------------------------------------------------------
# Task 1 — Schema validation on all returned tasks
# ---------------------------------------------------------------------------

def test_all_tasks_have_valid_schema(api_v1: APIRequestContext):
    """
    GET /tasks, iterate content[], call validate_task_schema() on each.
    Assert no tasks violate the schema.
    """
    # Developer attempt: calls unimplemented helper — will raise NotImplementedError
    resp = api_v1.get("/tasks")
    assert resp.status == 200
    for task in resp.json()["content"]:
        validate_task_schema(task)   # wrong: raises NotImplementedError


# ---------------------------------------------------------------------------
# Task 2 — Pagination assertions
# ---------------------------------------------------------------------------

def test_page_size_respected(api_v1: APIRequestContext):
    """GET /tasks with size=5 — assert len(content) == 5 (when totalElements >= 5)."""
    # Developer attempt: size param not passed — gets default page size instead
    resp = api_v1.get("/tasks")  # wrong: missing params={"size": 5}
    assert resp.status == 200
    # assert len(resp.json()["content"]) == 5  — this would fail because page size not set


def test_total_pages_is_consistent(api_v1: APIRequestContext):
    """GET /tasks?size=5, assert totalPages == ceil(totalElements / size)."""
    # Developer attempt: wrong formula — totalPages compared to totalElements
    resp = api_v1.get("/tasks", params={"size": 5})
    body = resp.json()
    total_elements = body["totalElements"]
    total_pages = body["totalPages"]
    assert total_pages == total_elements  # wrong: should be ceil(totalElements / 5)


def test_page_0_returns_first_records(api_v1: APIRequestContext):
    # TODO Task 2 — assert currentPage == 0, content non-empty
    pass


def test_last_page_is_partial(api_v1: APIRequestContext):
    # TODO Task 2 — navigate to last page, assert content non-empty and <= size
    pass


def test_beyond_last_page_returns_empty(api_v1: APIRequestContext):
    # TODO Task 2 — request page beyond totalPages, assert content == []
    pass


# ---------------------------------------------------------------------------
# Task 3 — Filter and search
# ---------------------------------------------------------------------------

def test_filter_by_status_todo(api_v1: APIRequestContext):
    """GET /tasks?status=TODO — assert every task in content has status == "TODO"."""
    # Developer attempt: only checks HTTP status, not per-task status field
    resp = api_v1.get("/tasks", params={"status": "TODO"})
    assert resp.status == 200  # wrong: must also assert each task["status"] == "TODO"
    # missing: for task in resp.json()["content"]: assert task["status"] == "TODO"


def test_filter_by_status_in_progress(api_v1: APIRequestContext):
    # TODO Task 3 — all returned tasks have status IN_PROGRESS
    pass


def test_filter_by_priority_high(api_v1: APIRequestContext):
    # TODO Task 3 — all returned tasks have priority HIGH
    pass


def test_search_api_in_title(api_v1: APIRequestContext):
    """GET /tasks?search=API — assert every returned task title contains "API" (case-insensitive)."""
    # TODO Task 3 — assert "api" in task["title"].lower() for each task in content
    pass


# ---------------------------------------------------------------------------
# Task 4 — Response time thresholds
# ---------------------------------------------------------------------------

def test_response_time_get_tasks(api_v1: APIRequestContext):
    """GET /tasks must respond in < 3 seconds."""
    # Developer attempt: threshold set to 30 seconds — test never catches slow responses
    start = time.time()
    resp = api_v1.get("/tasks")
    elapsed = time.time() - start
    assert resp.status == 200
    assert elapsed < 30  # wrong: threshold should be 3 seconds


def test_response_time_get_summary(api_v1: APIRequestContext):
    # TODO Task 4 — GET /tasks/summary < 3s
    pass


def test_response_time_create_task(api_v1: APIRequestContext):
    # TODO Task 4 — POST /tasks < 5s; cleanup in finally
    pass


# ---------------------------------------------------------------------------
# Task 5 — Sorting
# ---------------------------------------------------------------------------

def test_sort_priority_desc(api_v1: APIRequestContext):
    # TODO Task 5 — sort=priority,desc — URGENT before HIGH before MEDIUM before LOW
    pass


def test_sort_title_asc(api_v1: APIRequestContext):
    # TODO Task 5 — sort=title,asc — assert titles are alphabetically sorted
    pass