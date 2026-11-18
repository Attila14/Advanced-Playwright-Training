# Playwright with Python — Advanced Test Automation Training

This is a skeleton Python project for learning advanced test automation with AI-powered coding assistants such as GitHub Copilot.

## 📋 Overview

**Advanced Self-Study Training Program — Organizational Curriculum**

Participants follow the README, clone the repository, and complete the exercises independently. Videos and documentation are now placed directly inside the relevant chapter, immediately after its real-world example. The expected duration is up to 40 hours, with reasonable flexibility when additional time is needed.

For questions, use the [SelfStudy Advanced PlayWright Training Microsoft Teams group](https://teams.microsoft.com/l/channel/19%3AsYBwZNxmvNGMN0I8mPZiB15OueNG5XhDKe6EV3tn-b01%40thread.tacv2/SelfStudy_Advanced_PlayWright_Training?groupId=008a7c89-4582-424e-b229-1f74766df409&tenantId=e0793d39-0939-496d-b129-198edd916feb).

After completing the exercises, run the reviewer agent from `.github/agents/review.md` and share the generated report in the Teams group.

## 🌐 Application Under Test

| Resource | URL |
|---|---|
| UI list view | https://testauto.app/task-manager-spa |
| UI board view | https://testauto.app/task-manager-spa?view=board |
| Create modal | https://testauto.app/task-manager-spa?taskModal=create |
| API V1 | https://api.testauto.app/api/v1 |
| API V2 | https://api.testauto.app/api/v2 |
| Buggy API | https://api.testauto.app/api/buggy |
| API Docs | https://api.testauto.app/swagger-ui/index.html |
| App Docs | https://testauto.app/docs |

**Test credentials:** `admin/admin123` · `user/user123` · `testuser/test123`

## 🚀 Getting Started

1. Install Python 3.11+, Visual Studio Code, Git, and GitHub Copilot.
2. Clone the repository and create a virtual environment.
3. Install dependencies and Playwright browsers.
4. Run the smoke test.

```bash
git clone https://github.com/YOUR_USERNAME/playwright-python-advanced-training.git
cd playwright-python-advanced-training
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium firefox webkit
pytest src/tests/smoke_test.py -v
```

## 🔧 Useful Commands

```bash
pytest --browser=firefox --headed --slowmo=500
pytest -n 4
pytest -m fast
pytest --alluredir=allure-results
```

## 🎯 Training Exercises

Complete the exercises sequentially. Each chapter explains what you will learn, where you will use it, a real-world example, the relevant learning resources, and when to apply the technique.

---

# UI Testing — Browser and Page

## 01_BrowserContextManagement.md

### What you will learn

You will understand how Playwright manages browsers and how tests can create isolated environments inside the same browser.

You will learn:

- The difference between Browser, BrowserContext, and Page
- The lifecycle of browsers, contexts, and pages
- How to run multiple browser contexts simultaneously
- How cookies, local storage, and sessions are isolated between contexts
- How to save authentication state using `storage_state`
- How to restore an authenticated session without logging in before every test
- How to configure different browser viewport sizes
- How to simulate several users interacting with the application simultaneously

### Where you will use it

This is useful when testing authentication, different user roles, multi-user workflows, desktop and mobile layouts, parallel tests, and isolated user sessions.

### Real-world example

Alice creates a task and assigns it to Bob. Instead of repeatedly logging in and out, create two independent browser contexts:

```python
alice_context = browser.new_context(storage_state="alice.json")
bob_context = browser.new_context(storage_state="bob.json")
alice_page = alice_context.new_page()
bob_page = bob_context.new_page()
```

Alice and Bob remain logged in simultaneously without their sessions interfering with each other.

### Video

- [Playwright with Python and Pytest (Playlist)](https://www.youtube.com/watch?v=XSHERugHQCY)

> 💡 **When to use this concept:** When a test requires multiple independent users, authentication sessions, or browser configurations, use BrowserContext.

---

## 02_NetworkInterception.md

### What you will learn

You will learn how Playwright can observe and manipulate communication between the browser and backend APIs, including `page.route()`, mocked responses, empty states, request inspection, payload validation, HTTP errors, and slow or unstable backend behavior.

### Where you will use it

Use it for error-handling screens, empty states, loading indicators, backend failures, unavailable features, difficult API conditions, and responses that are difficult to create with real data.

### Real-world example

Instead of manually deleting every task, intercept the request:

```python
import re
page.route(
    re.compile(r".*/api/tasks$"),
    lambda route: route.fulfill(status=200, content_type="application/json", body="[]")
)
```

You can also simulate `GET /api/tasks → HTTP 500` and verify the UI error message.

### Videos

- [Network Interception Video 1](https://www.youtube.com/watch?v=egqzRXOc7cU)
- [Network Interception Video 2](https://www.youtube.com/watch?v=qjqAe8qe0kY)

> 💡 **When to use this concept:** When you need the backend to behave in a specific way for a UI test, use Network Interception.

---

# UI Testing — Locators and Interactions

## 03_AdvancedLocatorStrategies.md

### What you will learn

You will learn semantic locators, text filtering, `nth()`, `first`, `last`, container scoping, board-column scoping, dynamic loops, and locating elements in lists, tables, cards, and dynamic components.

### Where you will use it

Use reliable locator strategies when similar elements exist, positions change, lists are generated dynamically, components repeat, or HTML structure changes.

### Real-world example

To select Task A only inside the IN PROGRESS column:

```python
column = page.get_by_test_id("in-progress-column")
task = column.get_by_text("Task A")
```

### Video

- [Advanced Locator Strategies](https://www.youtube.com/watch?v=MXFAHvcqh7I)

### Additional Material

For `filter()`, `nth()`, `first`, `last`, dynamic loops, and board-column scoping, use:

```text
6-Playwright_MOD3_MOD4.pptx
```

> 💡 **When to use this concept:** When similar elements exist, scope the locator to the appropriate component before searching inside it.

---

## 04_PerformanceAndTracing.md

### What you will learn

You will learn Trace Recorder, Trace Viewer, DOM snapshots, screenshots, network inspection, HAR files, performance metrics, console monitoring, and automatic failure traces.

### Where you will use it

Use these techniques for CI failures, intermittent failures, slow pages, network problems, JavaScript errors, and difficult production-like scenarios.

### Real-world example

A trace can reveal that `POST /tasks` took 8.7 seconds, the UI remained in its loading state, and the assertion ran before the result appeared. It provides actions, snapshots, network evidence, console messages, screenshots, and the exact failure point.

### Videos

- [Performance and Tracing Video 1](https://www.youtube.com/watch?v=LrOXygsYnnk)
- [Performance and Tracing Video 2](https://www.youtube.com/watch?v=Zu_qzwH8zSs)
- [Performance and Tracing Video 3](https://www.youtube.com/watch?v=HNGPAjk_BCI)

### Documentation

- [HAR Replay and Analysis](https://ray.run/videos/148-network-replay-har-playwright-tutorial-part-79)

> 💡 **When to use this concept:** When a test fails and cannot be reproduced locally, investigate trace and runtime evidence.

---

# UI Testing — Test Quality

## 05_VisualTesting.md

### What you will learn

You will learn screenshot capture, pixel comparison, Pillow image comparison, dynamic-content masking, element screenshots, acceptable-difference thresholds, and mobile/desktop comparisons.

### Where you will use it

Use visual testing to find broken layouts, CSS regressions, missing icons, misaligned buttons, incorrect styling, overlaps, and responsive-design problems.

### Real-world example

A Save button may be visible but overlap another field. A normal visibility assertion passes, while a visual comparison detects that the page no longer matches the approved baseline.

### Videos

- [Visual Testing Video 1](https://www.youtube.com/watch?v=O5AyMSxfFbg)
- [Visual Testing Video 2](https://www.youtube.com/watch?v=LrOXygsYnnk)

> 💡 **When to use this concept:** Functional testing asks whether it works. Visual testing asks whether it still looks correct.

---

## 06_AdvancedPOMPatterns.md

### What you will learn

You will learn reusable Component Objects, a shared `BasePage`, SearchBar, Pagination and TaskModal components, fixture-integrated Page Objects, shared behavior, and reduced duplication.

### Where you will use it

Use these patterns as a suite grows from tens to hundreds of tests maintained by several engineers.

### Real-world example

Create one reusable `SearchBar` component instead of duplicating search behavior across 15 pages:

```python
class SearchBar:
    def __init__(self, page):
        self.input = page.get_by_placeholder("Search")
        self.button = page.get_by_role("button", name="Search")

    def search(self, text):
        self.input.fill(text)
        self.button.click()
```

### Videos

- [Advanced POM Patterns Video 1](https://www.youtube.com/watch?v=h-fpoNZdWCg)
- [Advanced POM Patterns Video 2](https://www.youtube.com/watch?v=AGYZk9ZlA4s&list=PLP5_A7hnY1Tj4pbbDY29wPdEgWu65uiWL)
- [Advanced POM Patterns Video 3](https://www.youtube.com/watch?v=lDK7UKWC0ak)
- [Advanced POM Patterns Video 4](https://www.youtube.com/watch?v=k488kAtT-Pw)

### Documentation

- [Reusable Components with Playwright Page Objects](https://python.plainenglish.io/enhancing-the-page-object-pattern-with-reusable-components-in-playwright-python-5a6d4481de30)

> 💡 **When to use this concept:** When UI behavior repeats, use Component Objects and Page Objects instead of duplicating code.

---

# Advanced Test Design

## 07_FixturesAndTestLifecycle.md

### What you will learn

You will learn function, class, module, and session fixture scopes; factory fixtures; dependencies; `yield` cleanup; `autouse`; parameterization; class-scoped contexts; and shared setup.

### Where you will use it

Fixtures manage users, test data, authentication, browsers, APIs, environments, and cleanup.

### Real-world example

```python
@pytest.fixture
def authenticated_page(page):
    login(page)
    return page

def test_create_task(authenticated_page):
    authenticated_page.goto("/tasks")
```

### Video

- [Fixtures and Test Lifecycle](https://www.youtube.com/watch?v=N_rCdPoltWo)

### Documentation

- [Playwright Test Runners](https://playwright.dev/python/docs/test-runners)
- [Pytest Fixtures Documentation](https://docs.pytest.org/en/stable/reference/fixtures.html)

> 💡 **When to use this concept:** When tests share setup, dependencies, data, or cleanup, use a pytest fixture.

---

## 08_ParallelExecutionAndSharding.md

### What you will learn

You will learn pytest-xdist, workers, isolation, UUID-based data, worker IDs, markers, CI matrix sharding, and avoiding shared-data collisions.

### Where you will use it

Use parallel execution when sequential regression runs are too slow. Four workers can often reduce a 60-minute suite to roughly 15–20 minutes, depending on the application and CI infrastructure.

### Real-world example

```python
import uuid
project_name = f"Automation-{uuid.uuid4()}"
```

Unique data prevents parallel tests from modifying the same records.

### Videos

- [Parallel Execution Video 1](https://www.youtube.com/watch?v=TSWXTqjMDkI)
- [Parallel Execution Video 2](https://www.youtube.com/watch?v=tBnfDaPAH44)

### Documentation

- [pytest-xdist Documentation](https://pytest-xdist.readthedocs.io/en/stable/how-to.html)

> 💡 **When to use this concept:** If tests pass alone but fail in parallel, investigate isolation and shared data.

---

## 09_AllureReporting.md

### What you will learn

You will learn Epic → Feature → Story hierarchy, `allure.step()`, screenshots, JSON evidence, request/response attachments, severity, automatic failure evidence, and GitHub Pages publishing.

### Where you will use it

Use reports to communicate results to developers, QA engineers, Product Owners, Release Managers, Technical Leads, and management.

### Real-world example

Instead of only `test_create_task FAILED`, Allure can show each step and attach screenshots, API evidence, logs, input data, and failure details.

### Video

- [Allure Reporting](https://www.youtube.com/watch?v=VHwl78QXF_0)

### Documentation

- [Allure Official Documentation](https://allurereport.org/docs/playwright/)
- [Allure Attachments and Trace Guide](https://qaskills.sh/blog/playwright-allure-attachment-trace-guide)
- [BrowserStack Guide: Allure Integration](https://www.browserstack.com/guide/integrate-allure-with-playwright)
- [Playwright Python Allure Example Project](https://github.com/nirtal85/Playwright-Python-Example)

> 💡 **When to use this concept:** A report should explain enough to start investigating without rerunning the test.

---

# API Testing

## 10_APIAuthentication.md

### What you will learn

You will learn JWT login, access tokens, refresh handling, expired and invalid tokens, unauthorized requests, and multi-user authentication.

### Where you will use it

Use it for login APIs, protected endpoints, role-based endpoints, session management, token expiration, and user-specific resources.

### Real-world example

Test the complete flow `POST /login → access token → GET /tasks` and validate missing, invalid, and expired tokens, cross-user access, and token refresh.

### Playlists and Videos

- [API Authentication Playlist 1](https://www.youtube.com/playlist?list=PLHT5rv7PEE4Oa19_17xS4I5Rbn297WJkt)
- [API Authentication Playlist 2](https://www.youtube.com/playlist?list=PLhW3qG5bs-L8WcAa9cfXaqGe0-Cq85y4X)
- [Playwright API Fundamentals](https://www.youtube.com/watch?v=XSHERugHQCY)

> 💡 **When to use this concept:** When an API returns `401` or `403`, or access depends on the user, test authentication and authorization.

---

## 11_AdvancedResponseValidation.md

### What you will learn

You will learn schema validation, required fields, data types, pagination consistency, filters, sorting, response time, and business-data consistency.

### Where you will use it

Use it for search APIs, filters, pagination, sorting, complex JSON, performance expectations, and business rules.

### Real-world example

```python
assert response.status == 200
for task in tasks:
    assert task["status"] == "completed"
```

For pagination, verify page number, page size, metadata, and that records do not repeat across pages.

### Video

- [Advanced API Validation](https://www.youtube.com/watch?v=qyCPtbEztvw)

### Documentation

- [Playwright API Testing Documentation](https://playwright.dev/python/docs/api-testing)
- [Pagination, Filtering and Sorting Validation](https://medium.com/@gunashekarr11/handling-pagination-filtering-sorting-validations-through-the-playwright-api-layer-612f010f0943)

> 💡 **When to use this concept:** Status codes prove technical success; response validation proves functional success.

---

## 12_APIFixturesAndTestData.md

### What you will learn

You will learn factory fixtures, task and comment fixtures, bulk generation, module-scoped data, cleanup, and cleanup verification.

### Where you will use it

Use API data setup for pagination, multiple users, projects, tasks, filters, comments, and complex relationships.

### Real-world example

```python
tasks = create_tasks(count=55)
```

This is much faster than creating 55 tasks manually through the UI.

### Video

- [API Fixtures and Test Data](https://www.youtube.com/watch?v=HPP_62VJQ3g)

This topic is also supported by the earlier fixtures, API testing, and parallel-execution materials.

> 💡 **When to use this concept:** For significant setup data, prefer API factories over UI creation.

---

## 13_ChainedWorkflowsAndHybridTests.md

### What you will learn

You will learn multi-step CRUD, comment lifecycles, API Create → UI Verify, UI Create → API Verify, transitions, cross-layer validation, and API-accelerated setup.

### Where you will use it

Use hybrid tests when UI setup is slow and difficult to maintain.

### Real-world example

Use API calls to create a user, project, and task, then log in through the UI and verify the task. Or create the task through the UI and use the API to validate the persisted data.

### Video

- [Hybrid UI + API Testing](https://www.youtube.com/watch?v=dv95_b8F8qM)

### Documentation

- [Playwright API Testing Documentation](https://playwright.dev/python/docs/api-testing)
- [Using Playwright for API and UI Testing Together](https://dev.to/ramamallika_kadali_49a08f/day-7-how-i-use-playwright-for-api-and-ui-testing-together-lh)

> 💡 **When to use this concept:** Use APIs for fast setup and deep verification; use UI automation for user-facing behavior.

---

## 14_MultiUserAndRoleBasedTesting.md

### What you will learn

You will learn permission matrices, admin and user behavior, concurrent actions, permission boundaries, multiple browser sessions, and cross-user workflows.

### Where you will use it

Use it for Admin, Manager, Employee, Guest, and Read-only roles.

### Real-world example

Verify that a Manager sees Delete while a regular user does not, then verify that `DELETE /tasks/123` with a regular-user token returns HTTP 403. Hiding a button is not sufficient security.

### Videos

- [Multi-User Testing Video 1](https://www.youtube.com/watch?v=XSHERugHQCY)
- [Multi-User Testing Video 2](https://www.youtube.com/watch?v=o-R1PTJ5Lws)
- [Multi-User Testing Video 3](https://www.youtube.com/watch?v=0mfLHPLZ7_k)

### Documentation

- [Testing Multiple Users and Roles with Playwright](https://playwrightqa.blogspot.com/2024/10/testing-multiple-users-and-roles-with.html)
- [Multi-User Testing with Playwright Fixtures](https://medium.com/@edtang44/isolate-and-conquer-multi-user-testing-with-playwright-fixtures-f211ad438974)
- [Handling Authentication for Multiple Users](https://www.neovasolutions.com/2024/11/14/handling-authentication-for-multiple-user-logins-in-playwright/)

> 💡 **When to use this concept:** Verify both UI restrictions and backend authorization boundaries.

---

## 15_ResilienceAndEdgeCases.md

### What you will learn

You will learn exponential-backoff retries, buggy API handling, boundaries, empty and long input, Unicode, invalid enums, missing fields, and concurrency.

### Where you will use it

Use it for forms, API validation, unstable services, user-generated content, boundary conditions, concurrent operations, and defensive behavior.

### Real-world example

Test empty input, 10,000 characters, emoji, non-Latin text, apostrophes, and script-like values. Test unsupported payloads such as `{"priority": "SUPER_MEGA_HIGH"}`. For transient failures, a controlled retry can wait 1, 2, then 4 seconds, but must not hide genuine defects.

### Videos

- [Resilience and Edge Cases Video 1](https://www.youtube.com/watch?v=NSDdeDYr3dY)
- [Resilience and Edge Cases Video 2](https://www.youtube.com/watch?v=axBr9gnITOo)

> 💡 **When to use this concept:** Happy-path tests show expected behavior; edge-case tests reveal behavior under unexpected conditions.

---

# Data-Driven Testing

## 16_DataDrivenTestingGUIAndAPI.md

### What you will learn

You will learn `@pytest.mark.parametrize`, priority and status coverage, shared UI/API datasets, form validation, filter combinations, and cross-layer reuse.

### Where you will use it

Use it for statuses, priorities, roles, form inputs, searches, filters, and valid or invalid payloads.

### Real-world example

```python
@pytest.mark.parametrize("priority", ["LOW", "MEDIUM", "HIGH"])
def test_priority(priority):
    pass
```

One test verifies all supported values and can be expanded to status-priority combinations.

### Learning material

This chapter reuses the parameterization, fixture, UI, and API concepts introduced in the preceding chapters.

> 💡 **When to use this concept:** When behavior stays the same but inputs change, use parameterization.

---

## 17_AutoWaitingAndFlakiness.md

### What you will learn

You will learn why `time.sleep()` is unreliable, Playwright auto-waiting, alternatives to `networkidle`, web-first assertions, application-state waiting, SPA-safe strategies, authenticated fixtures, and `storage_state` reuse.

### Where you will use it

Use these techniques when tests are flaky in CI, elements appear asynchronously, API timing varies, SPAs update dynamically, or background traffic continues.

### Real-world example

Replace this:

```python
page.get_by_role("button", name="Save").click()
time.sleep(5)
assert page.get_by_text("Saved")
```

with this:

```python
page.get_by_role("button", name="Save").click()
expect(page.get_by_text("Saved")).to_be_visible()
```

Also avoid blindly waiting for `networkidle`; wait for a meaningful element such as the Dashboard heading.

### Learning material

This chapter applies Playwright's built-in waiting behavior and the trace, fixture, authentication, and locator techniques introduced earlier.

> 💡 **When to use this concept:** Do not wait for time to pass. Wait for the expected application condition.

---

## 📋 Verification with GitHub Copilot

1. In GitHub Copilot, select Agent mode and use `.github/agents/review.md`.
2. Enter: `Review my exercises and follow closely the instructions on the review.md agent and create a report in my project`.
3. Select a capable model, run the review, and provide the generated report.

## 📝 License

This project is created for educational purposes.
