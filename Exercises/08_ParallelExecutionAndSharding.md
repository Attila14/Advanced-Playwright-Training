# Exercise 08 — Parallel Execution & Sharding

## 🎯 Goal

Run your tests in parallel to dramatically cut execution time, design tests that are safe to run concurrently on a shared live site, and configure CI jobs to split the suite across multiple machines using sharding.

Before writing any code, **run the existing tests and time them**:

```bash
time pytest src/tests/test_api_validation.py -v
```

Then run them in parallel and compare:

```bash
time pytest src/tests/test_api_validation.py -n 4 -v
```

---

## 📖 Background

### pytest-xdist parallel execution

```bash
pytest -n 4        # 4 parallel workers
pytest -n auto     # one worker per CPU core
```

Each worker gets its own browser instance. Tests in different workers run simultaneously.

### ⚠️ Critical rule for testauto.app

testauto.app is a **shared public site**. In parallel execution:

- If two tests create a task with the same title, they may interfere with each other's assertions
- Always use `uuid` to generate unique titles
- Always clean up in `try/finally`

```python
import uuid
title = f"test-{uuid.uuid4().hex[:8]}"    # e.g. "test-a3f92b1c"
```

### Test sharding

Split the suite across CI jobs — each job runs a slice:

```bash
# Job 1 of 3
pytest --shard-id=0 --num-shards=3

# Job 2 of 3
pytest --shard-id=1 --num-shards=3
```

Requires `pytest-shard` (already in `requirements.txt`).

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/tests/test_parallel.py` | All tasks for this exercise |
| `src/conftest.py` | Add `worker_id` fixture |

---

## ✅ Task 1 — Identify and fix tests that are not parallel-safe

Run the existing API tests in parallel and observe what fails:

```bash
pytest src/tests/test_api_validation.py -n 4 -v
```

Find tests that:
- Share a task title across multiple tests
- Assert on a global count (e.g. `totalElements`) that another worker may change
- Depend on a specific sort order that parallel execution disrupts

Fix each issue. The rules are:
1. Every test creates its own data with a `uuid`-based title
2. No test asserts on shared global state it didn't create

---

## ✅ Task 2 — Worker ID fixture

Add this to `src/conftest.py`:

```python
@pytest.fixture(scope="session")
def worker_id(request):
    return getattr(request.config, "workerinput", {}).get("workerid", "master")
```

Write a test that prints the worker ID. Run with `-n 3 -s` and confirm three different IDs appear in the output.

---

## ✅ Task 3 — Five fully isolated parallel API tests

Write 5 tests that can all run simultaneously without interfering:

```python
def test_parallel_alpha(api_v1):
    title = f"alpha-{uuid.uuid4().hex[:8]}"
    task_id = None
    try:
        resp = api_v1.post("/tasks", ...)
        task_id = resp.json()["id"]
        assert resp.json()["title"] == title
    finally:
        if task_id:
            api_v1.delete(f"/tasks/{task_id}")
```

Create `test_parallel_beta`, `gamma`, `delta`, `epsilon` with the same pattern.

Run all five simultaneously:

```bash
pytest src/tests/test_parallel.py -n 5 -v
```

---

## ✅ Task 4 — Shard the API test suite

Run the API V1 test suite in two shards and verify the split:

```bash
pytest src/tests/test_api_validation.py --shard-id=0 --num-shards=2 -v
pytest src/tests/test_api_validation.py --shard-id=1 --num-shards=2 -v
```

Assert (manually, by reading the output):
- Each shard runs a different subset of tests
- No test appears in both shards
- Both shards together cover all tests

---

## ✅ Task 5 — Mark fast vs slow tests

Mark all API tests with `@pytest.mark.fast` and all full browser-flow tests with `@pytest.mark.slow`.

Register the marks in `pytest.ini`:

```ini
markers =
    fast: API and unit tests — safe to run in parallel
    slow: Full browser flows — run sequentially
```

Then demonstrate the split:

```bash
# Fast tests in parallel
pytest -m fast -n 4 -v

# Slow tests sequentially
pytest -m slow -v
```

---

## 🏃 Run your tests

```bash
pytest src/tests/test_parallel.py -n 5 -v -s
```

---

## 💡 Tips

- Visual tests (`test_visual.py`) must **not** run in parallel — snapshot comparison is sensitive to rendering timing. Always exclude them: `pytest -n 4 --ignore=src/tests/test_visual.py`.
- `scope="session"` fixtures are shared **within a worker**, not across workers. Each of your 4 workers runs its own session.
- If a cleanup `DELETE` returns 404 in parallel mode, another worker may have already deleted the same task — check for duplicate titles.

---

## 📌 Reference

- [pytest-xdist docs](https://pytest-xdist.readthedocs.io/)
- [pytest-shard](https://pypi.org/project/pytest-shard/)
