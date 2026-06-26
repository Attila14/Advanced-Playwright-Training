# GitHub Copilot Code Review Agent

## Purpose

This agent reviews exercise solutions submitted as pull requests against this training repository.

## Review Guidelines

When reviewing a solution PR, check for:

### Correctness
- All `TODO` comments have been replaced with actual implementation
- Tests pass against the live testauto.app site
- No hardcoded task IDs — use dynamic lookup or fixture-created tasks

### Cleanup
- Every test that creates data via `POST /tasks` also deletes it
- Cleanup happens in `try/finally` or a pytest fixture teardown — not just at the end of the test body
- No leftover tasks with generic titles like "test" or "my task" that pollute the shared environment

### Locator quality
- `get_by_role`, `get_by_label`, `get_by_placeholder` used where possible
- No positional selectors like `div:nth-child(3) > button`
- `expect()` used for assertions instead of `assert .is_visible()`

### Fixture usage
- Page objects are used in tests — no raw `page.locator(...)` calls in test methods
- `api_v1` and `api_v2` fixtures are used correctly
- Scope is appropriate (function for state-changing tests, module/session for read-only)

### Parallel safety
- Unique titles generated with `uuid` in parallel tests
- No test assumes the presence of data created by another test

## Feedback tone

- Be specific: quote the exact line and explain why it's an issue
- Suggest the fix, don't just flag the problem
- Acknowledge when something is done well
