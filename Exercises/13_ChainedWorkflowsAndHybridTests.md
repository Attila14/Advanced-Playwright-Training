# Exercise 13 — Chained API Workflows & Hybrid Tests

## 🎯 Goal

Write multi-step API workflows where each step uses the output of the previous one. Then combine API and UI automation in hybrid tests — using the API for fast setup and the browser for visual verification.

Before writing any code, **think about the two test layers**:
- The API is 10–20x faster than driving the browser
- The browser is the only way to verify what users actually see
- The best tests use each layer for what it does best

---

## 📖 Background

### Chained workflow pattern

```python
def test_task_lifecycle(api_v1):
    # Step 1 — create
    create_resp = api_v1.post("/tasks", ...)
    task_id = create_resp.json()["id"]

    # Step 2 — update (using id from step 1)
    api_v1.put(f"/tasks/{task_id}", ...)

    # Step 3 — verify (reading back the updated state)
    get_resp = api_v1.get(f"/tasks/{task_id}")
    assert get_resp.json()["status"] == "DONE"
```

### Hybrid test pattern

```python
def test_api_create_ui_verify(api_v1, page):
    # Fast: create via API
    task = api_v1.post("/tasks", ...).json()
    task_id = task["id"]

    try:
        # Slow but visual: verify in browser
        page.goto(f"https://testauto.app/task-manager-spa")
        page.get_by_placeholder("Search tasks...").fill(task["title"])
        page.get_by_placeholder("Search tasks...").press("Enter")
        page.wait_for_load_state("networkidle")
        expect(page.locator("table tbody tr").filter(has_text=task["title"])).to_be_visible()

    finally:
        api_v1.delete(f"/tasks/{task_id}")
```

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/tests/test_workflows.py` | All tasks for this exercise |

---

## ✅ Task 1 — Full CRUD lifecycle chain

Write a single test `test_full_crud_chain` that executes every step in sequence and uses the previous step's output:

| Step | Action | Capture |
|------|--------|---------|
| 1 | `POST /tasks` with title, description, status `IN_PROGRESS`, priority `HIGH`, labels `["chain","test"]` | `task_id` |
| 2 | Assert status `201` and all fields in response | — |
| 3 | `GET /tasks/{task_id}` | `original_updated_at` |
| 4 | `PUT /tasks/{task_id}` — change title and status to `DONE` | — |
| 5 | `GET /tasks/{task_id}` — assert new title, new status, `updatedAt` changed | — |
| 6 | `DELETE /tasks/{task_id}` — assert `200` | — |
| 7 | `GET /tasks/{task_id}` — assert `404` | — |

Wrap in `try/finally`.

---

## ✅ Task 2 — Comment chain

Write `test_comment_chain`:

1. Create a task → get `task_id`
2. Add comment `"First comment"` → get `comment_id`
3. Update comment to `"Updated comment"` → assert updated text in response
4. Add a second comment → get `comment_id_2`
5. Delete `comment_id` → assert `200`
6. Delete `comment_id_2` → assert `200`
7. Delete the task

---

## ✅ Task 3 — Hybrid: API create → UI verify

Write `test_api_create_ui_verify`:

1. Create a task via `api_v1` with a unique, searchable title
2. Navigate to https://testauto.app/task-manager-spa in the browser
3. Search for the task title
4. Assert the row is visible in the table
5. Click the task title to open the detail modal
6. Assert the modal shows the correct status and priority
7. Clean up: delete via API in `finally`

---

## ✅ Task 4 — Hybrid: UI create → API verify

Write `test_ui_create_api_verify`:

1. Navigate to the create modal in the browser
2. Fill in a unique title and submit the form
3. Wait for the task to appear in the table
4. Call `GET /api/v1/tasks?search=<title>` via API
5. Assert the API returns the task with the correct fields
6. Clean up: delete via API in `finally`

---

## ✅ Task 5 — Status transition workflow

Write `test_status_transition_workflow` that moves a task through all three statuses and verifies each transition both via API and in the UI:

| Step | API action | UI assertion |
|------|-----------|-------------|
| 1 | Create with `status=TODO` | Navigate to detail modal — assert status shows `TODO` |
| 2 | `PUT` to `status=IN_PROGRESS` | Reload the detail modal — assert status shows `IN_PROGRESS` |
| 3 | `PUT` to `status=DONE` | Filter UI by `DONE` — assert task appears |

Clean up: delete the task in `finally`.

---

## 🏃 Run your tests

```bash
pytest src/tests/test_workflows.py -v -s --headed
```

---

## 💡 Tips

- In hybrid tests, the API and browser **share the same server** but are **separate HTTP clients**. The browser uses a cookie session; the API uses `APIRequestContext`. A task created via the API is immediately visible in the browser — no need to wait for sync.
- Use `page.wait_for_load_state("networkidle")` after searching to let the filtered results load before asserting.
- `expect(locator).to_be_visible()` has a built-in 5-second retry — use it for UI assertions in hybrid tests to absorb network latency.

---

## 📌 Reference

- [Playwright — APIRequestContext](https://playwright.dev/python/docs/api/class-apirequestcontext)
- [testauto.app API Guide](https://testauto.app/docs/api-guide)
- [testauto.app UI Guide](https://testauto.app/docs/ui-guide)
