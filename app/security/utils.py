from app.core.config import PEPPER


def _apply_pepper(password: str) -> str:
    return password + PEPPER
