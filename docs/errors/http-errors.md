# HTTP Errors

These are the HTTP error statuses currently returned by the API.

## 401 Unauthorized

- Returned when credentials are invalid.
- Also returned when login email does not match an existing user.

## 403 Forbidden

- Returned when authentication fails due to account state restrictions:
  - account not verified
  - account locked

## 422 Unprocessable Entity

- Returned automatically by FastAPI/Pydantic when the request body does not match `LoginSchema`.
