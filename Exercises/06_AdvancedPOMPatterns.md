# Exercise 06 — Advanced Page Object Model Patterns

## 🎯 Goal

Go beyond a basic POM. Build component objects for reusable UI pieces, a shared base page class, and integrate your page objects directly with pytest fixtures — so every test starts with clean, pre-configured page objects rather than raw `page` instances.

Before writing any code, **think about the repeated UI patterns** across testauto.app:
- The search bar and status filter appear on both list and board views
- The table pagination appears every time the list loads
- The modal structure is the same for create, edit, and detail

These are candidates for component objects.

---

## 📖 Background

### Component objects

A component is a self-contained piece of UI that appears in multiple places. Extract it to a reusable class:

```python
class SearchBar:
    def __init__(self, page):
        self._input  = page.get_by_placeholder("Search tasks...")
        self._filter = page.get_by_role("combobox").first

    def search(self, query: str):
        self._input.fill(query)
        self._input.press("Enter")

    def filter_by_status(self, status: str):
        self._filter.select_option(status)
```

### Base page class

```python
class BasePage:
    BASE_URL = "https://testauto.app"

    def __init__(self, page):
        self.page   = page
        self.search_bar = SearchBar(page)    # shared component

    def navigate(self, path: str):
        self.page.goto(f"{self.BASE_URL}{path}")

    @property
    def title(self) -> str:
        return self.page.title()
```

### Fixture-integrated page objects

```python
@pytest.fixture
def task_manager(page):
    """Returns a ready-to-use TaskManagerPage — already navigated."""
    tm = TaskManagerPage(page)
    tm.navigate()
    return tm
```

Tests then read cleanly:
```python
def test_search_works(task_manager):
    task_manager.search_bar.search("deploy")
    assert task_manager.get_task_count() > 0
```

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/pages/base_page.py` | Base class with navigate, title, shared components |
| `src/pages/components.py` | SearchBar, Pagination, Modal component classes |
| `src/pages/task_manager_page.py` | Extend BasePage, use components |
| `src/pages/task_form_modal.py` | Extend BasePage or use Modal component |
| `src/tests/test_advanced_pom.py` | Tests using fixture-integrated page objects |

---

## ✅ Task 1 — Build a `BasePage` class

Create `src/pages/base_page.py`:

| Member | What it does |
|--------|-------------|
| `__init__(page)` | Store `page`, instantiate shared components |
| `navigate(path)` | Go to `BASE_URL + path` |
| `title` property | Return `page.title()` |
| `url` property | Return `page.url` |
| `wait_for_load()` | Call `page.wait_for_load_state("networkidle")` |

---

## ✅ Task 2 — Build component objects

Create `src/pages/components.py` with three components:

**`SearchBar`**

| Method | What it does |
|--------|-------------|
| `search(query)` | Fill input and press Enter |
| `filter_by_status(status)` | Select from status dropdown |
| `clear()` | Clear the search input |

**`Pagination`**

| Method | What it does |
|--------|-------------|
| `next_page()` | Click next page button |
| `prev_page()` | Click previous page button |
| `current_page()` | Return current page number as `int` |
| `total_pages()` | Return total pages as `int` |
| `set_page_size(size)` | Select from items-per-page dropdown |

**`TaskModal`**

| Method | What it does |
|--------|-------------|
| `is_open()` | Return `True` if modal is visible |
| `close()` | Dismiss the modal |
| `get_title()` | Return the modal heading text |

---

## ✅ Task 3 — Rebuild `TaskManagerPage` using components

Rewrite `src/pages/task_manager_page.py` to:
- Extend `BasePage`
- Expose `self.search_bar` (a `SearchBar` instance)
- Expose `self.pagination` (a `Pagination` instance)
- Keep `get_task_titles()`, `get_task_count()`, `open_create_modal()`, `open_board_view()`

---

## ✅ Task 4 — Fixture-integrated page objects

Add fixtures to `src/conftest.py`:

```python
@pytest.fixture
def task_manager(page):
    tm = TaskManagerPage(page)
    tm.navigate("/task-manager")
    tm.wait_for_load()
    return tm
```

Write 3 tests in `src/tests/test_advanced_pom.py` that use **only** the `task_manager` fixture — no raw `page` calls:

| Test | What to assert |
|------|---------------|
| `test_search_via_component` | `task_manager.search_bar.search("API")` filters results |
| `test_pagination_via_component` | `task_manager.pagination.current_page() == 1` on load |
| `test_board_view_loads` | After `open_board_view()`, URL has `view=board` |

---

## ✅ Task 5 — Chained component interaction

Write a single test that chains multiple component interactions:

1. Use `task_manager.search_bar.filter_by_status("TODO")` — assert rows shown
2. Use `task_manager.pagination.set_page_size(10)` — assert `row_count <= 10`
3. Use `task_manager.pagination.next_page()` — assert `current_page() == 2`
4. Use `task_manager.search_bar.filter_by_status("")` — assert the filter is cleared

---

## 🏃 Run your tests

```bash
pytest src/tests/test_advanced_pom.py -v --headed
```

---

## 💡 Tips

- Components should not call `page.goto()` — that belongs in the page object. Components only interact with elements already on the page.
- Keep locators in the `__init__` of each class, not inside methods — this makes them easy to audit.
- If a component is used in multiple page objects, define it once in `components.py` and import it everywhere.

---

## 📌 Reference

- [Playwright — Page Object Model](https://playwright.dev/python/docs/pom)
- [pytest fixtures](https://docs.pytest.org/en/stable/reference/fixtures.html)
- [testauto.app UI Guide](https://testauto.app/docs/ui-guide)
