"""
TaskFormModal — Page Object for the create/edit task modal.

The modal opens at:
  ?taskModal=create
  ?taskModal=edit&taskId=ID

Exercise 06 — Task 2: Implement all methods below.
"""

from playwright.sync_api import Page


class TaskFormModal:

    def __init__(self, page: Page):
        self.page = page
        # TODO: define locators for the form fields inside the modal
        # Tip: use get_by_label("Title"), get_by_label("Status") etc.
        # These match the <label> elements and are the most stable approach.

    def fill_and_submit(
        self,
        title: str,
        description: str = "",
        status: str = "TODO",
        priority: str = "MEDIUM",
        labels: str = "",
    ):
        """Fill in the task form and click Save."""
        # TODO: fill each field that has a value, then click the Save button
        raise NotImplementedError

    def get_validation_error(self) -> str:
        """Return the text of any visible validation error message, or '' if none."""
        # TODO
        raise NotImplementedError
