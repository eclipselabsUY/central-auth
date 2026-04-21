from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.models.user import User
from app.core.database import get_async_session, 


async def get_user(email : str, session : AsyncSession = Depends(get_async_session)) -> User:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none