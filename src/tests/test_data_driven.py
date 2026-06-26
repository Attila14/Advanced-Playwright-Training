"""
test_data_driven.py — Exercise 16: Data-Driven Testing (GUI & API)

See Exercises/16_DataDrivenTestingGUIAndAPI.md for full instructions.
Run: pytest src/tests/test_data_driven.py -v
     pytest src/tests/test_data_driven.py --collect-only  (see all test names)
"""
import pytest
from playwright.sync_api import Page, APIRequestContext, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"

TASK_SCENARIOS = [
    {"title": "Scenario Alpha", "status": "TODO",        "priority": "LOW"},
    {"title": "Scenario Beta",  "status": "IN_PROGRESS", "priority": "HIGH"},
    {"title": "Scenario Gamma", "status": "DONE",        "priority": "URGENT"},
]


@pytest.mark.parametrize("priority", ["LOW", "MEDIUM", "HIGH", "URGENT"])
def test_api_create_with_priority(api_v1: APIRequestContext, priority: str):
    # TODO Task 1
    pass


@pytest.mark.parametrize("status", ["TODO", "IN_PROGRESS", "DONE"])
def test_ui_detail_shows_status(page: Page, task_factory, status: str):
    # TODO Task 2 — create via API, open detail modal, assert status visible
    pass


@pytest.mark.parametrize("data", TASK_SCENARIOS)
def test_api_create_scenario(api_v1: APIRequestContext, data: dict):
    # TODO Task 3
    pass


@pytest.mark.parametrize("data", TASK_SCENARIOS)
def test_ui_search_for_scenario(page: Page, task_factory, data: dict):
    # TODO Task 3
    pass


@pytest.mark.parametrize("title,expected_behaviour", [
    ("",        "error_shown"),
    ("   ",     "error_or_created"),
    ("A" * 200, "created"),
])
def test_form_validation(page: Page, title: str, expected_behaviour: str):
    # TODO Task 4
    pass


@pytest.mark.parametrize("filter_value,expected_status", [
    ("TODO",        "TODO"),
    ("IN_PROGRESS", "IN_PROGRESS"),
    ("DONE",        "DONE"),
], ids=["filter-todo", "filter-in-progress", "filter-done"])
def test_status_filter_parametrized(page: Page, filter_value: str, expected_status: str):
    # TODO Task 5
    pass
