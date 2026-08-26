# SDET Training Review — 2026-08-26

---

## Exercise 02 — Network Interception (`test_network.py`)

### Score Summary

| # | Task | Status | Score | Notes |
|---|------|--------|-------|-------|
| 1 | Stub empty task list | ✅ PASS | 1.18 | Route + goto + `to_have_count(0)` |
| 2 | Inject task into real response | ✅ PASS | 1.18 | `route.fetch()` + inject into `content[]` + scoped assertion |
| 3 | Capture search request | ✅ PASS | 1.18 | Listener registered before goto, summary filtered out, URL asserted |
| 4 | Simulate 500 error | ✅ PASS | 1.18 | 500 stub + `print(page.content())` + `to_have_count(0)` |
| 5 | Slow network simulation | ✅ PASS | 1.18 | `time.sleep` inside handler + `expect` before elapsed measurement |
| **TOTAL** | | | **5.88 / 5.88** | Band: **Outstanding** |

### Test Execution

| Suite | Passed | Failed | Errors | Duration |
|-------|--------|--------|--------|----------|
| test_network.py | 5 | 0 | 0 | 44.70s |

### Technical Notes (non-obvious fixes)
1. `**/api/v1/tasks**` also intercepts `/tasks/summary` → guard with `if "content" in data`
2. `page.goto()` returns on the `load` event, before the slow XHR responds → `expect` must come BEFORE measuring elapsed time
3. Strict mode violation on `get_by_text("INJECTED TASK")` → scoped to `page.locator("table")`

---

## Exercise 03 — Advanced Locator Strategies (`test_selectors.py`)

### Score Summary

| # | Task | Status | Score | Notes |
|---|------|--------|-------|-------|
| 1 | Semantic selectors only | ✅ PASS | 1.18 | `get_by_placeholder` + `get_by_role("button")` + `to_have_url` |
| 2 | filter() on specific row | ✅ PASS | 1.18 | `to_have_count(1)` + `to_contain_text("High")` |
| 3 | nth(), first, last, counting | ✅ PASS | 1.18 | `expect(rows).to_have_count(10)` to wait for table refresh |
| 4 | Board view column scoping | ✅ PASS | 1.18 | `.board-column` + `.board-column-title` + `.board-task-card` |
| 5 | Dynamic filter loop | ✅ PASS | 1.18 | uuid in titles + try/finally + `/api/v1/tasks` + `expect_response` |
| **TOTAL** | | | **5.88 / 5.88** | Band: **Outstanding** |

### Test Execution

| Suite | Passed | Failed | Errors | Duration |
|-------|--------|--------|--------|----------|
| test_selectors.py | 5 | 0 | 0 | 10.92s |

### Technical Notes (non-obvious fixes)
1. **Task 3**: `select_option("10")` does not block until React re-renders → `expect(rows).to_have_count(10)` retries until the count actually changes
2. **Task 4**: board DOM classes (`board-column`, `board-task-card`) discovered via `page.evaluate` — not derivable from the exercise .md
3. **Task 5**: path `/tasks` with a base_url lacking a trailing slash resolves to `/api/tasks` (401) → use `/api/v1/tasks` (absolute path from host root)
4. **Task 5**: asserting on the filtered row without waiting for the search response → `expect_response` required before the assertion

---

## Session Overall Score

| Exercise | Score | Band |
|----------|-------|------|
| 02 — Network Interception | 5.88 / 5.88 | Outstanding |
| 03 — Advanced Locators | 5.88 / 5.88 | Outstanding |
| **TOTAL** | **11.76 / 11.76** | **Outstanding** |

---

## Top Strengths

1. `test_selectors.py` — **Board view column scoping** implemented correctly: each column scoped via `.board-column` → `.board-column-title` → `.board-task-card`, a robust non-positional pattern.
2. `test_network.py` — **Task 5**: `time.sleep(3)` used correctly INSIDE the route handler (not in the test body), which is the standard approach for simulating network latency without being an anti-pattern.
3. `test_selectors.py` — **Task 5**: uuid in task titles ensures parallel isolation; cleanup in `try/finally` guarantees deletion even if the test fails mid-run.