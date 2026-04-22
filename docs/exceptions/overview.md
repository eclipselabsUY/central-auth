# Exceptions Overview

Custom exceptions are defined in `app/exceptions/users.py` and re-exported by `app/exceptions/__init__.py`.

## Custom Exceptions

### UserWrongPassword

- Raised when the provided password does not match the stored password hash.
- Mapped by `/login` to:
  - HTTP `401 Unauthorized`
  - `error: ACCOUNT_INVALID_CREDENTIALS`
  - `code: 1101`

### UserNotVerified

- Raised when user exists but is not verified.
- Mapped by `/login` to:
  - HTTP `403 Forbidden`
  - `error: ACCOUNT_NOT_VERIFIED`
  - `code: 1102`

### UserLocked

- Raised when user account is in a locked state.
- Mapped by `/login` to:
  - HTTP `403 Forbidden`
  - `error: ACCOUNT_LOCKED`
  - `code: 1103`

## Other Exceptions You May See

- `HTTPException` from FastAPI router-level checks.
- Request validation errors (FastAPI/Pydantic), returned as `422`.
