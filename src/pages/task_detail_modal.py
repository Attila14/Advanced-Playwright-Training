"""
TaskDetailModal — Page Object for the task detail modal.

The modal opens at: ?taskModal=detail&taskId=ID

Exercise 06 — Task 3: Implement all methods below.
"""

from playwright.sync_api import Page


class TaskDetailModal:

    def __init__(self, page: Page):
        self.page = page
        # TODO: define a locator for the modal container
        # Tip: look for [role='dialog'] or a class like .modal

    def get_title(self) -> str:
        """Return the task title shown in the modal."""
        # TODO
        raise NotImplementedError

    def get_status(self) -> str:
        """Return the status text shown in the modal."""
        # TODO
        raise NotImplementedError

    def get_priority(self) -> str:
        """Return the priority text shown in the modal."""
        # TODO
        raise NotImplementedError

    def get_labels(self) -> list[str]:
        """Return a list of label strings shown in the modal."""
        # TODO
        raise NotImplementedError

    def close(self):
        """Dismiss the modal (click X or press Escape)."""
        # TODO
        raise NotImplementedError
