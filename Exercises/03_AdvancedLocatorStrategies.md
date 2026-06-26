# Exercise 03 — Advanced Locator Strategies

## 🎯 Goal

Stop writing brittle CSS selectors. Use Playwright's semantic, accessible locator strategies to write tests that read like user actions and survive UI refactors without changing a single selector.

Before writing any code, **open https://testauto.app/task-manager-spa** and use DevTools Accessibility panel (F12 → Accessibility) to inspect the ARIA roles of the search input, the Add Task button, and the table rows.

---

## 📖 Background

### Locator priority — best to worst

```python
# ✅ Best — matches how a real user sees the page
page.get_by_role("button", name="Save")
page.get_by_role("link", name="Add New Task")

# ✅ Best for forms — uses the <label> element
page.get_by_label("Title")
page.get_by_label("Status")

# ✅ Good — visible placeholder or text
page.get_by_placeholder("Search tasks...")
page.get_by_text("No tasks found")

# ⚠️ Acceptable — structural when nothing else works
page.locator("table tbody tr")

# ❌ Avoid — breaks on any layout change
page.locator("div:nth-child(3) > div > button")
```

### filter() — narrow a locator to a subset

```python
# Find the specific row containing "Deploy to Railway" and click its Delete button
page.locator("table tbody tr") \
    .filter(has_text="Deploy to Railway.app") \
    .get_by_role("button", name="Delete") \
    .click()
```

### nth(), first, last

```python
page.locator("table tbody tr").first      # first row
page.locator("table tbody tr").nth(2)     # third row (0-indexed)
page.locator("table tbody tr").last       # last row
```

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/tests/test_selectors.py` | All tasks for this exercise |

---

## ✅ Task 1 — Rewrite brittle selectors with semantic alternatives

Navigate to https://testauto.app/task-manager-spa. Using **only** `get_by_role`, `get_by_label`, `get_by_placeholder`, or `get_by_text` — no `page.locator("css")` allowed:

| Action | Locator to use |
|--------|---------------|
| Fill the search input with `"deploy"` | `get_by_placeholder` |
| Click the Add New Task button | `get_by_role("link", ...)` |
| Assert URL contains `taskModal=create` | `expect(page).to_have_url(...)` |

---

## ✅ Task 2 — filter() to act on a specific row

Navigate to the task list. Find the row for **"Deploy to Railway.app"** using `.filter(has_text=...)`.

From within that row only:
- Read the priority cell text
- Assert it contains `"High"`
- Assert no other row is accidentally matched

---

## ✅ Task 3 — nth(), first, last and counting

1. Navigate to the task manager
2. Change the items-per-page dropdown to `10`
3. Assert `row_count <= 10`
4. Read the first row's title — assert it is not an empty string
5. Read the last row's title — assert it differs from the first

---

## ✅ Task 4 — Board view column scoping

Navigate to `https://testauto.app/task-manager-spa?view=board`.

The board has three columns. For each column (TODO, In Progress, Done):
- Scope a locator to that column's container (inspect the DOM to find it)
- Count the task cards inside it
- Store the count

Assert the sum of all three column counts is `> 0`.

---

## ✅ Task 5 — Dynamic filter loop

Use the `api_v1` fixture to create 3 tasks:

| Title | Priority |
|-------|----------|
| `Selector Alpha` | `LOW` |
| `Selector Beta` | `MEDIUM` |
| `Selector Gamma` | `HIGH` |

Navigate to the task manager and search for `"Selector"`. For each title, use `.filter(has_text=title)` on the table rows and assert the row is visible.

Clean up: delete all 3 tasks in `finally`.

---

## 🏃 Run your tests

```bash
pytest src/tests/test_selectors.py -v --headed

# Use the inspector to try locators live
# Add page.pause() anywhere in your test, then run headed
```

---

## 💡 Tips

- Use `page.pause()` in headed mode to open the Playwright Inspector — you can type locators and see what they match in real time on the live page.
- `expect(locator).to_be_visible()` retries automatically for up to 5 seconds. `assert locator.is_visible()` does not retry — it is flaky.
- `.filter(has_text=...)` is case-insensitive and matches partial text — `filter(has_text="deploy")` will match `"Deploy to Railway.app"`.

---

## 📌 Reference

- [Playwright — Locators](https://playwright.dev/python/docs/locators)
- [Playwright — Best practices](https://playwright.dev/python/docs/best-practices)
- [testauto.app UI Guide](https://testauto.app/docs/ui-guide)
