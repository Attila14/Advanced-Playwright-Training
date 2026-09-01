"""
test_fixtures.py — Exercise 07: Fixtures & Test Lifecycle

See Exercises/07_FixturesAndTestLifecycle.md for full instructions.
Run: pytest src/tests/test_fixtures.py -v -s

NOTE: The task_factory fixture (Task 1) should live in conftest.py, not in this file.
      The version below is a local stub to illustrate common mistakes.
"""
import json
import uuid
import pytest
from playwright.sync_api import Page, APIRequestContext, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"


# ---------------------------------------------------------------------------
# Task 1 — task_factory fixture (belongs in conftest.py)
# ---------------------------------------------------------------------------

@pytest.fixture
def task_factory(api_v1: APIRequestContext):
    """
    Factory fixture: accepts title, status, priority, labels, description.
    Tracks created task IDs. Yields the make() function.
    Cleans up ALL created tasks in a finally block after the test ends.
    """
    # TODO (this fixture should be in conftest.py):
    # created_ids = []
    # def make(title, status="TODO", priority="LOW", labels=None, description=""):
    #     resp = api_v1.post("/tasks", data=json.dumps({
    #         "title": title, "status": status, "priority": priority,
    #         "labels": labels or [], "description": description,
    #     }), headers={"Content-Type": "application/json"})
    #     assert resp.status == 201
    #     created_ids.append(resp.json()["id"])
    #     return resp.json()
    # yield make
    # for task_id in created_ids:
    #     api_v1.delete(f"/tasks/{task_id}")

    # Developer attempt: returns make immediately — no yield, no teardown
    created_ids = []

    def make(title, status="TODO", priority="LOW"):
        resp = api_v1.post(
            "/tasks",
            data=json.dumps({"title": title, "status": status, "priority": priority}),
            headers={"Content-Type": "application/json"},
        )
        created_ids.append(resp.json()["id"])
        return resp.json()

    return make  # wrong: should be "yield make" and include finally cleanup block


# ---------------------------------------------------------------------------
# Task 2 — Parametrize over statuses and priorities
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("status,priority", [
    ("TODO",        "LOW"),
    ("IN_PROGRESS", "MEDIUM"),
    ("DONE",        "HIGH"),
    ("TODO",        "URGENT"),
])
def test_create_task_parametrized(task_factory, status: str, priority: str):
    # TODO Task 2 — use task_factory to create tasks with each combination,
    # assert response has correct status and priority
    pass


# ---------------------------------------------------------------------------
# Task 3 — Module-scoped shared fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")  # wrong: should be scope="module"
def module_task(api_v1: APIRequestContext):
    """
    Creates a single task once for the entire module.
    All tests in this module read from it — none modify it.
    """
    # TODO: scope="module", create with uuid title, yield, delete in finally
    title = f"Module Task {uuid.uuid4()}"
    resp = api_v1.post(
        "/tasks",
        data=json.dumps({"title": title, "status": "TODO", "priority": "LOW"}),
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


# ---------------------------------------------------------------------------
# Task 4 — Class-scoped autouse fixture
# ---------------------------------------------------------------------------

class TestTaskCreation:
    # TODO Task 4 — implement a class-scoped setup fixture:
    # @pytest.fixture(scope="class", autouse=True)
    # def setup_context(self, api_v1, request):
    #     title = f"Class Task {uuid.uuid4()}"
    #     resp = api_v1.post("/tasks", ...)
    #     request.cls.task = resp.json()
    #     yield
    #     api_v1.delete(f"/tasks/{self.task['id']}")

    def test_task_created(self):
        # TODO: assert self.task["id"] is not None
        pass

    def test_task_is_todo(self):
        # TODO: assert self.task["status"] == "TODO"
        pass

    def test_task_priority_low(self):
        # TODO: assert self.task["priority"] == "LOW"
        pass


# ---------------------------------------------------------------------------
# Task 5 — Autouse log_test_name fixture
# ---------------------------------------------------------------------------

# TODO Task 5 — add to conftest.py:
# @pytest.fixture(autouse=True)
# def log_test_name(request):
#     print(f"\n>>> START: {request.node.name}")
#     yield
#     print(f"\n<<< END:   {request.node.name}")

def test_create_todo_task(task_factory):
    # TODO Task 1+5 — create a task, assert it has an id and status=="TODO"
    # Developer attempt: creates task but factory never deletes it (no yield in fixture)
    task = task_factory(title=f"Todo Task {uuid.uuid4()}", status="TODO", priority="LOW")
    assert task["id"] is not None
    assert task["status"] == "TODO"
    # cleanup never happens because task_factory uses return instead of yield