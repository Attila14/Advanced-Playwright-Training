"""
test_parallel.py — Exercise 08: Parallel Execution & Test Isolation

See Exercises/08_ParallelExecution.md for full instructions.
Run: pytest src/tests/test_parallel.py -v -n auto
     pytest src/tests/test_parallel.py -v -n auto --shard=1/2  (Task 4)
"""
import json
import uuid
import pytest
from playwright.sync_api import APIRequestContext, Page, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"


# ---------------------------------------------------------------------------
# Task 1 — Fix existing parallel-unsafe tests
# ---------------------------------------------------------------------------

def test_parallel_alpha(api_v1: APIRequestContext):
    """
    Create a task, assert 201, delete it.
    Title MUST be unique per run so parallel workers don't collide.
    """
    # TODO Task 1 — use uuid-based title and try/finally cleanup
    # Developer attempt: hardcoded title — collides when two workers run simultaneously
    title = "Parallel Alpha Task"  # wrong: hardcoded — breaks under -n auto
    task_id = None
    resp = api_v1.post(
        "/tasks",
        data=json.dumps({"title": title, "status": "TODO", "priority": "LOW"}),
        headers={"Content-Type": "application/json"},
    )
    assert resp.status == 201
    task_id = resp.json()["id"]
    api_v1.delete(f"/tasks/{task_id}")   # wrong: outside try/finally — leaks on failure


# ---------------------------------------------------------------------------
# Task 2 — Worker ID fixture
# ---------------------------------------------------------------------------

def test_worker_id_is_available(worker_id: str):
    """
    Print the worker_id provided by pytest-xdist.
    Assert it is a non-empty string.
    (worker_id fixture already defined in conftest.py)
    """
    # TODO Task 2 — print worker_id, assert non-empty
    print(f"Running on worker: {worker_id}")
    assert isinstance(worker_id, str) and len(worker_id) > 0


# ---------------------------------------------------------------------------
# Task 3 — Five fully isolated parallel tests
# ---------------------------------------------------------------------------

def test_parallel_beta(api_v1: APIRequestContext):
    """Create a uuid-titled task, assert 201, delete in finally."""
    # TODO Task 3
    title = f"Parallel Beta {uuid.uuid4()}"
    task_id = None
    try:
        resp = api_v1.post(
            "/tasks",
            data=json.dumps({"title": title, "status": "TODO", "priority": "LOW"}),
            headers={"Content-Type": "application/json"},
        )
        assert resp.status == 201
        task_id = resp.json()["id"]
    finally:
        if task_id:
            api_v1.delete(f"/tasks/{task_id}")


def test_parallel_gamma(api_v1: APIRequestContext):
    """Create a uuid-titled task with IN_PROGRESS status, assert priority field present."""
    # TODO Task 3
    pass


def test_parallel_delta(api_v1: APIRequestContext):
    """Create a uuid-titled task with HIGH priority, assert id is int."""
    # TODO Task 3
    pass


def test_parallel_epsilon(api_v1: APIRequestContext):
    """Create a uuid-titled task with URGENT priority and DONE status, verify via GET."""
    # TODO Task 3
    pass


# ---------------------------------------------------------------------------
# Task 4 — Sharding demonstration
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_slow_full_flow(page: Page, api_v1: APIRequestContext):
    """
    Create a task via API, navigate to Task Manager, search for it, assert visible, clean up.
    Mark as @pytest.mark.slow so it is included in a slow shard only.
    """
    # TODO Task 4 — implement full flow with uuid title
    # Run half tests in shard 1, half in shard 2:
    # pytest src/tests/test_parallel.py -n auto --shard=1/2
    # pytest src/tests/test_parallel.py -n auto --shard=2/2

    # Developer attempt: networkidle used instead of expect(), bare assert on count
    title = f"Slow Task {uuid.uuid4()}"
    task_id = None
    try:
        resp = api_v1.post(
            "/tasks",
            data=json.dumps({"title": title, "status": "TODO", "priority": "LOW"}),
            headers={"Content-Type": "application/json"},
        )
        task_id = resp.json()["id"]
        page.goto(TASK_MANAGER)
        page.wait_for_load_state("networkidle")  # wrong: use expect()
        count = page.locator("table tbody tr").count()
        assert count > 0  # wrong: assert specific task visible with filter(has_text=title)
    finally:
        if task_id:
            api_v1.delete(f"/tasks/{task_id}")


# ---------------------------------------------------------------------------
# Task 5 — Fast/slow markers
# ---------------------------------------------------------------------------

@pytest.mark.fast
def test_api_health(api_v1: APIRequestContext):
    """GET /tasks — assert 200. Fast test, no DB side effects."""
    resp = api_v1.get("/tasks")
    assert resp.status == 200