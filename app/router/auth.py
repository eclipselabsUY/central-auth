from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.login import LoginSchema
from app.services.auth import authenticate_user, check_verified, check_locked
from app.services.users import get_user
from app.core.database import get_async_session

router = APIRouter()


@router.post("/login")
async def login_request(request: Request, login: LoginSchema, session : AsyncSession = Depends(get_async_session)):

    user = await get_user(login.email, session)

    if not user:
        raise HTTPException(status_code=401)
    
    is_user_auth = await authenticate_user(user.id, user.password_hash, login.password)

    if not is_user_auth:
        raise HTTPException(status_code=401)
    
    check_verified(user.id)
    check_locked(user.id)