"""
test_network.py — Exercise 02: Network Interception

See Exercises/02_NetworkInterception.md for full instructions.
Run: pytest src/tests/test_network.py -v --headed
"""
import json
from playwright.sync_api import Page, Route, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"
EMPTY_RESPONSE = {"content": [], "totalElements": 0, "totalPages": 0, "currentPage": 0}


def test_stub_empty_task_list(page: Page):
    # TODO Task 1
    pass


def test_inject_task_into_real_response(page: Page):
    # TODO Task 2
    pass


def test_capture_search_request(page: Page):
    # TODO Task 3
    pass


def test_api_500_error_state(page: Page):
    # TODO Task 4
    pass


def test_slow_network_simulation(page: Page):
    # TODO Task 5
    pass
