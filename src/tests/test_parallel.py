"""
test_parallel.py — Exercise 08: Parallel Execution & Sharding

See Exercises/08_ParallelExecutionAndSharding.md for full instructions.
Run: pytest src/tests/test_parallel.py -n 5 -v -s
"""
import uuid
import pytest
from playwright.sync_api import APIRequestContext, Page, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"


def test_print_worker_id(worker_id):
    # TODO Task 2
    pass


def test_parallel_alpha(api_v1: APIRequestContext):
    # TODO Task 3
    pass

def test_parallel_beta(api_v1: APIRequestContext):
    pass

def test_parallel_gamma(api_v1: APIRequestContext):
    pass

def test_parallel_delta(api_v1: APIRequestContext):
    pass

def test_parallel_epsilon(api_v1: APIRequestContext):
    pass


@pytest.mark.fast
def test_fast_summary(api_v1: APIRequestContext):
    # TODO Task 5
    pass


@pytest.mark.fast
def test_fast_page_load(page: Page):
    # TODO Task 5
    pass


@pytest.mark.slow
def test_slow_full_flow(page: Page, api_v1: APIRequestContext):
    # TODO Task 5 — full create → UI verify → delete
    pass
