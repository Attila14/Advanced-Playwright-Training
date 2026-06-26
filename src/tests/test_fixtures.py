"""
test_fixtures.py — Exercise 07: Fixtures & Test Lifecycle

See Exercises/07_FixturesAndTestLifecycle.md for full instructions.
Run: pytest src/tests/test_fixtures.py -v -s
"""
import pytest
from playwright.sync_api import APIRequestContext


def test_create_todo_task(task_factory):
    # TODO Task 1
    pass


def test_create_high_priority_task(task_factory):
    # TODO Task 1
    pass


@pytest.mark.parametrize("status", ["TODO", "IN_PROGRESS", "DONE"])
def test_task_created_with_correct_status(task_factory, status):
    # TODO Task 2
    pass


@pytest.mark.parametrize("priority", ["LOW", "MEDIUM", "HIGH", "URGENT"])
def test_task_created_with_correct_priority(task_factory, priority):
    # TODO Task 2
    pass


def test_module_task_has_id(module_task):
    # TODO Task 3
    pass


def test_module_task_has_valid_status(module_task):
    # TODO Task 3
    pass


def test_module_task_has_valid_priority(module_task):
    # TODO Task 3
    pass


class TestTaskManagerFlow:
    # TODO Task 4 — class-scoped browser context

    def test_open_list(self):
        pass

    def test_filter_by_status(self):
        pass

    def test_switch_to_board(self):
        pass
