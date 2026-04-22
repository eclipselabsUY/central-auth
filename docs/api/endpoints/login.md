# POST /login

Authentication endpoint.

## Request

- Method: `POST`
- Path: `/login`
- Content-Type: `application/json`
- Body fields:
  - `email` (string, valid email format, required)
  - `password` (string, required)

## Current Behavior

1. Looks up user by email.
2. Returns `401` if user does not exist.
3. Validates password, verification status, and locked status.
4. Maps auth validation exceptions to custom error payloads.

## Responses

- Success:
  - The success token payload is not finalized yet in current code.
- Error:
  - `401 Unauthorized` for invalid credentials.
  - `403 Forbidden` for not verified or locked account states.
  - `422 Unprocessable Entity` for invalid request body.

See `Errors` and `Exceptions` sections for exact payload mappings.
