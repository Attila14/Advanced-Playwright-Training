# Playwright with Python — Advanced Test Automation Training

This is a skeleton Python project for learning advanced test automation with AI-powered coding assistants like GitHub Copilot.

## 📋 Overview

Advanced Self-Study Training Program  ** Organizatory curriculum **

This training is designed as an advanced self-study program. Participants will follow the instructions provided in the README.md file, clone the repository, and complete the required exercises independently.
To support the learning process, participants can refer to the videos linked within the README.md documentation. The expected duration of the training is up to 40 hours. However, if additional time is needed, participants may continue at a reasonable pace until they complete all requirements.

For questions or support during the training, a dedicated Microsoft Teams group is available (https://teams.microsoft.com/l/channel/19%3AsYBwZNxmvNGMN0I8mPZiB15OueNG5XhDKe6EV3tn-b01%40thread.tacv2/SelfStudy_Advanced_PlayWright_Training?groupId=008a7c89-4582-424e-b229-1f74766df409&tenantId=e0793d39-0939-496d-b129-198edd916feb). Participants can post their questions there, and the trainers will respond as their availability permits.
Upon completing the training, participants must review their solutions using the AI agent provided in the .github folder. Instructions for running and using the agent are available in the README.md file. The resulting output should then be shared in the Microsoft Teams group for review and feedback.
**************************************************************************************************************************
# 🧭 How the Chapters Fit Together

The exercises progress from Playwright fundamentals toward production-level automation engineering.

## Foundation

```text
01 Browser Context Management
       ↓
02 Network Interception
       ↓
03 Advanced Locator Strategies
```

You first learn how the browser is structured, how the UI communicates with backend services, and how to interact reliably with elements.

## Debugging and Test Quality

```text
04 Performance and Tracing
       ↓
05 Visual Testing
```

You learn how to investigate failures and identify problems that normal functional assertions cannot detect.

## Framework Architecture

```text
06 Advanced POM Patterns
       ↓
07 Fixtures and Test Lifecycle
```

You learn how to organize automation code so that a test suite remains maintainable as it grows.

## Scaling Automation

```text
08 Parallel Execution and Sharding
       ↓
09 Allure Reporting
```

You learn how to run a large regression suite efficiently and communicate its results clearly.

## API Automation

```text
10 API Authentication
       ↓
11 Advanced Response Validation
       ↓
12 API Fixtures and Test Data
```

You build the skills required to test backend services and use APIs as part of a broader automation strategy.

## Real End-to-End Testing

```text
13 Chained Workflows and Hybrid Tests
       ↓
14 Multi-User and Role-Based Testing
```

You combine UI testing, API testing, authentication, browser contexts, and test data into realistic business workflows.

## Production-Level Test Quality

```text
15 Resilience and Edge Cases
       ↓
16 Data-Driven Testing
       ↓
17 Auto-Waiting and Flakiness
```

You learn how to build test suites that cover unusual conditions, scale across many datasets, and remain reliable in CI/CD environments.

---

# 🧠 Problem and Automation Technique Mapping

A major objective of this training is to recognize a testing problem and identify the appropriate automation technique.

| When you encounter this situation | Technique to consider |
|---|---|
| I need two users logged in simultaneously | Browser Contexts |
| I need the backend to return a particular error | Network Interception |
| My locator keeps breaking | Semantic and Scoped Locators |
| My test fails only in CI | Trace Viewer and Diagnostics |
| The application works but visually looks wrong | Visual Testing |
| My framework contains duplicated UI code | POM and Component Objects |
| Every test repeats the same setup | pytest Fixtures |
| My regression suite takes too long | Parallel Execution and Sharding |
| Nobody understands why a CI test failed | Allure Reporting |
| My API returns `401` or `403` | Authentication and Authorization Testing |
| My API returns `200` but incorrect data | Advanced Response Validation |
| A test needs 50 records before it can start | API Fixtures and Test Data |
| UI preparation makes tests extremely slow | Hybrid API and UI Testing |
| Different users have different permissions | Multi-User and Role-Based Testing |
| I need to verify invalid or unexpected inputs | Resilience and Edge Cases |
| The same scenario must run with 20 inputs | Data-Driven Testing |
| A test randomly fails while the application loads | Auto-Waiting and Web-First Assertions |

---

> 💡 Recommendation:
>
> Complete the exercises sequentially. Each module introduces concepts that are reused in later exercises.
>
> The objective is not simply to learn individual Playwright commands. By the end of the training, you should be able to recognize a real testing problem, select an appropriate automation technique, and apply it within a maintainable Playwright and pytest framework.

---


## 🌐 Application Under Test

| | URL |
|---|---|
| UI (list view) | https://testauto.app/task-manager-spa |
| UI (board view) | https://testauto.app/task-manager-spa?view=board |
| Create modal | https://testauto.app/task-manager-spa?taskModal=create |
| API V1 (no auth) | https://api.testauto.app/api/v1 |
| API V2 (JWT) | https://api.testauto.app/api/v2 |
| Buggy API | https://api.testauto.app/api/buggy |
| API Docs | https://api.testauto.app/swagger-ui/index.html |
| App Docs | https://testauto.app/docs |

**Test credentials (API V2):** `admin/admin123` · `user/user123` · `testuser/test123`

---

## 📁 Project Structure

```
playwright-python-advanced-training/
├── Exercises/
│   ├── 01_BrowserContextManagement.md
│   ├── 02_NetworkInterception.md
│   ├── 03_AdvancedLocatorStrategies.md
│   ├── 04_PerformanceAndTracing.md
│   ├── 05_VisualTesting.md
│   ├── 06_AdvancedPOMPatterns.md
│   ├── 07_FixturesAndTestLifecycle.md
│   ├── 08_ParallelExecutionAndSharding.md
│   ├── 09_AllureReporting.md
│   ├── 10_APIAuthentication.md
│   ├── 11_AdvancedResponseValidation.md
│   ├── 12_APIFixturesAndTestData.md
│   ├── 13_ChainedWorkflowsAndHybridTests.md
│   ├── 14_MultiUserAndRoleBasedTesting.md
│   ├── 15_ResilienceAndEdgeCases.md
│   └── 16_DataDrivenTestingGUIAndAPI.md
├── src/
│   ├── pages/
│   │   ├── task_manager_page.py    # skeleton — fill in Exercise 06
│   │   ├── task_form_modal.py
│   │   ├── task_detail_modal.py
│   │   └── login_modal.py           # Exercise 17 — SPA login modal
│   ├── tests/
│   │   ├── smoke_test.py           # run first to verify setup
│   │   ├── test_browser_context.py # Exercise 01
│   │   ├── test_network.py         # Exercise 02
│   │   ├── test_selectors.py       # Exercise 03
│   │   ├── test_performance.py     # Exercise 04
│   │   ├── test_visual.py          # Exercise 05
│   │   ├── test_advanced_pom.py    # Exercise 06
│   │   ├── test_fixtures.py        # Exercise 07
│   │   ├── test_parallel.py        # Exercise 08
│   │   ├── test_allure.py          # Exercise 09
│   │   ├── test_api_auth.py        # Exercise 10
│   │   ├── test_api_validation.py  # Exercise 11
│   │   ├── test_api_data.py        # Exercise 12
│   │   ├── test_workflows.py       # Exercise 13
│   │   ├── test_multi_user.py      # Exercise 14
│   │   ├── test_resilience.py      # Exercise 15
│   │   ├── test_data_driven.py     # Exercise 16
│   │   └── test_auto_waiting.py    # Exercise 17
│   └── conftest.py
├── .github/
│   ├── agents/review.md
│   └── workflows/playwright.yml
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 🧪 Example Tests

### UI Testing (Playwright)
The smoke test in `src/tests/smoke_test.py` demonstrates basic navigation, element visibility, and API health checks.

### API Testing (Playwright APIRequestContext)
The `api_v1` and `api_v2` fixtures in `src/conftest.py` provide pre-configured request contexts — one unauthenticated, one pre-logged-in with JWT.

---

## 💡 Best Practices

- Page object code goes in `src/pages/` — locators and actions only
- Test code goes in `src/tests/` — test functions, no raw selectors
- Shared fixtures go in `src/conftest.py`
- Every test that creates API data **must clean it up** — use `try/finally`
- Use `uuid` to generate unique task titles — prevents cross-test interference
- Prefer `get_by_role`, `get_by_label`, `get_by_placeholder` over CSS selectors
- Use `expect()` for assertions — it retries automatically

---

## 🔧 Configuration

```bash
pytest --browser=firefox --headed --slowmo=500   # custom browser run
pytest -n 4                                       # parallel
pytest -m fast                                    # fast tests only
pytest --alluredir=allure-results                 # with Allure
```

---

## 📚 Dependencies

- Playwright 1.44+  ·  pytest 8+  ·  pytest-playwright 0.5+
- pytest-xdist 3.5+  ·  pytest-shard 0.1.2+  ·  allure-pytest 2.13+

---

## 🤝 Contributing

This is a training project. Feel free to add test cases, improve page objects, or share your learnings.

---

## 📖 Resources

The following videos, playlists, articles, and documentation are mapped to each training exercise and can be used as learning material while progressing through the course.





This project demonstrates advanced test automation using:

- **Playwright for Python** for UI/Web and API testing
- **pytest** as the testing framework
- **pytest-playwright** for Playwright fixtures and browser management
- **Allure** for test reporting
- **pytest-xdist** for parallel test execution

The training targets a real, live application: [testauto.app/task-manager-spa](https://testauto.app/task-manager-spa)

## 📋 Verification of the training will be done using a reviewer agent with GitHub Copilot
  Once you have finished the exercises, you need to run through GitHub Copilot a review of your project. Follow the following steps:
  1.On GitHub Copilot, select the agent mode together with the review.md file from the .github/agents/review.md 
  2. Enter the following prompt 'Review my exercises and follow closely the instructions on the review.md agent and create a report in my project' and select a capable LLM then hit enter
  3. Provide the report to us

---

## 🚀 Getting Started

### Prerequisites

#### 1. Python 3.11+
- Download: https://www.python.org/downloads/
- Installation: Run the installer. On Windows, check **"Add Python to PATH"** during setup
- Verify: Open terminal and run `python --version`

#### 2. Visual Studio Code (Recommended IDE)
- Download: https://code.visualstudio.com/
- Recommended Extensions:
  - **Python** (Microsoft)
  - **Pylance** (Microsoft)
  - **Playwright Test for VSCode** (Microsoft)
  - **GitHub Copilot** (for AI assistance)
- Alternative IDEs: PyCharm, IntelliJ IDEA with Python plugin

#### 3. Git
- Download: https://git-scm.com/downloads
- Verify: `git --version`

#### 4. GitHub Account
- Sign up: https://github.com/join
- Required for GitHub Copilot (even the free version)

#### 5. GitHub Copilot
1. Open VS Code
2. Click the Copilot icon at the top of the window
3. Sign in to your GitHub account when prompted
4. Optional: activate the 30-day free trial at https://github.com/github-copilot/pro

#### 6. Clone the repository

**Using terminal:**
```bash
git clone https://github.com/YOUR_USERNAME/playwright-python-advanced-training.git
cd playwright-python-advanced-training
```

**Using Visual Studio Code:**
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type `Git: Clone` and select it
3. Paste the repository URL
4. Choose a folder and open when prompted

> **Note:** If this is your first time using GitHub with VS Code, you will be prompted to sign in during the clone process.

#### 7. Set up the Python environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

pip install -r requirements.txt
playwright install chromium firefox webkit
```

#### 8. Verify your setup

```bash
pytest src/tests/smoke_test.py -v
```

All 5 smoke tests should pass — you are ready to start.

---


## 🎯 Training Exercises

The training is divided into a series of progressively advanced exercises located in the `Exercises/` folder.

Each exercise focuses on a specific area of Playwright, pytest, API testing, or modern test automation architecture.

For every chapter, you will understand:

1. What you will learn
2. Where you can use the concept
3. What kind of real-world testing problem the concept can solve

Complete the exercises in order because later chapters build on concepts introduced in earlier modules.

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

This is useful when testing:

- Applications requiring authentication
- Different user roles
- Multi-user workflows
- Desktop and mobile layouts
- Tests running in parallel
- Applications where one user's session must not interfere with another user's session

### Real-world example

Imagine that you are testing a task-management application.

Alice creates a task and assigns it to Bob. Bob should immediately see the task in his account.

Instead of performing this sequence:

1. Login as Alice
2. Create the task
3. Logout
4. Login as Bob
5. Verify the task

you can create two independent browser contexts:

```python
alice_context = browser.new_context(storage_state="alice.json")
bob_context = browser.new_context(storage_state="bob.json")

alice_page = alice_context.new_page()
bob_page = bob_context.new_page()
```

Alice and Bob can now remain logged in simultaneously without their sessions interfering with each other.

> 💡 When to use this concept:
>
> When a test requires multiple independent users, authentication sessions, or browser configurations, use BrowserContext.

---

## 02_NetworkInterception.md

### What you will learn

You will learn how Playwright can observe and manipulate communication between the browser and backend APIs.

You will learn:

- How to intercept API calls with `page.route()`
- How to return mocked responses instead of calling the real backend
- How to create empty-state responses
- How to inject custom data into API responses
- How to capture and inspect outgoing requests
- How to validate request payloads
- How to simulate HTTP errors such as `400`, `401`, `403`, `404`, and `500`
- How to simulate slow or unstable backend behavior

### Where you will use it

This is useful when testing:

- Error-handling screens
- Empty states
- Loading indicators
- Backend failures
- Features where the backend is not yet available
- Difficult-to-reproduce API conditions
- Responses that are difficult to create using real test data

### Real-world example

Suppose the application displays the following message only when the backend returns an empty list:

```text
No tasks available.
```

Instead of manually deleting every task from the test environment, you can intercept the request.

The following example uses a regular expression so that no wildcard formatting characters are required:

```python
import re

page.route(
    re.compile(r".*/api/tasks$"),
    lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body="[]"
    )
)
```

You can now test the empty state without modifying the actual backend data.

Another situation could be:

```text
GET /api/tasks
       ↓
HTTP 500
```

You can simulate this server error and verify that the UI displays an appropriate error message.

> 💡 When to use this concept:
>
> When you need the backend to behave in a specific way for a UI test, use Network Interception.

---

# UI Testing — Locators and Interactions

## 03_AdvancedLocatorStrategies.md

### What you will learn

You will learn how to identify UI elements reliably without depending on fragile CSS selectors or complicated XPath expressions.

You will learn:

- Semantic locators such as:
  - `get_by_role()`
  - `get_by_label()`
  - `get_by_placeholder()`
- Text-based filtering with `filter()`
- How to use `nth()`, `first`, and `last`
- How to scope locators inside specific containers
- Board-view column scoping
- Dynamic locator loops
- How to locate elements inside lists, tables, cards, and dynamic components

### Where you will use it

Reliable locator strategies are important in almost every Playwright UI test.

They become especially useful when:

- Multiple elements contain similar text
- Elements change position
- Lists are dynamically generated
- The same component appears multiple times
- The UI structure changes frequently
- Tests fail because selectors depend too heavily on HTML structure

### Real-world example

Imagine a Kanban board containing the following tasks:

```text
TODO
  Task A
  Task B

IN PROGRESS
  Task A
  Task C
```

You want to interact specifically with Task A inside the IN PROGRESS column.

Searching globally for Task A is ambiguous because two tasks have the same name.

Instead, first locate the correct column and then search inside it:

```python
column = page.get_by_test_id("in-progress-column")
task = column.get_by_text("Task A")
```

This approach makes the locator more specific and easier to maintain.

> 💡 When to use this concept:
>
> When several similar elements exist on the page, first scope the locator to the appropriate component and then search inside it.

---

## 04_PerformanceAndTracing.md

### What you will learn

You will learn how to investigate failing tests and collect diagnostic information automatically.

You will learn:

- How to use the Playwright Trace Recorder
- How to inspect test execution with Trace Viewer
- How to analyze DOM snapshots
- How to inspect screenshots captured during execution
- How to inspect network requests and responses
- How to capture and analyze HAR files
- How to collect page performance metrics
- How to monitor JavaScript console errors
- How to capture traces automatically when tests fail

### Where you will use it

These techniques are especially useful for:

- CI/CD pipeline failures
- Intermittent test failures
- Tests that pass locally but fail in CI
- Slow pages or API responses
- Network-related problems
- Unexpected JavaScript errors
- Difficult production-like scenarios

### Real-world example

Imagine that a test fails once every 20 executions:

```text
Expected: "Task created"
Received: "Loading..."
```

When you run the test again, it passes.

Instead of guessing, you can inspect the Playwright trace and discover the following sequence:

```text
POST /tasks
     ↓
The response took 8.7 seconds
     ↓
The UI was still displaying the loading state
     ↓
The assertion was executed before the result appeared
```

The trace provides evidence showing exactly what happened before the failure.

You can inspect:

- The actions performed by the test
- The page before and after each action
- The element targeted by Playwright
- Network requests and responses
- Browser console messages
- Screenshots and DOM snapshots
- The exact point at which the test failed

This helps you determine whether the failure was caused by:

- A slow backend response
- An incorrect locator
- A missing wait condition
- A frontend JavaScript error
- A network failure
- A genuine product defect

> 💡 When to use this concept:
>
> When a test fails and you cannot reproduce the problem locally, investigate the trace and runtime evidence instead of relying only on the final error message.

---

# UI Testing — Test Quality

## 05_VisualTesting.md

### What you will learn

You will learn how to detect visual problems that normal functional assertions may not detect.

You will learn:

- Screenshot capture
- Pixel-by-pixel comparison
- Image comparison using Pillow
- Masking dynamic content
- Element-level screenshots
- Defining acceptable visual differences
- Mobile and Desktop visual comparison

### Where you will use it

Visual testing is useful for discovering:

- Broken layouts
- CSS regressions
- Missing icons
- Misaligned buttons
- Incorrect styling
- Overlapping components
- Responsive design problems

### Real-world example

A functional test verifies:

```python
expect(
    page.get_by_role("button", name="Save")
).to_be_visible()
```

The test passes because the button exists and is visible.

However, a CSS change could cause the button to overlap another field or appear in the wrong location. A normal visibility assertion may not detect this.

A visual comparison can detect that the page no longer looks like the approved baseline.

> 💡 When to use this concept:
>
> Functional testing answers: Does it work?
>
> Visual testing answers: Does it still look correct?

---

## 06_AdvancedPOMPatterns.md

### What you will learn

You will move beyond basic Page Object Model implementation and learn how to create a scalable automation architecture.

You will learn:

- Reusable Component Objects
- Shared `BasePage` implementation
- `SearchBar` component
- `Pagination` component
- `TaskModal` component
- Sharing behavior between pages
- Fixture-integrated Page Objects
- How to reduce duplicated selectors and actions

### Where you will use it

This becomes important when an automation project grows from a small number of tests into hundreds of tests maintained by multiple engineers.

For example:

```text
20 tests
   ↓
100 tests
   ↓
500 or more tests
```

Without a good framework architecture, test maintenance becomes increasingly difficult as the suite grows.

### Real-world example

Imagine that 15 pages contain the same search component.

Instead of implementing search behavior independently on every page, create a reusable component:

```python
class SearchBar:

    def __init__(self, page):
        self.input = page.get_by_placeholder("Search")
        self.button = page.get_by_role(
            "button",
            name="Search"
        )

    def search(self, text):
        self.input.fill(text)
        self.button.click()
```

Every page can reuse the same component.

If the search component changes, you update the automation implementation in one place rather than modifying many tests.

> 💡 When to use this concept:
>
> When the same UI behavior or component appears repeatedly, use Component Objects and Page Objects instead of duplicating test code.

---

# Advanced Test Design

## 07_FixturesAndTestLifecycle.md

### What you will learn

You will learn how pytest manages test setup, shared resources, dependencies, and cleanup.

You will learn the following fixture scopes:

- Function
- Class
- Module
- Session

You will also learn:

- Factory fixtures
- Fixture dependencies
- Automatic cleanup using `yield`
- `autouse` fixtures
- `@pytest.mark.parametrize`
- Class-scoped browser contexts
- Sharing setup logic between tests

### Where you will use it

Fixtures help manage commonly repeated automation activities such as:

- Creating users
- Creating test data
- Authentication
- Browser initialization
- API setup
- Environment preparation
- Cleanup after tests

### Real-world example

Suppose 20 tests require an authenticated user.

Instead of calling login logic inside every test:

```python
login(page)
```

you can create a shared fixture:

```python
@pytest.fixture
def authenticated_page(page):
    login(page)
    return page
```

Tests can then use the fixture:

```python
def test_create_task(authenticated_page):
    authenticated_page.goto("/tasks")
```

The test focuses on the behavior being tested rather than repetitive setup.

> 💡 When to use this concept:
>
> When many tests require the same setup, dependency, data, or cleanup operation, use a pytest fixture.

---

## 08_ParallelExecutionAndSharding.md

### What you will learn

You will learn how to reduce test execution time by running tests simultaneously.

You will learn:

- How to run tests in parallel using `pytest-xdist`
- How multiple pytest workers operate
- Test isolation strategies
- UUID-based test data
- Worker ID fixtures
- Fast and slow test markers
- CI matrix sharding
- How to prevent parallel tests from modifying the same data

### Where you will use it

This becomes important when regression suites become too slow to execute sequentially.

For example:

```text
1 worker  → 60 minutes
4 workers → approximately 15 to 20 minutes
8 workers → potentially 8 to 12 minutes
```

The actual improvement depends on the tests, application, backend capacity, and CI infrastructure.

### Real-world example

Suppose four parallel tests create a project with the same name:

```text
Automation Project
```

The tests can interfere with each other because they manipulate identical data.

Instead, generate a unique project name:

```python
import uuid

project_name = f"Automation-{uuid.uuid4()}"
```

Each test execution now receives unique data.

> 💡 When to use this concept:
>
> When tests work individually but fail in parallel, investigate test isolation and shared data before assuming that parallel execution is the problem.

---

## 09_AllureReporting.md

### What you will learn

You will learn how to transform raw test execution results into structured reports that engineers and stakeholders can understand.

You will learn:

- Epic → Feature → Story hierarchy
- `allure.step()` annotations
- Screenshot attachments
- JSON attachments
- Request and response evidence
- Severity levels
- Automatic attachments on failure
- GitHub Pages report publishing

### Where you will use it

Reports are useful when communicating results to:

- Developers
- QA Engineers
- Product Owners
- Release Managers
- Technical Leads
- Management

### Real-world example

Instead of CI reporting only:

```text
test_create_task FAILED
```

Allure can provide a structured execution:

```text
Task Management
 └── Create Task
      ├── Login passed
      ├── Navigate to Tasks passed
      ├── Create Task passed
      └── Verify Status failed
```

The failure can additionally contain:

- Screenshots
- API requests
- API responses
- Logs
- Input data
- Failure details

> 💡 When to use this concept:
>
> When someone asks why an automated test failed, the report should provide enough evidence to begin the investigation without immediately rerunning the test.

---

# API Testing

## 10_APIAuthentication.md

### What you will learn

You will learn how modern APIs authenticate users and how authentication scenarios can be automated.

You will learn:

- JWT login workflows
- Access token management
- Token refresh handling
- Expired token handling
- Unauthorized request validation
- Invalid token scenarios
- Multi-user authentication scenarios

### Where you will use it

Authentication testing is essential for APIs that expose protected resources.

You will commonly use it for:

- Login APIs
- Protected endpoints
- Role-based endpoints
- Session management
- Token expiration
- User-specific resources

### Real-world example

A typical authentication flow could be:

```text
POST /login
     ↓
Access token returned
     ↓
GET /tasks

Authorization: Bearer token
```

You can test scenarios such as:

- What happens without a token?
- What happens with an invalid token?
- What happens with an expired token?
- Can User A access User B's resources?
- Does token refresh work correctly?

> 💡 When to use this concept:
>
> When an API returns `401` or `403`, or access depends on the authenticated user, use authentication and authorization testing.

---

## 11_AdvancedResponseValidation.md

### What you will learn

You will move beyond checking only the HTTP status code and verify whether the returned data is actually correct.

A basic check might be:

```python
assert response.status == 200
```

You will also learn:

- Schema validation
- Required fields and data types
- Pagination consistency checks
- Filter accuracy verification
- Sorting validation
- Response-time assertions
- Data consistency validation

### Where you will use it

Advanced response validation belongs in practically every serious API automation suite.

It is particularly useful for:

- Search APIs
- Filter endpoints
- Pagination
- Sorting
- Complex JSON responses
- Performance expectations
- Business-rule validation

### Real-world example

Suppose the following request returns HTTP `200`:

```http
GET /tasks?status=completed
```

This confirms only that the request technically succeeded.

You should also verify the returned data:

```python
for task in tasks:
    assert task["status"] == "completed"
```

The endpoint could return HTTP `200` while still returning incorrect business data.

For pagination, if you request:

```http
GET /tasks?page=2&size=10
```

you should verify that:

- The correct page was returned
- No more than 10 records were returned
- Pagination metadata is correct
- Records are not duplicated between pages

> 💡 When to use this concept:
>
> Status-code validation tells you whether a request succeeded technically. Response validation tells you whether it succeeded functionally.

---

## 12_APIFixturesAndTestData.md

### What you will learn

You will learn how to create predictable and reusable API test data automatically.

You will learn:

- Factory fixtures
- Complete task fixtures
- Task and comments fixtures
- Bulk data generation
- Module-scoped shared data
- Cleanup strategies
- Cleanup verification

### Where you will use it

This is useful whenever tests require predictable data before they can start.

Examples include:

- Testing pagination
- Preparing multiple users
- Creating projects and tasks
- Testing filters
- Creating comments
- Preparing complex entity relationships

### Real-world example

Suppose a pagination test requires 55 tasks.

Creating 55 tasks manually through the UI would be extremely slow.

Instead, an API fixture can prepare them:

```python
tasks = create_tasks(count=55)
```

You can then run the pagination test and delete the generated data afterward.

Another test might require:

```text
1 project
   ↓
5 tasks
   ↓
3 comments per task
```

A fixture can create this entire structure before the test starts.

> 💡 When to use this concept:
>
> When a test requires significant setup data, use API fixtures or data factories instead of creating everything through the UI.

---

## 13_ChainedWorkflowsAndHybridTests.md

### What you will learn

You will learn how to combine API and UI automation into efficient end-to-end workflows.

You will learn:

- Multi-step CRUD workflows
- Comment lifecycle validation
- API Create → UI Verify
- UI Create → API Verify
- Status transition testing
- Cross-layer validation
- Using APIs to accelerate UI-test preparation

### Where you will use it

Hybrid tests are useful when UI setup would otherwise make tests slow and difficult to maintain.

They allow you to test a specific UI behavior without spending most of the test preparing data through the UI.

### Real-world example

Suppose you want to verify that a backend-created task appears correctly in the UI.

You can use this workflow:

```text
API → Create user
API → Create project
API → Create task

UI  → Login
UI  → Open project
UI  → Verify task
```

This keeps setup fast while preserving the important UI verification.

The opposite direction is also possible:

```text
UI  → Create task
API → Retrieve the task
API → Verify persisted data
```

The UI verifies the user's experience while the API verifies that the correct information was stored.

> 💡 When to use this concept:
>
> Use APIs for fast setup and deep verification. Use UI automation for behavior that requires validation through the user interface.

---

## 14_MultiUserAndRoleBasedTesting.md

### What you will learn

You will learn how to verify that users can perform only the operations allowed by their roles and permissions.

You will learn:

- Role and permission documentation
- Permission matrices
- Admin and regular-user behavior
- Concurrent user actions
- Permission boundary testing
- Multiple browser sessions running simultaneously
- Cross-user workflows

### Where you will use it

This is important for applications containing roles such as:

```text
Admin
Manager
Employee
Guest
Read-only User
```

It is particularly useful when different users have different access to data or functionality.

### Real-world example

Suppose the requirement states:

```text
Managers may delete tasks.
Regular users may not delete tasks.
```

You can verify the UI behavior:

```text
Manager
   ↓
Delete button is visible

Regular User
   ↓
Delete button is unavailable
```

However, UI validation alone is not sufficient.

You should also verify the backend:

```text
DELETE /tasks/123
Regular User Token
        ↓
HTTP 403
```

A hidden Delete button does not provide actual security if the API still allows the operation.

> 💡 When to use this concept:
>
> Role-based testing should verify both UI restrictions and backend authorization boundaries.

---

## 15_ResilienceAndEdgeCases.md

### What you will learn

You will learn how to test situations outside the standard happy path and verify how the application behaves under unusual or invalid conditions.

You will learn:

- Retry with exponential backoff
- Buggy API handling
- Boundary value testing
- Empty input validation
- Long text validation
- Unicode testing
- Invalid enum values
- Missing required fields
- Concurrent request handling

### Where you will use it

This type of testing helps discover defects that normal happy-path testing frequently misses.

It is useful for:

- Form validation
- API validation
- Unstable services
- User-generated content
- Boundary conditions
- Concurrent operations
- Defensive application behavior

### Real-world example

A username field normally receives:

```text
Attila
```

Robust testing should also consider values such as:

```text
An empty string
A string containing 10,000 characters
Attila 😊
田中
O'Connor
A script-like input
```

An API could also receive:

```json
{
  "priority": "SUPER_MEGA_HIGH"
}
```

even though the supported values are:

```text
LOW
MEDIUM
HIGH
```

The test should verify that invalid input is rejected safely and predictably.

For a temporarily unstable API, retry logic with exponential backoff could follow this pattern:

```text
Attempt 1 → wait 1 second
Attempt 2 → wait 2 seconds
Attempt 3 → wait 4 seconds
```

Retries should be used only for expected transient failures. They should not hide genuine product defects.

> 💡 When to use this concept:
>
> Happy-path testing demonstrates that the application works under expected conditions. Edge-case testing discovers how it behaves when conditions are unexpected.

---

# Data-Driven Testing

## 16_DataDrivenTestingGUIAndAPI.md

### What you will learn

You will learn how to execute the same test logic against many different inputs without duplicating test code.

You will learn:

- `@pytest.mark.parametrize`
- Priority and status coverage
- Shared datasets across UI and API tests
- Form validation scenarios
- Filter-combination testing
- Reusing datasets across different test layers

### Where you will use it

Data-driven testing is useful when the same behavior must be verified using many different inputs.

Typical examples include:

- Supported statuses
- Priority values
- User roles
- Form inputs
- Search criteria
- Filter combinations
- Valid and invalid API payloads

### Real-world example

Instead of writing three separate tests:

```python
def test_low_priority():
    pass

def test_medium_priority():
    pass

def test_high_priority():
    pass
```

you can write:

```python
@pytest.mark.parametrize(
    "priority",
    ["LOW", "MEDIUM", "HIGH"]
)
def test_priority(priority):
    pass
```

One test now verifies all supported values.

You can expand this concept to combinations:

```text
Status       Priority
---------------------
Open         Low
Open         High
Closed       Low
Closed       High
```

The same dataset can potentially be reused for both UI and API validation.

> 💡 When to use this concept:
>
> When the test behavior stays the same but the input changes, use parameterization and data-driven testing.

---

## 17_AutoWaitingAndFlakiness.md

### What you will learn

You will learn how Playwright automatically waits for elements and application states instead of depending on fixed delays.

This chapter focuses on one of the biggest challenges in UI automation: flaky tests.

You will learn:

- Why `time.sleep()` creates slow and unreliable tests
- Playwright's built-in auto-waiting mechanism
- When to replace `wait_for_load_state("networkidle")`
- Web-first assertions using `expect()`
- Waiting for actual application state instead of arbitrary time
- SPA-safe waiting strategies
- Reusable `authenticated_page` fixtures
- Authentication state reuse with `storage_state`

### Where you will use it

You will use these techniques throughout almost every Playwright automation project.

They are especially important when:

- Tests pass locally but randomly fail in CI
- Elements appear after asynchronous operations
- APIs respond at different speeds
- React, Vue, Angular, or other SPA pages update dynamically
- Background requests continue after the page becomes usable
- Tests contain many explicit sleeps or unnecessary waits

### Real-world example

A fragile approach:

```python
page.get_by_role("button", name="Save").click()

time.sleep(5)

assert page.get_by_text("Saved")
```

The test assumes that five seconds is enough.

If CI requires six seconds, the test fails.

If the application responds in 300 milliseconds, the test unnecessarily waits for almost five additional seconds.

A better approach is:

```python
page.get_by_role("button", name="Save").click()

expect(
    page.get_by_text("Saved")
).to_be_visible()
```

Playwright now waits for the condition that actually matters.

### Another real-world example

Avoid relying blindly on:

```python
page.wait_for_load_state("networkidle")
```

A modern SPA may continuously perform:

- Analytics calls
- Polling
- WebSocket communication
- Background API requests

The application may already be ready for the user even though network activity continues.

Instead, wait for something meaningful:

```python
expect(
    page.get_by_role(
        "heading",
        name="Dashboard"
    )
).to_be_visible()
```

The test now waits for the application state that matters to the scenario.

> 💡 When to use this concept:
>
> Do not wait for time to pass. Wait for the expected application condition to become true.

---



---

# UI Testing — Browser & Page

## Point 1 — Browser Context Management

### Video
- [Playwright with Python and Pytest (Playlist)](https://www.youtube.com/watch?v=XSHERugHQCY)

---

## Point 2 — Network Interception

### Videos
- [Network Interception Video 1](https://www.youtube.com/watch?v=egqzRXOc7cU)
- [Network Interception Video 2](https://www.youtube.com/watch?v=qjqAe8qe0kY)

---

# UI Testing — Locators & Interactions

## Point 3 — Advanced Locator Strategies

### Video
- [Advanced Locator Strategies](https://www.youtube.com/watch?v=MXFAHvcqh7I)

### Additional Material
For the advanced parts:
- `filter()`
- `nth()`
- `first`
- `last`
- Dynamic loops
- Board-column scoping

Use:

```text
6-Playwright_MOD3_MOD4.pptx
```

---

## Point 4 — Performance and Tracing

### Videos
- [Performance and Tracing Video 1](https://www.youtube.com/watch?v=LrOXygsYnnk)
- [Performance and Tracing Video 2](https://www.youtube.com/watch?v=Zu_qzwH8zSs)
- [Performance and Tracing Video 3](https://www.youtube.com/watch?v=HNGPAjk_BCI)

### Documentation
- [HAR Replay and Analysis](https://ray.run/videos/148-network-replay-har-playwright-tutorial-part-79)

---

# UI Testing — Test Quality

## Point 5 — Visual Testing

### Videos
- [Visual Testing Video 1](https://www.youtube.com/watch?v=O5AyMSxfFbg)
- [Visual Testing Video 2](https://www.youtube.com/watch?v=LrOXygsYnnk)

---

## Point 6 — Advanced POM Patterns

### Videos
- [Advanced POM Patterns Video 1](https://www.youtube.com/watch?v=h-fpoNZdWCg)
- [Advanced POM Patterns Video 2](https://www.youtube.com/watch?v=AGYZk9ZlA4s&list=PLP5_A7hnY1Tj4pbbDY29wPdEgWu65uiWL)
- [Advanced POM Patterns Video 3](https://www.youtube.com/watch?v=lDK7UKWC0ak)
- [Advanced POM Patterns Video 4](https://www.youtube.com/watch?v=k488kAtT-Pw)

### Documentation
- [Reusable Components with Playwright Page Objects](https://python.plainenglish.io/enhancing-the-page-object-pattern-with-reusable-components-in-playwright-python-5a6d4481de30)

---

# Advanced Test Design

## Point 7 — Fixtures and Test Lifecycle

### Video
- [Fixtures and Test Lifecycle](https://www.youtube.com/watch?v=N_rCdPoltWo)

### Documentation
- [Playwright Test Runners](https://playwright.dev/python/docs/test-runners)
- [Pytest Fixtures Documentation](https://docs.pytest.org/en/stable/reference/fixtures.html)

---

## Point 8 — Parallel Execution and Sharding

### Videos
- [Parallel Execution Video 1](https://www.youtube.com/watch?v=TSWXTqjMDkI)
- [Parallel Execution Video 2](https://www.youtube.com/watch?v=tBnfDaPAH44)

### Documentation
- [pytest-xdist Documentation](https://pytest-xdist.readthedocs.io/en/stable/how-to.html)

---

## Point 9 — Allure Reporting

### Video
- [Allure Reporting](https://www.youtube.com/watch?v=VHwl78QXF_0)

### Documentation
- [Allure Official Documentation](https://allurereport.org/docs/playwright/)
- [Allure Attachments and Trace Guide](https://qaskills.sh/blog/playwright-allure-attachment-trace-guide)
- [BrowserStack Guide: Allure Integration](https://www.browserstack.com/guide/integrate-allure-with-playwright)
- [Playwright Python Allure Example Project](https://github.com/nirtal85/Playwright-Python-Example)

---

# API Testing

## Point 10 — API Authentication

### Playlists & Videos
- [API Authentication Playlist 1](https://www.youtube.com/playlist?list=PLHT5rv7PEE4Oa19_17xS4I5Rbn297WJkt)
- [API Authentication Playlist 2](https://www.youtube.com/playlist?list=PLhW3qG5bs-L8WcAa9cfXaqGe0-Cq85y4X)
- [Playwright API Fundamentals](https://www.youtube.com/watch?v=XSHERugHQCY)

---

## Point 11 — Advanced Response Validation

### Documentation
- [Playwright API Testing Documentation](https://playwright.dev/python/docs/api-testing)
- [Pagination, Filtering and Sorting Validation](https://medium.com/@gunashekarr11/handling-pagination-filtering-sorting-validations-through-the-playwright-api-layer-612f010f0943)

### Video
- [Advanced API Validation](https://www.youtube.com/watch?v=qyCPtbEztvw)

---

## Point 12 — API Fixtures and Test Data

Already covered in previous videos regarding:

- Fixtures
- API Testing
- Parallel Execution

### Video
- [API Fixtures and Test Data](https://www.youtube.com/watch?v=HPP_62VJQ3g)

---

## Point 13 — Chained Workflows and Hybrid Tests

### Video
- [Hybrid UI + API Testing](https://www.youtube.com/watch?v=dv95_b8F8qM)

### Documentation
- [Playwright API Testing Documentation](https://playwright.dev/python/docs/api-testing)
- [Using Playwright for API and UI Testing Together](https://dev.to/ramamallika_kadali_49a08f/day-7-how-i-use-playwright-for-api-and-ui-testing-together-lh)

---

## Point 14 — Multi-User and Role-Based Testing

### Documentation
- [Testing Multiple Users and Roles with Playwright](https://playwrightqa.blogspot.com/2024/10/testing-multiple-users-and-roles-with.html)
- [Multi-User Testing with Playwright Fixtures](https://medium.com/@edtang44/isolate-and-conquer-multi-user-testing-with-playwright-fixtures-f211ad438974)
- [Handling Authentication for Multiple Users](https://www.neovasolutions.com/2024/11/14/handling-authentication-for-multiple-user-logins-in-playwright/)

### Videos
- [Multi-User Testing Video 1](https://www.youtube.com/watch?v=XSHERugHQCY)
- [Multi-User Testing Video 2](https://www.youtube.com/watch?v=o-R1PTJ5Lws)
- [Multi-User Testing Video 3](https://www.youtube.com/watch?v=0mfLHPLZ7_k)

---

## Point 15 — Resilience and Edge Cases

### Videos
- [Resilience and Edge Cases Video 1](https://www.youtube.com/watch?v=NSDdeDYr3dY)
- [Resilience and Edge Cases Video 2](https://www.youtube.com/watch?v=axBr9gnITOo)

---

## 📝 License

This project is created for educational purposes.
