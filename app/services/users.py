from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.user import User


async def get_user(email : str, session : AsyncSession) -> User:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none

async def update_user_hash(user_id : UUID, new_hash : str, session : AsyncSession):
    await session.execute(update(User).where(User.id == user_id).values(password_hash = new_hash))