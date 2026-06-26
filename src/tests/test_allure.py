"""
test_allure.py — Exercise 09: Allure Reporting

See Exercises/09_AllureReporting.md for full instructions.
Run: pytest src/tests/test_allure.py --alluredir=allure-results -v
     allure serve allure-results
"""
import json
import allure
import pytest
from playwright.sync_api import Page, APIRequestContext, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"


# TODO Task 1 — add @allure.epic, @allure.feature, @allure.story to these classes

class TestTaskListUI:
    def test_table_visible(self, page: Page):
        # TODO
        pass

    def test_search_filters(self, page: Page):
        # TODO
        pass


class TestAPIV1:
    def test_create_task(self, api_v1: APIRequestContext):
        # TODO
        pass

    def test_delete_task(self, api_v1: APIRequestContext):
        # TODO
        pass


@allure.epic("Task Manager")
@allure.feature("Create Task")
@allure.story("UI modal flow")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_task_with_steps(page: Page, api_v1: APIRequestContext):
    # TODO Task 2 — at least 6 allure.step blocks
    pass


@allure.feature("Task List")
def test_attach_screenshot_and_api_data(page: Page, api_v1: APIRequestContext):
    # TODO Task 3
    pass


def test_intentional_failure_check_screenshot(page: Page):
    """Fails on purpose — check Allure for screenshot attachment."""
    page.goto(TASK_MANAGER)
    assert False, "Intentional — verify screenshot in Allure"


@allure.severity(allure.severity_level.CRITICAL)
def test_critical_severity(api_v1: APIRequestContext):
    # TODO Task 5
    pass


@allure.severity(allure.severity_level.HIGH)
def test_high_severity(page: Page):
    # TODO Task 5
    pass


@allure.severity(allure.severity_level.NORMAL)
def test_normal_severity(page: Page):
    # TODO Task 5
    pass


@allure.severity(allure.severity_level.MINOR)
def test_minor_severity(page: Page):
    # TODO Task 5
    pass
