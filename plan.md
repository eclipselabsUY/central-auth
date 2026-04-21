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
- Dependencies: fastapi, uvicorn, sqlalchemy, aiosqlite, asyncpg, psycopg2, dbwarden, dotenv, pwdlib[argon2], python-jose[cryptography]

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
| pwdlib[argon2] | latest | Password hashing |
| python-jose[cryptography] | latest | JWT tokens |

## Security Configuration

### Password Hashing
- **Algorithm:** Argon2id (OWASP 2025/2026 recommended)
- **Parameters:**
  - Memory: 19 MiB (OWASP minimum)
  - Iterations: 2
  - Parallelism: 1
- **Library:** pwdlib (FastAPI-recommended)

### JWT Tokens
- **Algorithm:** RS256 (asymmetric)
- **Signing:** `private_key.pem`
- **Verification:** `public_key.pem`
- **Expiration:** 2 hours (120 minutes)

### Account Lockout
- **Threshold:** 5 failed login attempts
- **Lockout:** Until email is verified via magic link
- **Tracked Fields:**
  - `failed_login_attempts` (exists)
  - `locked_at` (NEW - needs migration)
  - `verified` (exists - needs True to login)

### Rate Limiting
- Handled by external service (not implemented here)

## Difficulty Summary

| Level | Tasks |
|-------|-------|
| **Easy** | config, .env.example, security/__init__, password.py, token.py, verify.py, migrations |
| **Medium** | tokens.py (RS256), auth.py (login), email.py, verify.py (endpoints) |
| **Hard** | None |

## Implementation Status

### DONE
- `app/models/user.py` - User model with fields (including locked_at)
- `app/schemas/login.py` - Login request schema
- `app/core/database.py` - Database setup
- `app/main.py` - FastAPI app
- `pyproject.toml` - Dependencies

### TO DO (by file)

#### Phase 1: Foundation
- [ ] `app/core/config.py` - Add JWT/SMTP config variables **[Easy]**
- [ ] `.env.example` - Create template **[Easy]**

#### Phase 2: Security Module (CREATE)
- [ ] `app/core/security/__init__.py` **[Easy]**
- [ ] `app/core/security/password.py` - Argon2id hash/verify **[Easy]**
- [ ] `app/core/security/tokens.py` - JWT create/verify (RS256) **[Medium]**

#### Phase 3: Schemas (CREATE)
- [ ] `app/schemas/token.py` - Token response schema **[Easy]**
- [ ] `app/schemas/verify.py` - Verify request/response schemas **[Easy]**

#### Phase 4: Auth Logic (UPDATE)
- [ ] `app/router/auth.py` - Implement POST /auth/login **[Medium]**

#### Phase 5: Verification (CREATE)
- [ ] `app/services/email.py` - Email sending (Zoho SMTP) **[Medium]**
- [ ] `app/router/verify.py` - Verification endpoints **[Medium]**
  - POST /auth/verify/request - Request magic link
  - GET /auth/verify/{token} - Process magic link

#### Phase 6: Database
- [ ] Add migration for `locked_at` field **[Easy]**
- [ ] Run migrations **[Easy]**

---

## API Endpoints

### POST /auth/login
- **Request Body:** `{ "email": "user@example.com", "password": "..." }`
- **Success Response:** `{ "access_token": "eyJ...", "token_type": "bearer" }`
- **Error Responses:**
  - 401: Invalid credentials
  - 403: Account not verified
  - 423: Account locked
  - 422: Validation error

### POST /auth/verify/request
- **Request Body:** `{ "email": "user@example.com" }`
- **Success Response:** `{ "message": "Verification link sent" }`
- **Behavior:** Sends magic link if account exists

### GET /auth/verify/{token}
- **Path Parameter:** JWT verification token
- **Success Response:** Redirect to `https://auth.eclipselabs.com.uy/verified`
- **Behavior:** Sets verified=True, resets failed_login_attempts=0, clears locked_at

---

## File Structure

```
central-auth/
├── .env                         # Your config (not committed)
├── .env.example                 # Template for devs
├── private_key.pem              # JWT signing key
├── public_key.pem               # JWT verification key
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile
├── plan.md
├── migrations/
│   └── primary/
│       └── primary__0001_auto_generated.sql
├── app/
│   ├── main.py                  # FastAPI app
│   ├── core/
│   │   ├── config.py           # CONFIG (UPDATE needed)
│   │   ├── database.py         # Done
│   │   └── security/
│   │       ├── __init__.py    # CREATE
│   │       ├── password.py    # CREATE
│   │       └── tokens.py      # CREATE
│   ├── models/
│   │   └── user.py             # MODEL (UPDATE needed: locked_at)
│   ├── router/
│   │   ├── __init__.py
│   │   ├── auth.py            # UPDATE: implement login
│   │   └── verify.py          # CREATE
│   ├── schemas/
│   │   ├── login.py           # Done
│   │   ├── token.py           # CREATE
│   │   └── verify.py          # CREATE
│   └── services/
│       └── email.py           # CREATE
└── users.db
```

---

## Login Flow

```
1. Client POST /auth/login with {email, password}
2. Lookup user by email
3. IF user not found → 401 Invalid credentials
4. IF user.verified == False → 403 Account not verified
5. IF user.locked_at is not None → 423 Account locked
6. Verify password with Argon2id
7. IF password invalid:
   a. Increment failed_login_attempts
   b. IF failed_login_attempts >= 5:
      - Set locked_at = NOW()
      - Return 423 Account locked
   c. Return 401 Invalid credentials
8. IF password valid:
   a. Reset failed_login_attempts = 0
   b. Update last_login_at = NOW()
   c. Generate JWT (2hr expiry)
   d. Return {access_token, token_type}
```

---

## Verification Flow

```
POST /auth/verify/request:
1. Client POST with {email}
2. Lookup user by email
3. IF user exists:
   a. Generate verification JWT (15 min expiry)
   b. Build magic link: https://auth.eclipselabs.com.uy/verify/{token}
   c. Send email with magic link
4. Return "Verification link sent" (don't reveal if user exists)

GET /auth/verify/{token}:
1. Verify JWT signature
2. Extract user_id from token
3. IF token invalid/expired → 401/403 error
4. Lookup user by id
5. Set user.verified = True
6. Set user.failed_login_attempts = 0
7. Set user.locked_at = None
8. Redirect to https://auth.eclipselabs.com.uy/verified
```

---

## Configuration Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| ENVIRONMENT | Yes | - | DEV or PROD |
| DATABASE_URL | Yes | - | Database connection string |
| SECRET_KEY | Yes | - | Application secret key |
| PUBLIC_KEY_PATH | Yes | public_key.pem | JWT public key file |
| PRIVATE_KEY_PATH | Yes | private_key.pem | JWT private key file |
| JWT_ALGORITHM | No | RS256 | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | No | 120 | Token expiry |
| SMTP_HOST | Yes | - | Zoho SMTP server |
| SMTP_PORT | Yes | 587 | SMTP port |
| SMTP_USER | Yes | - | Zoho email |
| SMTP_PASSWORD | Yes | - | Zoho app password |
| SMTP_FROM | Yes | - | From address |
| VERIFY_BASE_URL | Yes | https://auth.eclipselabs.com.uy | Verification base URL |
| POSTGRES_USER | Prod | - | PostgreSQL username |
| POSTGRES_PASSWORD | Prod | - | PostgreSQL password |
| POSTGRES_HOST | Prod | localhost | PostgreSQL host |
| POSTGRES_PORT | Prod | 5432 | PostgreSQL port |
| POSTGRES_DB | Prod | - | Database name |

---

## .env.example Template

```bash
# Environment
ENVIRONMENT=DEV

# Database
DATABASE_URL=sqlite+aiosqlite:///./eclipse-labs.db

# Security Keys
SECRET_KEY=your-secret-key-here
PUBLIC_KEY_PATH=public_key.pem
PRIVATE_KEY_PATH=private_key.pem
JWT_ALGORITHM=RS256
ACCESS_TOKEN_EXPIRE_MINUTES=120

# Email (Zoho)
SMTP_HOST=smtp.zoho.com
SMTP_PORT=587
SMTP_USER=your@eclipselabs.com.uy
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@eclipselabs.com.uy

# Verification
VERIFY_BASE_URL=https://auth.eclipselabs.com.uy

# PostgreSQL (DEV only uses SQLite)
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=
```

---

## Database Migration

New migration needed:

```sql
-- Add locked_at field
ALTER TABLE users ADD COLUMN locked_at DATETIME;
```

---

## Testing Checklist

- [ ] Login with correct credentials returns JWT
- [ ] Login with wrong password returns 401
- [ ] Login with non-existent user returns 401
- [ ] Unverified user gets 403
- [ ] 5 failed attempts locks account (returns 423)
- [ ] Locked account cannot login even with correct password
- [ ] JWT expires after 2 hours
- [ ] JWT contains correct user claims
- [ ] Successful login resets failed_attempts
- [ ] POST /auth/verify/request sends magic link email
- [ ] GET /auth/verify/{valid_token} unlocks account
- [ ] GET /auth/verify/{invalid_token} returns error
- [ ] Verified user can login normally

---

## References

- [OWASP Password Storage Cheat Sheet 2025](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [FastAPI Security Docs](https://fastapi.tiangolo.com/tutorial/security/)
- [pwdlib Documentation](https://pwdlib.readthedocs.io/)
- [python-jose Documentation](https://python-jose.readthedocs.io/)