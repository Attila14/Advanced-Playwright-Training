"""
test_advanced_pom.py — Exercise 06: Advanced POM Patterns

See Exercises/06_AdvancedPOMPatterns.md for full instructions.
Run: pytest src/tests/test_advanced_pom.py -v --headed
"""
import pytest
from playwright.sync_api import Page, expect


def test_search_via_component(task_manager):
    # TODO Task 4 — task_manager.search_bar.search("API"), assert results
    pass


def test_pagination_via_component(task_manager):
    # TODO Task 4
    pass


def test_board_view_via_component(task_manager):
    # TODO Task 4
    pass


def test_chained_component_interactions(task_manager):
    # TODO Task 5 — filter → page size → next page → clear filter
    pass
