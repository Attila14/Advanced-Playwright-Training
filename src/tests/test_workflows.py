"""
test_workflows.py — Exercise 13: Chained Workflows & Hybrid Tests

See Exercises/13_ChainedWorkflowsAndHybridTests.md for full instructions.
Run: pytest src/tests/test_workflows.py -v --headed
"""
import json
import uuid
from playwright.sync_api import Page, APIRequestContext, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"


# ---------------------------------------------------------------------------
# Task 1 — Full API CRUD chain
# ---------------------------------------------------------------------------

def test_full_crud_chain(api_v1: APIRequestContext):
    """
    1. POST /tasks (title=uuid, desc, status=IN_PROGRESS, priority=HIGH, labels=[chain,test])
    2. GET /tasks/{id} — assert all fields match
    3. PUT /tasks/{id} — update title and status=DONE
    4. GET /tasks/{id} — assert updated title and status
    5. DELETE /tasks/{id}
    6. GET /tasks/{id} — assert 404
    """
    # TODO:
    # try: POST → GET → PUT → GET → DELETE
    # finally: DELETE if task still exists (safe cleanup)

    # Developer attempt: create + read done; update and 404 verification missing
    title = f"CRUD Chain {uuid.uuid4()}"
    task_id = None
    try:
        resp = api_v1.post(
            "/tasks",
            data=json.dumps({
                "title": title,
                "description": "Chained workflow task",
                "status": "IN_PROGRESS",
                "priority": "HIGH",
                "labels": ["chain", "test"],
            }),
            headers={"Content-Type": "application/json"},
        )
        assert resp.status == 201
        task_id = resp.json()["id"]

        get_resp = api_v1.get(f"/tasks/{task_id}")
        assert get_resp.status == 200
        assert get_resp.json()["title"] == title

        # missing: PUT /tasks/{task_id} to update title and status=DONE
        # missing: GET /tasks/{task_id} to verify updated fields
        # missing: DELETE and 404 check

    finally:
        if task_id:
            api_v1.delete(f"/tasks/{task_id}")


# ---------------------------------------------------------------------------
# Task 2 — Comment chain
# ---------------------------------------------------------------------------

def test_comment_chain(api_v1: APIRequestContext):
    """
    1. Create a task.
    2. POST /tasks/{id}/comments — "First comment" → save comment_id.
    3. PUT /tasks/{id}/comments/{comment_id} — update to "Updated comment".
    4. POST /tasks/{id}/comments — "Second comment" → save second_comment_id.
    5. DELETE both comments.
    6. DELETE the task.
    """
    # TODO Task 2 — implement full comment chain with cleanup
    pass


# ---------------------------------------------------------------------------
# Task 3 — API create → UI verify (hybrid)
# ---------------------------------------------------------------------------

def test_api_create_ui_verify(page: Page, api_v1: APIRequestContext):
    """
    1. Create task via API with unique uuid title (status=TODO, priority=MEDIUM).
    2. Navigate to Task Manager.
    3. Search for the title — assert the row is visible.
    4. Click the row to open the detail modal.
    5. Assert status and priority are visible in the modal.
    6. Delete the task via API in finally.
    """
    # TODO Task 3 — complete the UI navigation and modal assertion

    # Developer attempt: API create done but navigation and modal assertion missing
    title = f"Hybrid Task {uuid.uuid4()}"
    task_id = None
    try:
        resp = api_v1.post(
            "/tasks",
            data=json.dumps({"title": title, "status": "TODO", "priority": "MEDIUM"}),
            headers={"Content-Type": "application/json"},
        )
        assert resp.status == 201
        task_id = resp.json()["id"]

        # missing: page.goto(TASK_MANAGER)
        # missing: search for title
        # missing: expect(page.locator("table tbody tr").filter(has_text=title)).to_be_visible()
        # missing: click row to open detail modal
        # missing: expect(page.get_by_text("TODO")).to_be_visible() — status in modal
        # missing: expect(page.get_by_text("MEDIUM")).to_be_visible() — priority in modal

    finally:
        if task_id:
            api_v1.delete(f"/tasks/{task_id}")


# ---------------------------------------------------------------------------
# Task 4 — UI create → API verify (hybrid)
# ---------------------------------------------------------------------------

def test_ui_create_api_verify(page: Page, api_v1: APIRequestContext):
    """
    1. Navigate to Task Manager.
    2. Click Add New Task, fill a unique title, submit.
    3. Wait for the row to appear in the table.
    4. GET /tasks?search={title} via API — assert 200 and task present in content.
    5. Clean up the task via API in finally.
    """
    # TODO Task 4 — UI creates task, API verifies it exists
    pass


# ---------------------------------------------------------------------------
# Task 5 — Status transition workflow
# ---------------------------------------------------------------------------

def test_status_transition(page: Page, api_v1: APIRequestContext):
    """
    1. Create task via API as TODO.
    2. Navigate to detail modal — assert status shows TODO.
    3. PUT /tasks/{id} status=IN_PROGRESS.
    4. Reload page and navigate to detail — assert IN_PROGRESS.
    5. PUT /tasks/{id} status=DONE.
    6. Use status filter DONE — assert task appears.
    7. Delete in finally.
    """
    # TODO Task 5 — three-state transition test
    pass