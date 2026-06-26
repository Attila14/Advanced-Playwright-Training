"""
test_selectors.py — Exercise 03: Advanced Locator Strategies

See Exercises/03_AdvancedLocatorStrategies.md for full instructions.
Run: pytest src/tests/test_selectors.py -v --headed
"""
import json
import pytest
from playwright.sync_api import Page, APIRequestContext, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"


def test_semantic_selectors_only(page: Page):
    # TODO Task 1 — no page.locator("css") allowed
    pass


def test_filter_specific_row(page: Page):
    # TODO Task 2 — find "Deploy to Railway.app" row, assert priority "High"
    pass


def test_nth_first_last(page: Page):
    # TODO Task 3
    pass


def test_board_view_column_scoping(page: Page):
    # TODO Task 4
    pass


def test_dynamic_filter_loop(page: Page, api_v1: APIRequestContext):
    # TODO Task 5 — create 3 tasks, search, assert each row visible, clean up
    pass
