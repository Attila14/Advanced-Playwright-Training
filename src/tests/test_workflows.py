"""
test_workflows.py — Exercise 13: Chained Workflows & Hybrid Tests

See Exercises/13_ChainedWorkflowsAndHybridTests.md for full instructions.
Run: pytest src/tests/test_workflows.py -v -s --headed
"""
import json
from playwright.sync_api import Page, APIRequestContext, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"


def test_full_crud_chain(api_v1: APIRequestContext):
    # TODO Task 1 — create→read→update→verify→delete→verify 404
    task_id = None
    try:
        pass
    finally:
        if task_id:
            api_v1.delete(f"/tasks/{task_id}")


def test_comment_chain(api_v1: APIRequestContext):
    # TODO Task 2
    task_id = None
    try:
        pass
    finally:
        if task_id:
            api_v1.delete(f"/tasks/{task_id}")


def test_api_create_ui_verify(api_v1: APIRequestContext, page: Page):
    # TODO Task 3 — create via API, verify row visible in browser
    task_id = None
    try:
        pass
    finally:
        if task_id:
            api_v1.delete(f"/tasks/{task_id}")


def test_ui_create_api_verify(api_v1: APIRequestContext, page: Page):
    # TODO Task 4 — create via UI form, verify via API GET
    task_id = None
    try:
        pass
    finally:
        if task_id:
            api_v1.delete(f"/tasks/{task_id}")


def test_status_transition_workflow(api_v1: APIRequestContext, page: Page):
    # TODO Task 5 — TODO→IN_PROGRESS→DONE with UI verification at each step
    task_id = None
    try:
        pass
    finally:
        if task_id:
            api_v1.delete(f"/tasks/{task_id}")
