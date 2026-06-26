# Exercise 15 — Resilience & Edge Case Testing

## 🎯 Goal

Write tests that stay green even when the backend is unreliable — implementing retry logic with exponential backoff, handling intermittent failures gracefully, and testing the boundary conditions that break poorly-designed APIs.

Before writing any code, **call the buggy API several times** and observe the inconsistency:

```bash
for i in {1..5}; do
  curl -s -o /dev/null -w "%{http_code}\n" https://api.testauto.app/api/buggy/tasks
done
```

Notice that some calls return `500` and some return `200`. This is what your tests must handle.

---

## 📖 Background

### Buggy API

```
https://api.testauto.app/api/buggy
```

Same endpoints as V1, but with:

| Issue | Frequency |
|-------|-----------|
| Random `500` errors | ~10% of requests |
| Response delays | 2–5 seconds |
| Missing fields in response | Occasional |
| Inconsistent date formats | Occasional |

### Retry with exponential backoff

```python
import time

def call_with_retry(fn, max_attempts=5):
    """
    Retry fn() up to max_attempts times.
    Waits: 0.5s, 1s, 2s, 4s between attempts.
    Returns response on first success.
    """
    for attempt in range(max_attempts):
        if attempt > 0:
            wait = 0.5 * (2 ** (attempt - 1))
            time.sleep(wait)
        resp = fn()
        if resp.ok:
            return resp
    raise AssertionError(f"All {max_attempts} attempts failed")
```

### Boundary value patterns

```python
# Empty string
api_v1.post("/tasks", data=json.dumps({"title": ""}), ...)

# Extremely long value
api_v1.post("/tasks", data=json.dumps({"title": "x" * 10000}), ...)

# Missing required field
api_v1.post("/tasks", data=json.dumps({"status": "TODO"}), ...)   # no title

# Invalid enum value
api_v1.post("/tasks", data=json.dumps({"title": "t", "status": "INVALID"}), ...)
```

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/tests/test_resilience.py` | All tasks for this exercise |

---

## ✅ Task 1 — Implement call_with_retry

Implement `call_with_retry(fn, max_attempts=5)` with exponential backoff.

Write tests to prove it works:

| Test | What to verify |
|------|---------------|
| `test_retry_succeeds_eventually` | Buggy `GET /tasks` succeeds within 5 attempts |
| `test_retry_response_is_valid` | The eventual response has `"content"` key |
| `test_retry_schema_matches_v1` | Successful buggy response has same top-level keys as V1 |

---

## ✅ Task 2 — Boundary values: title field

Test the `title` field boundaries on `POST /api/v1/tasks`:

| Input | Expected |
|-------|---------|
| Empty string `""` | `400` or `422` |
| Single character `"a"` | `201` — assert created |
| 255 characters | `201` — assert created |
| 256+ characters | `400` or `201` — document the actual behaviour |
| Whitespace only `"   "` | `400` or `201` — document |
| Special characters `"<script>alert(1)</script>"` | `201` — assert title stored safely |
| Unicode `"Задача 任务 مهمة"` | `201` — assert title preserved exactly |

Clean up all tasks created in `finally`.

---

## ✅ Task 3 — Invalid enum values

Test invalid values for `status` and `priority` on `POST /api/v1/tasks`:

| Field | Invalid value | Expected status |
|-------|--------------|----------------|
| `status` | `"PENDING"` | `400` or `422` |
| `status` | `"todo"` (lowercase) | `400` or `201` — document |
| `priority` | `"EXTREME"` | `400` or `422` |
| `priority` | `""` (empty) | `400` or default applied |

Document the actual behaviour of the API for each case.

---

## ✅ Task 4 — Missing required fields

Test what happens when required fields are omitted:

| Payload | Expected |
|---------|---------|
| `{}` (empty body) | `400` or `422` |
| `{"status": "TODO"}` (no title) | `400` or `422` |
| `{"title": "t", "status": "TODO"}` (no priority) | `201` with default priority, or `400` |
| `null` body | `400` |

For each case, assert the status is either a documented success code or a documented client error code — never a `500`.

---

## ✅ Task 5 — Concurrent request handling

Write a test that fires 5 requests simultaneously using Python's `threading`:

```python
import threading

results = []

def create_task():
    resp = api_v1.post("/tasks", ...)
    results.append(resp.status)

threads = [threading.Thread(target=create_task) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
```

Assert:
- All 5 responses have status `200` or `201`
- No `500` errors occurred
- 5 unique task IDs were returned

Clean up all 5 tasks in `finally`.

---

## 🏃 Run your tests

```bash
pytest src/tests/test_resilience.py -v -s
```

---

## 💡 Tips

- When documenting API behaviour for boundary values, use `print(f"Status: {resp.status}, Body: {resp.text()}")` and run with `-s` — this output is the test's primary value.
- The buggy API has real random failures — your retry tests may pass most of the time but occasionally need all 5 attempts. The backoff ensures they don't spam the server.
- `threading` and `APIRequestContext` are not thread-safe together. For the concurrent test, use `playwright.request.new_context()` inside each thread.

---

## 📌 Reference

- [testauto.app API Guide](https://testauto.app/docs/api-guide)
- [Python threading docs](https://docs.python.org/3/library/threading.html)
