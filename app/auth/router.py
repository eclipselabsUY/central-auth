from fastapi import APIRouter


router = APIRouter()

@router.get("/login")
def login_request():
    pass