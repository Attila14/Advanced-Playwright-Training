# Exercise 14 — Multi-User & Role-Based Testing

## 🎯 Goal

Test how the application behaves when multiple users with different roles interact with the same resources simultaneously — using separate authenticated contexts to simulate `admin` and `user` sessions in the same test.

Before writing any code, **login as both users manually**:
- `POST /api/v2/auth/login` with `admin / admin123`
- `POST /api/v2/auth/login` with `user / user123`

Compare the tokens. Try creating and deleting tasks as each user. Document what each role is allowed to do.

---

## 📖 Background

### Two simultaneous authenticated contexts

```python
def test_two_users(playwright):
    # Admin context
    admin_ctx = playwright.request.new_context(base_url="https://api.testauto.app/api/v2")
    admin_resp = admin_ctx.post("/auth/login",
        data='{"username":"admin","password":"admin123"}',
        headers={"Content-Type": "application/json"})
    admin_token = admin_resp.json()["token"]
    admin_ctx.dispose()

    admin_api = playwright.request.new_context(
        base_url="https://api.testauto.app/api/v2",
        extra_http_headers={"Authorization": f"Bearer {admin_token}"},
    )

    # User context — same pattern, different credentials
    user_api = ...

    # Both are now active simultaneously
    try:
        # test body
        pass
    finally:
        admin_api.dispose()
        user_api.dispose()
```

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/tests/test_multi_user.py` | All tasks for this exercise |

---

## ✅ Task 1 — Document access permissions

Write `test_document_access_permissions` that systematically tests what each role can do:

For each combination, record the HTTP status code returned:

| Action | admin | user |
|--------|-------|------|
| `GET /tasks` | ? | ? |
| `POST /tasks` | ? | ? |
| `DELETE /tasks/{own_task}` | ? | ? |
| `DELETE /tasks/{other_user_task}` | ? | ? |

Print a summary table to stdout. Assert no unexpected `500` errors occur.

---

## ✅ Task 2 — Admin creates, user reads

Write `test_admin_creates_user_reads`:

1. Admin creates a task with title `"Admin task <uuid>"`
2. User calls `GET /tasks?search=<title>`
3. Assert user can see the task (status `200`, task in results)
4. Clean up: admin deletes the task

---

## ✅ Task 3 — Concurrent creation by two users

Write `test_concurrent_creation`:

1. Admin creates a task: `"Admin concurrent <uuid>"`
2. User creates a task: `"User concurrent <uuid>"`
3. Admin verifies his task exists via `GET /tasks?search=<admin_title>`
4. User verifies her task exists via `GET /tasks?search=<user_title>`
5. Assert neither search returns the other user's task

Clean up both tasks in `finally`.

---

## ✅ Task 4 — Permission boundary assertion

Write `test_permission_boundary`:

1. Admin creates a task
2. User attempts to `DELETE` that task
3. Capture the response status
4. Assert the status is either `403` (forbidden) or `200` (allowed) — not `500`
5. If `403`: assert the task still exists (admin can still get it)
6. If `200`: document that users can delete any task

Clean up in `finally` (admin deletes if still exists).

---

## ✅ Task 5 — Simultaneous browser sessions

Write `test_two_browser_sessions`:

Using two browser contexts (not just API contexts):

1. **Admin browser** — navigates to https://testauto.app/task-manager-spa
2. **User browser** — navigates to https://testauto.app/task-manager-spa
3. Take a screenshot of each context and save them side by side
4. Assert both pages show the task manager table

| Screenshot | Save to |
|-----------|---------|
| Admin view | `screenshots/admin-session.png` |
| User view | `screenshots/user-session.png` |

---

## 🏃 Run your tests

```bash
pytest src/tests/test_multi_user.py -v -s
```

---

## 💡 Tips

- Always dispose of every context you create — use `try/finally` to guarantee it even when the test fails.
- `playwright.request.new_context()` creates a stateless HTTP client. The browser context (`browser.new_context()`) creates a full browser session with cookies and local storage — these are different things.
- When documenting access permissions, use `print()` and run with `-s` — this is valuable information to capture in your test output.

---

## 📌 Reference

- [testauto.app API Guide](https://testauto.app/docs/api-guide)
- [Playwright — Multiple contexts](https://playwright.dev/python/docs/browser-contexts)
