"""
test_api_data.py — Exercise 12: API Test Data Management

See Exercises/12_APITestDataManagement.md for full instructions.
Run: pytest src/tests/test_api_data.py -v -s
"""
import json
import uuid
import pytest
from playwright.sync_api import APIRequestContext


# ---------------------------------------------------------------------------
# Task 1 — Rich task_factory fixture (full field set)
# ---------------------------------------------------------------------------

@pytest.fixture
def task_factory(api_v1: APIRequestContext):
    """
    Factory that accepts all fields: title, description, status, priority, labels, dueDate.
    Tracks created IDs. Yields make(). Deletes ALL created tasks in finally.
    """
    # TODO Task 1 — implement with all fields and proper yield/finally
    # created_ids = []
    # def make(title, description="", status="TODO", priority="LOW", labels=None, due_date=None):
    #     payload = {"title": title, "description": description, "status": status, "priority": priority}
    #     if labels: payload["labels"] = labels
    #     if due_date: payload["dueDate"] = due_date
    #     resp = api_v1.post("/tasks", data=json.dumps(payload), headers={...})
    #     assert resp.status == 201
    #     created_ids.append(resp.json()["id"])
    #     return resp.json()
    # yield make
    # finally:
    #     for id_ in created_ids: api_v1.delete(f"/tasks/{id_}")

    # Developer attempt: return instead of yield — tasks are never deleted after test
    created_ids = []

    def make(title, description="", status="TODO", priority="LOW", labels=None, due_date=None):
        payload = {"title": title, "status": status, "priority": priority}
        if description:
            payload["description"] = description
        resp = api_v1.post(
            "/tasks",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )
        assert resp.status == 201
        created_ids.append(resp.json()["id"])
        return resp.json()

    return make  # wrong: should be "yield make" with finally cleanup block


def test_create_task_with_all_fields(task_factory):
    """Create a task with all fields populated. Assert each field in the response."""
    # TODO Task 1 — pass labels=["feature","backend"], description, due_date
    title = f"Full Task {uuid.uuid4()}"
    task = task_factory(title=title, description="A rich task", status="TODO", priority="HIGH")
    assert task["title"] == title
    assert task["priority"] == "HIGH"
    # missing: assert description, labels, dueDate fields


# ---------------------------------------------------------------------------
# Task 2 — task_with_comments fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def task_with_comments(api_v1: APIRequestContext):
    """
    Create a task, add 3 comments, yield {"task": task_dict, "comment_ids": [id1, id2, id3]}.
    Teardown: delete all comments, then delete the task.
    """
    # TODO Task 2 — create task, POST 3 comments, yield, then cleanup comments then task
    # Currently not implemented
    pass


def test_task_has_three_comments(task_with_comments):
    # TODO Task 2 — assert task_with_comments["task"]["id"] exists, len(comment_ids) == 3
    pass


# ---------------------------------------------------------------------------
# Task 3 — bulk_task_factory fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def bulk_task_factory(api_v1: APIRequestContext):
    """
    Creates N tasks with uuid titles. Yields a list of task dicts.
    Teardown: deletes ALL created tasks.
    """
    # TODO Task 3 — create N tasks, yield list, delete ALL in finally
    created_ids = []

    def make(n: int, status="TODO", priority="LOW"):
        tasks = []
        for _ in range(n):
            resp = api_v1.post(
                "/tasks",
                data=json.dumps({"title": f"Bulk {uuid.uuid4()}", "status": status, "priority": priority}),
                headers={"Content-Type": "application/json"},
            )
            tasks.append(resp.json())
            created_ids.append(resp.json()["id"])
        return tasks

    yield make

    # Developer attempt: only first task deleted — the rest leak
    if created_ids:
        api_v1.delete(f"/tasks/{created_ids[0]}")  # wrong: must delete ALL with a loop


def test_bulk_pagination(bulk_task_factory, api_v1: APIRequestContext):
    """Create 15 tasks. Assert page 0 has 10 items. Assert page 1 has >= 5."""
    # TODO Task 3
    # tasks = bulk_task_factory(15)
    # page0 = api_v1.get("/tasks", params={"size": 10, "page": 0})
    # assert len(page0.json()["content"]) == 10
    # page1 = api_v1.get("/tasks", params={"size": 10, "page": 1})
    # assert len(page1.json()["content"]) >= 5
    pass


# ---------------------------------------------------------------------------
# Task 4 — Module-scoped task (read-only across 4 tests)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")  # wrong: should be scope="module"
def module_task(api_v1: APIRequestContext):
    """Single task created once for the module. Tests are read-only."""
    title = f"Module Task {uuid.uuid4()}"
    resp = api_v1.post(
        "/tasks",
        data=json.dumps({"title": title, "status": "TODO", "priority": "MEDIUM"}),
        headers={"Content-Type": "application/json"},
    )
    task = resp.json()
    yield task
    api_v1.delete(f"/tasks/{task['id']}")


def test_module_task_has_id(module_task):
    assert "id" in module_task


def test_module_task_has_title(module_task):
    assert len(module_task["title"]) > 0


def test_module_task_status_is_todo(module_task):
    assert module_task["status"] == "TODO"


def test_module_task_priority_is_medium(module_task):
    assert module_task["priority"] == "MEDIUM"


# ---------------------------------------------------------------------------
# Task 5 — Prove cleanup works even when the test fails
# ---------------------------------------------------------------------------

def test_cleanup_runs_on_failure(task_factory, api_v1: APIRequestContext):
    """
    Create a task via task_factory. Intentionally fail the test.
    After the test run, verify via GET /tasks that the task was deleted.
    (The fixture cleanup should have run even on failure — but it won't with "return make".)
    """
    # TODO Task 5 — create task, record id, assert False to force failure,
    # then in a separate test verify the task is gone
    task = task_factory(title=f"Fail Task {uuid.uuid4()}")
    assert False, "Intentional failure — fixture should still delete the task"