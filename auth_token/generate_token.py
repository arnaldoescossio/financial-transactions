from datetime import datetime, timedelta

from jose import jwt

from app.core.config.env_config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.jwt_algorithm
EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
