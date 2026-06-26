# Exercise 02 — Network Interception

## 🎯 Goal

Use `page.route()` to intercept the real API calls that testauto.app makes, replace or modify them, and test UI states that are impossible or slow to reproduce against the real backend — such as empty lists, server errors, and injected data.

Before writing any code, **open the site in your browser with DevTools open** (F12 → Network tab):
- Navigate to https://testauto.app/task-manager-spa and watch which API calls are made
- Note the exact URL pattern: `https://api.testauto.app/api/v1/tasks`
- Notice what happens in the UI when the task list loads

---

## 📖 Background

### page.route() — intercept a URL pattern

```python
import json

# Fully stub the response — the real server is never contacted
page.route("**/api/v1/tasks**", lambda route: route.fulfill(
    status=200,
    content_type="application/json",
    body=json.dumps({
        "content": [], "totalElements": 0,
        "totalPages": 0, "currentPage": 0
    })
))
page.goto("https://testauto.app/task-manager-spa")
```

### Modify a real response in flight

```python
def inject_handler(route):
    real = route.fetch()           # hit the actual server first
    data = real.json()             # get real data
    data["content"].insert(0, {    # add a fake task at position 0
        "id": 99999, "title": "INJECTED",
        "status": "TODO", "priority": "URGENT",
        "updatedAt": "2026-01-01T00:00:00Z"
    })
    route.fulfill(response=real, body=json.dumps(data))

page.route("**/api/v1/tasks**", inject_handler)
```

### Capture outgoing requests

```python
captured = []
page.on("request", lambda r: captured.append(r) if "/tasks" in r.url else None)
```

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/tests/test_network.py` | All tasks for this exercise |

---

## ✅ Task 1 — Stub an empty task list

Route `**/api/v1/tasks**` to return a response with `"content": []` and `"totalElements": 0`.

Navigate to https://testauto.app/task-manager-spa and assert the UI shows an empty state.

**Tip:** Run the test first *without* the route to see what the page normally looks like — then add the route and confirm the difference.

| Assertion | What to check |
|-----------|--------------|
| Zero rows | `page.locator("table tbody tr").count() == 0` |
| Empty message | Any "no tasks" or empty-state element is visible |

---

## ✅ Task 2 — Inject a task into a real response

Intercept `GET /api/v1/tasks`, fetch the real response, and **prepend** one fake task:

```python
fake_task = {
    "id": 99999,
    "title": "INJECTED TASK",
    "status": "TODO",
    "priority": "URGENT",
    "updatedAt": "2026-01-01T00:00:00Z"
}
```

Navigate to the task manager and assert `"INJECTED TASK"` is visible in the table without creating any real data.

---

## ✅ Task 3 — Capture and inspect outgoing requests

Set up a `page.on("request", ...)` listener before navigating. Then:

1. Navigate to https://testauto.app/task-manager-spa
2. Fill the search input with `"Deploy"` and press Enter
3. Wait for `networkidle`

Assert:
- At least one captured request URL contains `/api/v1/tasks`
- That URL contains a `search` parameter with value `Deploy` (or similar)

---

## ✅ Task 4 — Simulate a server error

Route `**/api/v1/tasks**` to return `status=500`.

Navigate to the task manager and assert the UI responds — either showing an error message or an empty state. Document what the app actually renders by printing the page content.

---

## ✅ Task 5 — Slow network simulation

Write a route handler that sleeps for 3 seconds before allowing the request to continue:

```python
import time

def slow_handler(route):
    time.sleep(3)
    route.continue_()
```

Register this handler, record the start time, navigate to the task manager with `timeout=15000`, then:

| Assertion | Value |
|-----------|-------|
| Elapsed time | `>= 2.5` seconds |
| Page loaded | Table or body is visible |

---

## 🏃 Run your tests

```bash
pytest src/tests/test_network.py -v --headed
```

Running `--headed` lets you see the UI state produced by each route interception.

---

## 💡 Tips

- Routes apply only to requests made **after** they are registered. Always call `page.route()` before `page.goto()`.
- `route.fetch()` fires the real request and returns the real response — use it when you want to modify rather than fully replace data.
- Remove a route mid-test with `page.unroute(pattern)` if you only want interception for part of the flow.

---

## 📌 Reference

- [Playwright — Network interception](https://playwright.dev/python/docs/network)
- [page.route() API](https://playwright.dev/python/docs/api/class-page#page-route)
