# Exercise 10 — API Authentication (JWT)

## 🎯 Goal

Test a JWT-secured REST API end-to-end — implement the login flow, use the token in requests, handle token refresh, and assert what happens when requests are made without a valid token.

Before writing any code, **make a manual login call** using curl or a REST client:

```bash
curl -X POST https://api.testauto.app/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"user123"}'
```

Inspect the response. Note the `token`, `username`, and `expiresIn` fields.

---

## 📖 Background

### API V2 Base URL

```
https://api.testauto.app/api/v2
```

All task endpoints require: `Authorization: Bearer <token>`

### Auth endpoints

| Method | Path | Body |
|--------|------|------|
| `POST` | `/auth/login` | `{"username": "...", "password": "..."}` |
| `POST` | `/auth/refresh` | *(no body — send old token in Authorization header)* |

### Test credentials

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | admin |
| `user` | `user123` | user |
| `testuser` | `test123` | user |

### Making authenticated requests

```python
import json

ctx = playwright.request.new_context(base_url="https://api.testauto.app/api/v2")

# Login
resp = ctx.post("/auth/login",
    data=json.dumps({"username": "user", "password": "user123"}),
    headers={"Content-Type": "application/json"})
token = resp.json()["token"]
ctx.dispose()

# Authenticated context
auth_ctx = playwright.request.new_context(
    base_url="https://api.testauto.app/api/v2",
    extra_http_headers={"Authorization": f"Bearer {token}"},
)
```

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/tests/test_api_auth.py` | All tasks for this exercise |

---

## ✅ Task 1 — Login flow validation

Implement these four tests:

| Test | What to assert |
|------|---------------|
| `test_valid_login` | Status `200`, response has `token`, `username`, `expiresIn` |
| `test_wrong_password` | Status `401` or `403` |
| `test_unknown_user` | Status `4xx` |
| `test_token_is_non_empty_string` | Token is a `str` with `len > 20` |

---

## ✅ Task 2 — Authenticated CRUD

Using the `api_v2` fixture (pre-authenticated as `user`):

| Test | What to do |
|------|-----------|
| `test_create_task_authenticated` | `POST /tasks` → assert `201`, capture `id`, clean up |
| `test_update_task_authenticated` | Create → `PUT` with new title → assert `200` and new title returned |
| `test_delete_task_authenticated` | Create → `DELETE` → assert `200` → `GET` → assert `404` |

---

## ✅ Task 3 — Reject unauthenticated requests

Create an `APIRequestContext` with **no** `Authorization` header. Make these requests and assert they are all rejected:

| Request | Expected status |
|---------|----------------|
| `GET /tasks` | `401` |
| `POST /tasks` | `401` |
| `DELETE /tasks/1` | `401` |

---

## ✅ Task 4 — Token refresh

Write `test_token_refresh`:

1. Login as `user/user123` — get `old_token`
2. `POST /auth/refresh` with `Authorization: Bearer <old_token>`
3. Assert a new token is returned
4. Use the new token to `GET /tasks` — assert `200`

---

## ✅ Task 5 — Multi-user access scenario

Write `test_admin_creates_user_reads`:

1. Login as `admin`, create a task, capture its `id`
2. Login as `user` (separate context)
3. `GET /tasks/{id}` as `user` — assert `200` (user can read)
4. `DELETE /tasks/{id}` as `user` — capture and print the status code
5. Document the actual behaviour: is deletion allowed or forbidden?

Clean up: always delete via admin context in `finally`.

---

## 🏃 Run your tests

```bash
pytest src/tests/test_api_auth.py -v -s
```

---

## 💡 Tips

- The `api_v2` fixture in `conftest.py` logs in automatically — use it for tests that just need an authenticated context.
- For tests that require a specific user (`admin`, `testuser`), create your own context using `playwright` directly.
- Dispose of every context you create: `ctx.dispose()` — otherwise you accumulate open connections.

---

## 📌 Reference

- [testauto.app API Guide](https://testauto.app/docs/api-guide)
- [Playwright — APIRequestContext](https://playwright.dev/python/docs/api/class-apirequestcontext)
- [Interactive API Docs](https://api.testauto.app/swagger-ui/index.html)
