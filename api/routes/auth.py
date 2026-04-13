from fastapi import APIRouter

from auth_token import generate_token


router = APIRouter(tags=["token"])

@router.get("", include_in_schema=False)
def get_token():
    return {"token": generate_token.create_access_token({"user": "admin"})}