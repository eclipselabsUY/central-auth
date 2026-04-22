from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.user import User
from app.exceptions.users import UserNotVerified, UserLocked, UserWrongPassword
from app.services.auth import authenticate_user

async def validate_user(user : User, input_password : str, session):

    if not await authenticate_user(user, input_password, session):
        raise UserWrongPassword()

    if not await check_user_verified(user):
        raise UserNotVerified()
    
    if not await check_user_locked(user):
        raise UserLocked()


async def get_user(email : str, session : AsyncSession) -> User:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none


async def update_user_hash(user_id : UUID, new_hash : str, session : AsyncSession):
    await session.execute(update(User).where(User.id == user_id).values(password_hash = new_hash))


async def check_user_verified(user: User) -> bool:
    return user.verified


async def check_user_locked(user :  User):
    return user.locked_out