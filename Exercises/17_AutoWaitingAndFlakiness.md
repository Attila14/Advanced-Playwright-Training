# Exercise 17 — Auto-waiting & Flakiness Prevention

## 🎯 Goal

Replace fragile `wait_for_load_state("networkidle")` and `time.sleep()` calls with Playwright's built-in web-first assertions — the correct strategy for async SPAs like testauto.app/task-manager-spa.

Before writing any code, **observe the difference**. Open DevTools → Network tab and navigate to https://testauto.app/task-manager-spa. Notice that:
- The SPA continues making background requests after the page appears interactive
- `networkidle` can fire too early, or fire and then trigger more requests
- The task list may render after `networkidle` is already satisfied

This exercise fixes these problems.

---

## 📖 Background

### Why `networkidle` is discouraged

The Playwright documentation explicitly warns against `networkidle`:

> *"We recommend not using networkidle. Tests using it are inherently flaky as 'no network requests for 500ms' is a timing coincidence, not a DOM readiness signal."*

On an async SPA, network requests happen continuously (polling, lazy loads, analytics). `networkidle` may never fire — or it fires based on timing, making the test environment-dependent.

### The web-first alternative

Instead of waiting for the network, wait for the **observable result** in the DOM:

```python
# ❌ Fragile — waits for an indirect signal
page.goto("https://testauto.app/task-manager-spa")
page.wait_for_load_state("networkidle")
assert page.locator("table tbody tr").count() > 0

# ✅ Correct — waits for the thing you actually care about
page.goto("https://testauto.app/task-manager-spa")
expect(page.locator("table tbody tr").first).to_be_visible()
# Playwright will retry this assertion for up to 5 seconds automatically
```

### `expect()` retries — how it works

```python
from playwright.sync_api import expect

expect(locator).to_be_visible()          # retries until visible or timeout
expect(locator).to_have_count(5)         # retries until count matches
expect(locator).to_have_text("Deploy")   # retries until text matches
expect(locator).not_to_be_visible()      # retries until gone
```

The default timeout is 5 seconds. Override per-assertion:

```python
expect(locator).to_be_visible(timeout=10_000)   # 10 seconds for slow pages
```

### `time.sleep()` is always wrong in Playwright

```python
# ❌ Never do this
import time
page.click("#load-more")
time.sleep(2)   # arbitrary wait — flaky on fast machines, too slow on slow ones

# ✅ Wait for the observable change
page.click("#load-more")
expect(page.locator(".task-card")).to_have_count(20)
```

### When `wait_for_load_state` IS appropriate

| State | When to use |
|-------|-------------|
| `"domcontentloaded"` | Only need the initial HTML — no JS required |
| `"load"` | Waiting for all static assets (images, CSS) |
| `"networkidle"` | Almost never — prefer `expect()` instead |

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/tests/test_auto_waiting.py` | All tasks for this exercise |

---

## ✅ Task 1 — Replace networkidle with web-first assertions

The following test uses `networkidle` and `time.sleep()`. Rewrite it using only `expect()`:

```python
# ❌ BEFORE — fragile
def test_task_list_loads(page):
    page.goto("https://testauto.app/task-manager-spa")
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    assert page.locator("table tbody tr").count() > 0

# ✅ AFTER — your implementation
def test_task_list_loads(page):
    page.goto("https://testauto.app/task-manager-spa")
    # TODO: use expect() to wait for the first row to be visible
```

---

## ✅ Task 2 — Wait for a specific element after action

Write a test that:
1. Navigates to the SPA
2. Clicks the Login button — opening the login modal
3. Uses `expect()` to assert the modal is visible **before** interacting with it
4. Clicks Cancel
5. Uses `expect()` to assert the modal is **gone** before the test ends

```python
def test_login_modal_open_close(page):
    # TODO: no sleep(), no networkidle — only expect()
```

---

## ✅ Task 3 — Wait for dynamic content after filtering

Write a test that:
1. Navigates to the SPA
2. Waits for the task table to appear
3. Selects "TODO" from the status filter
4. Uses `expect()` to wait until every visible row contains "TODO" in the status column

Do **not** use `time.sleep()` or `wait_for_load_state("networkidle")` anywhere.

---

## ✅ Task 4 — Wait for count change after creation

1. Create a task via the API (`api_v1`)
2. Navigate to the SPA
3. Record the initial row count as `count_before`
4. Create another task via the API
5. Reload the page
6. Use `expect(page.locator("table tbody tr")).to_have_count(count_before + 1, timeout=8000)` to wait for the new row

Clean up both tasks in `finally`.

---

## ✅ Task 5 — Authenticated SPA flow using `authenticated_page`

Use the session-scoped `authenticated_page` fixture from `conftest.py`. It logs in via the SPA V2 modal once per test run and reuses the storage state.

Write a test that:
1. Uses `authenticated_page` (already logged in)
2. Navigates to the SPA
3. Uses `expect()` to assert the task table is visible
4. Confirms the session is active (no login button visible, or a logout/user element is visible)

```python
def test_authenticated_session_reused(authenticated_page):
    # TODO: use authenticated_page, expect() assertions only
```

---

## 🏃 Run your tests

```bash
pytest src/tests/test_auto_waiting.py -v --headed
```

---

## 💡 Tips

- Every `expect()` assertion automatically retries until timeout. You rarely need anything else.
- Default timeout is 5 seconds. Increase it for elements that take longer to appear: `to_be_visible(timeout=10_000)`.
- `page.locator(...).wait_for()` is the imperative version of `expect().to_be_visible()` — use `expect()` in tests, `wait_for()` in page objects.
- `page.wait_for_url(pattern)` is the right tool when asserting navigation happened — it is web-first by design.
- If you find yourself adding `time.sleep()`, stop and ask: *what observable DOM change am I waiting for?* That is what you should `expect()`.

---

## 📌 Reference

- [Playwright — Auto-waiting](https://playwright.dev/python/docs/actionability)
- [Playwright — Assertions](https://playwright.dev/python/docs/test-assertions)
- [Playwright — Best practices (networkidle warning)](https://playwright.dev/python/docs/best-practices)
