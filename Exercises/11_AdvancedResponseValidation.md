# Exercise 11 — Advanced Response Validation

## 🎯 Goal

Go beyond simple status code checks. Validate full response schemas, assert pagination and filtering behaviour, check response time bounds, and verify that sorting works correctly — the skills needed to catch real backend bugs that a basic test suite would miss.

Before writing any code, **call the API manually** and inspect the full response:

```bash
curl "https://api.testauto.app/api/v1/tasks?size=5&page=0" | python -m json.tool
```

Note every field in the response. Which ones could be missing? Wrong type? Out of range?

---

## 📖 Background

### Schema validation

Checking that every required field is present and the right type:

```python
def validate_task_schema(task: dict):
    required_fields = {"id", "title", "status", "priority", "updatedAt"}
    missing = required_fields - set(task.keys())
    assert not missing, f"Task missing fields: {missing}"

    assert isinstance(task["id"], int), "id must be int"
    assert isinstance(task["title"], str), "title must be str"
    assert task["status"] in ("TODO", "IN_PROGRESS", "DONE")
    assert task["priority"] in ("LOW", "MEDIUM", "HIGH", "URGENT")
```

### Response time assertion

```python
import time

start = time.time()
resp = api_v1.get("/tasks")
elapsed = time.time() - start

assert elapsed < 3.0, f"Response took {elapsed:.2f}s — too slow"
```

### Pagination consistency check

```python
body = api_v1.get("/tasks?size=10&page=0").json()
assert len(body["content"]) <= body["totalElements"]
assert body["currentPage"] == 0
assert body["totalPages"] == math.ceil(body["totalElements"] / 10)
```

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/tests/test_api_validation.py` | All tasks for this exercise |

---

## ✅ Task 1 — Full schema validation

Write a reusable helper `validate_task_schema(task)` and apply it to every task returned by `GET /tasks`.

Assert for every task:

| Field | Type | Constraint |
|-------|------|-----------|
| `id` | `int` or `str` | Present and non-empty |
| `title` | `str` | Length `> 0` |
| `status` | `str` | One of `TODO`, `IN_PROGRESS`, `DONE` |
| `priority` | `str` | One of `LOW`, `MEDIUM`, `HIGH`, `URGENT` |
| `updatedAt` | `str` | Matches ISO 8601 format (contains `T` and `-`) |

---

## ✅ Task 2 — Pagination consistency

Write tests for the following:

| Test | What to assert |
|------|---------------|
| `test_page_size_respected` | `len(content) == size` when enough tasks exist |
| `test_current_page_matches_request` | `currentPage` matches the `page` parameter sent |
| `test_total_pages_is_consistent` | `totalPages == ceil(totalElements / size)` |
| `test_last_page_has_fewer_items` | Last page has `<= size` items |
| `test_empty_page_beyond_last` | Requesting `page=999` returns empty `content` with `200` |

---

## ✅ Task 3 — Filter accuracy

Write tests for every filter parameter:

| Filter | Assert |
|--------|--------|
| `?status=TODO` | Every returned task has `status == "TODO"` |
| `?status=IN_PROGRESS` | Every returned task has `status == "IN_PROGRESS"` |
| `?priority=HIGH` | Every returned task has `priority == "HIGH"` |
| `?search=API` | Every returned task contains `"api"` (case-insensitive) in `title`, `description`, or `labels` |

Also test combining filters: `?status=TODO&priority=HIGH` — assert every task satisfies **both** conditions.

---

## ✅ Task 4 — Response time bounds

Measure the actual response time for these endpoints and assert they are within acceptable limits:

| Endpoint | Max allowed time |
|----------|----------------|
| `GET /tasks` | `3.0` seconds |
| `GET /tasks/summary` | `3.0` seconds |
| `POST /tasks` (create) | `5.0` seconds |
| `DELETE /tasks/{id}` | `3.0` seconds |

Print the actual time for each endpoint so you can see the real numbers.

---

## ✅ Task 5 — Sorting verification

The API supports a `sort` parameter: `?sort=priority,desc` and `?sort=title,asc`.

Write tests that:

1. Request tasks sorted by `priority,desc`
2. Extract the `priority` values from `content`
3. Assert they appear in descending order: `URGENT → HIGH → MEDIUM → LOW`

Do the same for `title,asc` — assert titles are alphabetically sorted.

---

## 🏃 Run your tests

```bash
pytest src/tests/test_api_validation.py -v -s
```

---

## 💡 Tips

- Use `import math` for `math.ceil()` in pagination calculations.
- When asserting sort order, map priority strings to numeric weights first: `{"LOW":1,"MEDIUM":2,"HIGH":3,"URGENT":4}` — then compare adjacent elements.
- `time.time()` includes network latency — results will vary. Use generous thresholds (3–5s) unless you are on a fast, stable connection.

---

## 📌 Reference

- [testauto.app API Guide](https://testauto.app/docs/api-guide)
- [Interactive API Docs](https://api.testauto.app/swagger-ui/index.html)
