from dotenv import load_dotenv
import os
from argon2 import PasswordHasher

# Load Env Vars
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
dotenv_path = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(dotenv_path)

# DB Env
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# JWT
JWT_KEY = os.getenv("JWT_KEY", "7tibry8v3t7biyc8n3fvb7gfhneo8ybg3r8yf3hqrksbywin")

# PEPPER
PEPPER = os.getenv("PEPPER")

# SMTP
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_HOST")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS")
SMTP_USE_SSL = os.getenv("SMTP_USE_SSL")

ENVIRONMENT = os.getenv("ENVIRONMENT")

if ENVIRONMENT == "DEV":
    DATABASE_URL = "sqlite+aiosqlite:///./eclipse-labs.db"
else:
    DATABASE_URL = (
        f"postgresql+asyncpg://"
        f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}"
        f"/{POSTGRES_DB}"
    )

ph = PasswordHasher(
    time_cost=3, memory_cost=65536, parallelism=4, hash_len=64, salt_len=32
)
