# Exercise 01 — Browser & Context Management

## 🎯 Goal

Understand the three-level hierarchy of Playwright — `Browser`, `BrowserContext`, and `Page` — and learn how to use multiple contexts simultaneously to simulate independent sessions, persist authentication state, and avoid cross-test interference.

Before writing any code, **open the site in your browser and explore it manually**:
- Navigate to https://testauto.app/task-manager-spa
- Open a second tab and notice it shares your session
- Think about what it would mean for two separate users to be logged in at the same time

---

## 📖 Background

### The three-level hierarchy

```
Browser  (the engine — Chromium, Firefox, WebKit)
  └── BrowserContext  (an isolated session — own cookies, storage, auth)
        └── Page  (a single tab)
```

Most tests only ever touch `page` — but understanding the full hierarchy is what separates basic automation from production-grade test design.

```python
# Each context is fully isolated — like a private browsing window
context_a = browser.new_context()
context_b = browser.new_context()

page_a = context_a.new_page()   # user A's session
page_b = context_b.new_page()   # user B's session — completely separate
```

### Persisting authentication state

Logging in through the UI on every test is slow. Save the session once and reuse it:

```python
# Save after login
context.storage_state(path="auth_state.json")

# Restore in another test — skips the login UI entirely
context = browser.new_context(storage_state="auth_state.json")
```

### Custom viewport and locale

```python
context = browser.new_context(
    viewport={"width": 1440, "height": 900},
    locale="en-GB",
    timezone_id="Europe/London",
)
```

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/tests/test_browser_context.py` | All tasks for this exercise |

---

## ✅ Task 1 — Understand context isolation

Create two separate `BrowserContext` instances from the same `browser` fixture. In each context, navigate to https://testauto.app/task-manager-spa.

Assert that:
- Both pages have the same URL
- Both contexts are independent (modifying one page does not affect the other)
- Closing one context does not affect the other

```python
def test_two_contexts_are_independent(browser):
    ctx_a = browser.new_context()
    ctx_b = browser.new_context()
    # TODO: create pages, navigate both, assert independence
    ctx_a.close()
    ctx_b.close()
```

---

## ✅ Task 2 — Save and restore authentication state

1. Create a context and navigate to https://api.testauto.app/api/v2 to obtain a JWT token
2. Save the browser context storage state to a file using `context.storage_state(path=...)`
3. Create a **new** context using that saved state
4. Navigate to https://testauto.app/task-manager-spa in the new context
5. Assert the page loads correctly without requiring a fresh login flow

| Step | What to assert |
|------|---------------|
| After save | The state file exists on disk |
| After restore | New context page loads task manager without error |

---

## ✅ Task 3 — Multiple viewports in the same test

Create three contexts with different viewport sizes. In each, navigate to https://testauto.app/task-manager-spa and take a screenshot.

| Context | Viewport | Screenshot filename |
|---------|----------|-------------------|
| Desktop | 1440 × 900 | `screenshots/context-desktop.png` |
| Tablet | 768 × 1024 | `screenshots/context-tablet.png` |
| Mobile | 390 × 844 | `screenshots/context-mobile.png` |

Assert all three screenshot files exist after the test runs.

---

## ✅ Task 4 — Simulate two users simultaneously

Using two contexts at the same time, simulate two users interacting with the task manager concurrently:

- **User A** (context A) — creates a task via `POST /api/v1/tasks` using `api_v1`
- **User B** (context B) — navigates to the task manager and searches for User A's task title
- Assert User B can see the task User A created

Clean up: delete the task in `finally`.

---

## ✅ Task 5 — Context with custom headers and locale

Create a context that sets:
- `locale="en-GB"`
- `timezone_id="Europe/London"`
- `extra_http_headers={"X-Test-Run": "playwright-training"}`

Navigate to https://testauto.app/task-manager-spa. Assert:
- The page title is correct
- No errors occur when navigating with custom headers

---

## 🏃 Run your tests

```bash
pytest src/tests/test_browser_context.py -v --headed
```

---

## 💡 Tips

- Always close contexts in `finally` or use them as context managers to avoid browser leaks.
- `storage_state()` captures cookies and `localStorage` — it does not capture in-memory JavaScript state.
- The `browser` fixture provided by `pytest-playwright` is `scope="session"` — one browser for all tests. Contexts are cheap; create as many as you need.

---

## 📌 Reference

- [Playwright — Browser contexts](https://playwright.dev/python/docs/browser-contexts)
- [Playwright — Authentication](https://playwright.dev/python/docs/auth)
- [testauto.app UI Guide](https://testauto.app/docs/ui-guide)
