# eclipse-labs-auth Implementation Plan

## Project Overview

- **Project Name:** eclipse-labs-auth
- **Type:** FastAPI Authentication Microservice
- **Purpose:** Centralized authentication for Eclipse Labs services
- **Python Version:** 3.13
- **Database:** SQLite (dev) / PostgreSQL (prod)

## Current State

- Basic project structure in place
- User model defined with UUID, email, password_hash, timestamps
- Login schema (email/password) defined
- Auth router with placeholder endpoint
- No actual authentication logic implemented

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | >=0.128.2 | Web framework |
| uvicorn | >=0.40.0 | ASGI server |
| sqlalchemy | >=2.0.46 | ORM |
| aiosqlite | >=0.22.1 | SQLite driver |
| asyncpg | >=0.31.0 | PostgreSQL driver |
| psycopg2 | >=2.9.11 | PostgreSQL adapter |
| dbwarden | >=0.3.6 | Database management |
| dotenv | >=0.9.9 | Environment variables |
| **pwdlib[argon2]** | latest | **Password hashing** |
| **python-jose[cryptography]** | latest | **JWT tokens** |

## Security Configuration

### Password Hashing
- **Algorithm:** Argon2id (OWASP 2025/2026 recommended)
- **Parameters:**
  - Memory: 19 MiB (OWASP minimum)
  - Iterations: 2
  - Parallelism: 1
- **Library:** pwdlib (FastAPI-recommended, replaces aging passlib)

### JWT Tokens
- **Algorithm:** RS256 (asymmetric) or HS256 (symmetric)
- **Expiration:** 2 hours
- **Library:** python-jose

### Account Lockout
- **Threshold:** 5 failed login attempts
- **Lockout Duration:** Permanent until admin unlocks (or configurable)
- **Tracked Fields:**
  - `failed_login_attempts` (already exists in User model)
  - `locked_at` (new field to add)
  - `last_login_at` (already exists in User model)

### Rate Limiting
- Handled by external service (not implemented here)

## API Endpoints

### POST /auth/login
- **Request Body:** `{ "email": "user@example.com", "password": "..." }`
- **Success Response:** `{ "access_token": "eyJ...", "token_type": "bearer" }`
- **Error Responses:**
  - 401: Invalid credentials
  - 423: Account locked
  - 422: Validation error

### POST /auth/register (future)
- Create new user accounts

## Implementation Tasks

### Phase 1: Foundation
- [ ] Add pwdlib[argon2] and python-jose[cryptography] to dependencies
- [ ] Create .env.example template
- [ ] Update User model with locked_at field

### Phase 2: Security Module
- [ ] Create app/core/security.py
  - Password hashing utilities (pwdlib wrapper)
  - JWT token creation/validation
- [ ] Create app/schemas/token.py
  - Token response schema

### Phase 3: Authentication Logic
- [ ] Update app/auth/router.py
  - Change GET /login to POST /auth/login
  - Implement login validation logic
  - Handle account lockout
  - Return JWT on success

### Phase 4: Database
- [ ] Run database migrations
- [ ] Verify users table created

## File Structure

```
egos-auth/
├── app/
│   ├── auth/
│   │   ├── __init__.py
│   │   └── router.py          # Auth endpoints
│   ├── core/
│   │   ├── config.py          # Environment config
│   │   ├── database.py        # Database setup
│   │   └── security.py        # JWT + password utils (NEW)
│   ├── models/
│   │   └── user.py            # User model
│   ├── schemas/
│   │   ├── login.py           # Login request schema
│   │   └── token.py           # Token response schema (NEW)
│   └── main.py                # FastAPI app
├── migrations/
├── .env.example               # Environment template (NEW)
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile
└── plan.md
```

## Login Flow

```
1. Client POST /auth/login with {email, password}
2. Lookup user by email
3. IF user not found → 401 Invalid credentials
4. IF user.locked_at is not None → 423 Account locked
5. Verify password with Argon2id
6. IF password invalid:
   a. Increment failed_login_attempts
   b. IF failed_login_attempts >= 5:
      - Set locked_at = NOW()
      - Return 423 Account locked
   c. Return 401 Invalid credentials
7. IF password valid:
   a. Reset failed_login_attempts = 0
   b. Update last_login_at = NOW()
   c. Generate JWT (2hr expiry)
   d. Return {access_token, token_type}
```

## Configuration Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| ENVIRONMENT | Yes | - | DEV or PROD |
| DATABASE_URL | Yes | - | Database connection string |
| SECRET_KEY | Yes | - | JWT signing key |
| ALGORITHM | No | HS256 | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | No | 120 | Token expiry (2 hours) |
| POSTGRES_USER | Prod | - | PostgreSQL username |
| POSTGRES_PASSWORD | Prod | - | PostgreSQL password |
| POSTGRES_HOST | Prod | localhost | PostgreSQL host |
| POSTGRES_PORT | Prod | 5432 | PostgreSQL port |
| POSTGRES_DB | Prod | - | Database name |

## Testing Checklist

- [ ] Login with correct credentials returns JWT
- [ ] Login with wrong password returns 401
- [ ] Login with non-existent user returns 401
- [ ] 5 failed attempts locks account (returns 423)
- [ ] Locked account cannot login even with correct password
- [ ] JWT expires after 2 hours
- [ ] JWT contains correct user claims
- [ ] Successful login resets failed_attempts

## References

- [OWASP Password Storage Cheat Sheet 2025](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [FastAPI Security Docs](https://fastapi.tiangolo.com/tutorial/security/)
- [pwdlib Documentation](https://pwdlib.readthedocs.io/)
- [python-jose Documentation](https://python-jose.readthedocs.io/)
