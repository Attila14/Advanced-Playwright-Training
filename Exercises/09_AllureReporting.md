# Exercise 09 — Allure Reporting

## 🎯 Goal

Generate rich, navigable Allure reports for your testauto.app test suite — with epic/feature/story hierarchy, step-by-step annotations, screenshot and JSON attachments, severity levels, and automatic screenshot capture on failure.

Before writing any code, **install Allure and run a sample report**:

```bash
pip install allure-pytest

# macOS
brew install allure

# Windows
scoop install allure

pytest src/tests/smoke_test.py --alluredir=allure-results
allure serve allure-results
```

Explore the Overview, Suites, Behaviors, and Graphs tabs.

---

## 📖 Background

### Epic → Feature → Story hierarchy

```python
import allure

@allure.epic("Task Manager")
@allure.feature("Create Task")
@allure.story("UI modal flow")
def test_create_via_ui(page):
    ...
```

### Steps

```python
with allure.step("Navigate to Task Manager"):
    page.goto("https://testauto.app/task-manager-spa")

with allure.step("Open create modal"):
    page.get_by_role("link", name="Add New Task").click()
```

### Attachments

```python
# Screenshot
allure.attach(
    page.screenshot(full_page=True),
    name="Page state",
    attachment_type=allure.attachment_type.PNG,
)

# JSON data
allure.attach(
    json.dumps(data, indent=2),
    name="API response",
    attachment_type=allure.attachment_type.JSON,
)
```

### Severity

```python
@allure.severity(allure.severity_level.CRITICAL)
@allure.severity(allure.severity_level.HIGH)
@allure.severity(allure.severity_level.NORMAL)
@allure.severity(allure.severity_level.MINOR)
```

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/tests/test_allure.py` | All tasks for this exercise |
| `src/conftest.py` | Add auto-attach on failure fixture |

---

## ✅ Task 1 — Annotate with epic / feature / story

Add `@allure.epic`, `@allure.feature`, and `@allure.story` to at least 5 tests covering different areas of the application:

| Epic | Feature | Story |
|------|---------|-------|
| Task Manager | Task List | Page loads and shows tasks |
| Task Manager | Task List | Search filters results |
| Task Manager | API V1 | Create task returns 201 |
| Task Manager | API V1 | Delete task returns 200 |
| Task Manager | Authentication | V2 JWT login succeeds |

After adding the decorators, run and open the report — verify the **Behaviors** tab shows the hierarchy.

---

## ✅ Task 2 — Step-by-step test with allure.step

Write `test_create_task_via_ui_with_steps` using `with allure.step(...)` for every user action. Minimum 6 steps:

| Step | Action |
|------|--------|
| 1 | Navigate to Task Manager |
| 2 | Assert task list is loaded |
| 3 | Open the create task modal |
| 4 | Fill in title and select priority |
| 5 | Submit the form |
| 6 | Search for the new task |
| 7 | Assert the task appears in the list |
| 8 | Clean up via API |

---

## ✅ Task 3 — Attach screenshot and API response

Write a test that visits the task manager and attaches two things to the Allure report:

| Attachment | Type | Name in report |
|-----------|------|---------------|
| Full-page screenshot | `PNG` | `"Task Manager screenshot"` |
| `GET /tasks?size=5` response body | `JSON` | `"Task list (API)"` |

Open the report and verify both attachments appear in the test detail view.

---

## ✅ Task 4 — Auto-attach screenshot on failure

Add an `autouse=True` fixture to `src/conftest.py` that attaches a full-page screenshot to the Allure report whenever a test fails:

```python
@pytest.fixture(autouse=True)
def attach_screenshot_on_failure(page, request):
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        allure.attach(
            page.screenshot(full_page=True),
            name=f"FAILED: {request.node.name}",
            attachment_type=allure.attachment_type.PNG,
        )
```

Write a test that **intentionally fails** to verify the attachment appears in the report.

---

## ✅ Task 5 — Severity distribution

Mark all your existing tests with appropriate severity levels:

| Level | Tests to mark |
|-------|--------------|
| `CRITICAL` | Login, full CRUD lifecycle |
| `HIGH` | Search, status filter |
| `NORMAL` | Pagination, board view |
| `MINOR` | Page title check, smoke |

Run the full test suite with `--alluredir=allure-results`, open the report, and check the **Graphs** tab — verify the severity distribution pie chart is visible.

---

## 🏃 Run your tests

```bash
pytest src/tests/test_allure.py --alluredir=allure-results -v
allure serve allure-results
```

---

## 💡 Tips

- `allure serve allure-results` starts a temporary local web server — the report is interactive and much richer than HTML files.
- Steps appear as a nested tree in the test detail view — use descriptive names, not code comments.
- If the `rep_call` attribute is missing in the auto-attach fixture, the `pytest_runtest_makereport` hook in `conftest.py` is not present — check it is there.

---

## 📌 Reference

- [Allure pytest docs](https://allurereport.org/docs/pytest/)
- [allure-pytest on PyPI](https://pypi.org/project/allure-pytest/)
