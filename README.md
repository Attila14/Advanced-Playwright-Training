# Playwright with Python — Advanced Test Automation Training

This is a skeleton Python project for learning advanced test automation with AI-powered coding assistants like GitHub Copilot.

## 📋 Overview

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

The following guided exercises are available in the `Exercises/` folder:

### UI Testing — Browser & Page

**01_BrowserContextManagement.md:**
Browser vs context vs page lifecycle; multiple contexts simultaneously; saving and restoring auth state; viewport configuration; simulating two users at once

**02_NetworkInterception.md:**
Intercept real API calls with `page.route()`; stub empty states; inject data into live responses; capture outgoing requests; simulate server errors and slow networks

### UI Testing — Locators & Interactions

**03_AdvancedLocatorStrategies.md:**
Semantic locators `get_by_role`, `get_by_label`, `get_by_placeholder`; `filter()` to scope by text; `nth()`, `first`, `last`; board view column scoping; dynamic filter loops

**04_PerformanceAndTracing.md:**
Playwright trace recorder and viewer; HAR file capture and analysis; page timing metrics; console error detection; auto-save traces on test failure

### UI Testing — Test Quality

**05_VisualTesting.md:**
Raw screenshot capture with Pillow pixel-diff comparison; masking dynamic columns; element-level screenshots; mobile vs desktop comparison

**06_AdvancedPOMPatterns.md:**
Component objects for reusable UI pieces; `BasePage` with shared methods; `SearchBar`, `Pagination`, `TaskModal` components; fixture-integrated page objects

### Advanced Test Design

**07_FixturesAndTestLifecycle.md:**
Fixture scopes (function, class, module, session); factory fixtures with automatic cleanup; `autouse` hooks; `@pytest.mark.parametrize`; class-scoped browser contexts

**08_ParallelExecutionAndSharding.md:**
pytest-xdist parallel runs; isolation design with uuid; worker ID fixture; `@pytest.mark.fast` / `slow`; CI matrix sharding

**09_AllureReporting.md:**
Epic/feature/story hierarchy; `allure.step` annotations; screenshot and JSON attachments; severity levels; auto-attach on failure; GitHub Pages publishing

### API Testing

**10_APIAuthentication.md:**
JWT login flow; token handling; token refresh; unauthenticated request rejection; multi-user access scenarios

**11_AdvancedResponseValidation.md:**
Full schema validation; pagination consistency; filter accuracy; response time bounds; sorting verification

**12_APIFixturesAndTestData.md:**
Factory fixtures with all fields; task + comments fixture; bulk factory for pagination tests; module-scoped read-only data; proving cleanup works

**13_ChainedWorkflowsAndHybridTests.md:**
Multi-step CRUD chains; comment lifecycle; hybrid API-create + UI-verify; hybrid UI-create + API-verify; status transition workflow

**14_MultiUserAndRoleBasedTesting.md:**
Documenting access permissions; concurrent creation; permission boundary assertions; two simultaneous browser sessions

**15_ResilienceAndEdgeCases.md:**
Retry with exponential backoff; buggy API handling; boundary values (empty, long, unicode); invalid enum values; missing required fields; concurrent requests

### Data-Driven Testing

**16_DataDrivenTestingGUIAndAPI.md:**
`@pytest.mark.parametrize` for all priorities and statuses; shared data sets across UI and API tests; form validation parametrize; filter combination testing

**17_AutoWaitingAndFlakiness.md:**
Replace `wait_for_load_state("networkidle")` and `time.sleep()` with web-first `expect()` assertions; SPA-safe waiting strategies; `authenticated_page` fixture with storage_state reuse

Use these exercises as a step-by-step guide. Each file contains tasks and scenarios to implement. Work through them in order — later exercises build on earlier ones.

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

- [Playwright Python Documentation](https://playwright.dev/python/docs/intro)
- [pytest Documentation](https://docs.pytest.org/)
- [testauto.app Docs](https://testauto.app/docs)
- [Interactive API Docs](https://api.testauto.app/swagger-ui/index.html)

---

## 📝 License

This project is created for educational purposes.
