import secrets

from app.core.config import ph
from app.core.concurrency import run_cpu_bound
from app.security.utils import _apply_pepper


def hash_password(password: str) -> str:
    return ph.hash(_apply_pepper(password))


def verify_password(hash: str, password: str) -> bool:
    try:
        return ph.verify(hash, _apply_pepper(password))
    except:
        return False


def verify_and_update(hash: str, password: str) -> tuple[bool, str | None]:
    try:
        valid = ph.verify(hash, _apply_pepper(password))

        if valid and ph.check_needs_rehash(hash):
            return True, ph.hash(_apply_pepper(password))

        return True, None
    except:
        return False, None


def validate_password_strength(password: str) -> bool:
    return (
        len(password) >= 8
        and any(c.isupper() for c in password)
        and any(c.isdigit() for c in password)
    )


def generate_temp_password(length=12):
    return secrets.token_urlsafe(length)


async def async_hash_password(password: str) -> str:
    return await run_cpu_bound(hash_password, password)


async def async_verify_password(hash: str, password: str) -> bool:
    return await run_cpu_bound(verify_password, hash, password)


async def async_verify_and_update(hash: str, password: str) -> tuple[bool, str | None]:
    return await run_cpu_bound(verify_and_update, hash, password)
