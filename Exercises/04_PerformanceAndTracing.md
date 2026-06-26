# Exercise 04 — Performance & Tracing

## 🎯 Goal

Record Playwright traces of testauto.app user flows for CI debugging, capture real network traffic as HAR files, measure page timing metrics, and detect JavaScript console errors — all critical skills for diagnosing failures that only happen in CI.

Before writing any code, **run an existing test and open its trace**:

```bash
pytest src/tests/smoke_test.py --tracing=on
playwright show-trace test-results/*/trace.zip
```

Explore the timeline, screenshots, and network calls in the trace viewer.

---

## 📖 Background

### Recording a trace manually

```python
context = browser.new_context()
context.tracing.start(screenshots=True, snapshots=True, sources=True)

page = context.new_page()
# ... test actions ...

context.tracing.stop(path="traces/my-flow.zip")
```

Open with: `playwright show-trace traces/my-flow.zip`

### HAR files — full network archive

```python
context = browser.new_context(record_har_path="network.har")
page = context.new_page()
page.goto("https://testauto.app/task-manager-spa")
context.close()   # HAR is flushed on close
```

### Page timing

```python
timing = page.evaluate(
    "() => JSON.parse(JSON.stringify(window.performance.timing))"
)
dom_ready = timing["domContentLoadedEventEnd"] - timing["navigationStart"]
load      = timing["loadEventEnd"] - timing["navigationStart"]
```

### Console error capture

```python
errors = []
page.on("console", lambda msg: errors.append(msg) if msg.type == "error" else None)
```

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/tests/test_performance.py` | All tasks for this exercise |

---

## ✅ Task 1 — Record a trace of a full create-task flow

1. `context.tracing.start(screenshots=True, snapshots=True, sources=True)`
2. Navigate to https://testauto.app/task-manager-spa
3. Click "+ Add New Task", fill in the title, submit
4. Wait for the task to appear in the list
5. `context.tracing.stop(path="traces/task-create.zip")`
6. Assert the file exists

Then open it:
```bash
playwright show-trace traces/task-create.zip
```

Inspect the action timeline, page screenshots, and network requests tab.

Clean up: delete the created task via `api_v1` in `finally`.

---

## ✅ Task 2 — HAR capture and analysis

1. Create a context with `record_har_path` pointing to a temp file
2. Navigate to https://testauto.app/task-manager-spa and wait for `networkidle`
3. Close the context — the HAR file is written on close
4. Load and parse the HAR JSON

Assert:

| Assertion | What to check |
|-----------|--------------|
| API was called | At least one entry URL contains `api.testauto.app` |
| No errors | All response statuses are `< 400` |
| Task list fetched | At least one URL contains `/api/v1/tasks` |

---

## ✅ Task 3 — Page timing assertions

Navigate to https://testauto.app/task-manager-spa and wait for `networkidle`. Use `page.evaluate()` to read `window.performance.timing`.

| Metric | Formula | Assert |
|--------|---------|--------|
| DOM ready | `domContentLoadedEventEnd - navigationStart` | `< 5000 ms` |
| Full load | `loadEventEnd - navigationStart` | `< 10000 ms` |

Print both values using `-s` so you can see the real numbers.

---

## ✅ Task 4 — Console error detection

Attach a `page.on("console", ...)` listener **before** navigating. After the page loads:

1. Collect all console messages where `msg.type == "error"`
2. Filter for any containing `"Uncaught"`, `"TypeError"`, or `"SyntaxError"`
3. Assert none were found

This catches real JavaScript bugs that don't cause visible failures but will break users in production.

---

## ✅ Task 5 — Auto-save trace on test failure

Create a pytest fixture `traced_page` that:

- Starts tracing before each test
- On **failure** → stops trace and saves to `traces/<test_name>.zip`
- On **pass** → stops trace without saving

```python
@pytest.fixture
def traced_page(browser, request):
    ctx = browser.new_context()
    ctx.tracing.start(screenshots=True, snapshots=True)
    page = ctx.new_page()
    yield page
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        ctx.tracing.stop(path=f"traces/{request.node.name}.zip")
    else:
        ctx.tracing.stop()
    ctx.close()
```

Write one test using `traced_page` that intentionally fails. Verify the trace file appears in `traces/`.

---

## 🏃 Run your tests

```bash
pytest src/tests/test_performance.py -v -s

# Open a trace
playwright show-trace traces/task-create.zip
```

---

## 💡 Tips

- Traces are ZIP files — each contains a full replay of the test including DOM snapshots, screenshots, and network data.
- Save traces only on failure in CI — they can be 5–20 MB each.
- `record_har_path` must be set when creating the context, not after.
- `performance.timing` returns zeros for `loadEventEnd` if the page is still loading — always wait for `networkidle` first.

---

## 📌 Reference

- [Playwright — Trace Viewer](https://playwright.dev/python/docs/trace-viewer)
- [Playwright — Network HAR](https://playwright.dev/python/docs/network#record-and-replay-requests)
