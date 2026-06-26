# Exercise 07 — Fixtures & Test Lifecycle

## 🎯 Goal

Master pytest fixture scopes, share test state efficiently without coupling tests, build a factory fixture that always cleans up after itself, and use hooks to add automatic behaviour like screenshot capture on failure.

Before writing any code, **think about the cost of each setup step**:
- `page.goto(url)` — fast (~100ms)
- Logging in through the UI — slow (~2–3s)
- Creating test data via API — fast (~200ms)
- Creating test data through the UI form — slow (~3–5s)

The goal of advanced fixture design is to do the slow things as few times as possible while keeping tests independent.

---

## 📖 Background

### Fixture scopes

```python
@pytest.fixture(scope="function")  # default — new instance per test
@pytest.fixture(scope="class")     # shared within a test class
@pytest.fixture(scope="module")    # shared across all tests in a file
@pytest.fixture(scope="session")   # shared across the entire test run
```

### The factory pattern

Returns a callable so each test can create its own data with its own parameters — while teardown deletes everything automatically:

```python
@pytest.fixture
def task_factory(api_v1):
    created_ids = []

    def _create(**fields):
        resp = api_v1.post("/tasks", data=json.dumps({
            "title":    fields.get("title", "Test task"),
            "status":   fields.get("status", "TODO"),
            "priority": fields.get("priority", "MEDIUM"),
        }), headers={"Content-Type": "application/json"})
        assert resp.ok
        task = resp.json()
        created_ids.append(task["id"])
        return task

    yield _create

    for tid in created_ids:       # runs even if the test failed
        api_v1.delete(f"/tasks/{tid}")
```

### autouse hooks

```python
@pytest.fixture(autouse=True)
def screenshot_on_failure(page, request):
    yield
    if request.node.rep_call.failed:
        page.screenshot(path=f"screenshots/{request.node.name}.png")
```

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/conftest.py` | Add fixtures: `task_factory`, `module_task`, `log_test_name` |
| `src/tests/test_fixtures.py` | Tests that exercise the fixtures |

---

## ✅ Task 1 — Task factory fixture

Add `task_factory` to `src/conftest.py`. It must:

- Accept keyword args: `title`, `status`, `priority`, `labels`, `description`
- Call `POST /api/v1/tasks`
- Track all created IDs in a list
- Delete them all in teardown — **always**, even when the test fails

Test it by writing two tests that each create tasks with different parameters and assert the response shape.

---

## ✅ Task 2 — Parametrized test using the factory

Write a `@pytest.mark.parametrize` test that creates a task for each status value and verifies it:

```python
@pytest.mark.parametrize("status", ["TODO", "IN_PROGRESS", "DONE"])
def test_task_created_with_correct_status(task_factory, status):
    # TODO: create task with given status, assert task["status"] == status
```

Also parametrize across all priority values: `LOW`, `MEDIUM`, `HIGH`, `URGENT`.

---

## ✅ Task 3 — Module-scoped shared task

Create a `module_task` fixture with `scope="module"` that creates **one task** for the entire module and deletes it once at the end.

Write 3 tests that all read the same `module_task` without modifying it:

| Test | What to assert |
|------|---------------|
| `test_has_id` | `"id"` key exists in the task dict |
| `test_has_valid_status` | `status` is one of `TODO`, `IN_PROGRESS`, `DONE` |
| `test_has_valid_priority` | `priority` is one of `LOW`, `MEDIUM`, `HIGH`, `URGENT` |

---

## ✅ Task 4 — Class-scoped browser context

Build a test class where all methods share the same browser context (no re-navigation from scratch):

```python
class TestTaskManagerFlow:
    @pytest.fixture(scope="class", autouse=True)
    def setup_context(self, browser, request):
        ctx = browser.new_context()
        request.cls.page = ctx.new_page()
        yield
        ctx.close()

    def test_open_list(self): ...
    def test_filter_by_status(self): ...
    def test_switch_to_board(self): ...
```

The three tests should run in order on the same page, each building on the previous navigation state.

---

## ✅ Task 5 — Autouse logging fixture

Add an `autouse=True` fixture named `log_test_name` that prints to stdout:

```
▶  Starting: test_name_here
✅ Passed:  test_name_here      (or ❌ Failed: ...)
```

Run your full test file with `-s` to see the output:

```bash
pytest src/tests/test_fixtures.py -v -s
```

---

## 🏃 Run your tests

```bash
pytest src/tests/test_fixtures.py -v -s
```

---

## 💡 Tips

- For `rep_call` to work in autouse fixtures, the `pytest_runtest_makereport` hook must be in `conftest.py`. It is already provided — do not remove it.
- `scope="module"` fixtures cannot use `scope="function"` fixtures. The `api_v1` fixture in `conftest.py` is `function`-scoped — for module-scoped tasks, create your own `APIRequestContext` directly using `playwright`.
- Never share mutable data between tests via a module-scoped fixture. Use module scope only for **read-only** reference data.

---

## 📌 Reference

- [pytest — Fixtures](https://docs.pytest.org/en/stable/reference/fixtures.html)
- [pytest — Parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html)
