from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.login import LoginSchema
from app.services.users import get_user, validate_user
from app.core.database import get_async_session
from app.exceptions import UserLocked, UserNotVerified, UserWrongPassword
from app.security.apikey import verify_api_key

router = APIRouter()


@router.post("/login", dependencies=(Depends(verify_api_key)))
async def login_request(request: Request, login: LoginSchema, session : AsyncSession = Depends(get_async_session)):

    user = await get_user(login.email, session)

    if not user:
        raise HTTPException(status_code=401)
    try:
    
        validate_user(user, login.password, session)
    
    except UserWrongPassword:
        raise HTTPException(status_code=401, detail={
            "error":"ACCOUNT_INVALID_CREDENTIALS",
            "code":1101
        })
    
    except UserNotVerified:
        raise HTTPException(status_code=403, detail={
            "error":"ACCOUNT_NOT_VERIFIED",
            "code":1102            
        })
    
    except UserLocked:
        raise HTTPException(status_code=403, detail={
            "error":"ACCOUNT_LOCKED",
            "code":1103
        })

