"""
test_resilience.py — Exercise 15: Resilience & Edge Case Testing

See Exercises/15_ResilienceAndEdgeCases.md for full instructions.
Run: pytest src/tests/test_resilience.py -v -s
"""
import time
import json
import pytest
from playwright.sync_api import APIRequestContext, Playwright

API_BUGGY = "https://api.testauto.app/api/buggy"


def call_with_retry(fn, max_attempts=5):
    # TODO Task 1 — implement with exponential backoff
    raise NotImplementedError


def test_retry_succeeds_eventually(playwright: Playwright):
    # TODO Task 1
    pass


def test_retry_response_is_valid(playwright: Playwright):
    # TODO Task 1
    pass


def test_retry_schema_matches_v1(playwright: Playwright, api_v1: APIRequestContext):
    # TODO Task 1
    pass


def test_boundary_empty_title(api_v1: APIRequestContext):
    # TODO Task 2
    pass


def test_boundary_long_title(api_v1: APIRequestContext):
    # TODO Task 2
    pass


def test_boundary_unicode_title(api_v1: APIRequestContext):
    # TODO Task 2
    pass


def test_invalid_status_value(api_v1: APIRequestContext):
    # TODO Task 3
    pass


def test_invalid_priority_value(api_v1: APIRequestContext):
    # TODO Task 3
    pass


def test_missing_title_field(api_v1: APIRequestContext):
    # TODO Task 4
    pass


def test_empty_body(api_v1: APIRequestContext):
    # TODO Task 4
    pass


def test_concurrent_requests(playwright: Playwright):
    # TODO Task 5 — 5 threads, assert all 201, unique IDs, no 500
    pass
