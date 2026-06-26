"""
TaskManagerPage — Page Object for https://testauto.app/task-manager-spa

Exercise 06 — Task 1: Implement all methods below.
See Exercises/06_AdvancedPOMPatterns.md for full instructions.
"""

from playwright.sync_api import Page, expect

TASK_MANAGER_URL = "https://testauto.app/task-manager-spa"


class TaskManagerPage:

    def __init__(self, page: Page):
        self.page = page
        # TODO: define your locators here
        # Examples:
        #   self.search_input = page.get_by_placeholder("Search tasks...")
        #   self.status_filter = page.get_by_role("combobox").first
        #   self.rows = page.locator("table tbody tr")
        #   self.add_task_btn = page.get_by_role("link", name="Add New Task")
        #   self.board_view_link = page.get_by_role("link", name="Board view")

    def navigate(self):
        """Navigate to the task manager list view."""
        # TODO
        raise NotImplementedError

    def search(self, query: str):
        """Fill the search input and submit the search."""
        # TODO
        raise NotImplementedError

    def filter_by_status(self, status: str):
        """
        Select a status from the filter dropdown.
        status: "" (all) | "TODO" | "IN_PROGRESS" | "DONE"
        """
        # TODO
        raise NotImplementedError

    def get_task_titles(self) -> list[str]:
        """Return a list of all visible task titles in the table."""
        # TODO
        raise NotImplementedError

    def get_task_count(self) -> int:
        """Return the number of task rows currently visible."""
        # TODO
        raise NotImplementedError

    def open_create_modal(self):
        """Click the '+ Add New Task' button and assert the modal opened."""
        # TODO: click the button, then assert URL contains taskModal=create
        raise NotImplementedError

    def open_board_view(self):
        """Click the Board view link and assert the view changed."""
        # TODO: click the link, then assert URL contains view=board
        raise NotImplementedError
