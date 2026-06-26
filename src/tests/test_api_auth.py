"""
test_api_auth.py — Exercise 10: API Authentication (JWT)

See Exercises/10_APIAuthentication.md for full instructions.
Run: pytest src/tests/test_api_auth.py -v -s
"""
import json
import pytest
from playwright.sync_api import APIRequestContext, Playwright

API_V2 = "https://api.testauto.app/api/v2"


def test_valid_login(playwright: Playwright):
    # TODO Task 1
    pass


def test_wrong_password(playwright: Playwright):
    # TODO Task 1
    pass


def test_unknown_user(playwright: Playwright):
    # TODO Task 1
    pass


def test_token_is_non_empty_string(playwright: Playwright):
    # TODO Task 1
    pass


def test_create_task_authenticated(api_v2: APIRequestContext):
    # TODO Task 2
    pass


def test_update_task_authenticated(api_v2: APIRequestContext):
    # TODO Task 2
    pass


def test_delete_task_authenticated(api_v2: APIRequestContext):
    # TODO Task 2
    pass


def test_unauthenticated_get_rejected(playwright: Playwright):
    # TODO Task 3
    pass


def test_unauthenticated_post_rejected(playwright: Playwright):
    # TODO Task 3
    pass


def test_token_refresh(playwright: Playwright):
    # TODO Task 4
    pass


def test_admin_creates_user_reads(playwright: Playwright):
    # TODO Task 5
    pass
