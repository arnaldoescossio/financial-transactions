from fastapi import APIRouter

from auth_token import generate_token


router = APIRouter(prefix="/api/v1", tags=["token"])

@router.get("/token")
def get_token():
    return {"token": generate_token.create_access_token({"user": "admin"})}