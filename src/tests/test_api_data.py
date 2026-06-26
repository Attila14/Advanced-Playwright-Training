"""
test_api_data.py — Exercise 12: API Fixtures & Test Data Management

See Exercises/12_APIFixturesAndTestData.md for full instructions.
Run: pytest src/tests/test_api_data.py -v -s
"""
import pytest
from playwright.sync_api import APIRequestContext


def test_create_task_all_fields(task_factory):
    # TODO Task 1 — all fields: title, description, status, priority, labels, dueDate
    pass


def test_task_with_comments(task_with_comments):
    # TODO Task 2 — assert task and 3 comments exist
    pass


def test_pagination_with_bulk_tasks(bulk_task_factory, api_v1: APIRequestContext):
    # TODO Task 3 — create 15, assert page 0 = 10, page 1 >= 5
    pass


def test_module_task_has_id(module_task):
    # TODO Task 4
    pass


def test_module_task_has_valid_title(module_task):
    pass


def test_module_task_has_valid_status(module_task):
    pass


def test_module_task_has_updated_at(module_task):
    pass


def test_cleanup_works_after_failure(api_v1: APIRequestContext):
    # TODO Task 5 — prove cleanup runs even when test fails
    pass
