from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.security.password import async_verify_and_update
from app.services.users import get_user, update_user_hash

async def authenticate_user(user_id : UUID, user_password_hash: str, input_password: str, session : AsyncSession) -> bool:
    
    valid, new_hash = await async_verify_and_update(user_password_hash, input_password)

    if not valid:
        return False
    
    if new_hash:
        await update_user_hash(id, new_hash)
        await session.commit()
    
    return True