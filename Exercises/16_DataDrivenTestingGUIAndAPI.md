# Exercise 16 — Data-Driven Testing: GUI & API

## 🎯 Goal

Use `@pytest.mark.parametrize` to run the same test logic against multiple inputs — eliminating copy-pasted tests, covering all valid combinations, and sharing data sets across both UI and API test layers.

Before writing any code, **count how many separate tests you currently have** for different priority levels, status values, and form states. Data-driven testing replaces all of those with one parametrized test.

---

## 📖 Background

### Basic parametrize

```python
@pytest.mark.parametrize("status", ["TODO", "IN_PROGRESS", "DONE"])
def test_create_task_with_status(api_v1, status):
    # Runs 3 times — once for each status
    ...
```

### Multiple parameters

```python
@pytest.mark.parametrize("status,priority", [
    ("TODO",        "LOW"),
    ("IN_PROGRESS", "HIGH"),
    ("DONE",        "URGENT"),
])
def test_create_task_with_combinations(api_v1, status, priority):
    # Runs 3 times — once per tuple
    ...
```

### Shared data sets across UI and API

```python
# Define once
TASK_DATA = [
    {"title": "Alpha task", "status": "TODO",        "priority": "LOW"},
    {"title": "Beta task",  "status": "IN_PROGRESS", "priority": "HIGH"},
    {"title": "Gamma task", "status": "DONE",        "priority": "URGENT"},
]

# Reuse in API test
@pytest.mark.parametrize("data", TASK_DATA)
def test_api_task_creation(api_v1, data):
    ...

# Reuse in UI test — same data set
@pytest.mark.parametrize("data", TASK_DATA)
def test_ui_task_detail_shows_correct_fields(page, task_factory, data):
    ...
```

### IDs for readable test names

```python
@pytest.mark.parametrize("status", ["TODO", "IN_PROGRESS", "DONE"],
                          ids=["todo", "in-progress", "done"])
def test_status_filter(page, status):
    # Test names: test_status_filter[todo], test_status_filter[in-progress]
    ...
```

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/tests/test_data_driven.py` | All tasks for this exercise |

---

## ✅ Task 1 — Parametrize all priority values (API)

Write a single parametrized test that creates a task for each priority and verifies the API response:

| Priority | Assert |
|----------|--------|
| `LOW` | `task["priority"] == "LOW"` |
| `MEDIUM` | `task["priority"] == "MEDIUM"` |
| `HIGH` | `task["priority"] == "HIGH"` |
| `URGENT` | `task["priority"] == "URGENT"` |

The test runs 4 times. Each run creates and cleans up its own task.

---

## ✅ Task 2 — Parametrize all status values (UI)

Write a parametrized test that for each status value:

1. Creates a task via API with the given status
2. Opens `?taskModal=detail&taskId={id}` in the browser
3. Asserts the correct status is visible in the modal

| Status | Visible in modal |
|--------|-----------------|
| `TODO` | `"TODO"` text |
| `IN_PROGRESS` | `"In Progress"` or `"IN_PROGRESS"` text |
| `DONE` | `"Done"` or `"DONE"` text |

Use `task_factory` for setup and cleanup.

---

## ✅ Task 3 — Shared data set across UI and API

Define a shared list of task dictionaries at the top of the file:

```python
TASK_SCENARIOS = [
    {"title": "Scenario Alpha", "status": "TODO",        "priority": "LOW"},
    {"title": "Scenario Beta",  "status": "IN_PROGRESS", "priority": "HIGH"},
    {"title": "Scenario Gamma", "status": "DONE",        "priority": "URGENT"},
]
```

Write **two** tests, both parametrized with `TASK_SCENARIOS`:

1. `test_api_create_scenario` — creates each via API, asserts `status` and `priority` match
2. `test_ui_search_for_scenario` — creates via API, searches in UI, asserts row is visible

Both tests must clean up their own data.

---

## ✅ Task 4 — Parametrize form validation (UI)

Navigate to `?taskModal=create` and test the form with invalid inputs:

```python
@pytest.mark.parametrize("title,expected_behaviour", [
    ("",          "error_shown"),      # empty title
    ("   ",       "error_or_created"), # whitespace only
    ("A" * 200,   "created"),          # very long title
])
def test_form_validation(page, title, expected_behaviour):
    ...
```

For each case:
- Fill in the title and submit the form
- Assert the expected behaviour (error message visible, or task created)

---

## ✅ Task 5 — Parametrize filter combinations (UI)

Write a parametrized test for the status filter dropdown:

```python
@pytest.mark.parametrize("filter_value,expected_status", [
    ("TODO",        "TODO"),
    ("IN_PROGRESS", "IN_PROGRESS"),
    ("DONE",        "DONE"),
], ids=["filter-todo", "filter-in-progress", "filter-done"])
def test_status_filter_shows_correct_tasks(page, filter_value, expected_status):
    ...
```

For each value:
1. Navigate to the task manager
2. Select `filter_value` from the status dropdown
3. Assert every visible row shows `expected_status` in its status cell

---

## 🏃 Run your tests

```bash
pytest src/tests/test_data_driven.py -v

# See parametrized test names
pytest src/tests/test_data_driven.py --collect-only
```

---

## 💡 Tips

- Use `ids=["name1", "name2"]` in `parametrize` — test names like `test_create[high]` are much easier to read in CI output than `test_create[data0]`.
- When a parametrized test fails, pytest shows which parameter caused the failure — you don't have to grep through output.
- The `task_factory` fixture can be used in parametrized tests — it runs once per test invocation, creating and cleaning up independently.

---

## 📌 Reference

- [pytest — Parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [testauto.app UI Guide](https://testauto.app/docs/ui-guide)
- [testauto.app API Guide](https://testauto.app/docs/api-guide)
