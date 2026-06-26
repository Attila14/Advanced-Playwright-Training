# Exercise 12 — API Fixtures & Test Data Management

## 🎯 Goal

Design API test fixtures that create realistic, self-cleaning test data — so every test starts with a clean, known state and leaves no leftovers in the shared testauto.app environment.

Before writing any code, **check the current task list**:

```bash
curl "https://api.testauto.app/api/v1/tasks?search=test" | python -m json.tool
```

If you see orphaned tasks from previous training runs — that is the problem this exercise solves.

---

## 📖 Background

### Why cleanup matters on a shared site

testauto.app is used by everyone in this training simultaneously. Without cleanup:
- `GET /tasks?search=test` returns tasks from every trainee
- Count-based assertions break because another trainee added tasks
- The environment degrades over time

### The factory pattern — create, use, delete

```python
@pytest.fixture
def task_factory(api_v1):
    created_ids = []

    def _create(**fields):
        resp = api_v1.post("/tasks",
            data=json.dumps({
                "title":    fields.get("title", "Test task"),
                "status":   fields.get("status", "TODO"),
                "priority": fields.get("priority", "MEDIUM"),
            }),
            headers={"Content-Type": "application/json"})
        assert resp.ok, f"Create failed: {resp.status}"
        task = resp.json()
        created_ids.append(task["id"])
        return task

    yield _create

    for tid in created_ids:
        api_v1.delete(f"/tasks/{tid}")   # always runs — even on test failure
```

### try/finally in tests

```python
def test_crud(api_v1):
    task_id = None
    try:
        resp = api_v1.post("/tasks", ...)
        task_id = resp.json()["id"]
        # ... test body ...
    finally:
        if task_id:
            api_v1.delete(f"/tasks/{task_id}")
```

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/conftest.py` | Add `task_factory`, `task_with_comments`, `bulk_task_factory` |
| `src/tests/test_api_data.py` | Tests using the fixtures |

---

## ✅ Task 1 — Task factory with all fields

Extend `task_factory` in `src/conftest.py` to support all task fields:

| Field | Type | Example |
|-------|------|---------|
| `title` | `str` | `"Fix login bug"` |
| `description` | `str` | `"Steps to reproduce..."` |
| `status` | `str` | `"IN_PROGRESS"` |
| `priority` | `str` | `"HIGH"` |
| `labels` | `list[str]` | `["backend", "urgent"]` |
| `dueDate` | `str` | `"2026-12-31"` |

Write a test that creates a task with all fields populated and asserts each field in the response.

---

## ✅ Task 2 — Task with comments fixture

Create a `task_with_comments` fixture that:
1. Creates a task via `task_factory`
2. Adds 3 comments via `POST /tasks/{id}/comments`
3. Returns a dict: `{"task": {...}, "comment_ids": [...]}`
4. Cleans up comments then task in teardown

Write a test that uses `task_with_comments` and asserts the task and all 3 comments exist.

---

## ✅ Task 3 — Bulk factory for pagination testing

Create a `bulk_task_factory` fixture that creates N tasks at once:

```python
@pytest.fixture
def bulk_task_factory(api_v1):
    def _create(n: int, **base_fields) -> list[dict]:
        # create n tasks, each with a unique uuid-based title
        ...
    yield _create
    # cleanup all created tasks
```

Use it to create 15 tasks, then assert:
- `GET /tasks?size=10&page=0` returns exactly 10 items
- `GET /tasks?size=10&page=1` returns at least 5 items

---

## ✅ Task 4 — Module-scoped read-only dataset

Create a `module_task` fixture (`scope="module"`) that creates a single task once for the whole module and provides it as read-only reference data.

Write 4 tests that all read from `module_task` without modifying it:
- Assert the task `id` is an integer
- Assert the task `title` is a non-empty string
- Assert the task `status` is a valid value
- Assert the task `updatedAt` is a non-empty string

---

## ✅ Task 5 — Verify cleanup actually works

Write a test that proves the factory cleans up even when the test fails:

1. Create a task with a unique, searchable title
2. Store the `task_id`
3. **Deliberately fail** the test (use `assert False`)
4. In a **separate test** (using the same unique title), call `GET /tasks?search=<title>`
5. Assert the search returns **zero** results — proving the failed test cleaned up

---

## 🏃 Run your tests

```bash
pytest src/tests/test_api_data.py -v -s
```

---

## 💡 Tips

- Module-scoped fixtures cannot use function-scoped fixtures like `api_v1`. For module scope, create your own `playwright.request.new_context(base_url=...)` directly inside the fixture.
- Label your test tasks with something recognisable (`uuid` prefix + `"training"`) so if cleanup fails you can identify and delete them manually.
- The comment endpoint returns the comment `id` in the response — store it immediately, as you cannot list comments to find IDs later.

---

## 📌 Reference

- [pytest — Fixtures](https://docs.pytest.org/en/stable/reference/fixtures.html)
- [testauto.app API Guide](https://testauto.app/docs/api-guide)
