# Custom Error Codes

The login route includes custom auth errors in the `detail` payload.

## Error Format

```json
{
  "detail": {
    "error": "ACCOUNT_INVALID_CREDENTIALS",
    "code": 1101
  }
}
```

## Codes

### 1101 - ACCOUNT_INVALID_CREDENTIALS

- Meaning: password is incorrect.
- HTTP status: `401 Unauthorized`.
- Source exception: `UserWrongPassword`.

### 1102 - ACCOUNT_NOT_VERIFIED

- Meaning: account exists but has not been verified.
- HTTP status: `403 Forbidden`.
- Source exception: `UserNotVerified`.

### 1103 - ACCOUNT_LOCKED

- Meaning: account is currently locked.
- HTTP status: `403 Forbidden`.
- Source exception: `UserLocked`.
