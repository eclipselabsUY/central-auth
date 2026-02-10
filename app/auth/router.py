from fastapi import APIRouter, Request
from app.schemas.login import LoginSchema

router = APIRouter()

@router.get("/login")
def login_request(request : Request, login: LoginSchema):
    pass